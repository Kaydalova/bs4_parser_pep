import csv
import datetime as dt
import logging

from constants import (BASE_DIR, DATETIME_FORMAT, FILE_SAVING_FOLDER,
                       OUTPUT_FILE, OUTPUT_TABLE)
from prettytable import PrettyTable


def control_output(results, cli_args):
    output = cli_args.output
    if output == OUTPUT_TABLE:
        pretty_output(results)
    elif output == OUTPUT_FILE:
        file_output(results, cli_args)
    else:
        default_output(results)


def pretty_output(results):
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def default_output(results):
    for row in results:
        print(*row)


def file_output(results, cli_args):
    results_dir = BASE_DIR/FILE_SAVING_FOLDER
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formated = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formated}.csv'
    file_path = results_dir/file_name

    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='excel')
        writer.writerows(results)

    logging.info(f'Файл с результатами был сохранён: {file_path}')
