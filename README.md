# Universal File Converter

A modern, web-based file converter that allows you to convert files between multiple formats instantly. Built with Flask and vanilla JavaScript.

## Features

- 🔄 **10+ Format Support**: Convert between TXT, PDF, DOCX, HTML, JSON, CSV, XML, RTF, EPUB, and ODT
- ⚡ **Bidirectional Conversion**: Convert files in both directions (e.g., PDF to DOCX, DOCX to PDF)
- 📦 **Batch Processing**: Upload and convert multiple files simultaneously
- 🔒 **Secure & Private**: Files are automatically deleted after 1 hour
- 📊 **File Validation**: Get detailed metadata about your files
- 📜 **Conversion History**: Track your conversion history
- 🌙 **Dark Mode**: Beautiful dark theme with network visualization
- 📱 **Responsive Design**: Works seamlessly on mobile, tablet, and desktop

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Libraries**: reportlab, python-docx, PyPDF2, beautifulsoup4, ebooklib, odfpy

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kaibalya-biswal/universal-file-converter.git
cd universal-file-converter
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

1. **Upload a file**: Drag and drop or click to browse
2. **Select output format**: Choose from 9 supported formats
3. **Convert**: Click the convert button
4. **Download**: Download your converted file

## Supported Formats

### Input Formats
- TXT, PDF, DOCX, HTML, JSON, CSV, XML, RTF, EPUB, ODT

### Output Formats
- PDF, DOCX, HTML, JSON, CSV, XML, RTF, EPUB, ODT

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

Recommended platforms:
- Railway
- Render
- Heroku
- PythonAnywhere

## Project Structure

```
Converter/
├── app.py                 # Main Flask application
├── converters/            # Conversion modules
│   ├── base.py           # Base converter class
│   ├── parsers.py        # Input file parsers
│   ├── validators.py     # File metadata validators
│   └── *.py              # Format-specific converters
├── templates/            # HTML templates
├── static/              # CSS and JavaScript files
├── requirements.txt     # Python dependencies
└── Procfile            # Deployment configuration
```

## Features in Detail

### Batch Conversion
Upload multiple files and convert them all to the same format. Download individually or as a ZIP file.

### File Validation
Get detailed information about your files including:
- Character count
- Word count
- Line count
- Page count (for PDFs)
- Row count (for CSVs)

### Conversion History
Track all your conversions with timestamps and easy re-download options.

## Security

- All files are automatically deleted after 1 hour
- No permanent storage of file contents
- Secure file handling with validation
- Input sanitization

## Limitations

- Maximum file size: 16MB per file
- Files are stored temporarily (1 hour)
- Some complex formatting may not be preserved perfectly

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

**Kaibalya Biswal**
- Email: kaibalyabiswal77@gmail.com
- GitHub: [@kaibalya-biswal](https://github.com/kaibalya-biswal)

## Acknowledgments

Built with modern web technologies and best practices for file conversion and user experience.
