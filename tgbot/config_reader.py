from typing import Any, List, Type, Tuple

from pydantic import SecretStr, PostgresDsn
from pydantic.fields import FieldInfo

from pydantic_settings import (
    BaseSettings,
    DotEnvSettingsSource,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
)


class AdminSource(DotEnvSettingsSource):
    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        if field_name == "admin_list" and value:
            return [int(x) for x in value.split(",")]
        return value


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    bot_token: SecretStr
    admin_list: List[int]
    database_url: PostgresDsn
    use_redis: bool
    redis_prefix: str
    kinopoisk_token: SecretStr
    player_token: SecretStr

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (AdminSource(settings_cls),)


config = Settings()
