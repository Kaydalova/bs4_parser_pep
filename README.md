# Парсер для быстрого получения документации по Python
Парсер документации python c https://docs.python.org/3/ и https://peps.python.org/

Доступно 4 режима парсинга:
- **whats-new** (получение списка ссылок на перечень изменений в версиях Python)
- **latest-versions** (получение списка ссылок на документацию для всех версий Python)
- **download** (скачивание архива с документацией для последней версии Python)
- **pep** (получение данных о статусах всех PEP и вывод информации о несоответствиях статусов в общем списке и в карточках отдельных PEP)

Можно выбрать удобный формат вывода информации:
- стандартный вывод в терминал;
- вывод в терминал в табличной форме (prettytable);
- запись результатов работы в файл .csv.

Настроено логирование - логи выводятся в терминал и сохраняются в отдельной директории с ротацией.

## Ключевые технологии и библиотеки:
- [Python](https://www.python.org/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [requests_cache](https://pypi.org/project/requests-cache/)
- [argparse](https://docs.python.org/3/library/argparse.html)
- [prettytable](https://pypi.org/project/prettytable/)
- [tqdm](https://pypi.org/project/tqdm/)
## Установка проекта локально
1. Склонировать репозиторий на локальную машину:
```bash
git clone git@github.com:Kaydalova/bs4_parser_pep.git
cd bs4_parser_pep
```
2. Создать, активировать виртуальное окружение и установите зависимости:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Перейти в директорию src:
```
cd src
```

## Использование парсера:

Вызов справки по доступным аргументам:
```
usage: main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}

Парсер документации Python

positional arguments:
  {whats-new,latest-versions,download,pep}
                        Режимы работы парсера

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```

Выбор режима работы:
```
python main.py whats-new
```
```
python main.py latest-versions
```
```
python main.py download
```
```
python main.py pep
```

### Автор
[Александра Кайдалова](https://t.me/kaydalova)





