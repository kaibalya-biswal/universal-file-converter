import os
import json
import csv
import xml.etree.ElementTree as ET
from html import unescape
import re

class BaseParser:
    @staticmethod
    def parse(file_path):
        raise NotImplementedError

class TXTParser(BaseParser):
    @staticmethod
    def parse(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

class PDFParser(BaseParser):
    @staticmethod
    def parse(file_path):
        try:
            import PyPDF2
            text = ""
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except ImportError:
            raise ImportError("PyPDF2 is required for PDF parsing. Install it with: pip install PyPDF2")
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")

class DOCXParser(BaseParser):
    @staticmethod
    def parse(file_path):
        try:
            from docx import Document
            doc = Document(file_path)
            text = []
            for para in doc.paragraphs:
                if para.text.strip():
                    text.append(para.text)
            return "\n".join(text)
        except Exception as e:
            raise ValueError(f"Failed to parse DOCX: {str(e)}")

class HTMLParser(BaseParser):
    @staticmethod
    def parse(file_path):
        try:
            from bs4 import BeautifulSoup
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                for script in soup(["script", "style"]):
                    script.decompose()
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks if chunk)
            return text
        except ImportError:
            raise ImportError("BeautifulSoup4 is required for HTML parsing. Install it with: pip install beautifulsoup4")
        except Exception as e:
            raise ValueError(f"Failed to parse HTML: {str(e)}")

class JSONParser(BaseParser):
    @staticmethod
    def parse(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            def extract_text(obj, lines=None):
                if lines is None:
                    lines = []
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        if isinstance(value, (dict, list)):
                            extract_text(value, lines)
                        else:
                            lines.append(str(value))
                elif isinstance(obj, list):
                    for item in obj:
                        extract_text(item, lines)
                else:
                    lines.append(str(obj))
                return lines
            
            text_lines = extract_text(data)
            return "\n".join(text_lines)
        except Exception as e:
            raise ValueError(f"Failed to parse JSON: {str(e)}")

class CSVParser(BaseParser):
    @staticmethod
    def parse(file_path):
        try:
            text_lines = []
            with open(file_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    text_lines.append(" | ".join(row))
            return "\n".join(text_lines)
        except Exception as e:
            raise ValueError(f"Failed to parse CSV: {str(e)}")

class XMLParser(BaseParser):
    @staticmethod
    def parse(file_path):
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            def extract_text(elem):
                text_parts = []
                if elem.text and elem.text.strip():
                    text_parts.append(elem.text.strip())
                for child in elem:
                    text_parts.append(extract_text(child))
                    if child.tail and child.tail.strip():
                        text_parts.append(child.tail.strip())
                return "\n".join(text_parts)
            
            return extract_text(root)
        except Exception as e:
            raise ValueError(f"Failed to parse XML: {str(e)}")

class RTFParser(BaseParser):
    @staticmethod
    def parse(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            text = re.sub(r'\\[a-z]+\d*\s?', '', content)
            text = re.sub(r'\{[^}]*\}', '', text)
            text = text.replace('\\par', '\n')
            text = text.replace('\\tab', '\t')
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'\n\s*\n', '\n', text)
            
            return text.strip()
        except Exception as e:
            raise ValueError(f"Failed to parse RTF: {str(e)}")

class EPUBParser(BaseParser):
    @staticmethod
    def parse(file_path):
        try:
            import ebooklib
            from ebooklib import epub
            from bs4 import BeautifulSoup
            
            book = epub.read_epub(file_path)
            text_parts = []
            
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    for script in soup(["script", "style"]):
                        script.decompose()
                    text = soup.get_text()
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = '\n'.join(chunk for chunk in chunks if chunk)
                    if text.strip():
                        text_parts.append(text)
            
            return "\n\n".join(text_parts)
        except ImportError:
            raise ImportError("BeautifulSoup4 is required for EPUB parsing. Install it with: pip install beautifulsoup4")
        except Exception as e:
            raise ValueError(f"Failed to parse EPUB: {str(e)}")

class ODTParser(BaseParser):
    @staticmethod
    def parse(file_path):
        try:
            from odf.opendocument import load
            from odf.text import P, H
            
            doc = load(file_path)
            text_parts = []
            
            for element in doc.getElementsByType(P):
                text = ""
                for node in element.childNodes:
                    if node.nodeType == 3:
                        text += node.data
                if text.strip():
                    text_parts.append(text)
            
            for element in doc.getElementsByType(H):
                text = ""
                for node in element.childNodes:
                    if node.nodeType == 3:
                        text += node.data
                if text.strip():
                    text_parts.append(text)
            
            return "\n".join(text_parts)
        except Exception as e:
            raise ValueError(f"Failed to parse ODT: {str(e)}")

PARSERS = {
    'txt': TXTParser,
    'pdf': PDFParser,
    'docx': DOCXParser,
    'html': HTMLParser,
    'json': JSONParser,
    'csv': CSVParser,
    'xml': XMLParser,
    'rtf': RTFParser,
    'epub': EPUBParser,
    'odt': ODTParser,
}

def get_parser(file_extension):
    extension = file_extension.lower().lstrip('.')
    parser_class = PARSERS.get(extension)
    if not parser_class:
        raise ValueError(f"Unsupported input format: {extension}")
    return parser_class
