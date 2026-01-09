from .base import BaseConverter
import html

class HTMLConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['html']
    
    def convert(self, input_text, output_path, options=None):
        self.validate_input(input_text)
        self.ensure_output_dir(output_path)
        
        escaped_text = html.escape(input_text)
        lines = escaped_text.split('\n')
        html_lines = ['<p>' + line + '</p>' if line.strip() else '<br/>' for line in lines]
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Converted Document</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            line-height: 1.6;
        }}
    </style>
</head>
<body>
{''.join(html_lines)}
</body>
</html>"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
