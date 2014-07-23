__author__ = 'lcanavan'

import re
import calendar
from datetime import datetime as dt

import numpy as np


def match_batch_id(isd_data):
    """Parses CAS120 isd file and returns the first comment"""
    match = re.search(r'Comment]\n(.*)', isd_data)
    batch_id = match.group(1)
    return batch_id


def match_timestamp(isd_data):
    """parses CAS120 isd file and returns the timestamp as a string"""
    date_match = re.search(r'Date=(.*)', isd_data)
    time_match = re.search(r'Time=(.*)', isd_data)
    return date_match.group(1), time_match.group(1)


def convert_isd_timestamp_to_utc(date, time):
    """converts CAS120 timestamp string to utc int"""
    timestamp = dt.strptime(date + ' ' + time, '%m/%d/%Y %I:%M:%S %p')
    utc_time = calendar.timegm(timestamp.timetuple())
    return utc_time


def match_data(isd_data):
    """parses CAS120 isd file and returns 2D numpy array of measured wavelengths and intensitys"""
    match = re.search(r'Data\n((.|\n)*)', isd_data)
    spectra_match = match.group(1).rstrip('\n').split('\n')
    wavelength = [wave.split('\t')[0] for wave in spectra_match]
    intensity = [power.split('\t')[1] for power in spectra_match]
    return np.array([wavelength, intensity]).astype(np.float64)


class Spectrum(object):
    """Base data structure for spectral data."""
    def __init__(self, batch_id, spectrum, timestamp=None):
        self.batch_id = batch_id
        self.spectrum = spectrum
        self.timestamp = dt.fromtimestamp(timestamp)

    def __repr__(self):
        return str(self.batch_id)

    @property
    def integrate(self, wavelength_range=None):
        raise NotImplementedError

    @property
    def peak(self, wavelength_range=None):
        raise NotImplementedError

    @property
    def centroid(self, wavelength_range=None):
        raise NotImplementedError


def main():
    filename = 'C:/Users/lcanavan/Documents/BitBucket/notebook/isd/raw//EE02017-1-D 06-04-2014F2at12-40-50.isd'
    with open(filename) as f:
        isd_string = f.read()
        batch_id = match_batch_id(isd_string)
        isd_timestamp = match_timestamp(isd_string)
        timestamp = convert_isd_timestamp_to_utc(*isd_timestamp)
        spectrum = match_data(isd_string)
        obj = Spectrum(batch_id, spectrum, timestamp=timestamp)
        print 'results: '
        print 'name: ', obj
        print obj.batch_id
        print obj.timestamp
        print obj.spectrum[0:10]
        return


if __name__ == '__main__':
    main()
