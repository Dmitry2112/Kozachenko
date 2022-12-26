from AsyncLoader import AsyncLoader

#file_name = "vacancies_by_year.csv"


def main():
    file_name = input('Введите название файла: ')
    vac_name = input('Введите название вакансии: ')
    AsyncLoader.get_statistics(file_name, vac_name)


if __name__ == '__main__':
    main()
