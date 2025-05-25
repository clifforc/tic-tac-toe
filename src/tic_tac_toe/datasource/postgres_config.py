from dotenv import load_dotenv
from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class PostgresConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PG_",
        env_file_encoding="utf-8"
    )

    dialect: str = "postgresql"
    driver: str = "asyncpg"
    user: str
    password: str
    host: str = "localhost"
    port: int = 5432
    dbname: str = "postgres"

    max_retries: int = 5,
    delay: float = 2.0,
    backoff: float = 2.0

    @computed_field
    @property
    def pg_dsn(self) -> PostgresDsn:
        return PostgresDsn(
            f"{self.dialect}+{self.driver}://"
            f"{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.dbname}"
        )
