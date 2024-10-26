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
from langgraph.prebuilt import ToolNode, tools_condition
from tools import BaiduDitu
from output_format import FlyTask,OnePlace
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

# 由于当前任务字段迟迟确定不了，只好用这个了！
class State_New(TypedDict):
    messages: Annotated[list, add_messages]

class GraphBuilder():
    _BM = TypeVar("_BM", bound=BaseModel)
    _DictOrPydanticClass = Union[Dict[str, Any], Type[_BM], Type]
    def __init__(self):
        self.llm = None                 # online 大模型用来文本对话
        self.local_llm = None           # local  大模型用来图片转文字
        self.prompt = None              # 提示词：通过prompt.json
        self.graph = None               # langgraph 框架最主要的作用
        self.settings:Settings = None   # 通过用户传过来的配置信息

    def build(self):
        if self.llm is None or self.settings is None:
            raise

        # 加载 smith
        # 加载 output_structure
        self._load_smith()
        # 由于 task 字段没有办法确认
        # self._set_structed_output()
        logger.info("开始创建 langgraph")

        builder = StateGraph(state_schema=State_New)
        # Define the function that calls the model
        def call_model(state: State):
            response = self.llm.invoke(state["messages"]) # response 现在已经被格式化了
            # if len(response.location.baiduditu) == 0 \
            #     and response.location.region != "" \
            #     and response.location.query != "":
            #     response.location.baiduditu = [OnePlace.model_validate(i) for i in BaiduDitu().invoke({"region":response.location.region,"query":response.location.query})]
            # return {"messages": [AIMessage(content=response.model_dump_json())],"task":response}
            return {"messages":[response]}
        # 这个节点在这里没有任何作用
        tool_node = ToolNode(tools=[BaiduDitu()])        
        # Define the (single) node in the graph
        builder.add_node("tools",tool_node)
        builder.add_node("model", call_model)
        builder.add_edge(START, "model")
        builder.add_edge("model",END)
        builder.add_conditional_edges(
            "model",
            tools_condition,
        )
        # Any time a tool is called, we return to the chatbot to decide the next step
        builder.add_edge("tools", "model")

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