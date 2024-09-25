# table_detection

This FastAPI application detects tables in images and returns the processed images with bounding boxes along with extracted table data.


## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/table-detection.git
    cd table-detection
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the FastAPI application:
    ```bash
    uvicorn app.main:app --reload
    ```

5. Access the API at `http://127.0.0.1:8000/docs` to test the upload endpoint.

## Usage

Send a POST request to `/upload/` with an image file to detect tables.

## Example

Using `curl`:
```bash
curl -F 'file=@/path/to/your/image.jpg' http://127.0.0.1:8000/upload/
