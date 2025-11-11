# api/main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import easyocr
import io
from PIL import Image

app = FastAPI()
reader = easyocr.Reader(['en'], gpu=False)

@app.get("/")
def root():
    return {"message": "FastAPI on Vercel works!"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image.save("/tmp/temp.png")  # temp file for OCR
    result = reader.readtext("/tmp/temp.png", detail=0)
    text = ''.join(result)
    return JSONResponse({"filename": file.filename, "text": text})
