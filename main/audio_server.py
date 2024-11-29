import torch
import base64
import uvicorn
from fastapi import FastAPI
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
from pydantic import BaseModel

# asr model
model = AutoModel(
    model="iic/SenseVoiceSmall",
    trust_remote_code=True,
    remote_code="./model.py",
    vad_model="fsmn-vad",
    vad_kwargs={"max_single_segment_time": 30000},
    device="cuda:0",
)

# 定义asr数据模型，用于接收POST请求中的数据
class ASRItem(BaseModel):
    wav : str # 输入音频

app = FastAPI()
@app.post("/asr")
async def asr(item: ASRItem):
    try:
        data = base64.b64decode(item.wav)
        with open("test.wav", "wb") as f:
            f.write(data)
        res = model.generate("test.wav", 
                            language="auto",  # "zn", "en", "yue", "ja", "ko", "nospeech"
                            use_itn=True,
                            batch_size_s=60,
                            merge_vad=True,  #
                            merge_length_s=15,)
        text = rich_transcription_postprocess(res[0]["text"])
        result_dict = {"code": 0, "msg": "ok", "res": text}
    except Exception as e:
        result_dict = {"code": 1, "msg": str(e)}
    return result_dict

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)

