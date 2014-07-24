__author__ = 'lcanavan'

from scipy import integrate
import numpy as np
import math


def gaussian(x, mean, stdev, max, offset):
    ''' Returns the gaussian function for B=m,stdev,max,offset '''
    ''' x is x-axis array, feed into fx for y '''
    if not isinstance(x, np.ndarray):
        raise TypeError
    for input in [mean, stdev, max, offset]:
        if not isinstance(input, float):
            raise TypeError
    return offset + max / (stdev * math.sqrt(2 * math.pi)) * np.exp(-((x - mean) ** 2 / (2 * stdev ** 2)))


class Spectrum(object):
    """Base data structure for spectral data."""
    def __init__(self, spectrum, description=None, timestamp=None):
        if not isinstance(spectrum, np.ndarray):
            raise TypeError
        self.spectrum = spectrum
        self.description = description
        self.timestamp = timestamp

    def integrate(self, start=None, stop=None):
        """should probably do value checks on integration bounds"""
        if start is not None and not isinstance(start, float):
            raise TypeError
        if stop is not None and not isinstance(stop, float):
            raise TypeError
        if start is None:
            start = self.spectrum[0].min()
        if stop is None:
            stop = self.spectrum[0].max()

        idx = (self.spectrum[0, :] >= start) & (self.spectrum[0, :] <= stop)
        return integrate.trapz(self.spectrum[1, idx], self.spectrum[0, idx])

    def peak(self, start=None, stop=None):
        if start is not None and not isinstance(start, float):
            raise TypeError
        if stop is not None and not isinstance(stop, float):
            raise TypeError
        if start is None:
            start = self.spectrum[0].min()
        if stop is None:
            stop = self.spectrum[0].max()

        idx = np.argmax(np.max(self.spectrum, axis=0))
        return self.spectrum[0, idx]

    def centroid(self, start=None, stop=None):
        if start is not None and not isinstance(start, float):
            raise TypeError
        if stop is not None and not isinstance(stop, float):
            raise TypeError
        if start is None:
            start = self.spectrum[0].min()
        if stop is None:
            stop = self.spectrum[0].max()

        half_integral = self.integrate(start=start, stop=stop) / 2.
        idx = (self.spectrum[0, :] >= start) & (self.spectrum[0, :] <= stop)
        clipped_array = self.spectrum[:, idx]
        cum_integral = integrate.cumtrapz(clipped_array[1, :], clipped_array[0, :])
        cum_idx = (cum_integral >= half_integral)
        return clipped_array[:, cum_idx][0, 0]

