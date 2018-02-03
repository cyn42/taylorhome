from flask import Flask, jsonify, json
import weatherclock

app = Flask(__name__)

@app.route("/forecast/")
def get_weather_forecast():
    return weatherclock.get_weather_transitions()



if __name__ == '__main__':
    app.run(debug=True)

    