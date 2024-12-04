import tempfile
from pathlib import Path
from fastapi import UploadFile
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
from .models import ConversionResponse

async def convert_document(file: UploadFile) -> ConversionResponse:
    # Create temporary file to store uploaded document
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_path = Path(temp_file.name)

    try:
        # Configure pipeline options
        pipeline_options = PdfPipelineOptions(do_table_structure=True)
        pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE
        pipeline_options.table_structure_options.do_cell_matching = True

        # Initialize document converter with options
        doc_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

        # Convert document
        result = doc_converter.convert(temp_path)

        # Get markdown output
        markdown_content = result.document.export_to_markdown()
        
        return ConversionResponse(
            filename=file.filename,
            markdown_content=markdown_content
        )
    finally:
        # Clean up temporary file
        temp_path.unlink()
