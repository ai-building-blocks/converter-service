# Docling Service

A FastAPI web service for converting documents to markdown using docling. This service provides a simple API endpoint for converting PDF documents to markdown format, with support for OCR and table structure detection.

## Features

- PDF to Markdown conversion
- OCR support for scanned documents
- Table structure detection
- RESTful API with Swagger documentation
- Docker support with optimized multi-stage builds

## Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/hannes-sistemica/docling-service.git
cd docling-service
```

2. Build and run the Docker container:
```bash
docker build -t docling-service .
docker run -p 8000:8000 docling-service
```

### Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/hannes-sistemica/docling-service.git
cd docling-service
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the service:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Usage

Once the service is running, you can access:

- API endpoint: http://localhost:8000/convert
- Swagger documentation: http://localhost:8000/docs

### API Endpoints

#### POST /convert

Upload a PDF document and convert it to markdown format.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (PDF document)

**Response:**
```json
{
    "filename": "example.pdf",
    "markdown_content": "# Converted markdown content..."
}
```

## Development

The service is built with:
- FastAPI for the web framework
- docling for document conversion
- Python 3.11
- Docker for containerization

## License

[MIT License](LICENSE)
