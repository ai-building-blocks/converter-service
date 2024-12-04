import tempfile
import torch
from pathlib import Path
from fastapi import UploadFile
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter
from .models import ConversionResponse

async def convert_document(file: UploadFile) -> ConversionResponse:
    # Create temporary file to store uploaded document
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_path = Path(temp_file.name)

    try:
        # Configure pipeline options
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.do_cell_matching = True

        # Configure pipeline options with device
        device = "mps" if torch.backends.mps.is_available() else "cpu"
        pipeline_options = PdfPipelineOptions(device=device)
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.do_cell_matching = True
        
        # Initialize document converter
        doc_converter = DocumentConverter()

        # Convert document
        conv_result = doc_converter.convert(temp_path)

        # Get markdown output
        markdown_content = conv_result.document.export_to_markdown()
        
        return ConversionResponse(
            filename=file.filename,
            markdown_content=markdown_content
        )
    finally:
        # Clean up temporary file
        temp_path.unlink()
