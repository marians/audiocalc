# encoding: utf-8

import audiocalc
import unittest


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.octave_frequencies = {
            'f63': 71.5,
            'f125': 68.5,
            'f250': 64,
            'f500': 58,
            'f1000': 53,
            'f2000': 47,
            'f4000': 40,
            'f8000': 32}

    def test_damping_01(self):
        self.assertAlmostEqual(audiocalc.damping(20, 80, 8000), 0.06945538)

    def test_total_level_01(self):
        level = audiocalc.total_level(self.octave_frequencies)
        self.assertAlmostEqual(level, 73.91092323)

    def test_total_rated_level_01(self):
        level = audiocalc.total_rated_level(self.octave_frequencies)
        self.assertAlmostEqual(level, 60.5054659)

    def test_distant_level_01(self):
        l = audiocalc.distant_level(
                reference_level=100,
                distance=100,
                reference_distance=1)
        self.assertAlmostEqual(l, 60)

    def test_distant_total_level_damped_rated_01(self):
        level = audiocalc.distant_total_damped_rated_level(
            octave_frequencies=self.octave_frequencies,
            reference_distance=300,
            distance=5000,
            temp=20,
            relhum=80)
        self.assertAlmostEqual(level, 30.05875295)

    def test_distant_total_level_damped_rated_02(self):
        """distance < reference distance"""
        level = audiocalc.distant_total_damped_rated_level(
            octave_frequencies=self.octave_frequencies,
            reference_distance=300,
            distance=200,
            temp=20,
            relhum=80)
        self.assertAlmostEqual(level, 64.33378745)

    def test_level_to_power_01(self):
        p = audiocalc.level_to_power(100)
        self.assertEqual(p, 0.01)

if __name__ == '__main__':
    unittest.main()
