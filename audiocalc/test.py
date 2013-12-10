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
        damp = audiocalc.damping(20, 80, 8000)
        self.assertEqual("%.4f" % damp, "0.0695")

    def test_total_level_01(self):
        levels = [71.5, 68.5, 64, 58, 53, 47, 40, 32]
        level = audiocalc.total_level(levels)
        self.assertAlmostEqual(level, 73.9109, places=4)

    def test_total_rated_level_01(self):
        level = audiocalc.total_rated_level(self.octave_frequencies)
        self.assertEqual("%.4f" % level, "60.5055")

    def test_distant_level_01(self):
        l = audiocalc.distant_level(
                reference_level=100,
                distance=100,
                reference_distance=1)
        self.assertEqual("%.4f" % l, "60.0000")

    def test_distant_total_level_damped_rated_01(self):
        level = audiocalc.distant_total_damped_rated_level(
            octave_frequencies=self.octave_frequencies,
            reference_distance=300,
            distance=5000,
            temp=20,
            relhum=80)
        self.assertEqual("%.4f" % level, "30.0600")

    def test_distant_total_level_damped_rated_02(self):
        """distance < reference distance"""
        level = audiocalc.distant_total_damped_rated_level(
            octave_frequencies=self.octave_frequencies,
            reference_distance=300,
            distance=200,
            temp=20,
            relhum=80)
        self.assertEqual("%.4f" % level, "64.3338")

    def test_level_to_power_01(self):
        p = audiocalc.level_to_power(100)
        self.assertEqual(p, 0.01)

    def test_leq3_01(self):
        levels = [30, 30, 30]
        leq3 = audiocalc.leq3(levels)
        self.assertAlmostEqual(leq3, 30, places=4)

    def test_leq3_02(self):
        levels = [0, 0, 0]
        leq3 = audiocalc.leq3(levels)
        self.assertEqual(leq3, 0.0)

    def test_leq3_03(self):
        levels = [0, 0, 0.1]
        leq3 = audiocalc.leq3(levels)
        self.assertEqual(leq3, 0.0)

if __name__ == '__main__':
    unittest.main()
