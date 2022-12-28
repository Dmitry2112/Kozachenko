import requests
import pandas as pd
import json


class ApiCollector:
    @staticmethod
    def parse_response(hour):
        def get(dict, key):
            try:
                return dict.get(key)
            except:
                return None
        result_array = []
        for x in range(20):
            for i in range(5):
                res = requests.get(f'https://api.hh.ru/vacancies'
                                   f'?specialization=1'
                                   f'&per_page=100'
                                   f'&page={x}'
                                   f'&date_from=2022-12-26T{hour:02}:00:00'
                                   f'&date_to=2022-12-26T{hour + 1:02}:00:00')
                if res.status_code == 200:
                    print(x)
                    parsedJson = json.loads(res.text)["items"]
                    result_array.append(pd.DataFrame([{'name': get(item, 'name'),
                                          'salary_from': get(get(item, 'salary'), 'from'),
                                          'salary_to': get(get(item, 'salary'), 'to'),
                                          'salary_currency': get(get(item, 'salary'), 'currency'),
                                          'area_name': get(get(item, 'area'), 'name'),
                                          'published_at': get(item, 'published_at')} for item in parsedJson]))
                    break
        return pd.concat(result_array, ignore_index=True)

    @staticmethod
    def collect_api():
        final_dataframe_array = []
        for x in range(0, 23):
            final_dataframe_array.append(ApiCollector.parse_response(x))
        return pd.concat(final_dataframe_array, ignore_index=True)


ApiCollector.collect_api().to_csv('API_3_3_3.csv')
