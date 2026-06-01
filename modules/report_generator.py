import json
import csv


def save_report(results, output_file, report_format):
    if report_format == "json":
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)

    elif report_format == "csv":
        with open(output_file, "w", encoding="utf-8-sig", newline="") as f:
            fieldnames = ["value", "type", "result", "date"]
            writer = csv.DictWriter(
                f,
                fieldnames=fieldnames,
                delimiter=";"
            )

            writer.writeheader()
            for item in results:
                writer.writerow(item)

    else:
        print("[Ошибка] Неверный формат отчета")