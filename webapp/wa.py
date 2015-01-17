import os
from bottle import route, request, static_file, run

@route('/upload', method='POST')
def do_upload():
    email = request.forms.get('email')
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png', '.jpg', '.jpeg'):
        return "File extension not allowed."

    save_path = "/Users/stuwagsmac/pennapps/pennapps-2015/webapp/static"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
    upload.save(file_path)
    return "File successfully saved to '{0}'.".format(save_path)

@route('/static/<filename>')
def server_static(filename):
  return static_file(filename,root='/Users/stuwagsmac/pennapps/pennapps-2015/webapp/static')

@route('/static/stuwags@gmail.com/<filename>')
def server_static(filename):
  return static_file(filename,root='/Users/stuwagsmac/pennapps/pennapps-2015/webapp/static')

@route('/')
def index():
	doc = """
	<!DOCTYPE html> <html>
	<head>
  <p>Enter your email address</p>
  <script>
  var email = document.createElement("INPUT");
  x.setAttribute("type", "text");
  x.setAttribute("value", "Enter your email address.");
  document.body.appendChild(x);
  </script>
	<link rel="stylesheet" href="//assets.ziggeo.com/css/ziggeo-betajs-player.min.css" />
	<script src="//assets.ziggeo.com/js/ziggeo-jquery-json2-betajs-player.min.js"></script>
	<script>ZiggeoApi.token = "ded1df4caa4dfe85e18a82d451df14ad";</script>
    </head>
    <body>
	<ziggeo></ziggeo>
	<!-- <ziggeo ziggeo-video="VIDEO_TOKEN_HERE"> -->
    </body>
   	</html>

  <script>ZiggeoApi.Events.on("submitted", function (data) {
	alert("Submitted a new video with token '" + data.video.token + "'!");
  });</script>

	<form action="/upload" method="post" enctype="multipart/form-data">
  	Email:      <input type="text" name="email" />
  	Select a file: <input type="file" name="upload" />
  	<input type="submit" value="Start upload" />
	</form>
		"""
	return doc




run(host='localhost', port=8080, debug=True)