import re


def parse_callisto(message: str) -> dict:
    result = {}
    if "SELL" in message.upper():
        result["direction"] = "Sell"
    elif "BUY" in message.upper():
        result["direction"] = "Buy"

    m = re.search(r"SELL RANGE:\s*([\d.-]+)", message)
    if m:
        result["entry_range"] = m.group(1)

    m = re.search(r"SL\s+([\d.]+)", message)
    if m:
        result["stop_loss"] = float(m.group(1))

    m = re.search(r"TP\s*:\s*([\d/ ]+)", message)
    if m:
        result["take_profit"] = [
            float(x) for x in m.group(1).replace(" ", "").split("/")
        ]

    return result
