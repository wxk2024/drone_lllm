import os
from typing import Any, Dict, List, Optional
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
import huggingface_hub
huggingface_hub.login("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") 

#------------------------
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from log import logger


from langchain_huggingface import HuggingFacePipeline
# Load model directly
import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer,BitsAndBytesConfig,pipeline
from init_config import load_settings
from langchain.prompts import ChatPromptTemplate,HumanMessagePromptTemplate


# 现在使用该模型不能绑定 结构化输出 格式 ~
class ChatGLM4_LLM(LLM):
    # 基于本地 ChatGLM4 自定义 LLM 类
    tokenizer: AutoTokenizer = None
    model: AutoModelForCausalLM = None
    gen_kwargs: dict = None
        
    def __init__(self, gen_kwargs: dict = None):
        super().__init__()
        logger.info("正在从本地加载模型...")
        self.tokenizer = AutoTokenizer.from_pretrained("THUDM/glm-4v-9b",quantization_config=BitsAndBytesConfig( load_in_4bit=True), trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            "THUDM/glm-4v-9b",
            quantization_config=BitsAndBytesConfig(load_in_4bit=True),
            torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=True,
            trust_remote_code=True,
            cache_dir="/root/autodl-tmp/model"
        ).eval()
        gen_kwargs = {"max_length": 2500, "do_sample": True, "top_k": 1}
        logger.info("完成本地模型的加载")
        
        if gen_kwargs is None:
            gen_kwargs = {"max_length": 2500, "do_sample": True, "top_k": 1}
        self.gen_kwargs = gen_kwargs
        
    def _call(self, prompt: str = "请描述一下这张图片中主要物体的特征", 
              stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None,
              **kwargs: Any) -> str:
        # 这个地方的 image 二进制传进来使用的是 kwargs 参数，目前只能想到！
        messages = [{"role": "user", "image":kwargs["image"],"content": prompt}]
        model_inputs = self.tokenizer.apply_chat_template(
            messages, tokenize=True, return_tensors="pt", return_dict=True, add_generation_prompt=True
        )
        # 注意这个地方必须放到 GPU 上面
        model_inputs.to("cuda")
        generated_ids = self.model.generate(**model_inputs, **self.gen_kwargs)
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs['input_ids'], generated_ids)
        ]
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]   # 不用 [0] 就会出错误，因为要的不是字符串
        return response
    
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """返回用于识别LLM的字典,这对于缓存和跟踪目的至关重要。"""
        return {
            "model_name": "glm-4-9b",
            "max_length": self.gen_kwargs.get("max_length"),
            "do_sample": self.gen_kwargs.get("do_sample"),
            "top_k": self.gen_kwargs.get("top_k"),
        }

    @property
    def _llm_type(self) -> str:
        return "glm-4-9b"

