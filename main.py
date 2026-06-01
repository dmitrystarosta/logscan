import argparse
import logging
import os

from modules.log_parser import parse_log_file
from modules.virustotal import ch_artif
from modules.report_generator import save_report

logging.basicConfig(
    filename="logscan.log",
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

def main():
    parser = argparse.ArgumentParser(
        description="logscan — анализ логов и проверка артефактов"
    )

    parser.add_argument("-log-file", required=True, help="путь к логфайлу")
    parser.add_argument("-api-key", required=False, help="api virustotal")
    parser.add_argument("-output", required=True, help="путь к отчету")
    parser.add_argument("-format", required=True, choices=["json", "csv"], help="формат отчета")

    args = parser.parse_args()

    logging.info("Запуск logscan")

    if not os.path.exists(args.log_file):
        message = f"Логфайл не найден: {args.log_file}"
        print("[Ошибка]", message)
        logging.error(message)
        return

    try:
        ips, hashes = parse_log_file(args.log_file)
    except Exception as e:
        print("[Ошибка] Не удалось прочитать логфайл:", e)
        logging.error(f"Ошибка чтения логфайла: {e}")
        return

    print(f"Найдено IP: {len(ips)}")
    print(f"Найдено SHA-256: {len(hashes)}")

    logging.info(f"Найдено IP: {len(ips)}")
    logging.info(f"Найдено SHA-256: {len(hashes)}")

    results = []

    try:
        for ip in ips:
            result = ch_artif(ip, "IP", args.api_key)
            results.append(result)

        for file_hash in hashes:
            result = ch_artif(file_hash, "HASH", args.api_key)
            results.append(result)

    except Exception as e:
        print("[Ошибка] Не удалось проверить артефакты:", e)
        logging.error(f"Ошибка проверки артефактов: {e}")
        return

    try:
        save_report(results, args.output, args.format)
    except PermissionError:
        print("[Ошибка] Закройте файл отчета, если он открыт в Excel.")
        logging.error(f"Нет доступа к файлу отчета: {args.output}")
        return
    except Exception as e:
        print("[Ошибка] Не удалось сохранить отчет:", e)
        logging.error(f"Ошибка сохранения отчета: {e}")
        return

    logging.info(f"Отчет сохранен: {args.output}")
    print("Готово. Отчет сохранен:", args.output)


if __name__ == "__main__":
    main()