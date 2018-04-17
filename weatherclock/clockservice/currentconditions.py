""" Current weather conditions data """

class CurrentConditions:
    def __init__(self, cc, t, dt, sr, ss ):
        """ Initializes the summary object with empty values """
        self.condition_code = cc
        self.temp = t
        self.forecastdt = dt
        self.sunrise = sr
        self.sunset = ss
    
    def get_sunrise(self):
        return self.sunrise
    def get_sunset(self):
        return self.sunset
    
    def __repr__(self):
        return str(self.__dict__)

        