import os
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from uuid import uuid4

from modules.utils import remove_folder, create_folder, zip_content_in_folder
from modules.watermark import watermark

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOWNLOADS_FOLDER'] = 'downloads'


@app.route('/', methods=['GET'])
def home():
  return render_template('hello.html')


@app.route('/watermark', methods=['POST'])
def watermark_images():
  print('POST at %s' % request.path)

  # create single use folder
  watermark_id = uuid4()
  upload_folder = '%s/%s' % (app.config['UPLOAD_FOLDER'], watermark_id)
  downloads_folder = '%s/%s' % (app.config['DOWNLOADS_FOLDER'], watermark_id)
  create_folder(upload_folder)
  create_folder(downloads_folder)

  # fetch uploaded photos
  photos = request.files.getlist('photos')
  water_mark = request.files.get('watermark')
  position = request.form.get('position')

  # save files
  water_mark_path = os.path.join(upload_folder, secure_filename(water_mark.filename))
  water_mark.save(water_mark_path)
  for photo in photos:
    photo_path = os.path.join(upload_folder, secure_filename(photo.filename))
    photo.save(photo_path)

  # watermark
  watermark(upload_folder, (secure_filename(photo.filename) for photo in photos), water_mark_path, position, downloads_folder)
  remove_folder(upload_folder)

  # zip files
  data = zip_content_in_folder(downloads_folder)

  # delete single use folder and uploaded files
  remove_folder(downloads_folder)

  # send zipped files
  return send_file(
    data,
    mimetype='application/zip',
    as_attachment=True,
    attachment_filename='waterbatch.zip'
  )
  
  # return redirect(url_for('home'))
