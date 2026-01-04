import swisseph as swe
from datetime import datetime, timedelta
import pytz

# ---------------- CONFIG ----------------
TARGET_LONGITUDE = 205.0              # degrees (sidereal)
DATE = (1960, 3, 19)                  # YYYY, MM, DD
LAT = 8.5                             # Neyyattinkara approx
LON = 77.1
TZ = pytz.timezone("Asia/Kolkata")
AYANAMSA = swe.SIDM_LAHIRI
# --------------------------------------

swe.set_sid_mode(AYANAMSA)


def moon_longitude_sidereal(dt_utc):
    jd = swe.julday(
        dt_utc.year,
        dt_utc.month,
        dt_utc.day,
        dt_utc.hour + dt_utc.minute / 60 + dt_utc.second / 3600
    )
    pos, _ = swe.calc_ut(
        jd,
        swe.MOON,
        swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    )
    return pos[0]


def reverse_solve():
    start_local = TZ.localize(datetime(*DATE, 0, 0, 0))
    end_local = TZ.localize(datetime(*DATE, 23, 59, 59))

    start = start_local.astimezone(pytz.utc)
    end = end_local.astimezone(pytz.utc)

    # Binary search until ±1 second accuracy
    while (end - start).total_seconds() > 1:
        mid = start + (end - start) / 2
        lon = moon_longitude_sidereal(mid)

        if lon < TARGET_LONGITUDE:
            start = mid
        else:
            end = mid

    result_local = start.astimezone(TZ)

    print("Reverse-solved birth time (IST):")
    print(result_local.strftime("%H:%M:%S"))
    print("Moon longitude:", moon_longitude_sidereal(start))


reverse_solve()
