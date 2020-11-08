"""Plotly Dash HTML layout override."""

html_layout = '''
<!DOCTYPE html>
<html>
  <head>
    {%metas%} {%favicon%} {%css%}
    <meta charset="UTF-8" />
    <title>Drizzle Technologies</title>
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css"
      integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2"
      crossorigin="anonymous"
    />
  </head>
  <body class="plotlydash-template">
    <header>
      <nav class="navbar navbar-expand-lg navbar-dark py-4 standard-background">
        <div class='container'>
          <a class="navbar-brand" href="#"
            >
            <h1 class="mb-0 nav-title">
              Drizzle Technologies
            </h1>
          </a
          >
          <button
            class="navbar-toggler"
            type="button"
            data-toggle="collapse"
            data-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse justify-content-end" id="navbarSupportedContent">
            <ul class="navbar-nav">
              <li class="nav-item">
                <a class="nav-link" href="/dashboard">Entrar</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>
    <main class="container mt-5 min-height-dash-main">
        {%app_entry%}
    </main>
    <footer class="d-flex align-items-center navbar-dark standard-background mt-5">
        <div class="index-footer py-3">
            <div class="footer-links">
                <a href="https://github.com/joao-fb/inteng33" target="_blank">Contribua no GitHub!</a>
            </div>
            <copyright class="footer-links">
                <a href="http://opensource.org/licenses/mit-license.php">Copyright 2020 © Grupo 33 - Int. Eng. Ele. MIT License</a>
            </copyright>
        </div>
        {%config%} {%scripts%} {%renderer%}
    </footer>
  </body>
  <script
    src="https://code.jquery.com/jquery-3.5.1.slim.min.js"
    integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj"
    crossorigin="anonymous"
  ></script>
  <script
    src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js"
    integrity="sha384-ho+j7jyWK8fNQe+A12Hb8AhRq26LrZ/JpcUGGOn+Y7RsweNrtN/tE3MoK7ZeZDyx"
    crossorigin="anonymous"
  ></script>
</html>
'''
