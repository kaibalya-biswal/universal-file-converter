from .base import BaseConverter
import csv

class CSVConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['csv']
    
    def convert(self, input_text, output_path, options=None):
        self.validate_input(input_text)
        self.ensure_output_dir(output_path)
        
        lines = input_text.split('\n')
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Line Number', 'Content'])
            for idx, line in enumerate(lines, start=1):
                writer.writerow([idx, line])
        
        return output_path
