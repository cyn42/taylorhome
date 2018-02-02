import pytest
import grid

def test_todayhigh_neg17():
    result = grid.get_grid_coords('today_high','-17','cloudy',0,0)
    print(result)
    assert result == [50, 51, 0, 1, 65, 4, 5, 14, 15]

def test_todaylow_neg40():
    result = grid.get_grid_coords('today_low','-40','rain',0,0)
    print(result)
    assert result == [50, 51, 98, 99, 42, 43, 36, 37, 46, 47]

def test_tonighthigh_0():
    result = grid.get_grid_coords('tonight_high','0','sunny',0,0)
    print(result)
    assert result == [82, 83, 84, 0, 1, 27, 53, 54, 63, 64]

def test_tonightlow_22():
    result = grid.get_grid_coords('tonight_low','22','sun clouds',0,0)
    print(result)
    assert result == [82, 83, 84, 98, 99, 52, 75, 76, 85, 86]

def test_tonightlow_22_rain():
    result = grid.get_grid_coords('tonight_low','22','sun clouds',6,0)
    print(result)
    assert result == [82, 83, 84, 98, 99, 52, 75, 76, 85, 86, 66, 67]

def test_todayhigh_neg17_snow():
    result = grid.get_grid_coords('today_high','-17','cloudy',0,14)
    print(result)
    assert result == [50, 51, 0, 1, 65, 4, 5, 14, 15, 25, 26]

def test_todayhigh_neg2_snow_rain():
    result = grid.get_grid_coords('today_high','-2','cloudy',3,5)
    print(result)
    assert result == [50, 51, 0, 1, 27, 4, 5, 14, 15, 8, 9, 13]
