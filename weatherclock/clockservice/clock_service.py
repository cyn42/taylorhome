from flask import Flask, jsonify, json
from threading import Thread
import weatherclock

app = Flask(__name__)

@app.route("/current/")
def get_current_weather():
    return jsonify(json.dumps(weatherclock.current_conditions))

@app.route("/forecast/")
def get_weather_forecast():
    return "Upcoming weather forecast"



if __name__ == '__main__':
    app.run(debug=True)
    t = Thread(weatherclock.grab_weather())
    t.start()
    