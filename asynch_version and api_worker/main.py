from asynchronous_statistics_collector import AsynchCollector


def main():
    file_name = input('Введите название файла: ')
    vac_name = input('Введите название вакансии: ')
    AsynchCollector.get_statistics(file_name, vac_name)


if __name__ == '__main__':
    main()
