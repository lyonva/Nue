def get_y( df ):
    obj = []
    for c in df.columns:
        if c[-1] in ["+", "-"]:
            obj.append(c)
    return obj

def get_x( df ):
    y = get_y(df)
    return [ c for c in df.columns if c not in y and c[-1] != "?" ]

def get_sign( y ):
    sign = []
    for c in y:
        if c[-1] == "+":
            sign.append(1)
        elif c[-1] == "-":
            sign.append(-1)
        else:
            sign.append(0)
    return sign

def mult_by_sign(df):
    df = df.copy()
    ys = get_y(df)
    signs = get_sign(ys)
    for i, y in enumerate(ys):
        df[y] *= signs[i]
    return df
