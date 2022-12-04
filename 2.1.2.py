import csv
import re
import matplotlib.pyplot as plt


class Report:
    def __init__(self):
        pass


    def generate_image(self, job_name, all_dict):
        fig, ax = plt.subplots(2, 2)
        # 1 диаграмма
        ax[0, 0].bar([y - 0.2 for y in all_dict[0].keys()], all_dict[0].values(), width=0.4)
        ax[0, 0].bar([y + 0.2 for y in all_dict[1].keys()], all_dict[1].values(), width=0.4)
        ax[0, 0].grid(axis='y')
        ax[0, 0].title.set_text('Уровень зарплат по годам')
        ax[0, 0].legend(['средняя з/п', f'з/п {job_name}'], loc='upper left')
        xmarks = range(min(all_dict[0].keys()), max(all_dict[0].keys()) + 1)
        ax[0, 0].set_xticks(xmarks)
        ax[0, 0].set_xticklabels(xmarks, rotation=90)
        ax[0, 0].tick_params(axis='both', which='major', labelsize=8)
        plt.subplots_adjust(hspace=0.5)

        # 2 диаграмма
        ax[0, 1].bar([y - 0.2 for y in all_dict[2].keys()], all_dict[2].values(), width=0.4)
        ax[0, 1].bar([y + 0.2 for y in all_dict[3].keys()], all_dict[3].values(), width=0.4)
        ax[0, 1].grid(axis='y')
        ax[0, 1].title.set_text('Количество вакансий по годам')
        ax[0, 1].legend(['Количество вакансий', f'Количество вакансий\n{job_name}'], loc='upper left')
        xmarks = range(min(all_dict[2].keys()), max(all_dict[2].keys()) + 1)
        ax[0, 1].set_xticks(xmarks)
        ax[0, 1].set_xticklabels(xmarks, rotation=90)
        ax[0, 1].tick_params(axis='both', which='major', labelsize=8)

        # 3 диаграмма
        keys_rev = list(all_dict[4].keys()).copy()
        values_rev = list(all_dict[4].values()).copy()
        keys_rev.reverse()
        values_rev.reverse()
        ax[1, 0].barh([split_and_concat(city) for city in keys_rev], values_rev)
        ax[1, 0].grid(axis='x')
        ax[1, 0].title.set_text('Уровень зарплат по городам')
        ax[1, 0].tick_params(axis='y', which='major', labelsize=6)
        ax[1, 0].tick_params(axis='x', which='major', labelsize=8)

        # 4 диаграмма
        cities = all_dict[5].keys()
        vac_per_city = all_dict[5].values()
        ax[1, 1].pie(vac_per_city, labels=cities, textprops={'fontsize': 6})
        ax[1, 1].title.set_text('Доля вакансий по городам')
        
        plt.savefig('graph.png')


def clean_string(string):
    string = re.sub(r'<[^>]*>', '', string)
    string = ' '.join(string.split())
    return string


def split_and_concat(s):
    if ' ' not in s and '-' not in s:
        return s
    elif ' ' in s:
        return s.replace(' ', '\n')
    else:
        return s.replace('-', '-\n')


def collect_data(file_name, job_name):
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

    file_csv = csv.reader(open(file_name, encoding='utf_8_sig'))
    list_data = [x for x in file_csv]
    titles = list_data[0]
    values = [x for x in list_data[1:] if x.count('') == 0 and len(x) == len(titles)]
    total_vac_per_year = {}
    salary_per_year = {}
    job_vac_per_year = {}
    job_salary_per_year = {}
    salary_per_city = {}
    vac_per_city = {}
    limit_vac_num = int(len(values) * 0.01)
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
            vac.append(clean_string(raw_vac[j]))
        year = int(vac[published_at_index][0:4])
        salary_rub = (float(vac[salary_from_index]) + float(vac[salary_to_index])) * 0.5 * currency_to_rub[vac[salary_currency_index]]
        if year in total_vac_per_year:
            total_vac_per_year[year] += 1
        else:
            total_vac_per_year[year] = 1
        #job_name
        if job_name in vac[name_index]:
            if year in job_vac_per_year:
                job_vac_per_year[year] += 1
            else:
                job_vac_per_year[year] = 1
            if year in job_salary_per_year:
                x = job_salary_per_year[year]
                x = x[0] + salary_rub, x[1] + 1
                job_salary_per_year[year] = x
            else:
                job_salary_per_year[year] = salary_rub, 1

        if year in salary_per_year:
            x = salary_per_year[year]
            x = x[0] + salary_rub, x[1] + 1
            salary_per_year[year] = x
        else:
            salary_per_year[year] = salary_rub, 1

        #per_city
        if vac[area_name_index] in vac_per_city:
            vac_per_city[vac[area_name_index]] += 1
        else:
            vac_per_city[vac[area_name_index]] = 1

        if vac[area_name_index] in salary_per_city:
            x = salary_per_city[vac[area_name_index]]
            x = x[0] + salary_rub, x[1] + 1
            salary_per_city[vac[area_name_index]] = x
        else:
            salary_per_city[vac[area_name_index]] = salary_rub, 1

    for y in salary_per_year:
        x = salary_per_year[y]
        salary_per_year[y] = int(x[0] / x[1])

    for y in job_salary_per_year:
        x = job_salary_per_year[y]
        job_salary_per_year[y] = int(x[0] / x[1])

    for y in salary_per_city:
        x = salary_per_city[y]
        salary_per_city[y] = int(x[0] / x[1])

    for y in salary_per_year:
        if y not in job_salary_per_year:
            job_salary_per_year[y] = 0

    for y in salary_per_year:
        if y not in job_vac_per_year:
            job_vac_per_year[y] = 0

    filtered_salary_per_city = {}
    for s in salary_per_city:
        if vac_per_city[s] >= limit_vac_num:
            filtered_salary_per_city[s] = salary_per_city[s]


    filtered_vac_per_city = {}
    for s in vac_per_city:
        if vac_per_city[s] >= limit_vac_num:
            filtered_vac_per_city[s] = vac_per_city[s]

    final_salary_per_city = dict(sorted(filtered_salary_per_city.items(), key=lambda x: x[1], reverse=True))
    final_vac_per_city = dict(sorted(filtered_vac_per_city.items(), key=lambda x: x[1], reverse=True))

    for city in final_vac_per_city:
        final_vac_per_city[city] /= len(values)
    vac_per_city_with_others = {}
    if len(final_vac_per_city) > 10:
        vac_per_city_with_others['Другое'] = 0
    k = 0
    for c in final_vac_per_city:
        if k > 10:
            vac_per_city_with_others['Другое'] += final_vac_per_city[c]
        else:
            vac_per_city_with_others[c] = final_vac_per_city[c]
        k += 1

    return [salary_per_year, job_salary_per_year, total_vac_per_year, job_vac_per_year, final_salary_per_city, vac_per_city_with_others]

file_name = input('Введите название файла: ')
job_name = input('Введите название профессии: ')
rep = Report()
all_dict = collect_data(file_name, job_name)
rep.generate_image(job_name, all_dict)
# vacancies_by_year.csv
# Программист