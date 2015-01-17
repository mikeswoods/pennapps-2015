<!DOCTYPE html> 
<html>
  <head>    
    <link rel="stylesheet" href="//assets.ziggeo.com/css/ziggeo-betajs-player.min.css" />
    <script src="//assets.ziggeo.com/js/ziggeo-jquery-json2-betajs-player.min.js"></script>
    <script>ZiggeoApi.token = "ded1df4caa4dfe85e18a82d451df14ad";</script>
  </head>
  <body>
    
    <ziggeo></ziggeo>
    <!-- <ziggeo ziggeo-video="VIDEO_TOKEN_HERE"> -->
    <form action="/upload" method="post" enctype="multipart/form-data">
    Email:      <input type="text" name="email" />
    Select a file: <input type="file" name="upload" />
    <input type="submit" value="Start upload" />
    </form>

  </body>
</html>

<script>ZiggeoApi.Events.on("submitted", function (data) {
  alert("Submitted a new video with token '" + data.video.token + "'!");
});</script>

    