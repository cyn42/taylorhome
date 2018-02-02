""" Forecast Summary classes """
import math, json
from collections import Counter

class ForecastSummary:
    """ Encapsulates  the summary information for all
        forecast objects in the specified period """

    def __init__(self):
        """ Initializes the summary object with empty values """
        self.max_temp = float('nan')
        self.min_temp = float('nan')
        self.total_rain = 0
        self.total_snow = 0
        self.conditions = []

    def eval_new_temp(self, temp):
        """ Evaluates a new temperture to see if summary min / max has to be updated """
        if math.isnan(self.max_temp) or self.max_temp < temp:
            self.max_temp = temp
        if math.isnan(self.min_temp) or self.min_temp > temp:
            self.min_temp = temp

    def add_precipitation(self, rainfall, snowfall):
        """ Sums the rainfall and snowfall """
        self.total_rain += rainfall
        self.total_snow += snowfall

    def add_condition(self, condition):
        """ Add to the list of conditions so that they can be summarized """
        self.conditions.append(condition)

    def get_prevailing_condition(self):
        """ return the most prevlent condition from the list of conditions """
        return Counter(self.conditions).most_common(1)[0][0] if self.conditions else 'None'

