import csv
import os


class Splitter:
    """
    Класс для разделения большого csv на маленькие
    """
    __final_files_dict = {}

    @staticmethod
    def split_CSV(file_name):
        """
        Разделяет большой csv файл на маленькие файлы - группы по годам
        Args:
            file_name (str): Название файла
        """
        dirname = "SplittedFile"
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        with open(file_name, encoding="utf-8-sig") as csvfile:
            file_name = f"{dirname}/{file_name.split('/')[-1].split('.')[0]}"
            if not os.path.exists(file_name):
                os.mkdir(file_name)
            reader = csv.DictReader(csvfile)
            name_of_fields = list(reader.fieldnames)
            for row in reader:
                year = row["published_at"].split("-")[0]
                if year not in Splitter.__final_files_dict:
                    new_name_file = f"{file_name}/{year}.csv"
                    new_file = open(new_name_file, "w+", encoding="utf-8-sig", newline='')
                    Splitter.__final_files_dict[year] = csv.DictWriter(new_file, name_of_fields)
                    Splitter.__final_files_dict[year].writeheader()

                Splitter.__final_files_dict[year].writerow(row)
