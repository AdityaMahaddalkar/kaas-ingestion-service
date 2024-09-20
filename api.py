import os

from flask import Flask, request, jsonify

from config import Config

app = Flask(__name__)
config = Config().get_config()

temporary_directory_for_file_storage = config['local-storage']['temporary-directory']

os.makedirs(temporary_directory_for_file_storage, exist_ok=True)


@app.route('/ingest', methods=['POST'])
async def upload_files():
    files = request.files.getlist('files')

    if len(files) == 0:
        return jsonify({'error': 'No files were uploaded.'}), 400

    for file in files:
        # Process the file here (e.g., save it to a specific directory)
        file.save(f'{temporary_directory_for_file_storage}/{file.filename}')

    return jsonify({'message': 'Files uploaded successfully.'}), 200


if __name__ == '__main__':
    app.run(debug=True)
