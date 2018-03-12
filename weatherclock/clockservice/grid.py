"""The grid locations for the weather clock icons """

BUCKETS = {'now': [54, 55],
           'today_high': [40, 41, 98, 99],
           'today_low': [40, 41, 8, 9],
           'tonight_high': [15,16,17, 98,99],
           'tonight_low': [15,16,17,8,9],
           'tomorrow_high': [86, 87, 88, 89,98,99],
           'tomorrow_low': [86, 87, 88, 89, 8,9]}

PERCENTS = {'10': [45, 46],
            '20': [68, 69],
            '30': [75, 76],
            '40': [30, 31],
            '50': [21, 22],
            '60': [50, 51],
            '70': [96, 97],
            '80': [6, 7],
            '90': [58, 59],
            '100': [70, 71]}

ICONS = {'cloudy': [84, 85, 94, 95],
         'lightning': [60, 61, 78, 79],
         'rain': [52, 53, 66, 67],
         'moon': [92, 93],
         'cold warning': [77, 81, 82],
         'sunny': [35, 36, 43, 44],
         'windy': [48, 49],
         'snow': [0, 1, 18, 19],
         'sun clouds': [13, 14, 25, 26],
         'heat warning': [10, 28, 29]}
CONDITIONS = {'13d':'snow','13n':'snow',
              '01d':'sunny', '01n':'sunny',
              '03n':'cloudy', '03d':'cloudy', '04d':'cloudy', '04n':'cloudy',
              '10d':'rain', '10n':'rain', 
              '11d':'lightning', '11n':'lightning',
              '02d':'sun clouds', '02n':'sun clouds'}

TEMP = {'neg20': [56, 57],
        'neg15': [34],
        'neg10': [3, 4],
        'neg5': [20],
        '0': [72],
        '5': [5],
        '10': [4],
        '15': [80],
        '20': [47],
        '25': [42],
        '30': [2]}
PRECIPITATIONMM = {'1to3': [90, 91],
                   '3to7': [32, 33],
                   '7to10': [62, 63],
                   'over10': [37, 38, 39]}
PRECIPITATIONCM = {'1': [65],
                   '3': [83],
                   '5': [12],
                   '10': [27],
                   '15': [73],
                   'over15': [73, 74]}

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
