from pydantic import SecretStr

from .base import EnvSettings


class RedisConfig(EnvSettings, env_prefix="REDIS_"):
    host: str
    password: SecretStr | None
    port: int
    db: int
    data: str

    def build_url(self) -> str:
        if self.password and self.password.get_secret_value() != 'None':
            return (f"redis://:{self.password.get_secret_value()}@{self.host}:"
                    f"{self.port}/{self.db}")
        else:
            return f"redis://{self.host}:{self.port}/{self.db}"
