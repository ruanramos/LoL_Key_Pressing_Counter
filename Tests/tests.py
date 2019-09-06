import unittest
from key_counter import str_time_2_seconds


class TestStrTime2Seconds(unittest.TestCase):
    def test_str_time_2_seconds(self):
        self.assertEqual(9945, str_time_2_seconds('2:45:45'))

    def test_str_time_2_seconds_1_hour(self):
        self.assertEqual(3600, str_time_2_seconds('1:00:00'))

    def test_str_time_2_seconds_59_minutes_59_sec(self):
        self.assertEqual(3599, str_time_2_seconds('0:59:59'))


if __name__ == '__main__':
    unittest.main()
