# tests/test_banner.py
import banner
from datetime import date


def test_days_until_birthday_future():
    # Pick a date before Aug 29
    date(2026, 4, 28)
    days = banner.days_until_birthday(month=8, day=29)
    assert isinstance(days, int)
    assert days >= 0


def test_days_until_birthday_past():
    # Pick a date after Aug 29
    date(2026, 9, 1)
    days = banner.days_until_birthday(month=8, day=29)
    assert isinstance(days, int)
    assert days > 0


def test_startup_banner_runs_without_error():
    # Just ensure it prints without raising exceptions
    banner.startup_banner()


class FakeDate(date):
    @classmethod
    def today(cls):
        # Return a fixed date
        return cls(2026, 7, 1)


def test_startup_banner_countdown(monkeypatch, capfd):
    # Patch banner.date to our FakeDate
    monkeypatch.setattr(banner, "date", FakeDate)

    banner.startup_banner()
    out, _ = capfd.readouterr()
    assert "days until Aug 29" in out


class BirthdayDate(date):
    @classmethod
    def today(cls):
        return cls(2026, 8, 29)


def test_startup_banner_birthday(monkeypatch, capfd):
    monkeypatch.setattr(banner, "date", BirthdayDate)

    banner.startup_banner()
    out, _ = capfd.readouterr()
    assert "Happy Birthday Mishaelle" in out


class AfterBirthdayDate(date):
    @classmethod
    def today(cls):
        # Pick a date after Aug 29
        return cls(2026, 9, 1)


def test_days_until_birthday_after(monkeypatch):
    # Patch banner.date to our fake class
    monkeypatch.setattr(banner, "date", AfterBirthdayDate)

    days = banner.days_until_birthday()
    # Should be close to ~363 days until next Aug 29
    assert days > 300
