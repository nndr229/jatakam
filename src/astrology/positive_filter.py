POSITIVE_PLANETS = {"Jupiter", "Venus", "Moon", "Mercury"}


def filter_positive_periods(dasha_timeline):
    positive = []
    reframed = []

    for planet, years in dasha_timeline:
        if planet in POSITIVE_PLANETS:
            positive.append((planet, years))
        else:
            reframed.append((planet, years))

    return positive, reframed
