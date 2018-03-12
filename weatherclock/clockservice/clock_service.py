from flask import Flask, jsonify, json
#import weatherclock

app = Flask(__name__)

@app.route("/cleargrid/")
def get_weather_forecast():
    return "Clear Grid"



if __name__ == '__main__':
    app.run(debug=True)

    