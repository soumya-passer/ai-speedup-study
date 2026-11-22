def round_prices(xs, _int=int):
    try:
        return [((_int(xf * 10000 + 50.5) // 100) / 100) if xf >= 0 else -((_int(-xf * 10000 + 50.5) // 100) / 100) for xf in xs]
    except TypeError:
        return [((_int(xf * 10000 + 50.5) // 100) / 100) if xf >= 0 else -((_int(-xf * 10000 + 50.5) // 100) / 100) for xf in map(float, xs)]
