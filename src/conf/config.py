from pydantic import BaseModel


class Openai(BaseModel):
    api_key: str
    model: str
    default: bool


class Azure(BaseModel):
    api_version: str
    azure_endpoint: str
    api_key: str
    model: str


class Config(BaseModel):
    openai: Openai
    azure: Azure
