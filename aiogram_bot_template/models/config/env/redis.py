from .base import EnvSettings


class RedisConfig(EnvSettings, env_prefix="REDIS_"):
    host: str
    port: int
    db: int
    data: str

    def build_url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"
