RAJJU_GROUPS = {
    "Pada": [1, 6, 11, 16, 21, 26],
    "Kati": [2, 7, 12, 17, 22, 27],
    "Nabhi": [3, 8, 13, 18, 23],
    "Kantha": [4, 9, 14, 19, 24],
    "Siras": [5, 10, 15, 20, 25]
}


def dina_porutham(boy, girl):
    count = (girl - boy) % 27
    return count not in [0, 6, 13, 20]


def gana_porutham(boy, girl):
    return True  # placeholder (extend later)


def sthree_deergha(boy, girl):
    return (girl - boy) % 27 >= 7


def rajju_porutham(boy, girl):
    for group in RAJJU_GROUPS.values():
        if boy in group and girl in group:
            return False
    return True


def kerala_matching(boy_n, girl_n):
    return {
        "Dina Porutham": dina_porutham(boy_n, girl_n),
        "Sthree Deergha": sthree_deergha(boy_n, girl_n),
        "Rajju Porutham": rajju_porutham(boy_n, girl_n)
    }
