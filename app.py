from flask import Flask, request, render_template, send_from_directory
from spleeter.separator import Separator
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return "Tidak ada file"
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        separator = Separator('spleeter:2stems')
        separator.separate_to_file(filepath, OUTPUT_FOLDER)

        result_folder = os.path.join(OUTPUT_FOLDER, filename.split('.')[0])
        return send_from_directory(result_folder, 'accompaniment.wav', as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    app.run(debug=True)
