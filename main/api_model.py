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
from langchain_core.runnables import RunnableConfig
from langchain_core.output_parsers import PydanticOutputParser
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
from tools import BaiduDitu,get_datetime
from output_format import FlyTask,AiResponse
from log import logger
from init_config import Settings
from datetime import datetime
from langchain_ollama import ChatOllama
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
    task: AiResponse

# 由于当前任务字段迟迟确定不了，只好用这个了！
class State_New(TypedDict):
    messages: Annotated[list, add_messages]

class GraphBuilder():
    _BM = TypeVar("_BM", bound=BaseModel)
    _DictOrPydanticClass = Union[Dict[str, Any], Type[_BM], Type]
    def __init__(self):
        self.text_llm = None                 # ollama 大模型用来文本
        self.image_llm = None           # local  大模型用来图片转文字
        self.prompt = None              # 提示词：通过prompt.json
        self.graph = None               # langgraph 框架最主要的作用
        self.settings:Settings = None   # 通过用户传过来的配置信息

    # 自定义的 RecAct 结构的 Agent
    def build(self):
        if self.text_llm is None or self.settings is None:
            raise

        # 加载 smith
        # 加载 output_structure
        self._load_smith()
        # 由于 task 字段没有办法确认
        logger.info("开始创建 langgraph")
        builder = StateGraph(state_schema=State)

        # Define the function that calls the model
        async def call_model(state: State,config:RunnableConfig):
            now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            response = await self.text_llm.ainvoke(self.settings._prompt.format_messages() + [SystemMessage(content="当前的时间是"+now_time)] +state["messages"])
            print(response)
            return {"messages":response}
        
        async def format_output(state:State,config:RunnableConfig):
            now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info("format_output",config["configurable"])
            # TODO
            # text_llm = ChatOpenAI(
            #         temperature=0.0,
            #         # model="gpt-3.5-turbo-16k",
            #         model=self.settings.openai_model,
            #         api_key=self.settings.openai_api_key,
            #         base_url=self.settings.openai_api_base
            # )
            # text_llm = ChatOllama(model=self.settings.ollama_model,
            #      temperature=0.8,
            #      keep_alive=10 * 60)
            parser = PydanticOutputParser(pydantic_object=AiResponse)
            format_instructions =parser .get_format_instructions()
            format_llm = self.text_llm.with_structured_output(AiResponse)
            to_user = await format_llm.ainvoke(self.settings._prompt.format_messages()+[SystemMessage(content="当前的时间是"+now_time)]+state["messages"] + [HumanMessage(content=f"通过以下格式回复我\n {format_instructions}")])
            logger.info(to_user)
            return {"task":to_user}

        # TODO 这个节点在这里没有任何作用,因为我是在提示词里面写好的模板
        tools = [get_datetime]
        tool_node = ToolNode(tools=tools)        
        self.text_llm = self.text_llm.bind_tools(tools)  # 只有让 llm 知道有这个 tool 才可以
        # self._set_structed_output()
        # Define the (single) node in the graph
        builder.add_node("action",tool_node)
        builder.add_node("agent", call_model)
        builder.add_node("format", format_output)
        builder.add_edge(START, "agent")
        # builder.add_edge("agent","format")
        builder.add_edge("format",END)
        builder.add_conditional_edges(
            # First, we define the start node. We use `agent`.
            # This means these are the edges taken after the `agent` node is called.
            "agent",
            # Next, we pass in the function that will determine which node is called next.
            self._should_continue,
            # Next, we pass in the path map - all the possible nodes this edge could go to
            ["action", "format"],
        )
        # Any time a tool is called, we return to the chatbot to decide the next step
        builder.add_edge("action", "agent")

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
        self.text_llm = self.text_llm.with_structured_output(AiResponse)
        logger.info("设置输出格式成功")

    @staticmethod
    def _should_continue(state: State):
        """Return the next node to execute."""
        last_message = state["messages"][-1]
        print("_should_continue")
        # If there is no function call, then we finish
        if not last_message.tool_calls:
            return "format"
        # Otherwise if there is, we continue
        return "action"

    def set_image_llm(self,image_llm):
        self.image_llm = image_llm
    def set_llm(self,llm):
        self.text_llm = llm
    def set_settings(self,settings:Settings):
        self.settings = settings


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