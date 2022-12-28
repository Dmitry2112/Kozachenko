import pandas as pd


class CurrencyCounter:
    @staticmethod
    def get_statistics_by_cities(full_file_name):
        full_file = pd.read_csv(full_file_name, delimiter=',')
        full_file = full_file[['name', 'salary_from', 'area_name', 'salary_to', 'salary_currency']]
        all_currencies_dict = {}
        for row in full_file.itertuples():
            if row[5] not in all_currencies_dict.keys():
                all_currencies_dict[row[5]] = 1
            else:
                all_currencies_dict[row[5]] += 1
        result_array = []
        for currency in all_currencies_dict.items():
            if str(currency[0]) != 'nan' and currency[1] > 5000:
                result_array.append(str(currency[0]))
        return result_array

    @staticmethod
    def get_first_and_last_date(full_file_name):
        full_file = pd.read_csv(full_file_name, delimiter=',')
        full_file = full_file[['published_at']]
        full_file.sort_values(by='published_at',ascending=False)
        first_date = full_file['published_at'].iloc[-1][:7]
        last_date = full_file['published_at'].iloc[0][:7]
        print(first_date, last_date)
        return first_date, last_date


CurrencyCounter.get_first_and_last_date('vacancies_dif_currencies.csv')
