from typing import Optional,Dict,Any,List
from pydantic import BaseModel, Field
from typing_extensions import Annotated, TypedDict

class Feature(BaseModel):
    name:str = Field(description="the name of the feature")
    value:Any = Field(description="the value of the feature")

# 4. parser
class FlyTask(BaseModel):
    """飞行器任务格式"""
    fly_type: str = Field(description = "The type of task: 测量任务 or 追踪任务")
    fly_object:str = Field(description = "测量或者追踪的对象是谁")
    fly_object_feature: Optional[List[Feature]] = Field(description = "location:xxx, size:xxxx, color:XXX")
