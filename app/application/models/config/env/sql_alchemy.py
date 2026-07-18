from .base import EnvSettings


class SQLAlchemyConfig(EnvSettings, env_prefix="ALCHEMY_"):
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 25
    max_overflow: int = 25
    pool_timeout: int = 10
    pool_recycle: int = 3600
