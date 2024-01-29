from pydantic import BaseModel


class Openai(BaseModel):
    api_key: str
    model: str


class Azure(BaseModel):
    api_version: str
    azure_endpoint: str
    api_key: str
    model: str


class Moonshot(BaseModel):
    base_url: str
    api_key: str
    model: str


class Default(BaseModel):
    llm: str


class Config(BaseModel):
    default: Default
    openai: Openai
    azure: Azure
    moonshot: Moonshot