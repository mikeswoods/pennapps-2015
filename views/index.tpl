<!DOCTYPE html> 
<html>
  <head>    
    <link rel="stylesheet" href="//assets.ziggeo.com/css/ziggeo-betajs-player.min.css" />
    <script src="//assets.ziggeo.com/js/ziggeo-jquery-json2-betajs-player.min.js"></script>
    <link rel="stylesheet" href="./static/css/foundation.css" />
    <link rel="stylesheet" href="./static/css/emojifythis.css" />
    <script src="/static/js/vendor/modernizr.js"></script>
    <script src="/static/js/isotope.pkgd.min.js"></script>
    <script>ZiggeoApi.token = "ded1df4caa4dfe85e18a82d451df14ad";</script>
  </head>
  <body>
    <nav class="top-bar" data-topbar role="navigation">
      <ul class="title-area">
        <li class="name">
          <h1><a href="#">Emojify This!</a></h1>
        </li>
        <li class="toggle-topbar menu-icon"><a href="#"><span>Menu</span></a></li>
      </ul>
    </nav>
    <form action="/upload" method="post" enctype="multipart/form-data">
      <div class="row">
        <div class="large-8 large-offset-2 columns">
          <label>Email<input type="text" name="email" placeholder="Email"/></label>
        </div>
      </div>
      <div class="row">
        <div class="large-8 large-offset-2 columns">
          <label>Select a file<input type="file" name="upload" /></label>
        </div>
      </div>
      <div class="row or">
        <span><label>or</label></span>
      </div>
      <div class="row">
        <div class="large-8 large-offset-2 columns">
          <label>Emojify Yourself!<ziggeo ziggeo-input_bind='videotoken' ></ziggeo></label>
        </div>
      </div>

      <div class="row">
        <br>
        <input class="button large-8 large-offset-2" type="submit" value="Start upload" />
    </form>
  
  <div class="row">
    <div id="container">
    %for i in images:
      % if i[1][:3] != "mp4":
        % oldf = i[1][1:]
        <div class="item"><img src="{{oldf}}"></div>
        % if i[3]:
          % newf = i[3][1:]
          <div class="item"><img src="{{newf}}"></div>
  </div>

  </body>
  <script>
  var $container = $('#container');
  // init
  $container.isotope({
    // options
    itemSelector: '.item',
    layoutMode: 'fitRows'
  });
  </script>
</html>

