__author__ = 'lcanavan'

import re
import calendar
from datetime import datetime as dt

import numpy as np

import spectrum

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


def import_cas_isd(filename):
    with open(filename) as f:
        isd_data = f.read()
        xy = match_batch_id(isd_data)
        batch_id = match_batch_id(isd_data)
        timestamp = match_timestamp(isd_data)
        return spectrum.Spectrum(xy, description=batch_id, timestamp=timestamp)