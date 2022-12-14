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

    def test_collect_analyst(self):
        rep = Report()
        rep.collect_data('vacancies_by_year_small.csv', 'Аналитик')
        self.assertEqual(str(rep.all_dict[0][2007]), '45027')
        self.assertEqual(str(rep.all_dict[4]['Москва']), '50041')

    def test_split_and_concat(self):
        self.assertEqual(Report.split_and_concat('Москва'), 'Москва')
        self.assertEqual(Report.split_and_concat('Нижний Новгород'), 'Нижний\nНовгород')
        self.assertEqual(Report.split_and_concat('Санкт-Петербург'), 'Санкт-\nПетербург')


if __name__ == '__main__':
    unittest.main()
