import unittest

import numpy as np

import spectrum


__author__ = 'lcanavan'


class TestGaussian(unittest.TestCase):
    def test_gaussian_array_input(self):
        self.assertRaises(TypeError, spectrum.gaussian, [1,2,3], 400., 35., 1., 0.)

    def test_gassian_defintion_input(self):
        self.assertRaises(TypeError, spectrum.gaussian, np.linspace(350, 800, num=100), 400., 35., 1., 'zero')

    def test_gaussian_function(self):
        ideal_output = np.array([1.48671951473e-05, 1.75283004936e-01, 3.98942280e+00, 1.75283005e-01, 1.48671951e-05])
        wave = np.linspace(0, 1, num=5)
        gaussian_parameters = [0.5, 0.1, 1., 0.]
        test_output = spectrum.gaussian(wave, *gaussian_parameters).astype(np.float32)
        self.assertTrue(np.allclose(test_output, ideal_output))


class TestSpectrum(unittest.TestCase):
    gaussian_parameters = [0.5, 0.1, 1., 0.]
    wave = np.linspace(0, 1, num=400)
    counts = spectrum.gaussian(wave, *gaussian_parameters)
    s = spectrum.Spectrum(np.array([wave, counts]))

    def test_initialization(self):
        self.assertRaises(TypeError, spectrum.Spectrum, 'bad input')

    def test_integration_bound_input(self):
        self.assertRaises(TypeError, self.s.integrate, start=0, stop=0.5)
        self.assertRaises(TypeError, self.s.integrate, start=0.5, stop=1)

    def test_integrate(self):
        self.assertAlmostEqual(self.s.integrate(), 1, places=1)
        self.assertAlmostEqual(self.s.integrate(start=0.5), 0.5, places=1)
        self.assertAlmostEqual(self.s.integrate(start=0.0, stop=0.5), 0.5, places=2)
        self.assertAlmostEqual(self.s.integrate(start=0.5, stop=1.), 0.5, places=2)

    def test_peak(self):
        self.assertAlmostEqual(self.s.peak(), 0.5, places=2)
        self.assertAlmostEqual(self.s.peak(start=0.3), 0.5, places=2)
        self.assertAlmostEqual(self.s.peak(start=0.25, stop=0.8), 0.5, places=2)

    def test_centroid(self):
        self.assertAlmostEqual(self.s.centroid(start=0.25, stop=0.75), 0.5, places=2)
        self.assertAlmostEqual(self.s.centroid(start=0.5), 0.566, places=2)


if __name__ == '__main__':
    unittest.main()