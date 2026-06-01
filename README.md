# logscan
Программа для анализа логфайлов. Утилита ищет в логах IP и SHA-256, выполняет их проверку и сохраняет результат в файл отчета (csv, json).

## Что умеет программа
ищет IP в логфайле,
ищет SHA-256,
выполняет проверку найденных данных,
сохраняет отчет в json,
сохраняет отчет в csv,
записывает процесс в лог-файл.

## Установка
Установить библиотеку:
pip install -r requirements.txt

## Запуск с VirusTotal API
Если указать API-ключ, программа будет выполнять реальную проверку через VirusTotal API.

Пример запуска:
python main.py -log-file logs/sample.log -api-key YOUR_API_KEY -output output/report.json -format json

Если API-ключ не указан, используется mock-режим проверки.

## Запуск программы
1) Создать отчет в json:
python main.py -log-file logs/sample.log -output output/report.json -format json
2) Создать отчет в формате csv:
python main.py -log-file logs/sample.log -output output/report.csv -format csv

## Пример результата
Найдено IP: 3
Найдено SHA-256: 2
Готово. Отчет сохранен: output/report.json

## Структура проекта
logscan/
├── main.py
├── requirements.txt
├── README.md
├── logs/
├── output/
└── modules/

## Используемые библиотеки
argparse, re, json, csv, logging, requests

## Автор
Студент CyberYozh.