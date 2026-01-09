from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime, timedelta
import threading
import time
import zipfile
import io

from converters import (
    PDFConverter, DOCXConverter, HTMLConverter, JSONConverter,
    CSVConverter, XMLConverter, RTFConverter, EPUBConverter, ODTConverter
)
from converters.parsers import get_parser, PARSERS
from converters.validators import get_file_metadata

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'html', 'json', 'csv', 'xml', 'rtf', 'epub', 'odt'}

converters = {
    'pdf': PDFConverter(),
    'docx': DOCXConverter(),
    'html': HTMLConverter(),
    'json': JSONConverter(),
    'csv': CSVConverter(),
    'xml': XMLConverter(),
    'rtf': RTFConverter(),
    'epub': EPUBConverter(),
    'odt': ODTConverter(),
}

def allowed_file(filename):
    if '.' not in filename:
        return False
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS

def get_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def cleanup_old_files():
    now = datetime.now()
    for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                filepath = os.path.join(folder, filename)
                try:
                    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if now - file_time > timedelta(hours=1):
                        os.remove(filepath)
                except:
                    pass

def cleanup_worker():
    while True:
        time.sleep(3600)
        cleanup_old_files()

cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
cleanup_thread.start()

batch_conversions = {}
conversion_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/formats')
def formats():
    return render_template('formats.html')

@app.route('/how-it-works')
def how_it_works():
    return render_template('how-it-works.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Server is running'})

@app.route('/api/formats', methods=['GET'])
def get_formats():
    formats = [{'id': k, 'name': k.upper(), 'extension': k} for k in converters.keys()]
    return jsonify({'formats': formats})

@app.route('/api/input-formats', methods=['GET'])
def get_input_formats():
    input_formats = [{'id': k, 'name': k.upper(), 'extension': k} for k in PARSERS.keys()]
    return jsonify({'formats': input_formats})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '' or not file.filename:
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': f'Invalid file type. Supported formats: {", ".join(sorted(ALLOWED_EXTENSIONS))}'}), 400
    except Exception as e:
        return jsonify({'error': f'Request error: {str(e)}'}), 400
    
    try:
        original_filename = file.filename
        file_extension = get_file_extension(original_filename)
        
        if not file_extension or file_extension not in ALLOWED_EXTENSIONS:
            return jsonify({'error': f'Invalid file extension. Supported formats: {", ".join(sorted(ALLOWED_EXTENSIONS))}'}), 400
        
        filename = secure_filename(original_filename)
        if not filename:
            filename = f"upload.{file_extension}"
        
        unique_id = str(uuid.uuid4())[:8]
        safe_name = os.path.splitext(filename)[0]
        if not safe_name or safe_name.strip() == '':
            safe_name = "upload"
        else:
            safe_name = "".join(c for c in safe_name if c.isalnum() or c in (' ', '-', '_', '.')).strip()
            if not safe_name:
                safe_name = "upload"
        
        upload_filename = f"{safe_name}_{unique_id}.{file_extension}"
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], upload_filename)
        
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(upload_path)
        
        if not os.path.exists(upload_path):
            return jsonify({'error': 'Failed to save file'}), 500
        
        try:
            parser = get_parser(file_extension)
            content = parser.parse(upload_path)
        except Exception as e:
            if os.path.exists(upload_path):
                os.remove(upload_path)
            return jsonify({'error': f'Failed to parse file: {str(e)}'}), 400
        
        if len(content) == 0:
            os.remove(upload_path)
            return jsonify({'error': 'File is empty or could not extract text'}), 400
        
        metadata = get_file_metadata(upload_path, file_extension)
        
        return jsonify({
            'success': True,
            'file_id': upload_filename,
            'filename': original_filename,
            'size': len(content),
            'metadata': metadata
        })
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/api/convert', methods=['POST'])
def convert_file():
    data = request.get_json()
    
    if not data or 'file_id' not in data or 'format' not in data:
        return jsonify({'error': 'Missing file_id or format'}), 400
    
    file_id = data['file_id']
    format_type = data['format'].lower()
    
    if format_type not in converters:
        return jsonify({'error': f'Unsupported format: {format_type}'}), 400
    
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], file_id)
    
    if not os.path.exists(upload_path):
        return jsonify({'error': 'File not found'}), 404
    
    try:
        file_extension = get_file_extension(file_id)
        parser = get_parser(file_extension)
        content = parser.parse(upload_path)
        
        converter = converters[format_type]
        base_name = os.path.splitext(file_id)[0]
        output_filename = converter.generate_output_filename(base_name, format_type)
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
        
        converter.convert(content, output_path)
        
        history_entry = {
            'id': str(uuid.uuid4()),
            'input_file': file_id,
            'input_filename': os.path.splitext(file_id)[0],
            'input_format': file_extension,
            'output_file': output_filename,
            'output_format': format_type,
            'timestamp': datetime.now().isoformat(),
            'download_url': f'/api/download/{output_filename}'
        }
        conversion_history.append(history_entry)
        
        if len(conversion_history) > 100:
            conversion_history.pop(0)
        
        return jsonify({
            'success': True,
            'output_file': output_filename,
            'download_url': f'/api/download/{output_filename}',
            'history_id': history_entry['id']
        })
    except ValueError as e:
        return jsonify({'error': f'Validation error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500

@app.route('/api/file-info/<file_id>', methods=['GET'])
def get_file_info(file_id):
    file_id = secure_filename(file_id)
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], file_id)
    
    if not os.path.exists(upload_path):
        return jsonify({'error': 'File not found'}), 404
    
    if '..' in file_id or file_id.startswith('/'):
        return jsonify({'error': 'Invalid filename'}), 400
    
    file_extension = get_file_extension(file_id)
    metadata = get_file_metadata(upload_path, file_extension)
    
    return jsonify({'metadata': metadata})

@app.route('/api/history', methods=['GET'])
def get_history():
    return jsonify({
        'success': True,
        'history': conversion_history[-50:]
    })

@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    conversion_history.clear()
    return jsonify({'success': True, 'message': 'History cleared'})

@app.route('/api/batch-upload', methods=['POST'])
def batch_upload():
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files selected'}), 400
    
    batch_id = str(uuid.uuid4())
    uploaded_files = []
    
    for file in files:
        if not allowed_file(file.filename):
            continue
        
        try:
            filename = secure_filename(file.filename)
            file_extension = get_file_extension(filename)
            unique_id = str(uuid.uuid4())[:8]
            safe_name = os.path.splitext(filename)[0]
            safe_name = "".join(c for c in safe_name if c.isalnum() or c in (' ', '-', '_', '.')).strip()
            if not safe_name:
                safe_name = "upload"
            
            upload_filename = f"{safe_name}_{unique_id}.{file_extension}"
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], upload_filename)
            
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(upload_path)
            
            if os.path.exists(upload_path):
                parser = get_parser(file_extension)
                content = parser.parse(upload_path)
                
                if len(content) > 0:
                    metadata = get_file_metadata(upload_path, file_extension)
                    uploaded_files.append({
                        'file_id': upload_filename,
                        'filename': filename,
                        'size': len(content),
                        'metadata': metadata
                    })
        except Exception as e:
            continue
    
    if not uploaded_files:
        return jsonify({'error': 'No valid files uploaded'}), 400
    
    batch_conversions[batch_id] = {
        'files': uploaded_files,
        'created_at': datetime.now().isoformat()
    }
    
    return jsonify({
        'success': True,
        'batch_id': batch_id,
        'files': uploaded_files,
        'count': len(uploaded_files)
    })

@app.route('/api/batch-convert', methods=['POST'])
def batch_convert():
    data = request.get_json()
    
    if not data or 'batch_id' not in data or 'format' not in data:
        return jsonify({'error': 'Missing batch_id or format'}), 400
    
    batch_id = data['batch_id']
    format_type = data['format'].lower()
    
    if batch_id not in batch_conversions:
        return jsonify({'error': 'Batch not found'}), 404
    
    if format_type not in converters:
        return jsonify({'error': f'Unsupported format: {format_type}'}), 400
    
    batch = batch_conversions[batch_id]
    converted_files = []
    
    for file_info in batch['files']:
        try:
            file_id = file_info['file_id']
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], file_id)
            
            if not os.path.exists(upload_path):
                continue
            
            file_extension = get_file_extension(file_id)
            parser = get_parser(file_extension)
            content = parser.parse(upload_path)
            
            converter = converters[format_type]
            base_name = os.path.splitext(file_id)[0]
            output_filename = converter.generate_output_filename(base_name, format_type)
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            
            os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
            converter.convert(content, output_path)
            
            converted_files.append({
                'original_filename': file_info['filename'],
                'output_file': output_filename,
                'download_url': f'/api/download/{output_filename}'
            })
        except Exception as e:
            continue
    
    batch_conversions[batch_id]['converted'] = converted_files
    batch_conversions[batch_id]['format'] = format_type
    
    return jsonify({
        'success': True,
        'batch_id': batch_id,
        'converted_files': converted_files,
        'count': len(converted_files)
    })

@app.route('/api/batch-download/<batch_id>', methods=['GET'])
def batch_download(batch_id):
    if batch_id not in batch_conversions:
        return jsonify({'error': 'Batch not found'}), 404
    
    batch = batch_conversions[batch_id]
    if 'converted' not in batch:
        return jsonify({'error': 'Batch not converted yet'}), 400
    
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_info in batch['converted']:
            file_path = os.path.join(app.config['OUTPUT_FOLDER'], file_info['output_file'])
            if os.path.exists(file_path):
                zf.write(file_path, file_info['output_file'])
    
    memory_file.seek(0)
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'converted_files_{batch_id[:8]}.zip'
    )

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    filename = secure_filename(filename)
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    if '..' in filename or filename.startswith('/'):
        return jsonify({'error': 'Invalid filename'}), 400
    
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
