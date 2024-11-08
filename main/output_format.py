from typing import Optional,Dict,Any,List
from pydantic import BaseModel, Field
from typing_extensions import Annotated, TypedDict
from typing import Union
from pydantic import ValidationError,model_validator

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
from datetime import datetime
class FlyTask(BaseModel):
    """Respond in a conversational manner. Be kind and helpful."""
    fly_type: Optional[str] = Field(description = "任务类型: 应急任务 or 测量任务",default=None)
    # fly_object:str = Field(description = "测量或者追踪的对象是谁")
    # location:Location = Field(description = "city:北京 query:故宫")
    fly_description:Optional[str] = Field(description= "有关任务的详细描述,通过询问用户更多细节进行增加",default=None)
    deadline:Optional[str] = Field(description="任务的截至日期和时间点,格式为 YYYY-MM-DD HH:MM:SS",default=None)

    # @model_validator(mode='after')
    # def check_passwords_match(self) -> 'FlyTask':
    #     if self.deadline:
    #         self.deadline = self.deadline.strftime("%Y/%m/%d %H:%M:%S")
    #     return self

class AiResponse(BaseModel):
    answer_and_ask:str = Field(description="给用户的最新回复")
    task:FlyTask = Field(description="本次对话中确定下来的任务",default=None)

# 和上面两个一摸一样
# class FlyTaskNew(TypedDict):
#     '''无人机任务相关信息'''    
#     fly_type:Annotated[str,...,"任务类型：应急任务 或者 测量任务"]
#     fly_description:Annotated[str,...,"有关任务的详细描述,通过询问用户更多细节进行增加"]
#     deadline:Annotated[datetime,...,"任务的截至日期和时间点"]

# class AiResponseNew(TypedDict):
#     '''response to user'''
#     answer_and_ask:Annotated[str,...,"给用户的最新回复"]
#     task:Annotated[FlyTaskNew,...,"无人机任务"]
