from core.abstracts.providers import LanguageProvider


class AppLanguageProvider(LanguageProvider):
    def get_supported_languages(self) -> list[str]:
        return ["English", "Ukrainian", "Croatian"]
