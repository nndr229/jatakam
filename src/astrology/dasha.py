VIMSHOTTARI_ORDER = [
    ("Ketu", 7),
    ("Venus", 20),
    ("Sun", 6),
    ("Moon", 10),
    ("Mars", 7),
    ("Rahu", 18),
    ("Jupiter", 16),
    ("Saturn", 19),
    ("Mercury", 17)
]


def generate_dasha_timeline(start_planet, years=10):
    timeline = []
    remaining = years
    idx = next(i for i, p in enumerate(
        VIMSHOTTARI_ORDER) if p[0] == start_planet)

    while remaining > 0:
        planet, length = VIMSHOTTARI_ORDER[idx]
        used = min(length, remaining)
        timeline.append((planet, used))
        remaining -= used
        idx = (idx + 1) % len(VIMSHOTTARI_ORDER)

    return timeline
