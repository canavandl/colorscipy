import unittest
import cas_isd
import numpy as np

__author__ = 'lcanavan'


class TestMatchBatchId(unittest.TestCase):
    """Assures match_batch_id returns correct batch id"""

    def test_match_batch_id(self):
        isd_chunk = '\n' \
                    '[Comment]\n' \
                    'EE02017-1-D\n' \
                    '\n' \
                    '[Measurement Conditions]\n'
        self.assertEqual(cas_isd.match_batch_id(isd_chunk), 'EE02017-1-D')


class TestMatchTimestamp(unittest.TestCase):
    """Assures match_timestamp returns isd date/time tuple (raw format"""

    def test_match_timestamp(self):
        isd_chuck = '[General Information]\n' \
                    'Date=6/4/2014\n' \
                    'Time=10:50:28 AM\n' \
                    'User=instruments\n'
        self.assertEqual(cas_isd.match_timestamp(isd_chuck), ('6/4/2014', '10:50:28 AM'))


class TestConvertISDTimestampToUTC(unittest.TestCase):
    """Assures isd timestamp converts to utc correctly"""

    def test_convert_isd_timestamp_to_utc(self):
        isd_timestamp = ('6/4/2014', '10:50:28 AM')
        self.assertEqual(cas_isd.convert_isd_timestamp_to_utc(*isd_timestamp), 1401879028)


class TestMatchData(unittest.TestCase):
    """Assures isd data is correctly parsed"""

    def test_match_data(self):
        isd_chunk = 'Y-Unit=W/nm\n' \
                    'Data\n' \
                    '238.135131835938	4.79304985711359E-006\n' \
                    '238.502563476562	3.77735772486167E-006\n' \
                    '238.869995117187	4.82081126825212E-006\n'
        demo_spectra = np.array([[238.135131835938, 238.502563476562, 238.869995117187],
                                 [4.79304985711359E-006, 3.77735772486167E-006, 4.82081126825212E-006]])
        self.assertTrue(np.array_equal(cas_isd.match_data(isd_chunk), demo_spectra))


if __name__ == '__main__':
    unittest.main()