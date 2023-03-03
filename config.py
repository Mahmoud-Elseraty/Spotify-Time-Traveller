from dynaconf import Dynaconf


settings = Dynaconf(
    settings_files=['settings.toml', '.secrets.toml'],
    env_switcher="SPOTIFYAPI_env",
    load_dotenv=False,
)
