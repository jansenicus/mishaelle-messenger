# banner.py
from rich.console import Console
from rich.text import Text
from datetime import date

console = Console()

def days_until_birthday(month=8, day=29):
    today = date.today()
    this_year = date(today.year, month, day)

    # If birthday already passed this year, calculate for next year
    if today > this_year:
        next_year = date(today.year + 1, month, day)
        delta = next_year - today
    else:
        delta = this_year - today

    return delta.days

def startup_banner():
    today = date.today()
    countdown = days_until_birthday()

    banner = Text()
    banner.append("✧━━━━━━━━━━━━━━━━━━━━━━━✧\n", style="bold magenta")
    banner.append("   Mishaelle Messenger\n", style="bold purple")
    banner.append("   Virgo-born clarity ✧\n", style="bold gold1")

    # Birthday check
    if today.month == 8 and today.day == 29:
        banner.append("   🎂 Happy Birthday Mishaelle ✧\n", style="bold green")
    else:
        banner.append(f"   {countdown} days until Aug 29\n", style="bold cyan")

    banner.append("✧━━━━━━━━━━━━━━━━━━━━━━━✧", style="bold magenta")
    console.print(banner)
