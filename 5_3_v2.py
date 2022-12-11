import csv
import re


class Statistic:
    currency_to_rub = {
        "AZN": 35.68,
        "BYR": 23.91,
        "EUR": 59.90,
        "GEL": 21.74,
        "KGS": 0.76,
        "KZT": 0.13,
        "RUR": 1,
        "UAH": 1.64,
        "USD": 60.66,
        "UZS": 0.0055,
    }

    def __init__(self, file_name):
        self.file_name = file_name
        self.salary_per_year = {}
        self.total_vac_per_year = {}
        self.job_salary_per_year = {}
        self.job_vac_per_year = {}
        self.salary_per_city = {}
        self.vac_per_city = {}
        self.limit_vac_num = 0
        self.vac_count = 0


    @staticmethod
    def clean_string(string):
        string = re.sub(r'<[^>]*>', '', string)
        string = ' '.join(string.split())
        return string

    def print_data(self):
        print(f'Динамика уровня зарплат по годам: {self.salary_per_year}')

        print(f'Динамика количества вакансий по годам: {self.total_vac_per_year}')

        for y in self.salary_per_year:
            if y not in self.job_salary_per_year:
                self.job_salary_per_year[y] = 0
        print(f'Динамика уровня зарплат по годам для выбранной профессии: {self.job_salary_per_year}')

        for y in self.salary_per_year:
            if y not in self.job_vac_per_year:
                self.job_vac_per_year[y] = 0
        print(f'Динамика количества вакансий по годам для выбранной профессии: {self.job_vac_per_year}')

        filtered_salary_per_city = {}
        for s in self.salary_per_city:
            if self.vac_per_city[s] >= self.limit_vac_num:
                filtered_salary_per_city[s] = self.salary_per_city[s]

        filtered_vac_per_city = {}
        for s in self.vac_per_city:
            if self.vac_per_city[s] >= self.limit_vac_num:
                filtered_vac_per_city[s] = self.vac_per_city[s]

        final_salary_per_city = dict(sorted(filtered_salary_per_city.items(), key=lambda x: x[1], reverse=True))
        final_vac_per_city = dict(sorted(filtered_vac_per_city.items(), key=lambda x: x[1], reverse=True))

        k = 0
        print('Уровень зарплат по городам (в порядке убывания): {', end='')
        for city in final_salary_per_city:
            print(f'\'{city}\': {final_salary_per_city[city]}', end='')
            if k < len(final_salary_per_city) - 1 and k < 9:
                print(', ', end='')
            k += 1
            if k == 10:
                break
        print('}')

        k = 0
        print('Доля вакансий по городам (в порядке убывания): {', end='')
        for city in final_vac_per_city:
            frac_str = f'{final_vac_per_city[city] / self.vac_count:.4f}'.rstrip('0')
            if frac_str.endswith('.'):
                frac_str += '0'
            print(f'\'{city}\': {frac_str}', end='')
            if k < len(final_vac_per_city) - 1 and k < 9:
                print(', ', end='')
            k += 1
            if k == 10:
                break
        print('}')

    def collect_data(self, job_name):
        file_csv = csv.reader(open(self.file_name, encoding='utf_8_sig'))
        list_data = [x for x in file_csv]
        titles = list_data[0]
        values = [x for x in list_data[1:] if x.count('') == 0 and len(x) == len(titles)]
        self.total_vac_per_year = {}
        self.salary_per_year = {}
        self.job_vac_per_year = {}
        self.job_salary_per_year = {}
        self.salary_per_city = {}
        self.vac_per_city = {}
        self.limit_vac_num = int(len(values) * 0.01)
        self.vac_count = len(values)
        name_index = 0
        salary_from_index = 0
        salary_to_index = 0
        salary_currency_index = 0
        area_name_index = 0
        published_at_index = 0
        for i in range(len(titles)):
            if titles[i] == 'name':
                name_index = i
            if titles[i] == 'salary_from':
                salary_from_index = i
            if titles[i] == 'salary_to':
                salary_to_index = i
            if titles[i] == 'salary_currency':
                salary_currency_index = i
            if titles[i] == 'area_name':
                area_name_index = i
            if titles[i] == 'published_at':
                published_at_index = i

        for k in range(len(values)):
            raw_vac = values[k]
            vac = []
            for j in range(len(raw_vac)):
                vac.append(Statistic.clean_string(raw_vac[j]))
            year = int(vac[published_at_index][0:4])
            salary_rub = (float(vac[salary_from_index]) + float(vac[salary_to_index])) * 0.5 * Statistic.currency_to_rub[vac[salary_currency_index]]
            if year in self.total_vac_per_year:
                self.total_vac_per_year[year] += 1
            else:
                self.total_vac_per_year[year] = 1
            # job_name
            if job_name in vac[name_index]:
                if year in self.job_vac_per_year:
                    self.job_vac_per_year[year] += 1
                else:
                    self.job_vac_per_year[year] = 1
                if year in self.job_salary_per_year:
                    x = self.job_salary_per_year[year]
                    x = x[0] + salary_rub, x[1] + 1
                    self.job_salary_per_year[year] = x
                else:
                    self.job_salary_per_year[year] = salary_rub, 1

            if year in self.salary_per_year:
                x = self.salary_per_year[year]
                x = x[0] + salary_rub, x[1] + 1
                self.salary_per_year[year] = x
            else:
                self.salary_per_year[year] = salary_rub, 1

            # per_city
            if vac[area_name_index] in self.vac_per_city:
                self.vac_per_city[vac[area_name_index]] += 1
            else:
                self.vac_per_city[vac[area_name_index]] = 1

            if vac[area_name_index] in self.salary_per_city:
                x = self.salary_per_city[vac[area_name_index]]
                x = x[0] + salary_rub, x[1] + 1
                self.salary_per_city[vac[area_name_index]] = x
            else:
                self.salary_per_city[vac[area_name_index]] = salary_rub, 1

        for y in self.salary_per_year:
            x = self.salary_per_year[y]
            self.salary_per_year[y] = int(x[0] / x[1])

        for y in self.job_salary_per_year:
            x = self.job_salary_per_year[y]
            self.job_salary_per_year[y] = int(x[0] / x[1])

        for y in self.salary_per_city:
            x = self.salary_per_city[y]
            self.salary_per_city[y] = int(x[0] / x[1])


def main_5_3_v2():
    file_name = input('Введите название файла: ')
    stat = Statistic(file_name)
    job_name = input('Введите название профессии: ')
    stat.collect_data(job_name)
    stat.print_data()


main_5_3_v2()
