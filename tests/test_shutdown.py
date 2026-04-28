import asyncio
import pytest
import logging
import signal
from shutdown import shutdown
from shutdown import register_shutdown_handler


class DummyClient:
    def __init__(self, hang=False):
        self._connected = True
        self._hang = hang

    def is_connected(self):
        return self._connected

    async def disconnect(self):
        if self._hang:
            await asyncio.sleep(10)  # simulate hang
        else:
            await asyncio.sleep(0.1)  # quick disconnect
        self._connected = False


@pytest.mark.asyncio
async def test_shutdown_completes_quickly(caplog):
    caplog.set_level(logging.INFO)
    client = DummyClient(hang=False)

    await shutdown(client, timeout=2)

    assert not client.is_connected()
    assert "Session disconnected and saved" in caplog.text


@pytest.mark.asyncio
async def test_shutdown_times_out(caplog):
    caplog.set_level(logging.INFO)
    client = DummyClient(hang=True)

    await shutdown(client, timeout=1)

    assert "Disconnect timed out" in caplog.text


@pytest.mark.asyncio
async def test_shutdown_saves_disconnect(caplog):
    caplog.set_level(logging.INFO)
    client = DummyClient(hang=False)

    await shutdown(client, timeout=2)

    assert "Session disconnected and saved" in caplog.text


@pytest.mark.asyncio
async def test_shutdown_forced_timeout(caplog):
    caplog.set_level(logging.INFO)
    client = DummyClient(hang=True)

    await shutdown(client, timeout=1)

    assert "Disconnect timed out" in caplog.text


class DummyLoop:
    def __init__(self, fail=False):
        self.fail = fail
        self.handlers = {}

    def add_signal_handler(self, sig, handler):
        if self.fail:
            raise NotImplementedError
        self.handlers[sig] = handler


@pytest.mark.asyncio
async def test_register_shutdown_handler_success():
    loop = DummyLoop(fail=False)
    client = type("C", (), {"is_connected": lambda self: False})()
    register_shutdown_handler(loop, client, timeout=1)
    # Verify handlers were registered
    assert signal.SIGINT in loop.handlers
    assert signal.SIGTERM in loop.handlers


@pytest.mark.asyncio
async def test_register_shutdown_handler_fallback(monkeypatch):
    loop = DummyLoop(fail=True)
    client = type("C", (), {"is_connected": lambda self: False})()
    register_shutdown_handler(loop, client, timeout=1)
    # Verify fallback installed via signal.signal
    assert callable(signal.getsignal(signal.SIGINT))
    assert callable(signal.getsignal(signal.SIGTERM))


@pytest.mark.asyncio
async def test_register_shutdown_handler_invokes_handler():
    class DummyLoop:
        def __init__(self):
            self.tasks = []

        def add_signal_handler(self, sig, handler):
            self.handler = handler

        def create_task(self, coro):
            self.tasks.append(coro)
            return coro

    loop = DummyLoop()
    client = type("C", (), {"is_connected": lambda self: False})()

    # Register handler
    register_shutdown_handler(loop, client, timeout=1)

    # Manually invoke the stored handler
    loop.handler()

    # Verify that create_task was called
    assert loop.tasks, "Handler should schedule shutdown coroutine"

    # Optionally, run the scheduled coroutine to completion
    await loop.tasks[0]
