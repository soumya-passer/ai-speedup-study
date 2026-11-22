import ctypes as _ctypes
import mmap as _mmap
import platform as _platform
import struct as _struct
from array import array as _array


def _ref_sums(xs, w):
    out = []
    for i in range(len(xs) - w + 1):
        total = 0.0
        for v in xs[i:i + w]:
            total += v
        out.append(total)
    return out


def _x86_code():
    buf = bytearray()
    labels = {}
    fix = []

    def emit(*b):
        buf.extend(b)

    def lab(n):
        labels[n] = len(buf)

    def jcc(op, n):
        emit(op)
        fix.append((len(buf), n))
        emit(0)

    def jmp(n):
        emit(0xEB)
        fix.append((len(buf), n))
        emit(0)

    # test rdx, rdx ; jle done
    emit(0x48, 0x85, 0xD2)
    jcc(0x7E, 'done')
    # xor r8, r8
    emit(0x4D, 0x31, 0xC0)
    lab('outer')
    # xorps xmm0, xmm0
    emit(0x0F, 0x57, 0xC0)
    # mov r10, rdi
    emit(0x49, 0x89, 0xFA)
    # xor r9, r9
    emit(0x4D, 0x31, 0xC9)
    lab('inner')
    # cmp r9, rcx ; jae inner_done
    emit(0x49, 0x39, 0xC9)
    jcc(0x73, 'inner_done')
    # addsd xmm0, [r10]
    emit(0xF2, 0x41, 0x0F, 0x58, 0x02)
    # add r10, 8
    emit(0x49, 0x83, 0xC2, 0x08)
    # inc r9
    emit(0x49, 0xFF, 0xC1)
    jmp('inner')
    lab('inner_done')
    # movsd [rsi], xmm0
    emit(0xF2, 0x0F, 0x11, 0x06)
    # add rsi, 8 ; add rdi, 8
    emit(0x48, 0x83, 0xC6, 0x08)
    emit(0x48, 0x83, 0xC7, 0x08)
    # inc r8
    emit(0x49, 0xFF, 0xC0)
    # cmp r8, rdx ; jb outer
    emit(0x49, 0x39, 0xD0)
    jcc(0x72, 'outer')
    lab('done')
    emit(0xC3)
    for pos, n in fix:
        buf[pos] = (labels[n] - (pos + 1)) & 0xFF
    return bytes(buf)


def _arm_code():
    words = []
    labels = {}
    fix = []

    def emit(w):
        words.append(w & 0xFFFFFFFF)

    def lab(n):
        labels[n] = len(words)

    def b(n):
        fix.append((len(words), n, None))
        emit(0)

    def bcond(n, cond):
        fix.append((len(words), n, cond))
        emit(0)

    # mov x5, xzr   (ORR X5, XZR, XZR)
    emit(0xAA000000 | (31 << 16) | (31 << 5) | 5)
    lab('outer')
    # ldr d0, [x4]   (zero)
    emit(0xFD400000 | (4 << 5) | 0)
    # mov x7, x0
    emit(0xAA000000 | (0 << 16) | (31 << 5) | 7)
    # mov x6, xzr
    emit(0xAA000000 | (31 << 16) | (31 << 5) | 6)
    lab('inner')
    # cmp x6, x3
    emit(0xEB000000 | (3 << 16) | (6 << 5) | 31)
    bcond('inner_done', 2)  # b.hs
    # ldr d1, [x7]
    emit(0xFD400000 | (7 << 5) | 1)
    # fadd d0, d0, d1
    emit(0x1E602800 | (1 << 16) | (0 << 5) | 0)
    # add x7, x7, #8
    emit(0x91000000 | (8 << 10) | (7 << 5) | 7)
    # add x6, x6, #1
    emit(0x91000000 | (1 << 10) | (6 << 5) | 6)
    b('inner')
    lab('inner_done')
    # str d0, [x1]
    emit(0xFD000000 | (1 << 5) | 0)
    # add x1, x1, #8
    emit(0x91000000 | (8 << 10) | (1 << 5) | 1)
    # add x0, x0, #8
    emit(0x91000000 | (8 << 10) | (0 << 5) | 0)
    # add x5, x5, #1
    emit(0x91000000 | (1 << 10) | (5 << 5) | 5)
    # cmp x5, x2
    emit(0xEB000000 | (2 << 16) | (5 << 5) | 31)
    bcond('outer', 11)  # b.lt
    # ret
    emit(0xD65F03C0)
    for idx, n, cond in fix:
        off = labels[n] - idx
        if cond is None:
            words[idx] = 0x14000000 | (off & 0x3FFFFFF)
        else:
            words[idx] = 0x54000000 | ((off & 0x7FFFF) << 5) | cond
    return b''.join(w.to_bytes(4, 'little') for w in words)


_ZERO = _array('d', [0.0])
_ZERO_PTR = _ctypes.cast(_ZERO.buffer_info()[0], _ctypes.POINTER(_ctypes.c_double))
_JIT = None
_JIT_MM = None
_IS_ARM = False


def _jit_sums(func, is_arm, xs, w):
    m = len(xs) - w + 1
    a = _array('d', xs)
    out = _array('d', bytes(8 * m))
    ap = _ctypes.cast(a.buffer_info()[0], _ctypes.POINTER(_ctypes.c_double))
    op = _ctypes.cast(out.buffer_info()[0], _ctypes.POINTER(_ctypes.c_double))
    if is_arm:
        func(ap, op, m, w, _ZERO_PTR)
    else:
        func(ap, op, m, w)
    return out.tolist()


try:
    _mach = _platform.machine().lower()
    if _mach in ('x86_64', 'amd64'):
        _code = _x86_code()
        _is_arm = False
        _ft = _ctypes.CFUNCTYPE(
            None,
            _ctypes.POINTER(_ctypes.c_double),
            _ctypes.POINTER(_ctypes.c_double),
            _ctypes.c_int64,
            _ctypes.c_int64,
        )
    elif _mach in ('arm64', 'aarch64'):
        _code = _arm_code()
        _is_arm = True
        _ft = _ctypes.CFUNCTYPE(
            None,
            _ctypes.POINTER(_ctypes.c_double),
            _ctypes.POINTER(_ctypes.c_double),
            _ctypes.c_int64,
            _ctypes.c_int64,
            _ctypes.POINTER(_ctypes.c_double),
        )
    else:
        raise ValueError(_mach)
    _length = (_len(_code) + 4095) & ~4095
    _mm = None
    _addr = None
    try:
        _mm = _mmap.mmap(
            -1, _length,
            flags=_mmap.MAP_PRIVATE | _mmap.MAP_ANONYMOUS,
            prot=_mmap.PROT_READ | _mmap.PROT_WRITE | _mmap.PROT_EXEC,
        )
        _mm.write(_code)
        _addr = _ctypes.addressof(_ctypes.c_char.from_buffer(_mm))
    except Exception:
        _mm = _mmap.mmap(
            -1, _length,
            flags=_mmap.MAP_PRIVATE | _mmap.MAP_ANONYMOUS,
            prot=_mmap.PROT_READ | _mmap.PROT_WRITE,
        )
        _mm.write(_code)
        _addr = _ctypes.addressof(_ctypes.c_char.from_buffer(_mm))
        _libc = None
        for _name in ('libc.dylib', 'libc.so.6', 'libc.so', None):
            try:
                _libc = _ctypes.CDLL(_name, use_errno=True)
                break
            except Exception:
                _libc = None
        if _libc is None:
            raise ValueError('no libc')
        _libc.mprotect.argtypes = [_ctypes.c_void_p, _ctypes.c_size_t, _ctypes.c_int]
        _libc.mprotect.restype = _ctypes.c_int
        if _libc.mprotect(_ctypes.c_void_p(_addr), _ctypes.c_size_t(_length), 5) != 0:
            raise ValueError('mprotect')
        try:
            _libc.pthread_jit_write_protect_np(_ctypes.c_void_p(_addr), _ctypes.c_int(0))
        except Exception:
            pass
    _func = _ft(_addr)
    # Self-test: only keep the JIT if it is bit-identical on adversarial data.
    _seed = 1234567
    _rand = []
    for _ in range(40):
        _seed = (_seed * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
        _rand.append(((_seed >> 11) & 0x1FFFFFFFFFFFFF) / float(1 << 51) - 0.5)
    _tests = [
        ([1e16, 1.0, -1e16, 1.0, 1.0, -1e16, 1e16, 1.0], 3),
        ([1e16, 1.0, 1.0, -1e16, 1.0, 1.0], 4),
        (_rand, 7),
        ([-0.0, -0.0, -0.0, 0.0, -0.0], 2),
        ([float('inf'), 1.0, -float('inf'), 2.0, 3.0], 3),
        ([5e-324, 5e-324, 1.0, -1.0, 5e-324], 3),
        ([1e308, 1e308, -1e308, 1e308], 2),
        ([0.1] * 20, 5),
        ([3.5], 1),
        ([1.0, 2.0, 3.0, 4.0], 2),
    ]
    for _xs, _w in _tests:
        _got = _jit_sums(_func, _is_arm, list(_xs), _w)
        _want = _ref_sums(list(_xs), _w)
        if len(_got) != len(_want):
            raise ValueError('len')
        for _a, _b in zip(_got, _want):
            if _struct.pack('<d', _a) != _struct.pack('<d', _b):
                raise ValueError('bits')
    _JIT = _func
    _JIT_MM = _mm
    _IS_ARM = _is_arm
except Exception:
    _JIT = None
    _JIT_MM = None


def moving_average(xs, w):
    """Average of each window of w numbers in a row.
    Results must be bit-for-bit identical to this function: each window is
    added left to right, starting from 0.0, then divided by w.
    Returns [] when w > len(xs). Raises ValueError when w < 1."""
    if w < 1:
        raise ValueError("w < 1")
    m = len(xs) - w + 1
    if m <= 0:
        return []
    fl = list(map(float, xs))
    if _JIT is not None:
        sums = _jit_sums(_JIT, _IS_ARM, fl, w)
        return [s / w for s in sums]
    out = []
    append = out.append
    for i in range(m):
        total = 0.0
        for v in fl[i:i + w]:
            total += v
        append(total / w)
    return out
