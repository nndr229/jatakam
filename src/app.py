from flask import Flask, render_template, request, send_file
from .jatakam.calculator import Calculator
from .astrology.jataka import generate_jataka
from .astrology.dasha import get_dasha_details # if it exists
from datetime import datetime
import io

app = Flask(__name__)
calc = Calculator()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get Form Data
        name = request.form['name']
        dob = request.form['dob'] # YYYY-MM-DD
        tob = request.form['tob'] # HH:MM
        lat = float(request.form['lat'])
        lon = float(request.form['lon'])
        
        # 1. Calculate Planetary Positions (using Swiss Ephemeris)
        dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
        planets = calc.calculate_planets(dt, lat, lon)
        
        # 2. Get Moon Longitude
        moon_longitude = planets['Moon']['longitude']
        
        # 3. Calculate Jatakam (Nakshatra, Rasi) using ORIGINAL logic
        jataka_data = generate_jataka(name, moon_longitude)
        
        # 4. Generate Additional Charts (D1, D9)
        charts = calc.get_divisional_charts(planets)
        
        # 5. Get Dasha (if logic exists in original code or new code)
        # Try original dasha logic if available, else fallback
        try:
             from .astrology.dasha import get_dasha_details
             dashas = get_dasha_details(moon_longitude, dt)
        except ImportError:
             dashas = calc.get_dasha_details(moon_longitude, dt)
        
        # Generate Report Data
        report_data = {
            'name': name,
            'datetime': dt.strftime("%d %b %Y, %I:%M %p"),
            'location': f"{lat}, {lon}",
            'planets': planets,
            'charts': charts,
            'dashas': dashas,
            'jataka': jataka_data # Original Nakshatra/Rasi data
        }
        
        return render_template('report.html', data=report_data)
    
    return render_template('index.html')

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    # Similar to report route, but generates PDF
    # In reality, cache the report_data or regenerate
    # For now, just a placeholder
    return "PDF Download (Not Implemented Yet)"

if __name__ == '__main__':
    app.run(debug=True)
