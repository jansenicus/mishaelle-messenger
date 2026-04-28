import re


def parse_pandai(message: str) -> dict:
    result = {}
    m = re.search(r"-\s*(\w+)\s*(Buy|Sell)", message, re.IGNORECASE)
    if m:
        result["symbol"] = m.group(1)
        result["direction"] = m.group(2).capitalize()

    m = re.search(r"Entry\s+\w+:\s*([\d.]+)", message)
    if m:
        result["entry"] = float(m.group(1))

    m = re.search(r"Leverage:\s*([\dx]+)", message)
    if m:
        result["leverage"] = m.group(1)

    m = re.search(r"Lot Size:\s*([\d.]+)", message)
    if m:
        result["lot_size"] = float(m.group(1))

    return result
