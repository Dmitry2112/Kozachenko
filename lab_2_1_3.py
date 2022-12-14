import csv
import re
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader
import pdfkit
import os


class Report:
    """
    Класс для формирования отчета с графиками и таблицами

    Attributes:
        all_dict (list): Список словарей со статистикой по вакансиям

    >>> rep = Report()
    >>> rep.collect_data('vacancies_by_year_small.csv', 'Аналитик')
    >>> print(rep.all_dict)
    [{2007: 45027}, {2007: 57500}, {2007: 9}, {2007: 1}, {'Москва': 50041, 'Санкт-Петербург': 48750, 'Саратов': 7500}, {'Москва': 0.6666666666666666, 'Санкт-Петербург': 0.2222222222222222, 'Саратов': 0.1111111111111111}]
    """
    def __init__(self):
        """
        Инициализирует объект Report

        >>> rep = Report()
        >>> len(rep.all_dict)
        0
        """
        self.all_dict = []

    def generate_html(self, job_name):
        """
        Генерирует html страницу с таблицами
        Args:
            job_name (str): Название профессии
        """
        tbl1 = f'<h2>Статистика по годам</h2><table><tr><th>Год</th><th>Средняя зарплата</th><th>Средняя зарплата - {job_name}</th><th>Количество вакансий</th><th>Количество вакансий - {job_name}</th></tr>'
        for y in self.all_dict[0]:
            tbl1 += '<tr>'
            tbl1 += '<td>'
            tbl1 += str(y)
            tbl1 += '</td>'
            tbl1 += '<td>'
            tbl1 += str(self.all_dict[0][y])
            tbl1 += '</td>'
            tbl1 += '<td>'
            tbl1 += str(self.all_dict[1][y])
            tbl1 += '</td>'
            tbl1 += '<td>'
            tbl1 += str(self.all_dict[2][y])
            tbl1 += '</td>'
            tbl1 += '<td>'
            tbl1 += str(self.all_dict[3][y])
            tbl1 += '</td>'
            tbl1 += '</tr>'
        tbl1 += '</table>'

        tbl2 = '<table><tr><th>Город</th><th>Уровень зарплат</th></tr>'
        k = 0
        for city in self.all_dict[4]:
            if k == 10:
                break
            tbl2 += '<tr>'
            tbl2 += '<td>'
            tbl2 += str(city)
            tbl2 += '</td>'
            tbl2 += '<td>'
            tbl2 += str(self.all_dict[4][city])
            tbl2 += '</td>'
            tbl2 += '</tr>'
            k += 1
        tbl2 += '</table>'

        tbl3 = '<table><tr><th>Город</th><th>Доля вакансий</th></tr>'
        k = 0
        other = ''
        for city in self.all_dict[5]:
            if k == 10:
                break
            if k == 0:
                other = f'{self.all_dict[5][city] * 100:.2f}%'
                k += 1
                continue
            tbl3 += '<tr>'
            tbl3 += '<td>'
            tbl3 += str(city)
            tbl3 += '</td>'
            tbl3 += '<td>'
            tbl3 += f'{self.all_dict[5][city] * 100:.2f}%'
            tbl3 += '</td>'
            tbl3 += '</tr>'
            k += 1
        tbl3 += '<tr>'
        tbl3 += '<td>'
        tbl3 += 'Другое'
        tbl3 += '</td>'
        tbl3 += '<td>'
        tbl3 += other
        tbl3 += '</td>'
        tbl3 += '</tr>'
        tbl3 += '</table>'

        data = {'page_title': 'Генерация pdf', 'job': job_name, 'first_table_data': tbl1, 'second_table_data': tbl2,
                'third_table_data': tbl3}
        env = Environment(loader=FileSystemLoader('.'))
        j2_t = env.get_template("templ.html")
        html_content = j2_t.render(data)
        f = open(output_dir + 'hello.html', 'w')
        f.write(html_content)
        f.close()

    def generate_image(self, job_name):
        """
        Генерирует png с графиками со статистикой по вакансиям
        Args:
            job_name (str): Название профессии
        """
        fig, ax = plt.subplots(2, 2)
        # 1 диаграмма
        ax[0, 0].bar([y - 0.2 for y in self.all_dict[0].keys()], self.all_dict[0].values(), width=0.4)
        ax[0, 0].bar([y + 0.2 for y in self.all_dict[1].keys()], self.all_dict[1].values(), width=0.4)
        ax[0, 0].grid(axis='y')
        ax[0, 0].title.set_text('Уровень зарплат по годам')
        ax[0, 0].legend(['средняя з/п', f'з/п {job_name}'], loc='upper left')
        xmarks = range(min(self.all_dict[0].keys()), max(self.all_dict[0].keys()) + 1)
        ax[0, 0].set_xticks(xmarks)
        ax[0, 0].set_xticklabels(xmarks, rotation=90)
        ax[0, 0].tick_params(axis='both', which='major', labelsize=8)
        plt.subplots_adjust(hspace=0.5)

        # 2 диаграмма
        ax[0, 1].bar([y - 0.2 for y in self.all_dict[2].keys()], self.all_dict[2].values(), width=0.4)
        ax[0, 1].bar([y + 0.2 for y in self.all_dict[3].keys()], self.all_dict[3].values(), width=0.4)
        ax[0, 1].grid(axis='y')
        ax[0, 1].title.set_text('Количество вакансий по годам')
        ax[0, 1].legend(['Количество вакансий', f'Количество вакансий\n{job_name}'], loc='upper left')
        xmarks = range(min(self.all_dict[2].keys()), max(self.all_dict[2].keys()) + 1)
        ax[0, 1].set_xticks(xmarks)
        ax[0, 1].set_xticklabels(xmarks, rotation=90)
        ax[0, 1].tick_params(axis='both', which='major', labelsize=8)

        # 3 диаграмма
        keys_rev = list(self.all_dict[4].keys()).copy()
        values_rev = list(self.all_dict[4].values()).copy()
        keys_rev.reverse()
        values_rev.reverse()
        range_lim = 10 if len(self.all_dict[4]) >= 10 else len(self.all_dict[4])
        ax[1, 0].barh([Report.split_and_concat(keys_rev[city]) for city in range(0, range_lim)],
                      [values_rev[city] for city in range(0, range_lim)])
        ax[1, 0].grid(axis='x')
        ax[1, 0].title.set_text('Уровень зарплат по городам')
        ax[1, 0].tick_params(axis='y', which='major', labelsize=6)
        ax[1, 0].tick_params(axis='x', which='major', labelsize=8)

        # 4 диаграмма
        cities = list(self.all_dict[5].keys()).copy()
        vac_per_city = list(self.all_dict[5].values()).copy()

        ax[1, 1].pie(vac_per_city[:10], labels=cities[:10], textprops={'fontsize': 6})
        ax[1, 1].title.set_text('Доля вакансий по городам')

        cur_dir = os.getcwd()
        out_dir = os.path.join(cur_dir, output_dir)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        plt.savefig(output_dir + 'graph.png')

    @staticmethod
    def clean_string(string):
        """
        Очищает строку с информацией о вакансии от лишних пробелов и html тегов
        Args:
            string (str): Строка с информацией о вакансии (содержащая лишние символы)

        Returns:
            str: "чистая" строка

        >>> Report.clean_string('<p><strong>Обязанности</strong>')
        'Обязанности'
        >>> Report.clean_string('<p><strong>О нас:</strong></p>')
        'О нас:'
        >>> Report.clean_string('<li>Участвовать в приемке в эксплуатацию нового, модернизированного оборудования;</li>')
        'Участвовать в приемке в эксплуатацию нового, модернизированного оборудования;'
        """
        string = re.sub(r'<[^>]*>', '', string)
        string = ' '.join(string.split())
        return string

    @staticmethod
    def split_and_concat(city):
        """
        Если название города состоит из нескольких слов или содержит '-' делает перенос слов на новую строку
        Args:
            city (str): Название города

        Returns:
            str: Название города с переносами строк (если они были сделаны) или исходную строку

        >>> Report.split_and_concat('Москва')
        'Москва'
        """
        if ' ' not in city and '-' not in city:
            return city
        elif ' ' in city:
            return city.replace(' ', '\n')
        else:
            return city.replace('-', '-\n')


    def collect_data(self, file_name, job_name):
        """
        Формирует данные для дальнейшего использования в составлении отчета
        Args:
            file_name (str): Название csv файла с котрого считываются исходные данные
            job_name (str): Название вакансии

        Returns:
            list: Список словарей со статистикой по вакансиям
        """
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

        file_csv = csv.reader(open(work_dir + file_name, encoding='utf_8_sig'))
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
                vac.append(Report.clean_string(raw_vac[j]))
            year = int(vac[published_at_index][0:4])
            salary_rub = (float(vac[salary_from_index]) + float(vac[salary_to_index])) * 0.5 * currency_to_rub[
                vac[salary_currency_index]]
            if year in total_vac_per_year:
                total_vac_per_year[year] += 1
            else:
                total_vac_per_year[year] = 1
            # job_name
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

            # per_city
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


        self.all_dict = [salary_per_year, job_salary_per_year, total_vac_per_year, job_vac_per_year, final_salary_per_city,
                        vac_per_city_with_others]
        # return [salary_per_year, job_salary_per_year, total_vac_per_year, job_vac_per_year, final_salary_per_city,
        #         vac_per_city_with_others]


output_dir = 'output/'
work_dir = 'work_files/'


def main_2_1_3():
    """
    Осуществляет работу взаимодействия с пользователем (ввод данных)
    """
    file_name = input('Введите название файла: ')
    job_name = input('Введите название профессии: ')
    rep = Report()
    rep.collect_data(file_name, job_name)
    print(rep.all_dict)
    rep.generate_image(job_name)
    rep.generate_html(job_name)

    config = pdfkit.configuration(wkhtmltopdf=r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    opt = {'enable-local-file-access': None, 'encoding': 'windows-1251'}
    pdfkit.from_file(output_dir + 'hello.html', output_dir + 'report.pdf', configuration=config, options=opt)


if __name__ == '__main__':
    main_2_1_3()

# vacancies_by_year_small.csv
# Аналитик