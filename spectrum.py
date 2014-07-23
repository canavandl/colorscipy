__author__ = 'lcanavan'


class Spectrum(object):
    """Base data structure for spectral data."""
    def __init__(self, batch_id=None, spectrum=None, timestamp=None):
        self.batch_id = batch_id
        self.spectrum = spectrum
        self.timestamp = timestamp

    @property
    def integrate(self, wavelength_range=None):
        raise NotImplementedError

    @property
    def peak(self, wavelength_range=None):
        raise NotImplementedError

    @property
    def centroid(self, wavelength_range=None):
        raise NotImplementedError
