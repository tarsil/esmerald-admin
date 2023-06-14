import asyncio
from typing import Generator

import pytest


@pytest.fixture(scope="module")
def anyio_backend():
    return ("asyncio", {"debug": True})


@pytest.fixture(scope="module")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().get_event_loop()
    yield loop
    loop.close()
