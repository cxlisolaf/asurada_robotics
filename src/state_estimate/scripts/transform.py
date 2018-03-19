def transform(measurement):
    k = [-2.475, -0.87, -0.285]
    b = [795.5, 570.8, 430.4]
    if measurement < 360:
        return (measurement - b[2]) / k[2]
    elif measurement < 440:
        return (measurement - b[1]) / k[1]
    else:
        return (measurement - b[0]) / k[0]
