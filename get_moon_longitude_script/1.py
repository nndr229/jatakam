import swisseph as swe
from datetime import datetime
import pytz


def get_sidereal_moon_longitude(
    year, month, day,
    hour, minute,
    latitude, longitude,
    timezone_str="Asia/Kolkata",
    ayanamsa=swe.SIDM_LAHIRI
):
    """
    Returns sidereal (nirayana) Moon longitude in degrees
    """

    # 1. Set ayanamsa (Lahiri for Kerala astrology)
    swe.set_sid_mode(ayanamsa)

    # 2. Create timezone-aware datetime
    local_tz = pytz.timezone(timezone_str)
    local_dt = local_tz.localize(
        datetime(year, month, day, hour, minute)
    )

    # 3. Convert to UTC
    utc_dt = local_dt.astimezone(pytz.utc)

    # 4. Convert to Julian Day (UT)
    jd_ut = swe.julday(
        utc_dt.year,
        utc_dt.month,
        utc_dt.day,
        utc_dt.hour + utc_dt.minute / 60.0
    )

    # 5. Calculate Moon position (sidereal)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    position, _ = swe.calc_ut(jd_ut, swe.MOON, flags)

    moon_longitude = position[0]  # degrees 0–360

    return moon_longitude


# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":

    # Example: Kollam, Kerala
    moon_long = get_sidereal_moon_longitude(
        year=2001,
        month=9,
        day=16,
        hour=12,
        minute=30,
        latitude=26.33,
        longitude=89.66
    )

    print(f"Sidereal Moon Longitude: {moon_long:.6f}°")
