from pydantic import BaseModel

class ConversionResponse(BaseModel):
    filename: str
    markdown_content: str
