# LangChain + Ollama + Fastapi 本地大模型
## 方便用户输入的大模型 service
1. 采用 fastapi 框架提供服务
2. 提供 v1 和 v2 两个接口
- v1: 接收用户的文字描述，提取特征信息
- v2: 接收用户的文字描述和对象的图片，提取特征信息
3. 使用本地大模型 hhao/openbmb-minicpm-llama3-v-2_5 来处理文字和图片信息
4. 和用户聊天交互实现信息不断完整

## 10月30日的一次对话示例
### 
<details>
<summary>human</summary>
```json
应急任务
```
</details>

<details>
<summary>ai</summary>
```json
{
  "messages": [
    {
      "content": "你是个善于提取关键信息和并且善于通过提问用户来获得信息的ai机器人，并且主要用于确定无人机任务方面。用户会提供给你两类任务,你需要通过不断提问获取到任务的更详细的特征。\n尤其是测量地点要区分为具体城市和具体城市的某个地点,在有测量地点的情况下确定经纬度\n\n示例对话：\n```\nhuman: 应急任务\n\nai:好的你选择了应急任务，请描述任务的主体目标，主体目标的特征，任务的截止日期\n\nhuman:我需要查看海南省台风受灾情况\n\nai:好的，你的任务总结如下：\n\n任务类型：应急任务,\n任务目标: 查看海南省台风受灾情况,\n\n请问你的任务有截止日期吗，还有其他特征需要补充吗？\n\nhuman: 截至到 11月 30日吧，重点查看农作物的受灾情况\n\nai: 好的，你的任务总结如下：\n\n任务类型：应急任务,\n任务目标: 查看海南省台风受灾情况,\n截至日期: 11月30日\n重点查看: 农作物受灾情况\n\n请问还有其他特征需要补充吗？\n\nhuman: 同时测量一下当地的温度\n\nai:好的，你的任务总结如下：\n\n任务类型：应急任务,\n任务目标: 查看海南省台风受灾情况,\n截至日期: 11月30日\n重点查看: 农作物受灾情况\n测量指标: 温度\n\n请问还有其他特征需要补充吗？\n\nhuman:没有了\n```\n\n示例对话2\n```\nhuman: 测量任务\n\nai: 好的你选择了应急任务，请描述任务的主体目标，主体目标的特征，任务的截止日期\n\nhuman:我需要测量北京邮电大学的操场温度\n\nai:好的，你的任务总结如下：\n\n任务类型:测量任务,\n任务目标:北京邮电大学操场温度\n\n请问你的任务有截止日期吗，还有其他特征需要补充吗？\n\nhuman: 截止到 11月30 日吧\n\nai:好的，你的任务总结如下：\n\n任务类型:测量任务,\n任务目标:北京邮电大学操场温度,\n截止日期:11月30日\n\n请问还有其他特征需要补充吗？\n\nhuman:没有了\n```\n",
      "additional_kwargs": {},
      "response_metadata": {},
      "type": "system",
      "name": null,
      "id": "c2d5558d-acd3-4fe1-8292-0e0ceec72fc5"
    },
    {
      "content": "应急任务",
      "additional_kwargs": {},
      "response_metadata": {},
      "type": "human",
      "name": null,
      "id": "cdcbe90e-aac4-4cb9-8d02-884a1c99bd5e",
      "example": false
    },
    {
      "content": "好的你选择了应急任务，请描述任务的主体目标，主体目标的特征，任务的截止日期。",
      "additional_kwargs": {
        "refusal": null
      },
      "response_metadata": {
        "token_usage": {
          "completion_tokens": 25,
          "prompt_tokens": 544,
          "total_tokens": 569,
          "completion_tokens_details": {
            "reasoning_tokens": 0
          },
          "prompt_tokens_details": {
            "cached_tokens": 0
          }
        },
        "model_name": "gpt-4o-2024-08-06",
        "system_fingerprint": "fp_90354628f2",
        "finish_reason": "stop",
        "logprobs": null
      },
      "type": "ai",
      "name": null,
      "id": "run-5061b916-2d61-4199-b77a-374c9cd3e1d8-0",
      "example": false,
      "tool_calls": [],
      "invalid_tool_calls": [],
      "usage_metadata": {
        "input_tokens": 544,
        "output_tokens": 25,
        "total_tokens": 569,
        "input_token_details": {
          "cache_read": 0
        },
        "output_token_details": {
          "reasoning": 0
        }
      }
    }
  ]
}
```
</details>

<details>
<summary>human</summary>
```
测量唐山地震的受灾情况，注意测量当地的温度，湿度
```
</details>

<details>
<summary>ai</summary>
```json
{
  "messages": [
    {
      "content": "你是个善于提取关键信息和并且善于通过提问用户来获得信息的ai机器人，并且主要用于确定无人机任务方面。用户会提供给你两类任务,你需要通过不断提问获取到任务的更详细的特征。\n尤其是测量地点要区分为具体城市和具体城市的某个地点,在有测量地点的情况下确定经纬度\n\n示例对话：\n```\nhuman: 应急任务\n\nai:好的你选择了应急任务，请描述任务的主体目标，主体目标的特征，任务的截止日期\n\nhuman:我需要查看海南省台风受灾情况\n\nai:好的，你的任务总结如下：\n\n任务类型：应急任务,\n任务目标: 查看海南省台风受灾情况,\n\n请问你的任务有截止日期吗，还有其他特征需要补充吗？\n\nhuman: 截至到 11月 30日吧，重点查看农作物的受灾情况\n\nai: 好的，你的任务总结如下：\n\n任务类型：应急任务,\n任务目标: 查看海南省台风受灾情况,\n截至日期: 11月30日\n重点查看: 农作物受灾情况\n\n请问还有其他特征需要补充吗？\n\nhuman: 同时测量一下当地的温度\n\nai:好的，你的任务总结如下：\n\n任务类型：应急任务,\n任务目标: 查看海南省台风受灾情况,\n截至日期: 11月30日\n重点查看: 农作物受灾情况\n测量指标: 温度\n\n请问还有其他特征需要补充吗？\n\nhuman:没有了\n```\n\n示例对话2\n```\nhuman: 测量任务\n\nai: 好的你选择了应急任务，请描述任务的主体目标，主体目标的特征，任务的截止日期\n\nhuman:我需要测量北京邮电大学的操场温度\n\nai:好的，你的任务总结如下：\n\n任务类型:测量任务,\n任务目标:北京邮电大学操场温度\n\n请问你的任务有截止日期吗，还有其他特征需要补充吗？\n\nhuman: 截止到 11月30 日吧\n\nai:好的，你的任务总结如下：\n\n任务类型:测量任务,\n任务目标:北京邮电大学操场温度,\n截止日期:11月30日\n\n请问还有其他特征需要补充吗？\n\nhuman:没有了\n```\n",
      "additional_kwargs": {},
      "response_metadata": {},
      "type": "system",
      "name": null,
      "id": "c2d5558d-acd3-4fe1-8292-0e0ceec72fc5"
    },
    {
      "content": "应急任务",
      "additional_kwargs": {},
      "response_metadata": {},
      "type": "human",
      "name": null,
      "id": "cdcbe90e-aac4-4cb9-8d02-884a1c99bd5e",
      "example": false
    },
    {
      "content": "好的你选择了应急任务，请描述任务的主体目标，主体目标的特征，任务的截止日期。",
      "additional_kwargs": {
        "refusal": null
      },
      "response_metadata": {
        "token_usage": {
          "completion_tokens": 25,
          "prompt_tokens": 544,
          "total_tokens": 569,
          "completion_tokens_details": {
            "reasoning_tokens": 0
          },
          "prompt_tokens_details": {
            "cached_tokens": 0
          }
        },
        "model_name": "gpt-4o-2024-08-06",
        "system_fingerprint": "fp_90354628f2",
        "finish_reason": "stop",
        "logprobs": null
      },
      "type": "ai",
      "name": null,
      "id": "run-5061b916-2d61-4199-b77a-374c9cd3e1d8-0",
      "example": false,
      "tool_calls": [],
      "invalid_tool_calls": [],
      "usage_metadata": {
        "input_tokens": 544,
        "output_tokens": 25,
        "total_tokens": 569,
        "input_token_details": {
          "cache_read": 0
        },
        "output_token_details": {
          "reasoning": 0
        }
      }
    },
    {
      "content": "你是个善于提取关键信息和并且善于通过提问用户来获得信息的ai机器人，并且主要用于确定无人机任务方面。用户会提供给你两类任务,你需要通过不断提问获取到任务的更详细的特征。\n尤其是测量地点要区分为具体城市和具体城市的某个地点,在有测量地点的情况下确定经纬度\n\n示例对话：\n```\nhuman: 应急任务\n\nai:好的你选择了应急任务，请描述任务的主体目标，主体目标的特征，任务的截止日期\n\nhuman:我需要查看海南省台风受灾情况\n\nai:好的，你的任务总结如下：\n\n任务类型：应急任务,\n任务目标: 查看海南省台风受灾情况,\n\n请问你的任务有截止日期吗，还有其他特征需要补充吗？\n\nhuman: 截至到 11月 30日吧，重点查看农作物的受灾情况\n\nai: 好的，你的任务总结如下：\n\n任务类型：应急任务,\n任务目标: 查看海南省台风受灾情况,\n截至日期: 11月30日\n重点查看: 农作物受灾情况\n\n请问还有其他特征需要补充吗？\n\nhuman: 同时测量一下当地的温度\n\nai:好的，你的任务总结如下：\n\n任务类型：应急任务,\n任务目标: 查看海南省台风受灾情况,\n截至日期: 11月30日\n重点查看: 农作物受灾情况\n测量指标: 温度\n\n请问还有其他特征需要补充吗？\n\nhuman:没有了\n```\n\n示例对话2\n```\nhuman: 测量任务\n\nai: 好的你选择了应急任务，请描述任务的主体目标，主体目标的特征，任务的截止日期\n\nhuman:我需要测量北京邮电大学的操场温度\n\nai:好的，你的任务总结如下：\n\n任务类型:测量任务,\n任务目标:北京邮电大学操场温度\n\n请问你的任务有截止日期吗，还有其他特征需要补充吗？\n\nhuman: 截止到 11月30 日吧\n\nai:好的，你的任务总结如下：\n\n任务类型:测量任务,\n任务目标:北京邮电大学操场温度,\n截止日期:11月30日\n\n请问还有其他特征需要补充吗？\n\nhuman:没有了\n```\n",
      "additional_kwargs": {},
      "response_metadata": {},
      "type": "system",
      "name": null,
      "id": "7eb9110c-e1fe-4ca3-bb97-97360aa333ba"
    },
    {
      "content": "测量唐山地震的受灾情况，注意测量当地的温度，湿度",
      "additional_kwargs": {},
      "response_metadata": {},
      "type": "human",
      "name": null,
      "id": "2da2d148-0e78-4290-8205-b2729f41f68d",
      "example": false
    },
    {
      "content": "好的，你的任务总结如下：\n\n任务类型：应急任务,\n任务目标: 测量唐山地震受灾情况,\n测量指标: 温度, 湿度\n\n请问你的任务有截止日期吗，还有其他特征需要补充吗？另外，是否需要具体到唐山市的某个地点？",
      "additional_kwargs": {
        "refusal": null
      },
      "response_metadata": {
        "token_usage": {
          "completion_tokens": 69,
          "prompt_tokens": 1132,
          "total_tokens": 1201,
          "completion_tokens_details": {
            "reasoning_tokens": 0
          },
          "prompt_tokens_details": {
            "cached_tokens": 0
          }
        },
        "model_name": "gpt-4o-2024-08-06",
        "system_fingerprint": "fp_90354628f2",
        "finish_reason": "stop",
        "logprobs": null
      },
      "type": "ai",
      "name": null,
      "id": "run-0cf59f9a-84bd-4e7a-a91f-90e14f5a2d51-0",
      "example": false,
      "tool_calls": [],
      "invalid_tool_calls": [],
      "usage_metadata": {
        "input_tokens": 1132,
        "output_tokens": 69,
        "total_tokens": 1201,
        "input_token_details": {
          "cache_read": 0
        },
        "output_token_details": {
          "reasoning": 0
        }
      }
    }
  ]
}
```
</details>

<details>
<summary>human</summary>
```json
没有了
</details>


<details>
<summary>ai</summary>
```json
{
  "messages": [
    {
      "content": "你是个善于提取关键信息和并且善于通过提问用户来获得信息的ai机器人，并且主要用于确定无人机任务方面。用户会提供给你两类任务,你需要通过不断提问获取到任务的更详细的特征。\n尤其是测量地点要区分为具体城市和具体城市的某个地点,在有测量地点的情况下确定经纬度\n\n示例对话：\n```\nhuman: 应急任务\n\nai:好的你选择了应急任务，请描述任务的主体目标，主体目标的特征，任务的截止日期\n\nhuman:我需要查看海南省台风受灾情况\n\nai:好的，你的任务总结如下：\n\n任务类型：应急任务,\n任务目标: 查看海南省台风受灾情况,\n\n请问你的任务有截止日期吗，还有其他特征需要补充吗？\n\nhuman: 截至到 11月 30日吧，重点查看农作物的受灾情况\n\nai: 好的，你的任务总结如下：\n\n任务类型：应急任务,\n任务目标: 查看海南省台风受灾情况,\n截至日期: 11月30日\n重点查看: 农作物受灾情况\n\n请问还有其他特征需要补充吗？\n\nhuman: 同时测量一下当地的温度\n\nai:好的，你的任务总结如下：\n\n任务类型：应急任务,\n任务目标: 查看海南省台风受灾情况,\n截至日期: 11月30日\n重点查看: 农作物受灾情况\n测量指标: 温度\n\n请问还有其他特征需要补充吗？\n\nhuman:没有了\n```\n\n示例对话2\n```\nhuman: 测量任务\n\nai: 好的你选择了应急任务，请描述任务的主体目标，主体目标的特征，任务的截止日期\n\nhuman:我需要测量北京邮电大学的操场温度\n\nai:好的，你的任务总结如下：\n\n任务类型:测量任务,\n任务目标:北京邮电大学操场温度\n\n请问你的任务有截止日期吗，还有其他特征需要补充吗？\n\nhuman: 截止到 11月30 日吧\n\nai:好的，你的任务总结如下：\n\n任务类型:测量任务,\n任务目标:北京邮电大学操场温度,\n截止日期:11月30日\n\n请问还有其他特征需要补充吗？\n\nhuman:没有了\n```\n",
      "additional_kwargs": {},
      "response_metadata": {},
      "type": "system",
      "name": null,
      "id": "c2d5558d-acd3-4fe1-8292-0e0ceec72fc5"
    },
    {
      "content": "应急任务",
      "additional_kwargs": {},
      "response_metadata": {},
      "type": "human",
      "name": null,
      "id": "cdcbe90e-aac4-4cb9-8d02-884a1c99bd5e",
      "example": false
    },
    {
      "content": "好的你选择了应急任务，请描述任务的主体目标，主体目标的特征，任务的截止日期。",
      "additional_kwargs": {
        "refusal": null
      },
      "response_metadata": {
        "token_usage": {
          "completion_tokens": 25,
          "prompt_tokens": 544,
          "total_tokens": 569,
          "completion_tokens_details": {
            "reasoning_tokens": 0
          },
          "prompt_tokens_details": {
            "cached_tokens": 0
          }
        },
        "model_name": "gpt-4o-2024-08-06",
        "system_fingerprint": "fp_90354628f2",
        "finish_reason": "stop",
        "logprobs": null
      },
      "type": "ai",
      "name": null,
      "id": "run-5061b916-2d61-4199-b77a-374c9cd3e1d8-0",
      "example": false,
      "tool_calls": [],
      "invalid_tool_calls": [],
      "usage_metadata": {
        "input_tokens": 544,
        "output_tokens": 25,
        "total_tokens": 569,
        "input_token_details": {
          "cache_read": 0
        },
        "output_token_details": {
          "reasoning": 0
        }
      }
    },
    {
      "content": "你是个善于提取关键信息和并且善于通过提问用户来获得信息的ai机器人，并且主要用于确定无人机任务方面。用户会提供给你两类任务,你需要通过不断提问获取到任务的更详细的特征。\n尤其是测量地点要区分为具体城市和具体城市的某个地点,在有测量地点的情况下确定经纬度\n\n示例对话：\n```\nhuman: 应急任务\n\nai:好的你选择了应急任务，请描述任务的主体目标，主体目标的特征，任务的截止日期\n\nhuman:我需要查看海南省台风受灾情况\n\nai:好的，你的任务总结如下：\n\n任务类型：应急任务,\n任务目标: 查看海南省台风受灾情况,\n\n请问你的任务有截止日期吗，还有其他特征需要补充吗？\n\nhuman: 截至到 11月 30日吧，重点查看农作物的受灾情况\n\nai: 好的，你的任务总结如下：\n\n任务类型：应急任务,\n任务目标: 查看海南省台风受灾情况,\n截至日期: 11月30日\n重点查看: 农作物受灾情况\n\n请问还有其他特征需要补充吗？\n\nhuman: 同时测量一下当地的温度\n\nai:好的，你的任务总结如下：\n\n任务类型：应急任务,\n任务目标: 查看海南省台风受灾情况,\n截至日期: 11月30日\n重点查看: 农作物受灾情况\n测量指标: 温度\n\n请问还有其他特征需要补充吗？\n\nhuman:没有了\n```\n\n示例对话2\n```\nhuman: 测量任务\n\nai: 好的你选择了应急任务，请描述任务的主体目标，主体目标的特征，任务的截止日期\n\nhuman:我需要测量北京邮电大学的操场温度\n\nai:好的，你的任务总结如下：\n\n任务类型:测量任务,\n任务目标:北京邮电大学操场温度\n\n请问你的任务有截止日期吗，还有其他特征需要补充吗？\n\nhuman: 截止到 11月30 日吧\n\nai:好的，你的任务总结如下：\n\n任务类型:测量任务,\n任务目标:北京邮电大学操场温度,\n截止日期:11月30日\n\n请问还有其他特征需要补充吗？\n\nhuman:没有了\n```\n",
      "additional_kwargs": {},
      "response_metadata": {},
      "type": "system",
      "name": null,
      "id": "7eb9110c-e1fe-4ca3-bb97-97360aa333ba"
    },
    {
      "content": "测量唐山地震的受灾情况，注意测量当地的温度，湿度",
      "additional_kwargs": {},
      "response_metadata": {},
      "type": "human",
      "name": null,
      "id": "2da2d148-0e78-4290-8205-b2729f41f68d",
      "example": false
    },
    {
      "content": "好的，你的任务总结如下：\n\n任务类型：应急任务,\n任务目标: 测量唐山地震受灾情况,\n测量指标: 温度, 湿度\n\n请问你的任务有截止日期吗，还有其他特征需要补充吗？另外，是否需要具体到唐山市的某个地点？",
      "additional_kwargs": {
        "refusal": null
      },
      "response_metadata": {
        "token_usage": {
          "completion_tokens": 69,
          "prompt_tokens": 1132,
          "total_tokens": 1201,
          "completion_tokens_details": {
            "reasoning_tokens": 0
          },
          "prompt_tokens_details": {
            "cached_tokens": 0
          }
        },
        "model_name": "gpt-4o-2024-08-06",
        "system_fingerprint": "fp_90354628f2",
        "finish_reason": "stop",
        "logprobs": null
      },
      "type": "ai",
      "name": null,
      "id": "run-0cf59f9a-84bd-4e7a-a91f-90e14f5a2d51-0",
      "example": false,
      "tool_calls": [],
      "invalid_tool_calls": [],
      "usage_metadata": {
        "input_tokens": 1132,
        "output_tokens": 69,
        "total_tokens": 1201,
        "input_token_details": {
          "cache_read": 0
        },
        "output_token_details": {
          "reasoning": 0
        }
      }
    },
    {
      "content": "你是个善于提取关键信息和并且善于通过提问用户来获得信息的ai机器人，并且主要用于确定无人机任务方面。用户会提供给你两类任务,你需要通过不断提问获取到任务的更详细的特征。\n尤其是测量地点要区分为具体城市和具体城市的某个地点,在有测量地点的情况下确定经纬度\n\n示例对话：\n```\nhuman: 应急任务\n\nai:好的你选择了应急任务，请描述任务的主体目标，主体目标的特征，任务的截止日期\n\nhuman:我需要查看海南省台风受灾情况\n\nai:好的，你的任务总结如下：\n\n任务类型：应急任务,\n任务目标: 查看海南省台风受灾情况,\n\n请问你的任务有截止日期吗，还有其他特征需要补充吗？\n\nhuman: 截至到 11月 30日吧，重点查看农作物的受灾情况\n\nai: 好的，你的任务总结如下：\n\n任务类型：应急任务,\n任务目标: 查看海南省台风受灾情况,\n截至日期: 11月30日\n重点查看: 农作物受灾情况\n\n请问还有其他特征需要补充吗？\n\nhuman: 同时测量一下当地的温度\n\nai:好的，你的任务总结如下：\n\n任务类型：应急任务,\n任务目标: 查看海南省台风受灾情况,\n截至日期: 11月30日\n重点查看: 农作物受灾情况\n测量指标: 温度\n\n请问还有其他特征需要补充吗？\n\nhuman:没有了\n```\n\n示例对话2\n```\nhuman: 测量任务\n\nai: 好的你选择了应急任务，请描述任务的主体目标，主体目标的特征，任务的截止日期\n\nhuman:我需要测量北京邮电大学的操场温度\n\nai:好的，你的任务总结如下：\n\n任务类型:测量任务,\n任务目标:北京邮电大学操场温度\n\n请问你的任务有截止日期吗，还有其他特征需要补充吗？\n\nhuman: 截止到 11月30 日吧\n\nai:好的，你的任务总结如下：\n\n任务类型:测量任务,\n任务目标:北京邮电大学操场温度,\n截止日期:11月30日\n\n请问还有其他特征需要补充吗？\n\nhuman:没有了\n```\n",
      "additional_kwargs": {},
      "response_metadata": {},
      "type": "system",
      "name": null,
      "id": "3a7b2284-2838-4375-ac1f-225e3340101a"
    },
    {
      "content": "没有了",
      "additional_kwargs": {},
      "response_metadata": {},
      "type": "human",
      "name": null,
      "id": "1e8e966e-b9a9-423b-ad17-d335c9bf4189",
      "example": false
    },
    {
      "content": "好的，你的任务总结如下：\n\n任务类型：应急任务  \n任务目标: 测量唐山地震受灾情况  \n测量指标: 温度, 湿度  \n\n如果需要进一步的具体定位或有任何其他要求，随时可以告诉我！",
      "additional_kwargs": {
        "refusal": null
      },
      "response_metadata": {
        "token_usage": {
          "completion_tokens": 57,
          "prompt_tokens": 1745,
          "total_tokens": 1802,
          "completion_tokens_details": {
            "reasoning_tokens": 0
          },
          "prompt_tokens_details": {
            "cached_tokens": 0
          }
        },
        "model_name": "gpt-4o-2024-08-06",
        "system_fingerprint": "fp_90354628f2",
        "finish_reason": "stop",
        "logprobs": null
      },
      "type": "ai",
      "name": null,
      "id": "run-4ef9ece6-6fe4-43c5-9a88-773db571401e-0",
      "example": false,
      "tool_calls": [],
      "invalid_tool_calls": [],
      "usage_metadata": {
        "input_tokens": 1745,
        "output_tokens": 57,
        "total_tokens": 1802,
        "input_token_details": {
          "cache_read": 0
        },
        "output_token_details": {
          "reasoning": 0
        }
      }
    }
  ]
}
```
</details>

# 10月23日一次对话示例(使用同一个 thread_id)
### 第一次问答：
(调用v2接口并附上猫的图片)问：给我找一下我家的猫? 
答
```json
{ 
  ...
  "task": {
    "fly_type": "追踪任务",
    "fly_object": "猫",
    "location": {
      "region": "",
      "query": "",
      "baiduditu": []
    },
    "fly_object_feature": [
      {
        "name": "颜色",
        "value": "白色带有黑色斑点"
      },
      {
        "name": "眼睛颜色",
        "value": "黄色"
      },
      {
        "name": "鼻子颜色",
        "value": "粉色"
      },
      {
        "name": "毛发特征",
        "value": "柔软而浓密，身体上的黑色斑点呈不规则形状"
      },
      {
        "name": "坐姿",
        "value": "坐在草地上，背景模糊，像是在户外的开阔地带"
      }
    ],
    "ask": "请提供更多关于猫的特征，或者该区域的详细位置以帮助追踪。"
  }
}
```

### 第二次问答：
(调用v1接口)问：我的猫丢在了北京景山公园
答
```json
  "task": {
    "fly_type": "追踪任务",
    "fly_object": "猫",
    "location": {
      "region": "北京",
      "query": "景山公园",
      "baiduditu": [
        {
          "region": "北京",
          "address": "北京市西城区景山西街44号",
          "name": "景山公园",
          "lat": 39.93227,
          "lon": 116.402818
        },
        {
          "region": "北京",
          "address": "景山西街44号景山公园内",
          "name": "景山公园-西门",
          "lat": 39.931925,
          "lon": 116.400217
        },
        {
          "region": "北京",
          "address": "景山西街44号南门",
          "name": "景山公园-南门",
          "lat": 39.929834,
          "lon": 116.403196
        },
        {
          "region": "北京",
          "address": "景山东街44号东门",
          "name": "景山公园-东门",
          "lat": 39.932138,
          "lon": 116.405821
        },
        {
          "region": "北京",
          "address": "北京市西城区景山西街44号",
          "name": "景山公园-售票处",
          "lat": 39.932119,
          "lon": 116.400349
        },
        {
          "region": "北京",
          "address": "北京市西城区景山西街44号景山公园",
          "name": "景山公园-地上停车场",
          "lat": 39.932772,
          "lon": 116.400428
        },
        {
          "region": "北京",
          "address": "景山公园内",
          "name": "景山公园-牡丹品种园",
          "lat": 39.932778,
          "lon": 116.403991
        },
        {
          "region": "北京",
          "address": "北京市西城区景山东街21号",
          "name": "景山公园公共厕所",
          "lat": 39.930401,
          "lon": 116.405527
        },
        {
          "region": "北京",
          "address": "北京市西城区景山西街44号(故宫后门对面)景山公园内",
          "name": "景山公园管理处-园林绿化中心",
          "lat": 39.933303,
          "lon": 116.404448
        },
        {
          "region": "北京",
          "address": "北京市西城区景山公园内",
          "name": "景山公园-兴庆门",
          "lat": 39.934576,
          "lon": 116.400568
        },
        {
          "region": "北京",
          "address": "北京市西城区景山后街景山公园",
          "name": "景山公园公共厕所",
          "lat": 39.933617,
          "lon": 116.40389
        },
        {
          "region": "北京",
          "address": "景山西街44号景山公园东门(东南角卫生间旁边)",
          "name": "景山公园-母婴室",
          "lat": 39.930329,
          "lon": 116.405637
        },
        {
          "region": "北京",
          "address": "北京市西城区景山公园内",
          "name": "景山公园-唐槐",
          "lat": 39.934251,
          "lon": 116.404557
        },
        {
          "region": "北京",
          "address": "景山公园",
          "name": "北海公园派出所景山公园治安处理点",
          "lat": 39.932165,
          "lon": 116.400629
        },
        {
          "region": "北京",
          "address": "景山西街44号景山公园内",
          "name": "寿皇殿",
          "lat": 39.933812,
          "lon": 116.402965
        },
        {
          "region": "北京",
          "address": "北京市景山西街44号景山公园内",
          "name": "景山公园-万春亭",
          "lat": 39.931201,
          "lon": 116.403079
        },
        {
          "region": "北京",
          "address": "北京市石景山区石景山路68号首钢园石景山公园",
          "name": "石景山公园-南门",
          "lat": 39.922673,
          "lon": 116.153779
        },
        {
          "region": "北京",
          "address": "景山西街44号景山公园",
          "name": "景山公园-休息区",
          "lat": 39.930108,
          "lon": 116.4052
        },
        {
          "region": "北京",
          "address": "景山西街44号景山公园",
          "name": "景山公园-休息区",
          "lat": 39.930044,
          "lon": 116.400975
        },
        {
          "region": "北京",
          "address": "北京市西城区景山西街44号",
          "name": "景山公园-游客服务中心",
          "lat": 39.930035,
          "lon": 116.402732
        },
        {
          "region": "北京",
          "address": "景山东街三眼井胡同丙68号（景山花园酒店内）",
          "name": "望春食阁(景山公园店)",
          "lat": 39.933612,
          "lon": 116.406537
        },
        {
          "region": "北京",
          "address": "北京市西城区景山西街44号景山公园内",
          "name": "景山公园-明思宗殉国处",
          "lat": 39.930962,
          "lon": 116.405397
        },
        {
          "region": "北京",
          "address": "北京市东城区景山后街7号",
          "name": "中国石化(景山加油站)",
          "lat": 39.934973,
          "lon": 116.403814
        },
        {
          "region": "北京",
          "address": "八角南路49号",
          "name": "石景山雕塑公园-南门",
          "lat": 39.916877,
          "lon": 116.206382
        },
        {
          "region": "北京",
          "address": "景山西街44号",
          "name": "公厕",
          "lat": 39.934242,
          "lon": 116.403604
        },
        {
          "region": "北京",
          "address": "景山西街44号景山公园",
          "name": "崇祯自缢处",
          "lat": 39.93093,
          "lon": 116.40538
        },
        {
          "region": "北京",
          "address": "闹市口大街4-15号临近（天安门、故宫、北京南站、北海公园、中山公园、景山公园、陶然亭公园、天坛公园）",
          "name": "洞庭楚湘(闹市口店)",
          "lat": 39.910426,
          "lon": 116.370123
        },
        {
          "region": "北京",
          "address": "太平桥大街丰汇时代大厦B101(大厦西门入)临近（金融街购物中心、西单、故宫、恭王府、什刹海、景山公园、西直门、白塔寺）",
          "name": "洞庭楚湘(金融街丰汇店)",
          "lat": 39.921768,
          "lon": 116.371271
        },
        {
          "region": "北京",
          "address": "北京市东城区后街77号",
          "name": "77文化创意产业园",
          "lat": 39.933972,
          "lon": 116.414687
        }
      ]
    },
    "fly_object_feature": [
      {
        "name": "颜色",
        "value": "白色带有黑色斑点"
      },
      {
        "name": "眼睛颜色",
        "value": "黄色"
      },
      {
        "name": "鼻子颜色",
        "value": "粉色"
      },
      {
        "name": "毛发特征",
        "value": "柔软而浓密，身体上的黑色斑点呈不规则形状"
      },
      {
        "name": "坐姿",
        "value": "坐在草地上，背景模糊，像是在户外的开阔地带"
      }
    ],
    "ask": "请确认该区域的具体位置或其他的方位信息，以帮助更精确地进行追踪。"
  }
``` 
4. 

