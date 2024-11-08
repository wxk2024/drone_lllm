from pydantic_settings import BaseSettings, SettingsConfigDict
from utils import Singleton
from langchain.prompts import (
    ChatPromptTemplate,
)
from pydantic import (
    AliasChoices,
    AmqpDsn,
    BaseModel,
    Field,
    ImportString,
    PostgresDsn,
    RedisDsn,
    HttpUrl,
)
from pydantic import ValidationError,model_validator
from log import logger
import json,os


def _load_prompt(version: str)->ChatPromptTemplate:
    with open("prompt.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for entry in data:
            if entry["version"] != version:
                continue
            if entry["file"] == True:
                system_str = open(os.path.join("../prompt",entry["version"]+'.txt'),encoding="utf-8").read()
                messages = [
                    ("system",system_str),
                ]
            else:
                # TODO: 用的旧代码
                messages = [
                    (msg["type"], msg["content"])
                    for entry in data
                    if entry["version"] == version
                    for msg in entry["template"]
                ]
    pro = ChatPromptTemplate.from_messages(messages)
    logger.info("提示词加载完毕")
    print("提示词加载完毕")
    logger.info(pro.model_dump_json())
    # print(pro)
    return pro



class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    langchain_tracing_v2:str=Field(validation_alias='LANGCHAIN_TRACING_V2')
    langchain_endpoint:str=Field(validation_alias='LANGCHAIN_ENDPOINT')
    langchain_api_key:str=Field(validation_alias='LANGCHAIN_API_KEY')
    langchain_project:str=Field(validation_alias='LANGCHAIN_PROJECT')
    prompt_version:str=Field(validation_alias='PROMPT_VERSION') 
    openai_model:str=Field(validation_alias="OPENAI_MODEL")
    openai_api_key:str=Field(validation_alias="OPENAI_API_KEY")
    openai_api_base:str=Field(validation_alias="OPENAI_API_BASE")
    huggingfacehub_api_token:str=Field(validation_alias="HUGGINGFACEHUB_API_TOKEN")
    ollama_model:str=Field(validation_alias="OLLAMA_MODEL")
    ollama_multimodal:str=Field(validation_alias="OLLAMA_MULTIMODAL")

    # 必须要隐藏起来，否则的话 init 函数通过不了
    _prompt:ChatPromptTemplate = None

     # 在进入模型处理之后运行，只在模型成功验证后处理。
    @model_validator(mode='after')
    def check_passwords_match(self) -> 'Settings':
        self._prompt = _load_prompt(self.prompt_version)
        return self

def load_settings() -> Settings:
    return Settings()

# print(load_settings())
# print(_load_prompt("v1"))
