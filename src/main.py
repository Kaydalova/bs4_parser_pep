import logging
import re
from exceptions import ParserFindTextException
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup, NavigableString, Tag
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, EXPECTED_STATUS, MAIN_DOC_URL, PEP_DOCS_URL,
                       STATUS_COUNT_DICT)
from outputs import control_output
from utils import cook_soup, find_tag, get_response


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = cook_soup(session, whats_new_url)
    sections_by_python = find_tag(
        find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'}),
        'div', attrs={'class': 'toctree-wrapper'}).find_all(
            'li', attrs={'class': 'toctree-l1'})

    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]

    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        soup = cook_soup(session, version_link)
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append((version_link, h1.text, dl_text))
    return results


def latest_versions(session):
    soup = cook_soup(session, MAIN_DOC_URL)
    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')

    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
        else:
            raise ParserFindTextException(
                f'В тексте тега {ul} нет All versions')

    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'

    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((link, version, status))

    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = cook_soup(session, downloads_url)
    table_tag = find_tag(soup, 'table', attrs={'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)

    with open(archive_path, 'wb') as file:
        file.write(response.content)

    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    status_list = list(set([
        status for st_set in EXPECTED_STATUS.values() for status in st_set]))
    response = get_response(session, PEP_DOCS_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    # нужны только из таблицы Numerical index
    numerical_index_table = find_tag(
        soup, 'section', attrs={'id': 'numerical-index'})
    tbody = find_tag(numerical_index_table, 'tbody')
    tr_tags = tbody.find_all(
        'tr', attrs={'class': ['row-even', 'row-odd']})

    for tr in tqdm(tr_tags):
        status_in_table = find_tag(tr, 'abbr')
        relative_link = find_tag(
            tr, 'a', attrs={'class': 'pep reference internal'})
        link = urljoin(PEP_DOCS_URL, relative_link['href'])
        soup = cook_soup(session, link)
        article = find_tag(soup, 'article')
        dl = find_tag(article, 'dl')
        status_on_page = dl.find(string=status_list)

        if status_on_page is None:
            for tag in dl:
                if isinstance(tag, NavigableString):
                    continue
                if isinstance(tag, Tag) and tag.text == 'Status:':
                    status_on_page = tag.nextSibling.nextSibling.text

        if status_on_page not in EXPECTED_STATUS[status_in_table.text[1:]]:
            logging.info(
                f'''Несовпадающие статусы:
                {link}
                Статус в карточке: {status_on_page}
                Ожидаемые статусы: {EXPECTED_STATUS[status_in_table.text[1:]]}
                ''')
        elif status_on_page == 'Draft':
            STATUS_COUNT_DICT[''] += 1
        else:
            STATUS_COUNT_DICT[status_on_page[:1]] += 1

    total = sum(STATUS_COUNT_DICT.values())
    STATUS_COUNT_DICT['Total'] = total
    results = list(STATUS_COUNT_DICT.items())

    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    # Запускаем функцию с конфигурацией логов.
    configure_logging()
    # Отмечаем в логах момент запуска программы.
    logging.info('Парсер запущен!')

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        control_output(results, args)
    # Логируем завершение работы парсера.
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
