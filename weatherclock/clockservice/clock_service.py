from flask import Flask

app = Flask(__name__)

@app.route("/current/")
def get_current_weather():
    return "Current weather forecast"

@app.route("/forecast/")
def get_weather_forecast():
    return "Upcoming weather forecast"



if __name__ == '__main__':
    app.run(debug=True)