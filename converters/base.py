from abc import ABC, abstractmethod
import os
import uuid

class BaseConverter(ABC):
    def __init__(self):
        self.supported_extensions = []
    
    @abstractmethod
    def convert(self, input_text, output_path, options=None):
        pass
    
    def validate_input(self, input_text):
        if not input_text or not isinstance(input_text, str):
            raise ValueError("Input text must be a non-empty string")
        return True
    
    def ensure_output_dir(self, output_path):
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
    
    def generate_output_filename(self, base_name, extension):
        safe_name = "".join(c for c in base_name if c.isalnum() or c in (' ', '-', '_', '.')).strip()
        if not safe_name:
            safe_name = "converted"
        unique_id = str(uuid.uuid4())[:8]
        return f"{safe_name}_{unique_id}.{extension}"
