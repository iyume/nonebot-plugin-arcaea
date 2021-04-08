from . import _call_api
from ...adapters import estertion
from ... import schema


async def query_recent() -> schema.Recent:
    ...


async def query_b30() -> schema.Best30:
    ...
