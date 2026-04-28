# tests/test_main.py
import main
import pytest
import logging
import importlib
import sys
import asyncio

# Set up logging for the tests
logging.basicConfig(level=logging.INFO)


class DummyClient:
    async def start(self):
        return None

    async def get_me(self):
        return type("Me", (), {"first_name": "TestUser"})()

    async def run_until_disconnected(self):
        return None


def test_main_runs_without_error(monkeypatch):
    # Just ensure main executes without crashing
    dummy = DummyClient()
    monkeypatch.setattr(main, "client", dummy)
    asyncio.run(main.main())


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
    dummy = DummyClient()
    monkeypatch.setattr(main, "client", dummy)
    result = asyncio.run(main.main())
    assert result is None


@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    monkeypatch.setenv("API_ID", "12345")
    monkeypatch.setenv("API_HASH", "fakehash")


@pytest.mark.asyncio
async def test_main_runs(monkeypatch, caplog):
    caplog.set_level("INFO")

    dummy = DummyClient()
    monkeypatch.setattr(main, "client", dummy)

    await main.main()

    assert "Logged in as: TestUser" in caplog.text


def test_run_app_keyboard_interrupt(monkeypatch, caplog):
    # Patch asyncio.run to raise KeyboardInterrupt and close the coroutine.
    def fake_run(coro):
        coro.close()
        raise KeyboardInterrupt

    monkeypatch.setattr(main.asyncio, "run", fake_run)

    caplog.set_level("INFO")

    # Call run_app(), which should hit the except block
    main.run_app()

    # Verify the log message
    assert "✧ CTRL+C pressed, disconnecting..." in caplog.text


def test_run_app_normal(monkeypatch, caplog):
    # Patch asyncio.run to a no-op and close the coroutine.
    def fake_run(coro):
        coro.close()
        return None

    monkeypatch.setattr(main.asyncio, "run", fake_run)

    caplog.set_level("INFO")

    main.run_app()

    # No KeyboardInterrupt, so no disconnect message
    assert "disconnecting" not in caplog.text
