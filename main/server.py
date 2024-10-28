from fastapi import FastAPI,UploadFile,File,Depends,Form
from fastapi.responses import RedirectResponse
# from langserve import add_routes
from fastapi.middleware.cors import CORSMiddleware
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field,ValidationError
from typing import Optional,Dict,List,Union
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from fastapi import Depends, FastAPI, Header, HTTPException
from typing_extensions import Annotated, TypedDict
from api_model import GraphBuilder
from log import logger
from init_config import load_settings
from output_format import FlyTask
from local_model import ChatGLM4_LLM
from PIL import Image
settings = load_settings()
# 1.llm 该模型可以调用 with_structed 接口进行输出
# 实现 text-to-txt 任务格式输出
llm = ChatOpenAI(
    temperature=0.95,
    # model="gpt-3.5-turbo-16k",
    model=settings.openai_model,
    api_key=settings.openai_api_key,
    base_url=settings.openai_api_base
)
# 实现 image-to-text
# local_llm = ChatGLM4_LLM()

graph_builder = GraphBuilder()
graph_builder.set_settings(settings)
graph_builder.set_llm(llm)
# graph_builder.set_local_llm(local_llm)
graph = graph_builder.build()

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",)

@app.get("/")
def read_root():
    return {"Hello": "World"}

class TaskDescription(BaseModel):
    thread_id: str = Field(description="标识一个session")
    text: str = Field(description = "标识用户的文字输入")



@app.post("/masifan/v1")
async def get_task_v1(task:TaskDescription):
    config = {"configurable":{"thread_id":task.thread_id}}
    # 这里的调用方式 更改了，减少了 token 的使用量
    return await graph.ainvoke({"messages":[('user',task.text)]},config=config)

# 这个地方不加上 =Depends() 就会报错,加上后会使得 request-type'Content-Type: multipart/form-data'
@app.post("/masifan/v2")
async def get_task_v2(task:TaskDescription=Depends(),image_file:UploadFile=File(...)):
    config = {"configurable":{"thread_id":task.thread_id}}
    text_from_image = ""
    if image_file is not None:
        import hashlib,os
        # 保存 image_file 到 ../session/thread_id/
        # 并且使用 MD5 算法重命名图片
        # 生成 MD5 哈希值
        image_hash = hashlib.md5(image_file.file.read()).hexdigest()
        
        # 重置文件指针
        image_file.file.seek(0)
        
        # 生成图片名称
        image_name = f"{image_hash}.jpg"
        
        # 生成图片路径
        image_dir = os.path.join("../session/", task.thread_id)
        os.makedirs(image_dir, exist_ok=True)  # 确保目录存在
        image_path = os.path.join(image_dir, image_name)
        
        # 保存图片
        with open(image_path, "wb") as f:
            f.write(image_file.file.read())

        # 打开并转换图片
        image = Image.open(image_path).convert('RGB')
        # TODO 这个地方的 input 参数有点耦合
        # nonlocal text_from_image
        text_from_image = await graph_builder.local_llm.ainvoke(input="请描述一下这张图片中主要物体的特征",image=image) 
    return await graph.ainvoke({"messages":[('user',task.text+text_from_image)]}, config=config)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)



if __name__ == "__main__":
    import uvicorn

    logger.info("服务器启动 0.0.0.0 8000")
    uvicorn.run(app='server:app', host="0.0.0.0", port=8000)

