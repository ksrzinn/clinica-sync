from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    cnn_client_id: str
    cnn_client_secret: str
    cnn_clinic_token: str
    cnn_base_url: str = "https://api.clinicanasnuvens.com.br"


settings = Settings()
