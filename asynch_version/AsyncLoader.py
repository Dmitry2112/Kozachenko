from multiprocessing import Pool
from One_Year_Statistics import OneYearStatistics
from FileSplitter import Splitter
from All_Years_Statistics import AllYearsStatistics
import concurrent.futures as pool
import os


class AsyncLoader:
    """
    Класс для асинхронного сбора статистики по годам
    """
    @staticmethod
    def split_file(file_name):
        """
        Разбивает большой файл на маленькие
        Args:
            file_name (str): Имя большого файла
        """
        Splitter.split_CSV(file_name)

    @staticmethod
    def get_statistics(full_file_name, vacancy_name):
        """
        Запускает работу по получению статистики асинхронно
        Args:
            full_file_name (str): Имя файла
            vacancy_name (str): Название вакансии
        """
        directory_list = os.listdir(f'SplittedFile/{full_file_name[:-4]}')
        array_to_async = []
        for dirname in directory_list:
            array_to_async.append((f'SplittedFile/{full_file_name[:-4]}/{dirname}', vacancy_name))
        with pool.ThreadPoolExecutor(max_workers=3) as executor:
            statistics_for_years_array = executor.map(OneYearStatistics.read_file, array_to_async)
        # with Pool(6) as p:
        #     statistics_for_years_array = p.map(OneYearStatistics.read_file, array_to_async)
        AllYearsStatistics.merge_statistics(statistics_for_years_array, full_file_name)
