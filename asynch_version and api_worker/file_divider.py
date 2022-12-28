import csv
import os


class Divider:
    """
    Класс для разделения большого csv на маленькие
    """
    __final_files_dict = {}

    @staticmethod
    def divide_csv(file_name):
        """
        Разделяет большой csv файл на маленькие файлы - группы по годам
        Args:
            file_name (str): Название файла
        """
        dirname = "DividedFile"
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
                if year not in Divider.__final_files_dict:
                    new_name_file = f"{file_name}/{year}.csv"
                    new_file = open(new_name_file, "w+", encoding="utf-8-sig", newline='')
                    Divider.__final_files_dict[year] = csv.DictWriter(new_file, name_of_fields)
                    Divider.__final_files_dict[year].writeheader()

                Divider.__final_files_dict[year].writerow(row)
