from multiprocessing import Pool
from statistics_for_one_year import StatisticsForOneYear
from file_divider import Divider
from statistics_for_the_years import StatisticsForTheYears
import pandas as pd
import os

class AsynchCollector:
    """
    Класс для асинхронного сбора статистики по годам
    """
    @staticmethod
    def divide_file(file_name):
        """
        Разбивает большой файл на маленькие
        Args:
            file_name (str): Имя большого файла
        """
        Divider.divide_csv(file_name)

    @staticmethod
    def get_statistics(full_file_name, vacancy_name):
        """
        Запускает работу по получению статистики асинхронно
        Args:
            full_file_name (str): Имя файла
            vacancy_name (str): Название вакансии
        """
        currencies_df= pd.read_csv("Currencies.csv", delimiter=',', index_col ="date")
        directoryList = os.listdir(f'SplittedFile/{full_file_name[:-4]}')
        array_to_async = []
        for dirname in directoryList:
            array_to_async.append((f'SplittedFile/{full_file_name[:-4]}/{dirname}',vacancy_name, currencies_df))
        with Pool(len(directoryList)) as p:
            statistics_for_years_array = p.map(StatisticsForOneYear.read_file, array_to_async)
        StatisticsForTheYears.merge_statistics(statistics_for_years_array, full_file_name)
