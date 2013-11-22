# encoding: utf-8

import audiocalc
import unittest


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_damping_01(self):
        self.assertAlmostEqual(audiocalc.damping(20, 80, 8000), 0.06945538)

    def test_total_level_01(self):
        octave_frequencies = {
            'f63': 71.5,
            'f125': 68.5,
            'f250': 64,
            'f500': 58,
            'f1000': 53,
            'f2000': 47,
            'f4000': 40,
            'f8000': 32
        }
        level = audiocalc.total_level(octave_frequencies)
        self.assertAlmostEqual(level, 73.91092323)

    def test_total_level_rated_01(self):
        octave_frequencies = {
            'f63': 71.5,
            'f125': 68.5,
            'f250': 64,
            'f500': 58,
            'f1000': 53,
            'f2000': 47,
            'f4000': 40,
            'f8000': 32
        }
        level = audiocalc.total_level_rated(octave_frequencies)
        self.assertAlmostEqual(level, 60.5054659)

    def test_distant_level_01(self):
        l = audiocalc.distant_level(
                reference_level=100,
                distance=100,
                reference_distance=1)
        self.assertAlmostEqual(l, 60)

if __name__ == '__main__':
    unittest.main()
