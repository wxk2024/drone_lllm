import os
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)

from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langgraph.graph.message import add_messages
from typing import Optional,Dict,Any,List
from pydantic import BaseModel, Field
from typing_extensions import Annotated, TypedDict
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph,END
from output_format import FlyTask
from log import logger
from init_config import Settings
import json
from typing import (
    Dict,
    Optional,
    Type,
    TypedDict,
    TypeVar,
    Union,
    Any,
)

#----------------------------- graph -----------------------------
# 创建自己的状态
class State(TypedDict):
    messages: Annotated[list, add_messages]
    task: FlyTask


class GraphBuilder():
    _BM = TypeVar("_BM", bound=BaseModel)
    _DictOrPydanticClass = Union[Dict[str, Any], Type[_BM], Type]
    def __init__(self):
        self.llm = None
        self.local_llm = None
        self.prompt = None
        self.graph = None
        self.settings:Settings = None

    def build(self):
        if self.llm is None or self.settings is None:
            raise

        # 加载 smith
        # 加载 output_structure
        self._load_smith()
        self._set_structed_output()
        logger.info("开始创建 langgraph")

        builder = StateGraph(state_schema=State)
        # Define the function that calls the model
        def call_model(state: State):
            response = self.llm.invoke(state["messages"])
            return {"messages": [AIMessage(content=response.model_dump_json())],"task":response}
        
        # Define the (single) node in the graph
        builder.add_node("model", call_model)
        builder.add_edge(START, "model")
        builder.add_edge("model",END)

        # Add memory
        memory = MemorySaver()
        self.graph = builder.compile(checkpointer=memory)
        logger.info("构建langgraph成功")
        return self.graph

    def _load_smith(self):
        os.environ['LANGCHAIN_TRACING_V2'] = self.settings.langchain_tracing_v2
        os.environ['LANGCHAIN_ENDPOINT'] = self.settings.langchain_endpoint
        os.environ['LANGCHAIN_API_KEY'] = self.settings.langchain_api_key
        os.environ['LANGCHAIN_PROJECT'] = self.settings.langchain_project
        logger.info("langchain smith 监控设置完毕")

    def _set_structed_output(self,schema: Optional[_DictOrPydanticClass] = None):
        self.llm = self.llm.with_structured_output(FlyTask)
        logger.info("设置输出格式成功")

    def set_llm(self,llm):
        self.llm = llm
    def set_settings(self,settings:Settings):
        self.settings = settings
    def set_local_llm(self,local_llm):
        self.local_llm = local_llm


# ---

# response = llm.invoke({"text":"给我测量北京邮电大学的温度"})
# print(response)

# response = llm.invoke({"text":"给我找一下我家的黄毛狗，它40厘米高呢。"})
# print(response)

# response = llm.invoke({"text":"给我跟踪一下这辆黄色的车，它的车牌号是京A23456,是一辆白色面包车，核载10人"})
# print(response)

'''
            返回格式为json格式 \
            比如: {  \
                task_type: '追踪任务',\
                task_object: '车',\
                features: [\
                    {\
                        name: '车牌',\
                        value: '京A234446'\
                    },\
                    {\
                        name: '颜色',\
                        value: '黄色'\
                    }\
                ]\
            }\
'''