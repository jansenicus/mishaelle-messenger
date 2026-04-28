# shutdown.py
import asyncio
import signal
import logging

logger = logging.getLogger("mishaelle")

async def shutdown(client, timeout: int = 5):
    """
    Gracefully disconnect the Telethon client with a timeout safeguard.
    """
    logger.info("✧ Graceful shutdown initiated...")
    try:
        if client.is_connected():
            await asyncio.wait_for(client.disconnect(), timeout=timeout)
        logger.info("✧ Session disconnected and saved ✧")
    except asyncio.TimeoutError:
        logger.warning(f"⚠ Disconnect timed out after {timeout}s, forcing exit.")

def register_shutdown_handler(loop, client, timeout: int = 5):
    """
    Register signal handlers for SIGINT and SIGTERM inside the given event loop.
    """
    def handler():
        loop.create_task(shutdown(client, timeout))

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, handler)
        except NotImplementedError:
            signal.signal(sig, lambda s, f: handler())
