from asynchronous_statistics_collector import AsynchCollector

#file_name = "vacancies_by_year.csv"


def main():
    file_name = input('Введите название файла: ')
    vac_name = input('Введите название вакансии: ')
    AsynchCollector.get_statistics(file_name, vac_name)


if __name__ == '__main__':
    main()
