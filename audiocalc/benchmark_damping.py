# encoding: utf-8

"""
Performance test

Run with -p parameter to activate profiling.
"""

import audiocalc


if __name__ == '__main__':
    import argparse
    info = "Run benchmark"
    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('-p', '--profile', dest="profile",
            action="store_true", help='Activate profiling', default=False)
    args = parser.parse_args()
    if args.profile:
        import cProfile
        cProfile.run('audiocalc.benchmark_damping()')
    else:
        audiocalc.benchmark_damping()

