import re


def parse_log_file(log_file):
    ip_pat = r"\b(?:\d{1,3}\.){3}\d{1,3}\b" # шаблон ipv4

    sha256_pat = r"\b[a-fA-F0-9]{64}\b" # шаблон sha-256

    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()

    ips = re.findall(ip_pat, content)
    hashes = re.findall(sha256_pat, content)

    # сторно дубликатов ip и hash
    ips = list(set(ips))
    hashes = list(set(hashes))

    return ips, hashes