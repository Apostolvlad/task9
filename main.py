import service_table
import api_xmlriver
import time
import os

TABLE_ID = '1hkn1c0Y6IMkUg2m7orn0DTG-OojNnn9Najyki1RdY-s'

table_data = list() 
table_i_start = 1

table_row_count_update = 100 # раз в сколько строк нужно обновлять таблицу

def update_table():
    global table_data, table_i_start
    table.update_values(table_data, list_range = f'A{table_i_start}:J{table_i_start + len(table_data)}')
    table_i_start += len(table_data)
    table_data = list()

def get_data():
    with open('query.txt', encoding='UTF-8') as f: base_query = set(f.read().split('\n'))
    base_query.remove('')
    base_files = set(map(lambda name:name.replace("'", '"'), os.listdir('data')))
    base_query = base_query.difference(base_files)
    for query in list(base_query)[:10]:
        api_xmlriver.generation('data', f'{query} Минск', filename = query.replace('"', "'"))
        time.sleep(1)

def process_table():
    global table_data
    if table_i_start == 1: table_data.append(('url', 'query', 'zero', 'oneline_sitelinks', 'oneline_sitelinks', 'oneline_sitelinks', 'oneline_sitelinks', 'oneline_sitelinks', 'oneline_sitelinks', 'oneline_sitelinks'))
    i_row = 0
    for filename in os.listdir('data'):
        if table_row_count_update > i_row:
            result, url = api_xmlriver.process2(f'data\\{filename}')
            for item in result['items']:
                if item['url'].find('redsale.by') == -1: continue
                table_row = [item['url'], filename.replace('.xml', '').replace("'", '"')]
                i_row += 1
                table_row.append(url)  
                table_row.extend(item.get('oneline_sitelinks', ()))
                table_data.append(table_row)  
        else:
            i_row = 0
            update_table()
    if len(table_data):update_table()

def main():
    global table
    table = service_table.Table(TABLE_ID, table_title='result')
    #get_data() # парсинг данных в DATA
    process_table() # обработка данных из DATA и загрузка в таблицу
    
    


if __name__ == '__main__':
    main()
    