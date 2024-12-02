import tempfile
import torch
from pathlib import Path
from fastapi import UploadFile
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
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

        # Configure device and pipeline options
        device = "mps" if torch.backends.mps.is_available() else "cpu"
        pipeline_options.model_config.device = device
        
        # Initialize document converter
        doc_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

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
