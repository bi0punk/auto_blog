from datetime import datetime, timezone
from unittest.mock import patch

from django.test import TestCase

from .tasks import _parse_float, _parse_lat_lon, _parse_utc_time


class TaskHelpersTest(TestCase):
    def test_parse_float_valid(self):
        self.assertEqual(_parse_float('3.8'), 3.8)
        self.assertEqual(_parse_float('  239  '), 239.0)

    def test_parse_float_none(self):
        self.assertIsNone(_parse_float(''))
        self.assertIsNone(_parse_float('N/A'))

    def test_parse_lat_lon_valid(self):
        lat, lon = _parse_lat_lon('-23.576 / -67.224')
        self.assertAlmostEqual(lat, -23.576)
        self.assertAlmostEqual(lon, -67.224)

    def test_parse_lat_lon_invalid(self):
        lat, lon = _parse_lat_lon('')
        self.assertIsNone(lat)
        self.assertIsNone(lon)

    def test_parse_utc_time_valid(self):
        dt = _parse_utc_time('2024-07-02 18:38:57')
        self.assertIsNotNone(dt)
        self.assertEqual(dt.year, 2024)
        self.assertEqual(dt.month, 7)
        self.assertEqual(dt.tzinfo, timezone.utc)

    def test_parse_utc_time_invalid(self):
        self.assertIsNone(_parse_utc_time(''))
        self.assertIsNone(_parse_utc_time('no-date'))
