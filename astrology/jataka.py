from .nakshatra import get_nakshatra
from .rasi import nakshatra_to_rasi


def generate_jataka(name, moon_longitude):
    nakshatra, nak_no = get_nakshatra(moon_longitude)
    rasi = nakshatra_to_rasi(nak_no)

    return {
        "name": name,
        "moon_longitude": moon_longitude,
        "nakshatra": nakshatra,
        "nakshatra_no": nak_no,
        "janma_rasi": rasi
    }
