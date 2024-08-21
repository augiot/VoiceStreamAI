from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from faster_whisper import WhisperModel
import shutil
import os
import uvicorn
 
app = FastAPI()
 
# 配置 Whisper 模型
model_size = "/mnt/user2/workspace/Aug/model/faster-whisper-large-v3"
model = WhisperModel(model_size, device="cuda", compute_type="float16")
 
@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    temp_file = f"temp_{file.filename}"
    
    # 保存上传的文件到临时文件
    with open(temp_file, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
 
    try:
        # 使用 Whisper 模型进行转录
        segments, info = model.transcribe(temp_file, beam_size=5)
        os.remove(temp_file)  # 删除临时文件
        
        # 组装转录结果
        results = [{
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        } for segment in segments]
 
        return JSONResponse(content={
            "language": info.language,
            "language_probability": info.language_probability,
            "transcription": results
        })
    except Exception as e:
        os.remove(temp_file)  # 确保即使出错也删除临时文件
        return JSONResponse(status_code=500, content={"message": str(e)})
 
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8007)
