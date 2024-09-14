from functools import lru_cache
from punq import Container, Scope

from co




@lru_cache(1)
def _init_container():
    return _init_container()


@lru_cache(None)
def init_container():
    container = Container()

    container.register()

    return container
