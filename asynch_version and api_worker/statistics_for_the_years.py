import math
import pandas as pd
from statistics_for_one_year import StatisticsForOneYear

from statistics_for_one_year import StatisticsForOneYearInfo


class StatisticsForTheYears:
    """
    Класс для сбора статистики по всем годам
    """
    @staticmethod
    def sort_dic(dic):
        """
        Сортирует значения словаря
        Args:
            dic (dict): Словарь, значения которого нужно отсортировать

        Returns:
            dict: Словарь с отсортированными значениями
        """
        return dict(sorted(dic.items(), key=lambda item: float(item[1]), reverse=True))

    @staticmethod
    def get_ten_len(dic):
        """
        Берет первые 10 значений из словаря
        Args:
            dic (dict): Исходный словарь

        Returns:
            dict: Словарь с первыми 10 значениями
        """
        result = {}
        for x in dic.keys():
            result[x] = dic[x]
            if len(result) == 10:
                return result
        return result

    @staticmethod
    def get_statistics_by_cities(full_file_name):
        """
        Составляет статистику по городам
        Args:
            full_file_name (str): Название csv файла с вакансиями

        Returns:
            dict, dict: Словари со статистикой
        """
        full_file = pd.read_csv(full_file_name, delimiter=',')
        full_file = full_file[['name', 'salary_from', 'area_name', 'salary_to', 'salary_currency']]
        full_file = full_file.assign(salary_middle=lambda row: (row.salary_from + row.salary_to) / 2)
        full_file['salary_middle'] = full_file['salary_middle'] * full_file['salary_currency'].apply(lambda y: StatisticsForOneYear.currency_to_rub[y])
        all_towns_array = []
        towns_statistics_salary_dic = {}
        towns_statistics_amount_dic = {}
        groups_by_towns = full_file.groupby('area_name')
        for row in full_file.itertuples():
            if row[3] in all_towns_array:
                continue
            else:
                all_towns_array.append(row[3])

        for town in all_towns_array:
            current_group = groups_by_towns.get_group(town)
            if len(current_group) < len(full_file) / 100:
                continue
            else:
                towns_statistics_salary_dic[town] = math.ceil(current_group['salary_middle'].mean())
                towns_statistics_amount_dic[town] = len(current_group)
        towns_statistics_salary_dic = StatisticsForTheYears.get_ten_len(StatisticsForTheYears.sort_dic(towns_statistics_salary_dic))
        towns_statistics_amount_dic = StatisticsForTheYears.get_ten_len(StatisticsForTheYears.sort_dic(towns_statistics_amount_dic))
        return towns_statistics_amount_dic, towns_statistics_salary_dic

    @staticmethod
    def merge_statistics(array_of_year_stat_objects: [StatisticsForOneYearInfo], full_file_name: str):
        """
        Объединяет статистики и распечатывает их
        Args:
            array_of_year_stat_objects: Массив со статистиками по годам
            full_file_name (str): Имя файла
        """
        towns_statistics_amount_dic, towns_statistics_salary_dic = StatisticsForTheYears.get_statistics_by_cities(full_file_name)
        dic_year_amount = {}
        dic_year_salary = {}
        vac_year_amount = {}
        vac_year_salary = {}
        for year_stat_object in array_of_year_stat_objects:
            dic_year_amount[year_stat_object.year] = year_stat_object.vacancies_amount_by_year
            dic_year_salary[year_stat_object.year] = round(year_stat_object.middle_salary_by_year,2)
            vac_year_amount[year_stat_object.year] = year_stat_object.vacancies_amount_by_year_for_vac
            vac_year_salary[year_stat_object.year] = round(year_stat_object.middle_salary_by_year_for_vac,2)
        print(f'Динамика уровня зарплат по годам: {dic_year_amount}')
        print(f'Динамика количества вакансий по годам: {dic_year_salary}')
        print(f'Динамика уровня зарплат по годам для выбранной профессии: {vac_year_amount}')
        print(f'Динамика количества вакансий по годам для выбранной профессии: {vac_year_salary}')
        print(f'Уровень зарплат по городам (в порядке убывания): {towns_statistics_salary_dic}')
        print(f'Доля вакансий по городам (в порядке убывания): {towns_statistics_amount_dic}')


