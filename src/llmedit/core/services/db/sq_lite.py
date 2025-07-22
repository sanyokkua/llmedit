import sqlite3
from pathlib import Path

from core.abstracts.providers import DBClientProvider
from core.abstracts.services import DBClient
from core.abstracts.types import AppSettings, AppLLMProviderType, AppTheme


class SQLiteClient(DBClient):
    def __init__(self, db_path: Path):
        """Initialize database connection and create a table if needed"""
        self.db_path = db_path
        self._create_table()

    def _connect(self):
        """Create a database connection with the row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn

    def _create_table(self):
        """Create a settings table if it doesn't exist"""
        with self._connect() as conn:
            conn.execute("""
                         CREATE TABLE IF NOT EXISTS app_settings
                         (
                             id
                             INTEGER
                             PRIMARY
                             KEY
                             DEFAULT
                             1,
                             model_name
                             TEXT
                             NOT
                             NULL,
                             model_temperature
                             REAL
                             NOT
                             NULL
                             DEFAULT
                             0.5,
                             app_llm_provider
                             TEXT
                             NOT
                             NULL
                             DEFAULT
                             'llama-cpp',
                             theme
                             TEXT
                             NOT
                             NULL
                             DEFAULT
                             'dark',
                             CHECK
                         (
                             id =
                             1
                         )
                             )
                         """)
            conn.commit()

    def save_settings(self, settings: AppSettings):
        """Save settings to a database, replacing existing record"""
        with self._connect() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO app_settings
                (id, model_name, model_temperature, app_llm_provider, theme)
                VALUES (?, ?, ?, ?, ?)
            """, (
                1,  # Always use the single settings record
                settings.model_name,
                settings.model_temperature,
                settings.app_llm_provider.value,
                settings.theme.value
            ))
            conn.commit()

    def load_settings(self) -> AppSettings | None:
        """Load settings from a database, using defaults if no record exists"""
        with self._connect() as conn:
            cursor = conn.execute("SELECT * FROM app_settings LIMIT 1")
            row = cursor.fetchone()

            if not row:
                return None

            return AppSettings(
                model_name=row['model_name'],
                model_temperature=row['model_temperature'],
                app_llm_provider=AppLLMProviderType(row['app_llm_provider']),
                theme=AppTheme(row['theme'])
            )


class SQLiteProvider(DBClientProvider):
    def __init__(self, client: DBClient):
        self.client = client

    def get_client(self) -> DBClient:
        return self.client
