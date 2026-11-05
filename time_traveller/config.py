from pathlib import Path

from dynaconf import Dynaconf

ROOT = Path(__file__).resolve().parent.parent

settings = Dynaconf(
    root_path=str(ROOT),
    settings_files=["settings.toml", ".secrets.toml"],
    load_dotenv=False,
)

