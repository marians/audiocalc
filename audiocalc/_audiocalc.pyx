# encoding: utf-8

from libc.math cimport exp, log, log10, pow, sqrt

ctypedef double mydouble

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


cpdef mydouble damping(mydouble temp, int relhum, mydouble freq, mydouble pres=101325.0):
    """
    Calculates the damping factor for sound in dB/m
    depending on temperature, humidity and sound frequency.
    Source: http://www.sengpielaudio.com/LuftdaempfungFormel.htm

    temp: Temperature in degrees celsius
    relhum: Relative humidity as percentage, e.g. 50
    freq: Sound frequency in herz
    pres: Atmospheric pressure in kilopascal
    """
    cdef mydouble c_humid
    cdef mydouble hum
    cdef mydouble tempr
    cdef mydouble frO
    cdef mydouble frN

    temp += 273.15  # convert to kelvin
    pres = pres / 101325.0  # convert to relative pressure
    c_humid = 4.6151 - 6.8346 * pow((273.15 / temp), 1.261)
    hum = relhum * pow(10.0, c_humid) * pres
    tempr = temp / 293.15  # convert to relative air temp (re 20 deg C)
    frO = pres * (24.0 + 4.04e4 * hum * (0.02 + hum) / (0.391 + hum))
    frN = pres * pow(tempr, -0.5) * (9.0 + 280.0 * hum * exp(-4.17 * (pow(tempr, (-1.0 / 3.0)) - 1.0)))
    return 8.686 * freq * freq * (1.84e-11 * (1.0 / pres) * sqrt(tempr) + pow(tempr, -2.5) * (0.01275 * (exp(-2239.1 / temp) * 1.0 / (frO + freq * freq / frO)) + 0.1068 * (exp(-3352 / temp) * 1.0 / (frN + freq * freq / frN))))



def total_level(source_levels):
    """
    Calculates the total sound pressure level based on octave band frequencies
    """
    cdef mydouble level
    cdef mydouble sums = 0.0

    for l in source_levels:
        if l is None:
            continue
        if l == 0:
            continue
        sums += pow(10.0, (<mydouble>l / 10.0))
    level = 10.0 * log10(sums)
    return level


def total_rated_level(octave_frequencies):
    """
    Calculates the A-rated total sound pressure level
    based on octave band frequencies
    """
    cdef mydouble level
    cdef mydouble dummy
    cdef mydouble afactor
    cdef mydouble sums = 0.0

    for band, (dummy, afactor) in OCTAVE_BANDS.iteritems():
        if octave_frequencies.get(band) is None:
            continue

        sums += pow(10.0, ((<mydouble>octave_frequencies[band] + afactor) / 10.0))

    level = 10.0 * log10(sums)
    return level


cpdef mydouble leq3(levels):
    """
    Calculates the energy-equivalent (Leq3) value
    given a regular measurement interval.
    """
    cdef mydouble q
    cdef mydouble n
    cdef mydouble sums = 0.0
    q = 10.0 * log10(2.0)  # pretty much 3
    n = <mydouble>len(levels)
    if sum(levels) == 0.0:
        return 0.0
    for l in levels:
        if l == 0:
            continue
        sums += pow(10.0, <mydouble>l / 10.0)
    leq3 = (q / log10(2.0)) * log10((1.0 / n) * sums)
    leq3 = max(0.0, leq3)
    return leq3


cpdef mydouble distant_level(mydouble reference_level, mydouble distance, mydouble reference_distance=1.0):
    """
    Calculates the sound pressure level
    in dependence of a distance
    where a perfect ball-shaped source and spread is assumed.

    reference_level: Sound pressure level in reference distance in dB
    distance: Distance to calculate sound pressure level for, in meters
    reference_distance: reference distance in meters (defaults to 1)
    """
    cdef mydouble rel_dist

    rel_dist = reference_distance / distance
    return reference_level + 20.0 * (log(rel_dist) / log(10))


cpdef mydouble distant_total_damped_rated_level(
            octave_frequencies,
            int distance,
            mydouble temp,
            int relhum,
            mydouble reference_distance=1.0):
    """
    Calculates the damped, A-rated total sound pressure level
    in a given distance, temperature and relative humidity
    from octave frequency sound pressure levels in a reference distance
    """
    cdef mydouble damping_distance
    cdef mydouble sums
    cdef mydouble distant_val
    cdef mydouble damp_per_meter
    cdef mydouble level
    cdef mydouble midfreq
    cdef mydouble afactor

    damping_distance = distance - reference_distance
    sums = 0.0

    for band, (midfreq, afactor) in OCTAVE_BANDS.iteritems():
        if octave_frequencies.get(band) is None:
            continue

        # distance-adjusted level per band
        distant_val = distant_level(
            reference_level=<mydouble>octave_frequencies[band],
            distance=distance,
            reference_distance=reference_distance
        )
        # damping
        damp_per_meter = damping(
            temp=temp,
            relhum=relhum,
            freq=midfreq)
        distant_val = distant_val - (damping_distance * damp_per_meter)
        # applyng A-rating
        distant_val += afactor
        sums += pow(10.0, (distant_val / 10.0))

    return 10.0 * log10(sums)


def level_to_power(mydouble level):
    """
    Converts logarithmic sound pressure level value (dB)
    to metric power value (W/m^2)
    """
    return pow(10.0, level / 10.0) * 1e-12


def benchmark_damping():
    cdef mydouble reference_distance
    cdef mydouble temp
    cdef int hum
    cdef int distance

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

    for temp in range(-20, 35):
        for hum in range(30, 98):
            for distance in range(500, 10000, 500):
                distant_total_damped_rated_level(
                    octave_frequencies=octave_frequencies,
                    reference_distance=reference_distance,
                    distance=distance,
                    temp=<mydouble>temp,
                    relhum=hum)

    print("Duration: %.3f sec" % (time.clock() - start))
