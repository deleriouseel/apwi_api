from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    # Comma-separated list of origins allowed to send credentialed requests.
    # Reads are public, so the default stays permissive for plain GETs.
    cors_allow_origins: str = "*"

    @property
    def cors_origin_list(self) -> List[str]:
        return [o.strip() for o in self.cors_allow_origins.split(",") if o.strip()]

    class Config:
        env_file = ".env"


settings = Settings()
