from flask import Flask, render_template, request, send_file
from .jatakam.calculator import Calculator
from .jatakam.report import generate_pdf
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
        
        # Calculate
        dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
        planets = calc.calculate_planets(dt, lat, lon)
        charts = calc.get_divisional_charts(planets)
        dashas = calc.get_dasha_details(planets['Moon']['longitude'], dt)
        
        # Generate Report Data
        report_data = {
            'name': name,
            'datetime': dt.strftime("%d %b %Y, %I:%M %p"),
            'location': f"{lat}, {lon}",
            'planets': planets,
            'charts': charts,
            'dashas': dashas
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
