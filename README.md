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

#### Option 1: Pull from GitHub Container Registry

```bash
docker pull ghcr.io/sistemica/docling-service:latest
docker run -p 8000:8000 ghcr.io/sistemica/docling-service:latest
```

#### Option 2: Build Locally

1. Clone the repository:
```bash
git clone https://github.com/sistemica/docling-service.git
cd docling-service
```

2. Build and run the Docker container:

For Intel/AMD (x86_64):
```bash
docker build --platform linux/amd64 -t docling-service .
docker run -p 8000:8000 docling-service
```

For Apple Silicon (M1/M2):
```bash
docker build --platform linux/arm64 -t docling-service .
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

### GPU Support

The document conversion process can be accelerated using GPU support. You might see this message during execution:
```
neither CUDA nor MPS are available - defaulting to CPU. Note: This module is much faster with a GPU.
```

To enable GPU acceleration:

#### For NVIDIA GPUs (CUDA):
1. Install NVIDIA drivers for your GPU
2. Install CUDA Toolkit from [NVIDIA's website](https://developer.nvidia.com/cuda-downloads)
3. When running with Docker, use NVIDIA Container Toolkit:
```bash
# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Run the container with GPU support
docker run --gpus all -p 8000:8000 ghcr.io/hannes-sistemica/docling-service:latest
```

#### For Apple Silicon (MPS):
The Metal Performance Shaders (MPS) backend is automatically used on Apple Silicon Macs when available. No additional setup is required.

Note: If neither CUDA nor MPS is available, the service will continue to work using CPU, just at a slower speed.

### GitHub Actions Workflow

The repository includes a GitHub Actions workflow that automatically builds and publishes the Docker image to GitHub Container Registry (GHCR). To enable this workflow:

1. Go to your repository settings on GitHub
2. Navigate to "Actions" → "General"
3. Under "Workflow permissions", select "Read and write permissions"
4. Save the changes

The workflow will:
- Build the Docker image on every push to main and pull requests
- Push the image to GHCR when changes are merged to main
- Create versioned tags when you push version tags (e.g., v1.0.0)

To create a versioned release:
```bash
git tag v1.0.0
git push origin v1.0.0
```

## License

[MIT License](LICENSE)
