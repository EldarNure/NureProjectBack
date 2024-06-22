from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_NAME: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: str
    DATABASE_USER: str
    DATABASE_URL: str
    SECRET: str
    
    class Config:
        env_file = ".env"


settings = Settings()