# encoding: utf-8

"""
Performance test

Run with -p parameter to activate profiling.
"""

import audiocalc


def main():
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

    for temp in range(-20, 35):
        for hum in range(30, 98):
            for distance in range(500, 10000, 500):
                audiocalc.distant_total_damped_rated_level(
                    octave_frequencies=octave_frequencies,
                    reference_distance=reference_distance,
                    distance=distance,
                    temp=temp,
                    relhum=hum)


if __name__ == '__main__':
    import argparse
    import time
    start = time.clock()
    info = "Run benchmark"
    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('-p', '--profile', dest="profile",
            action="store_true", help='Activate profiling', default=False)
    args = parser.parse_args()
    if args.profile:
        import cProfile
        cProfile.run('main()')
    else:
        main()
    print "Duration: %.3f sec" % (time.clock() - start)
