import os

from flask import Flask, request, jsonify

from constants import TEMPORARY_DOCUMENTS_STORAGE_DIRECTORY

app = Flask(__name__)

os.makedirs(TEMPORARY_DOCUMENTS_STORAGE_DIRECTORY, exist_ok=True)


@app.route('/ingest', methods=['POST'])
async def upload_files():
    files = request.files.getlist('files')

    if len(files) == 0:
        return jsonify({'error': 'No files were uploaded.'}), 400

    for file in files:
        # Process the file here (e.g., save it to a specific directory)
        file.save(f'{TEMPORARY_DOCUMENTS_STORAGE_DIRECTORY}/{file.filename}')

    return jsonify({'message': 'Files uploaded successfully.'}), 200


if __name__ == '__main__':
    app.run(debug=True)
