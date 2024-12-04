import tempfile
from pathlib import Path
from fastapi import UploadFile
from docling import DocumentConverter
from .models import ConversionResponse

async def convert_document(file: UploadFile) -> ConversionResponse:
    # Create temporary file to store uploaded document
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_path = Path(temp_file.name)

    try:
        # Initialize document converter
        doc_converter = DocumentConverter()

        # Convert document
        result = doc_converter.convert(temp_path)

        # Get markdown output
        markdown_content = result.to_markdown()
        
        return ConversionResponse(
            filename=file.filename,
            markdown_content=markdown_content
        )
    finally:
        # Clean up temporary file
        temp_path.unlink()
