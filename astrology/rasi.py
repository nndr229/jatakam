RASIS = [
    "Mesha", "Vrishabha", "Mithuna", "Karka",
    "Simha", "Kanya", "Tula", "Vrischika",
    "Dhanu", "Makara", "Kumbha", "Meena"
]


def nakshatra_to_rasi(nak_no):
    return RASIS[int((nak_no - 1) // 2.25)]
