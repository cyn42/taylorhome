""" Forecast Summary classes """
import math
from collections import Counter

class ForecastSummary:
    """ Encapsulates  the summary information for all
        forecast objects in the specified period """

    def __init__(self):
        """ Initializes the summary object with empty values """
        self.max_temp = float('nan')
        self.min_temp = float('nan')
        self.total_precip = 0
        self.conditions = []

    def eval_new_temp(self, temp):
        """ Evaluates a new temperture to see if summary min / max has to be updated """
        if math.isnan(self.max_temp) or self.max_temp < temp:
            self.max_temp = temp
        if math.isnan(self.min_temp) or self.min_temp > temp:
            self.min_temp = temp

    def add_precipitation(self, rainfall, snowfall):
        self.total_precip += rainfall
        self.total_precip += snowfall

    def add_condition(self, condition):
        self.conditions.append(condition)

    def get_prevailing_condition(self):
        return Counter(self.conditions).most_common(1)[0][0] if len(self.conditions)>0 else 'None'