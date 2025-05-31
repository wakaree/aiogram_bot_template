from pydantic import SecretStr

from .base import EnvSettings


class RedisConfig(EnvSettings, env_prefix="REDIS_"):
    host: str
    password: SecretStr
    port: int
    db: int

    def build_url(self) -> str:
        return f"redis://:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"
