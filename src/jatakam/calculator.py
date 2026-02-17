import swisseph as swe
from datetime import datetime
import pytz
from typing import Dict, List, Tuple
import math

class Calculator:
    """
    Core Vedic Astrology Calculator using Swiss Ephemeris.
    Supports Lahiri Ayanamsa and Sidereal Zodiac.
    """
    
    # Planet IDs in Swiss Ephemeris
    PLANETS = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mars': swe.MARS,
        'Mercury': swe.MERCURY,
        'Jupiter': swe.JUPITER,
        'Venus': swe.VENUS,
        'Saturn': swe.SATURN,
        'Rahu': swe.MEAN_NODE,  # Mean Node
        'Ketu': None # Calculated as 180 deg from Rahu
    }

    RASIS = [
        "Mesha", "Vrishabha", "Mithuna", "Karka", 
        "Simha", "Kanya", "Tula", "Vrischika", 
        "Dhanu", "Makara", "Kumbha", "Meena"
    ]

    def __init__(self, ephe_path: str = './ephe'):
        swe.set_ephe_path(ephe_path)
        # Set Sidereal (Lahiri)
        swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)

    def calculate_planets(
        self, 
        dt: datetime, 
        lat: float, 
        lon: float
    ) -> Dict[str, Dict]:
        """
        Calculate planetary positions for a given date/time/location.
        """
        # Convert to UTC Julian Day
        utc_dt = dt.astimezone(pytz.utc)
        jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, 
                        utc_dt.hour + utc_dt.minute/60.0 + utc_dt.second/3600.0)

        positions = {}
        
        # Calculate Ascendant (Lagna)
        houses, ascmc = swe.houses_ex(jd, lat, lon, b'A', flag=swe.FLG_SIDEREAL)
        ascendant = ascmc[0]
        positions['Ascendant'] = self._format_planet(ascendant)

        # Calculate Planets
        for name, planet_id in self.PLANETS.items():
            if name == 'Ketu':
                rahu_long = positions['Rahu']['longitude']
                ketu_long = (rahu_long + 180) % 360
                positions['Ketu'] = self._format_planet(ketu_long)
                continue

            flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
            res, _ = swe.calc_ut(jd, planet_id, flags)
            
            longitude = res[0]
            speed = res[3]
            is_retrograde = speed < 0

            positions[name] = self._format_planet(longitude, is_retrograde)

        return positions

    def _format_planet(self, longitude: float, is_retrograde: bool = False) -> Dict:
        """
        Format raw longitude into Rasi, Degree, Minute.
        """
        # Normalize 0-360
        longitude = longitude % 360
        
        rasi_num = int(longitude / 30)
        degree_in_rasi = longitude % 30
        
        d = int(degree_in_rasi)
        m = int((degree_in_rasi - d) * 60)
        s = int(((degree_in_rasi - d) * 60 - m) * 60)

        return {
            'longitude': longitude,
            'rasi': self.RASIS[rasi_num],
            'rasi_no': rasi_num + 1, # 1-based index
            'degree': d,
            'minute': m,
            'second': s,
            'retrograde': is_retrograde,
            'display': f"{d}°{m}'{s}\"" + (" (R)" if is_retrograde else "")
        }

    def get_dasha_details(self, moon_long: float, birth_date: datetime) -> List[Dict]:
        """
        Calculate Vimshottari Dasha periods.
        """
        # Basic implementation: calculate current Mahadasha based on Moon's nakshatra
        nakshatra_long = (moon_long * 60) % (360 * 60) # in minutes
        # TODO: Implement full Vimshottari logic
        return []

    def get_divisional_charts(self, planets: Dict) -> Dict:
        """
        Generate D1, D9, D10 charts.
        """
        charts = {
            'D1': {},
            'D9': {}
        }
        
        # D1 (Rasi) is just the rasi_no
        for p, data in planets.items():
            charts['D1'][p] = data['rasi_no']
            
            # D9 Calculation
            # Each rasi (30 deg) has 9 navamsas (3 deg 20 min each)
            total_minutes = (data['longitude'] % 30) * 60
            navamsa_idx = int(total_minutes / 200) # 200 mins per navamsa
            
            # Start depends on element (Fire/Earth/Air/Water)
            # Simplified logic for now:
            # - Movable (1,4,7,10): Starts from same sign
            # - Fixed (2,5,8,11): Starts from 9th from same sign
            # - Dual (3,6,9,12): Starts from 5th from same sign
            
            # Let's use exact longitude based formula:
            # Navamsa Longitude = (Longitude * 9) % 360
            # Navamsa Rasi = int(Navamsa Longitude / 30) + 1
            
            navamsa_long = (data['longitude'] * 9) % 360
            navamsa_rasi = int(navamsa_long / 30) + 1
            charts['D9'][p] = navamsa_rasi

        return charts
