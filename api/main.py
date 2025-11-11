from fastapi import FastAPI, UploadFile, File
import requests

app = FastAPI()

OCR_API_URL = "https://api.ocr.space/parse/image"
API_KEY = "helloworld"  # free demo key from OCR.Space

@app.get("/")
async def root():
    return {"status": "OK", "message": "FastAPI OCR running on Vercel"}

@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    # Read uploaded file
    content = await file.read()

    # Send to OCR.Space API
    response = requests.post(
        OCR_API_URL,
        files={"file": (file.filename, content)},
        data={"apikey": API_KEY, "language": "eng"}
    )

    data = response.json()
    if not data.get("IsErroredOnProcessing"):
        text = data["ParsedResults"][0]["ParsedText"]
        return {"success": True, "text": text.strip()}
    else:
        return {"success": False, "error": data.get("ErrorMessage")}
