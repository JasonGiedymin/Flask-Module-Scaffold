from flaskext.assets import Bundle

frontend_css = Bundle (
    # core css
    Bundle("frontend/style.css"),
    # Chain additional css groups here
    # additional css
    #Bundle(...),
    # even more css
    #Bundle(...),
    
    filter="cssmin",
    output="frontend/combine.css")
    
