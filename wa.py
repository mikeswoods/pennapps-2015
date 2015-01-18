import os, sqlite3
from bottle import Bottle, route, request, static_file, run, template, SimpleTemplate, static_file, default_app

indexTemplate = SimpleTemplate(name='views/index.tpl')

app = Bottle()

SimpleTemplate.defaults["get_url"] = app.get_url

@app.route('/upload', method='POST')
def do_upload():
    email = request.forms.get('email')
    print request.forms.get('videotoken')
    if request.forms.get('videotoken'):
      videotoken = request.forms.get('videotoken')
      
      upload = ziggeo.videos().download_video(videotoken)

      save_path = "./static"
      if not os.path.exists(save_path):
        os.makedirs(save_path)
      file_path = "{path}/{email}_{videotoken}.mp4".format(path=save_path, email=email,videotoken=videotoken)
      with open(file_path,'w') as f:
        f.write(upload)

    else:
      upload = request.files.get('upload')
      name, ext = os.path.splitext(upload.filename)
      if ext not in ('.png', '.jpg', '.jpeg','.mp4'):
        return "File extension not allowed."

      save_path = "./static"
      if not os.path.exists(save_path):
        os.makedirs(save_path)

      file_path = "{path}/{email}_{file}".format(path=save_path, email=email, file=upload.filename)
      upload.save(file_path)

    db = sqlite3.connect('image.db')
    c = db.cursor()
    c.execute("INSERT INTO images (original, email) VALUES (?,?)",(file_path,email))
    db.commit()
    c.close()

    return "File successfully saved to '{0}'.".format(save_path)

@app.route('/static/<filename>', name='static')
def server_static(filename):
  return static_file(filename,root='./static')

@app.route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

@app.route('/',name='root')
def index():
	db = sqlite3.connect('image.db')
  	c = db.cursor()
  	c.execute("SELECT * FROM images")
  	images = c.fetchall()
  	return template('index',images=images)

@app.route('/<email>')
def show_images(email):
  db = sqlite3.connect('image.db')
  c = db.cursor()
  c.execute("SELECT * FROM images WHERE email=?",(email,))
  images = c.fetchall()
  return template('images',images = images, get_url = app.get_url)



#app.run(host='localhost', port=8080, debug=True)
