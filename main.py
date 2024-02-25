import csv
import re
from pprint import pprint


def read_file_csv():
    with open('phonebook_raw.csv', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=',')
        contacts_list = list(rows)
    return contacts_list


def change_raw_list(list_cont):
    phone_pattern = re.compile(r'(\+7|8)\s*\(*(\d{3})\)*\s*\-*(\d{3})\s*\-*(\d{2})\s*\-*(\d{2})')
    phone_pattern1 = re.compile(r'\s*\(*(доб.)\s*(\d+)\)*\s*')
    text_pattern = re.compile(r'(\w+[А-яЁё])\s*\,*(\w+[А-яЁё])\s*\,*(\w+[А-яЁё])*\,*(\w+[А-яЁё])*\,*(\w+[А-яЁё]'
                              r'\w+[А-яЁё –]*\–*\s*)*\,*(\+*\d\s*\(*\d+\)*\-*\s*\d+\-*\d+\-*\d+\s*\(*\w*\.*\s*\d*\)*)'
                              r'*\,*([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)*')

    raw_list = []
    for c in range(len(list_cont)):
        if c == 0:
            raw_list.append(list_cont[c])
        else:
            line = ','.join(list_cont[c])
            result = re.search(text_pattern, line)
            raw_list.append(list(result.groups()))
            if raw_list[c][5] is not None:
                raw_list[c][5] = phone_pattern.sub(r'+7(\2)\3-\4-\5', raw_list[c][5])
                raw_list[c][5] = phone_pattern1.sub(r' \1\2', raw_list[c][5])
    return raw_list


def change_final_list(list_cont):
    final_list = []
    for i in range(len(list_cont)):
        for j in range(len(list_cont)):
            if list_cont[i][0] == list_cont[j][0]:
                list_cont[i] = [x or y for x, y in zip(list_cont[i], list_cont[j])]
        if list_cont[i] not in final_list:
            final_list.append(list_cont[i])
    return final_list


def write_file_csv(list_write, name):
    with open(name + '.csv', 'w', encoding='utf-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(list_write)


if __name__ == '__main__':
    phone_list = change_raw_list(read_file_csv())
    # pprint(phone_list)
    new_phone_list = change_final_list(phone_list)
    # pprint(new_phone_list)
    write_file_csv(new_phone_list, 'phonebook')