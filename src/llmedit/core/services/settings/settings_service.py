from core.abstracts.providers import DBClientProvider
from core.abstracts.services import SettingsService
from core.abstracts.types import AppSettings, AppLLMProviderType, AppTheme


class AppSettingsService(SettingsService):
    def __init__(self, db_client_provider: DBClientProvider):
        self.db_client_provider = db_client_provider

    def get_settings(self) -> AppSettings:
        client = self.db_client_provider.get_client()

        settings = client.load_settings()
        if settings is not None:
            return settings

        return AppSettings(
            model_name="gemma-3n-E4B-it-Q4_K_M",
            model_temperature=0.5,
            app_llm_provider=AppLLMProviderType.LLAMA_CPP,
            theme=AppTheme.LIGHT
        )

    def save_settings(self, settings: AppSettings) -> None:
        client = self.db_client_provider.get_client()
        client.save_settings(settings)
