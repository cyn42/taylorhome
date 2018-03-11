"""The grid locations for the weather clock icons """

BUCKETS = {'now': [44, 45],
           'today_high': [50, 51, 0, 1],
           'today_low': [50, 51, 98, 99],
           'tonight_high': [82, 83, 84, 0, 1],
           'tonight_low': [82, 83, 84, 98, 99],
           'tomorrow_high': [16, 17, 18, 19, 0, 1],
           'tomorrow_low': [16, 17, 18, 19, 98, 99]}

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
         'wifi': [100],
         'internet': [101]}
CONDITIONS = {'13d':'snow','13n':'snow',
              '01d':'sunny', '01n':'sunny',
              '03n':'cloudy', '03d':'cloudy', '04d':'cloudy', '04n':'cloudy',
              '10d':'rain', '10n':'rain', 
              '11d':'lightning', '11n':'lightning',
              '02d':'sun clouds', '02n':'sun clouds'}

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
    print('Get Grid Coords for ',bucket,condition)
    _bucket = BUCKETS[bucket]
    _temp = TEMP[get_temp_key(float(temp))]
    _icon = ICONS[CONDITIONS[condition]]
    _rain = PRECIPITATIONMM[get_rain(float(rain))] if float(rain) > 0 else []
    _snow = PRECIPITATIONCM[get_snow(float(snow))] if float(snow) > 0 else []
    return _bucket + _temp + _icon + _rain + _snow

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
