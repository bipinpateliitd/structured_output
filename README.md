# ID Card Data Extractor

An AI-powered application that extracts structured information from ID card images using computer vision and natural language processing.

## Features

- Supports multiple ID card types (Passport, Aadhaar, Driving License, PAN Card, Voter ID, etc.)
- Extracts key information like name, age, address, ID number, etc.
- Available in multiple interfaces:
  - Web UI (Streamlit)
  - Command Line Interface
  - Python API

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Web Interface
```bash
streamlit run main_app.py
```

### CLI
```bash
python str_output.py
```

### Environment Variables
Create a `.env` file with:
```
OPENAI_API_KEY=your_api_key_here
```

## Supported ID Types
- Passport
- Aadhaar Card
- Driving License
- PAN Card
- Voter ID
- Company ID
- School ID

## License
MIT
