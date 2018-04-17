""" Future forecast conditions data """

class Forecast:
    def __init__(self, cc, t, mintemp, maxtemp, dt, r, s ):
        """ Initializes the summary object with empty values """
        self.condition_code = cc
        self.temp = t
        self.min_temp = mintemp
        self.max_temp = maxtemp
        self.forecastdt = dt
        self.rain = r
        self.snow = s
    
    def __repr__(self):
        return str(self.__dict__)
