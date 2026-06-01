import requests
import logging
from datetime import datetime


def mock_check(value, artifact_type):
    if artifact_type == "IP":
        if value.startswith("192.168") or value.startswith("10."):
            result = "internal"
        else:
            result = "clean"

    elif artifact_type == "HASH":
        if value.startswith("275a"):
            result = "malicious"
        else:
            result = "clean"

    else:
        result = "unknown"

    return result


def get_result_from_stats(stats):
    malicious = stats.get("malicious", 0)
    suspicious = stats.get("suspicious", 0)

    if malicious > 0:
        return "malicious"
    elif suspicious > 0:
        return "suspicious"
    else:
        return "clean"


def ch_artif(value, artifact_type, api_key=None):
    if api_key is None:
        result = mock_check(value, artifact_type)

        return {
            "value": value,
            "type": artifact_type,
            "result": result,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    headers = {
        "x-apikey": api_key
    }

    if artifact_type == "IP":
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{value}"
    elif artifact_type == "HASH":
        url = f"https://www.virustotal.com/api/v3/files/{value}"
    else:
        url = None

    if url is None:
        result = "unknown"
    else:
        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 401:
                result = "api_error_unauthorized"
                logging.error("Ошибка api VirusTotal: неверный api-ключ")

            elif response.status_code == 403:
                result = "api_error_forbidden"
                logging.error("Ошибка api VirusTotal: доступ запрещен")

            elif response.status_code == 404:
                result = "not_found"
                logging.error(f"Объект не найден в VirusTotal: {value}")

            elif response.status_code == 429:
                result = "api_error_rate_limit"
                logging.error("Ошибка api VirusTotal: превышен лимит запросов")

            else:
                response.raise_for_status()
                data = response.json()

                stats = data["data"]["attributes"]["last_analysis_stats"]
                result = get_result_from_stats(stats)

        except requests.exceptions.Timeout:
            result = "api_error_timeout"
            logging.error(f"Таймаут при запросе к VirusTotal: {value}")

        except requests.exceptions.RequestException as e:
            result = "api_error"
            logging.error(f"Ошибка запроса к VirusTotal: {e}")

        except Exception as e:
            result = "api_error"
            logging.error(f"Ошибка обработки ответа VirusTotal: {e}")

    return {
        "value": value,
        "type": artifact_type,
        "result": result,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }