# encoding: utf-8

"""
Example using audiocalc to create a series
of values describing the damping effect of
temperature, humidity and distance.
"""

import audiocalc
import csv

# this is our sound source (a Airbus A319 airplane at start, maybe?)
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

with open('example01.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['humidity', 'temperature', 'distance', 'sound_pressure_level'])
    for temp in range(35):
        for hum in range(20, 90):
            for distance in [500, 1000, 1500, 2000, 2500]:
                level = audiocalc.distant_total_damped_rated_level(
                    octave_frequencies=octave_frequencies,
                    reference_distance=reference_distance,
                    distance=distance,
                    temp=temp,
                    relhum=hum)
                writer.writerow([str(hum), str(temp), str(distance), "%.3f" % level])
