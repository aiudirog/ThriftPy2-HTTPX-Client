from types import ModuleType
from typing import Union

from thriftpy2.protocol import TProtocolBase, TBinaryProtocolFactory
from thriftpy2.transport import TTransportBase, TBufferedTransportFactory
from thriftpy2.thrift import TClient

import httpx

from .transport import THTTPXClient

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol


class TProtocolFactory(Protocol):
    def get_protocol(self, trans: TTransportBase) -> TProtocolBase:
        ...


class TTransportFactory(Protocol):
    def get_transport(self, trans: TTransportBase) -> TTransportBase:
        ...


def make_client(
    service: ModuleType,
    host: str = 'localhost',
    port: int = 9090,
    url: Union[str, httpx.URL] = None,
    proto_factory: TProtocolFactory = TBinaryProtocolFactory(),
    trans_factory: TTransportFactory = TBufferedTransportFactory(),
    **kwargs,
) -> TClient:
    url = url if url else f'http://{host}:{port}/'
    client = THTTPXClient(url, **kwargs)
    transport = trans_factory.get_transport(client)
    protocol = proto_factory.get_protocol(transport)
    transport.open()
    return TClient(service, protocol)
