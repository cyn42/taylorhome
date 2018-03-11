"""The grid locations for the weather clock icons """

BUCKETS = {'now': [0],
           'today_high': [1],
           'today_low': [2],
           'tonight_high': [3],
           'tonight_low': [4],
           'tomorrow_high': [5],
           'tomorrow_low': [6]}

PERCENTS = {'10': [55, 56],
            '20': [38, 39],
            '30': [23, 24],
            '40': [68, 69],
            '50': [71, 72],
            '60': [48, 49],
            '70': [2, 3],
            '80': [96, 97],
            '90': [4, 5],
            '100': [28, 29]}

ICONS = {'cloudy': [4, 5, 14, 15],
         'lightning': [20, 21, 30, 31],
         'rain': [36, 37, 46, 47],
         'fog': [6, 7],
         'cold warning': [11, 12, 22],
         'sunny': [53, 54, 63, 64],
         'windy': [58, 59],
         'snow': [80, 81, 90, 91],
         'sun clouds': [75, 76, 85, 86],
         'heat warning': [78, 79, 88, 89],
         'wifi': [9],
         'internet': [101]}

TEMP = {'neg20': [42, 43],
        'neg15': [65],
        'neg10': [93, 94],
        'neg5': [70],
        '0': [27],
        '5': [95],
        '10': [88],
        '15': [10],
        '20': [57],
        '25': [52],
        '30': [92]}
PRECIPITATIONMM = {'1to3': [8, 9],
                   '3to7': [66, 67],
                   '7to10': [32, 33],
                   'over10': [60, 61, 62]}
PRECIPITATIONCM = {'1': [35],
                   '3': [77],
                   '5': [13],
                   '10': [87],
                   '15': [25, 26]}

def get_grid_coords( bucket, temp, condition, rain, snow ):
    _bucket = BUCKETS[bucket]
    _testval = [7,8,12,18,25,35,45,55]
    return _bucket + _testval

def get_temp_key( temp ):
    if temp <= -20:
        return 'neg20'
    if temp <= -15:
        return 'neg15'
    if temp <= -10:
        return 'neg10'
    if temp <= -5:
        return 'neg5'
    if temp <= 0:
        return '0'
    if temp <= 5:
        return '5'
    if temp <= 10:
        return '10'
    if temp <= 15:
        return '15'
    if temp <= 20:
        return '20'
    if temp <= 25:
        return '25'
    return '30'

def get_rain( rain ):
    if rain <= 3:
        return '1to3'
    if rain <= 7:
        return '3to7'
    if rain <= 10:
        return '7to10'
    return 'over10'

def get_snow( snow ):
    if snow <= 1:
        return '1'
    if snow <= 3:
        return '3'
    if snow <= 5:
        return '5'
    if snow <= 10:
        return '10'
    return '15'

def get_icon( icon ):
    return ICONS[icon]

if __name__ == '__main__':
    wifi_pos = get_icon('wifi')
    print(wifi_pos)