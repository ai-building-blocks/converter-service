from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from .service import convert_document
from .models import ConversionResponse

app = FastAPI(
    title="Document Converter API",
    description="API for converting documents to markdown using docling",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/convert", 
         response_model=ConversionResponse,
         summary="Convert document to markdown",
         description="Upload a document (PDF) and convert it to markdown format")
async def convert_file(file: UploadFile = File(...)):
    try:
        result = await convert_document(file)
        return result
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
