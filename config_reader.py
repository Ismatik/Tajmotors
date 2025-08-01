from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    #Hide token as SecretStr not Str
    bot_token: SecretStr
    
    #Setting configuration using model_config
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    

# When importing a file, a config object will be immediately created
# and validated,
# which can then be imported from different places
config = Settings()
    