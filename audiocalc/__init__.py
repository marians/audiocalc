# encoding: utf-8

import math


OCTAVE_BANDS = {
    'f63': -26.21,
    'f125': -16.18,
    'f250': -8.67,
    'f500': -3.25,
    'f1000': 0,
    'f2000': 1.2,
    'f4000': 0.96,
    'f8000': -1.15
}


def damping(temp, relhum, freq, pres=101325):
    """
    Calculates the damping factor for sound in dB/m
    depending on temperature, humidity and sound frequency.
    Source: http://www.sengpielaudio.com/LuftdaempfungFormel.htm

    temp: Temperature in degrees celsius
    relhum: Relative humidity as percentage, e.g. 50
    freq: Sound frequency in herz
    pres: Atmospheric pressure in kilopascal
    """
    temp += 273.15  # convert to kelvin
    pres = pres / 101325.0  # convert to relative pressure
    c_humid = 4.6151 - 6.8346 * pow((273.15 / temp), 1.261)
    hum = relhum * pow(10.0, c_humid) * pres
    tempr = temp / 293.15  # convert to relative air temp (re 20 deg C)
    frO = pres * (24.0 + 4.04e4 * hum * (0.02 + hum) / (0.391 + hum))
    frN = pres * pow(tempr, -0.5) * (9.0 + 280.0 * hum * math.exp(-4.17 * (pow(tempr, (-1.0 / 3.0)) - 1.0)))
    damp = 8.686 * freq * freq * (1.84e-11 * (1.0 / pres) * math.sqrt(tempr) + pow(tempr, -2.5) * (0.01275 * (math.exp(-2239.1 / temp) * 1.0 / (frO + freq * freq / frO)) + 0.1068 * (math.exp(-3352 / temp) * 1.0 / (frN + freq * freq / frN))))
    return damp


def total_level(octave_frequencies):
    """
    Calculates the total sound pressure level based on octave band frequencies
    """
    #print args
    sums = 0.0
    for band in OCTAVE_BANDS.keys():
        if band not in octave_frequencies:
            continue
        if octave_frequencies[band] is None:
            continue
        sums += pow(10.0, (float(octave_frequencies[band]) / 10.0))
    level = 10.0 * math.log(sums, 10.0)
    return level


def total_level_rated(octave_frequencies):
    """
    Calculates the A-rated total sound pressure level
    based on octave band frequencies
    """
    sums = 0.0
    for band in OCTAVE_BANDS.keys():
        if band not in octave_frequencies:
            continue
        if octave_frequencies[band] is None:
            continue
        sums += pow(10.0, ((float(octave_frequencies[band]) + OCTAVE_BANDS[band]) / 10.0))
    level = 10.0 * math.log(sums, 10.0)
    return level


def distant_level(reference_level, distance, reference_distance=1.0):
    """
    Calculates the sound pressure level
    in dependence of a distance
    where a perfect ball-shaped source and spread is assumed.

    reference_level: Sound pressure level in reference distance in dB
    distance: Distance to calculate sound pressure level for, in meters
    reference_distance: reference distance in meters (defaults to 1)
    """
    rel_dist = float(reference_distance) / float(distance)
    level = float(reference_level) + 20.0 * (math.log(rel_dist) / math.log(10))
    return level
