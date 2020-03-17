from types import ModuleType
from typing import Union

from thriftpy2.contrib.aio.protocol import (
    TAsyncProtocolBase,
    TAsyncBinaryProtocolFactory,
)
from thriftpy2.contrib.aio.transport import (
    TAsyncTransportBase,
    TAsyncBufferedTransportFactory,
)
from thriftpy2.contrib.aio.client import TAsyncClient

import httpx

from .transport import TAsyncHTTPXClient

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol


class TProtocolFactory(Protocol):
    def get_protocol(self, trans: TAsyncTransportBase) -> TAsyncProtocolBase:
        ...


class TTransportFactory(Protocol):
    def get_transport(self, trans: TAsyncTransportBase) -> TAsyncTransportBase:
        ...


async def make_client(
    service: ModuleType,
    host: str = 'localhost',
    port: int = 9090,
    url: Union[str, httpx.URL] = None,
    proto_factory: TProtocolFactory = TAsyncBinaryProtocolFactory(),
    trans_factory: TTransportFactory = TAsyncBufferedTransportFactory(),
    **kwargs,
) -> TAsyncClient:
    url = url if url else f'http://{host}:{port}/'
    client = TAsyncHTTPXClient(url, **kwargs)
    transport = trans_factory.get_transport(client)
    protocol = proto_factory.get_protocol(transport)
    await transport.open()
    return TAsyncClient(service, protocol)
