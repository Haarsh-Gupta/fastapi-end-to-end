from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_name: str
    database_password: str
    database_host: str = "localhost"
    database_username: str = "postgres"
    database_port: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 30

    @computed_field
    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.database_username}:"
            f"{self.database_password}@"
            f"{self.database_host}:"
            f"{self.database_port}/"
            f"{self.database_name}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()
