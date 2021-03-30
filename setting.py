# https://xmlriver.com/api/

API_URL = 'http://xmlriver.com/search/xml?user=1660&key=9d9ea875799adf551c8329d0a6dcf50ed168f9b8'
# https://xmlriver.com/apidoc/api-about/
API_PARAMS = {
    'query':'', # текст запроса, если требуется использовать &, вместо него ставить %26
    'groupby':10, # Числовое значение, ТОП позиций для сбора. Возможные значения: 10, 20, 30, 50, 100;
    'loc': 1001493, # Минск, смотреть в файле geo.cvs
    'country': 2643, # Россия, countries.xlsx
    'lr': 'ru', # langs.xlsx
    'domain': 'com', # domains.xlsx
    'device': 'mobile', # device – устройство (desktop, tablet, mobile).
    'ads':0, # 0 - не собирает рекламу, 1 собирает
    'highlights':1 # Подсветка ключевых слов.
}