__author__ = 'lcanavan'

import numpy as np
import nptdms as tdms
import spectrum

GROUP = 'Planck_Data'
CHANNELS = ['Wavelength', 'SampleCounts']


def import_planck_tdms(filename):
    tdms_obj = tdms.TdmsFile(filename)
    tdms_data = np.array([tdms_obj.channel_data(GROUP, channel) for channel in CHANNELS])
    return spectrum.Spectrum(np.vstack(tdms_data))