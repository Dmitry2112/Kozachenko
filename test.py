from unittest import TestCase
from lab_2_1_3 import Report
import unittest


class ReportTest(TestCase):
    def test_report_type(self):
        self.assertEqual(type(Report()).__name__, 'Report')

    def test_collect_programmer(self):
        rep = Report()
        rep.collect_data('vacancies_by_year_small.csv', 'Программист')
        self.assertEqual(str(rep.all_dict[1][2007]), '7500')
        self.assertEqual(len(rep.all_dict), 6)


if __name__ == '__main__':
    unittest.main()
