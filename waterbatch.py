import os
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from uuid import uuid4

from modules.utils import remove_folder, create_folder, zip_content_in_folder

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/', methods=['GET'])
def home():
  return render_template('hello.html')


@app.route('/watermark', methods=['POST'])
def watermark_images():
  print('POST at %s' % request.path)

  # create single use folder
  upload_folder = '%s/%s' % (app.config['UPLOAD_FOLDER'], uuid4())
  create_folder(upload_folder)

  # fetch uploaded photos
  photos = request.files.getlist('photos')
  watermark = request.files.get('watermark')
  position = request.form.get('position')

  # save files
  watermark_path = os.path.join(upload_folder, secure_filename(watermark.filename))
  watermark.save(watermark_path)
  for photo in photos:
    photo_path = os.path.join(upload_folder, secure_filename(photo.filename))
    photo.save(photo_path)

  # zip files
  data = zip_content_in_folder(upload_folder)

  # delete single use folder and uploaded files
  remove_folder(upload_folder)

  # send zipped files
  return send_file(
    data,
    mimetype='application/zip',
    as_attachment=True,
    attachment_filename='waterbatch.zip'
  )
  
  # return redirect(url_for('home'))
