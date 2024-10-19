from typing import Optional,Dict,Any,List
from pydantic import BaseModel, Field
from typing_extensions import Annotated, TypedDict

class OnePlace(BaseModel):
    region:str = Field("region name")
    address:str = Field("address name")
    name:str = Field("place name")
    lat:float = Field("latitude")   #纬度
    lon:float = Field("longitude")  #经度


class Feature(BaseModel):
    name:str = Field(description="the name of the feature")
    value:Any = Field(description="the value of the feature")

class Location(BaseModel):
    region:str = Field(description="the region's name",default="")
    query:str = Field(description="the query location of the region",default="")
    baiduditu:Optional[List[OnePlace]] = Field(description="the response of the tool",default=[])

# 4. parser
class FlyTask(BaseModel):
    """飞行器任务格式"""
    fly_type: str = Field(description = "The type of task: 测量任务 or 追踪任务")
    fly_object:str = Field(description = "测量或者追踪的对象是谁")
    location:Location = Field(description = "city:北京 query:故宫")
    fly_object_feature: Optional[List[Feature]] = Field(description = "location:xxx, size:xxxx, color:XXX")
    ask:str = Field(description="ask user to fill a flytask")
