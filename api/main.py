from fastapi import FastAPI, UploadFile, File
import requests, json

app = FastAPI()
OCR_API_URL = "https://api.ocr.space/parse/image"
API_KEY = "helloworld"  # demo key

@app.get("/")
async def root():
    return {"status": "OK", "message": "Vercel OCR API working"}

@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    content = await file.read()
    response = requests.post(
        OCR_API_URL,
        files={"file": (file.filename, content)},
        data={"apikey": API_KEY, "language": "eng"},
    )
    try:
        data = response.json()
    except json.JSONDecodeError:
        data = json.loads(response.text)

    if not data.get("IsErroredOnProcessing"):
        text = data["ParsedResults"][0]["ParsedText"]
        return {"success": True, "text": text.strip()}
    return {"success": False, "error": data.get("ErrorMessage")}
