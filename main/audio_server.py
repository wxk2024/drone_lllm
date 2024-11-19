import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
from fastapi import FastAPI,UploadFile,File,Depends,Form,HTTPException
from fastapi.responses import RedirectResponse
# from langserve import add_routes
from fastapi.middleware.cors import CORSMiddleware
import urllib.parse
import aiohttp

async def make_async_request(audio_path):
    base_url = "http://localhost:8001/audio"
    encoded_audio_path = urllib.parse.quote(audio_path)
    url = f"{base_url}?audio_path={encoded_audio_path}"
    headers = {"accept": "application/json"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"请求失败，状态码: {response.status}")

if __name__ == "__main__":
    import uvicorn
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = "openai/whisper-large-v3"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, 
        low_cpu_mem_usage=True, 
        use_safetensors=True,
        cache_dir="/home/user/wangxiaoke/TransModel",
        local_files_only=True
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id,
        cache_dir="/home/user/wangxiaoke/TransModel",
        local_files_only=True)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device,
        return_timestamps=True,
    )

    # import gradio as gr
    # gr.Interface.from_pipeline(pipe).launch(server_name='0.0.0.0',server_port=8001)

    audio_app = FastAPI(
        title="Pipeline audio-to-text Server",
        version="1.0",
        description="A simple api server audio-to-text",)

    @audio_app.get("/")
    def read_root():
        return {"Hello": "audio"}

    @audio_app.get("/audio")
    async def audio_to_text(audio_path: str):
      try:
          result = pipe(audio_path)
          return {"transcription": result["text"]}
      except Exception as e:
          raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

    uvicorn.run(app='audio_server:audio_app', host="0.0.0.0", port=8001)