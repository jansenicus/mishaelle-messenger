import asyncio
import pytest
import logging
from shutdown import shutdown

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
