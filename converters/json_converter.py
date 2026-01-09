from .base import BaseConverter
import json

class JSONConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['json']
    
    def convert(self, input_text, output_path, options=None):
        self.validate_input(input_text)
        self.ensure_output_dir(output_path)
        
        lines = [line for line in input_text.split('\n') if line.strip()]
        
        data = {
            'content': input_text,
            'lines': lines,
            'line_count': len(lines),
            'character_count': len(input_text)
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return output_path
