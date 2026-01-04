from flask import Flask, render_template, request
from astrology.nakshatra import get_nakshatra
from astrology.porutham import kerala_matching
from astrology.jataka import generate_jataka
from astrology.interpretations import POSITIVE_MESSAGES
from astrology.interpretations import REFRAME_MESSAGES
from astrology.dasha import generate_dasha_timeline
from astrology.positive_filter import filter_positive_periods
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/jataka", methods=["POST"])
def jataka():
    name = request.form["name"]
    moon = float(request.form["moon"])

    data = generate_jataka(name, moon)
    return render_template("jataka.html", data=data)


@app.route("/match", methods=["POST"])
def match():
    boy_moon = float(request.form["boy_moon"])
    girl_moon = float(request.form["girl_moon"])

    _, boy_n = get_nakshatra(boy_moon)
    _, girl_n = get_nakshatra(girl_moon)

    result = kerala_matching(boy_n, girl_n)
    return render_template("matching.html", result=result)


@app.route("/positive-forecast")
def positive_forecast():
    start_planet = "Mars"  # from Nakshatra mapping
    timeline = generate_dasha_timeline(start_planet, 10)

    positive, reframed = filter_positive_periods(timeline)

    return render_template(
        "positive_forecast.html",
        positive=positive,
        reframed=reframed,
        positive_msgs=POSITIVE_MESSAGES,
        reframe_msgs=REFRAME_MESSAGES
    )


if __name__ == "__main__":
    app.run(debug=True)
