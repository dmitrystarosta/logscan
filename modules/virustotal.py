from datetime import datetime


def ch_artif(value, artifact_type, api_key=None):
    """
    Проверка артефакта.
    Пока используется mock-режим.
    """

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

    return {
        "value": value,
        "type": artifact_type,
        "result": result,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }