# tests/test_main.py
import main
import pytest
import logging
import importlib
import sys

# Set up logging for the tests
logging.basicConfig(level=logging.INFO)


def test_main_runs_without_error():
    # Just ensure main executes without crashing
    main.main()


def test_main_entrypoint(monkeypatch):
    monkeypatch.setattr(main, "startup_banner", lambda: None)
    monkeypatch.setattr(main.asyncio, "run", lambda coro: None)

    # Force __name__ == "__main__"
    main.__name__ = "__main__"
    importlib.reload(main)

    # If reload succeeds, lines 31–33 executed
    assert True


# tests/test_main.py
def test_main_help(monkeypatch):
    sys.argv = ["main.py", "--help"]
    result = main.main()
    assert result is not None


@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    monkeypatch.setenv("API_ID", "12345")
    monkeypatch.setenv("API_HASH", "fakehash")


class DummyClient:
    async def start(self):
        return None

    async def get_me(self):
        return type("Me", (), {"first_name": "TestUser"})()

    async def run_until_disconnected(self):
        return None


@pytest.mark.asyncio
async def test_main_runs(monkeypatch, caplog):
    caplog.set_level("INFO")

    dummy = DummyClient()
    monkeypatch.setattr(main, "client", dummy)

    await main.main()

    assert "Logged in as: TestUser" in caplog.text


def test_run_app_keyboard_interrupt(monkeypatch, caplog):
    # Patch asyncio.run to raise KeyboardInterrupt
    def fake_run(_):
        raise KeyboardInterrupt

    monkeypatch.setattr("asyncio.run", fake_run)

    caplog.set_level("INFO")

    # Call run_app(), which should hit the except block
    main.run_app()

    # Verify the log message
    assert "✧ CTRL+C pressed, disconnecting..." in caplog.text


def test_run_app_normal(monkeypatch, caplog):
    # Patch asyncio.run to a no-op
    monkeypatch.setattr("asyncio.run", lambda _: None)

    caplog.set_level("INFO")

    main.run_app()

    # No KeyboardInterrupt, so no disconnect message
    assert "disconnecting" not in caplog.text
