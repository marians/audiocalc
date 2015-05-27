# encoding: utf-8

import math


# per named ocatve band: Tuple of (middle frequency, A factor)
OCTAVE_BANDS = {
    'f63': (62.5, -26.21),
    'f125': (125, -16.18),
    'f250': (250, -8.67),
    'f500': (500, -3.25),
    'f1000': (1000, 0),
    'f2000': (2000, 1.2),
    'f4000': (4000, 0.96),
    'f8000': (8000, -1.15)
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
    frN = (pres * pow(tempr, -0.5) * (9.0 + 280.0 * hum * math.exp(-4.17 *
        (pow(tempr, (-1.0 / 3.0)) - 1.0))))
    damp = (8.686 * freq * freq * (
            1.84e-11 * (1.0 / pres) * math.sqrt(tempr) +
            pow(tempr, -2.5) *
            (
                0.01275 * (math.exp(-2239.1 / temp) * 1.0 /
                (frO + freq * freq / frO)) +
                0.1068 * (
                    math.exp(-3352 / temp) * 1.0 /
                    (frN + freq * freq / frN)
                )
            )
        )
    )
    return damp


def total_level(source_levels):
    """
    Calculates the total sound pressure level based on multiple source levels
    """
    sums = 0.0
    for l in source_levels:
        if l is None:
            continue
        if l == 0:
            continue
        sums += pow(10.0, float(l) / 10.0)
    level = 10.0 * math.log10(sums)
    return level


def total_rated_level(octave_frequencies):
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
        if octave_frequencies[band] == 0:
            continue
        sums += pow(10.0, ((float(octave_frequencies[band]) + OCTAVE_BANDS[band][1]) / 10.0))
    level = 10.0 * math.log10(sums)
    return level


def leq3(levels):
    """
    Calculates the energy-equivalent (Leq3) value
    given a regular measurement interval.
    """
    n = float(len(levels))
    sums = 0.0
    if sum(levels) == 0.0:
        return 0.0
    for l in levels:
        if l == 0:
            continue
        sums += pow(10.0, float(l) / 10.0)
    leq3 = 10.0 * math.log10((1.0 / n) * sums)
    leq3 = max(0.0, leq3)
    return leq3


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


def distant_total_damped_rated_level(
            octave_frequencies,
            distance,
            temp,
            relhum,
            reference_distance=1.0):
    """
    Calculates the damped, A-rated total sound pressure level
    in a given distance, temperature and relative humidity
    from octave frequency sound pressure levels in a reference distance
    """
    damping_distance = distance - reference_distance
    sums = 0.0
    for band in OCTAVE_BANDS.keys():
        if band not in octave_frequencies:
            continue
        if octave_frequencies[band] is None:
            continue
        # distance-adjusted level per band
        distant_val = distant_level(
            reference_level=float(octave_frequencies[band]),
            distance=distance,
            reference_distance=reference_distance
        )
        # damping
        damp_per_meter = damping(
            temp=temp,
            relhum=relhum,
            freq=OCTAVE_BANDS[band][0])
        distant_val = distant_val - (damping_distance * damp_per_meter)
        # applyng A-rating
        distant_val += OCTAVE_BANDS[band][1]
        sums += pow(10.0, (distant_val / 10.0))
    level = 10.0 * math.log10(sums)
    return level


def level_to_power(level):
    """
    Converts logarithmic sound pressure level value (dB)
    to metric power value (W/m^2)
    """
    return pow(10.0, (float(level) / 10.0)) * 1e-12


def benchmark_damping():
    # this is our sound source
    octave_frequencies = {
        'f63': 86,
        'f125': 89.5,
        'f250': 87.5,
        'f500': 86.0,
        'f1000': 83.0,
        'f2000': 80.0,
        'f4000': 77,
        'f8000': 67.5
    }

    # the above values have been measure in this distance:
    reference_distance = 300

    import time
    start = time.clock()

    for temp in xrange(-20, 35):
        for hum in xrange(30, 98):
            for distance in xrange(500, 10000, 500):
                distant_total_damped_rated_level(
                    octave_frequencies=octave_frequencies,
                    reference_distance=reference_distance,
                    distance=distance,
                    temp=temp,
                    relhum=hum)
    print("Duration: %.3f sec" % (time.clock() - start))
