from .base import EnvSettings


class ServerConfig(EnvSettings, env_prefix="SERVER_"):
    port: int
    host: str
    url: str

    def build_url(self, path: str) -> str:
        return f"{self.url}{path}"
