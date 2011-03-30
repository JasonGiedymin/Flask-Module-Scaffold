import os
import sys

from flask import Flask

from myapp import settings

def _createFlaskApp(debug = False):
	'''
	It is important to retain debug information here as this init could
	be called without a 'Flask Script' Manager bootstrapping the app.
	'''

	app = Flask(settings.APP_NAME)

	if debug:
			app.config.from_object("myapp.configs.DevelopmentConfig")
	else:
			app.config.from_object("myapp.configs.ProductionConfig")

	return app

def _registerDebugToolbar(app):
    '''
    Look into using https://github.com/mvantellingen/flask-debugtoolbar/ for your project.
    NOTE: You will need trunk, pypi is out of date at the moment and not able to handle modules
    '''

	#toolbar = DebugToolbarExtension(app)
    pass

def _registerAssets(app):
    '''
    Look into using https://github.com/miracle2k/flask-assets/ for your project
    '''

	#assets = Environment(app)

	#from myapp.apps.frontend.assets import frontend_css
	#assets.register("frontend_css", frontend_css)

    pass

def _registerApps(app):
    '''
	Dynamic Loading:
		Add an entry to "APPS" in settings.py.
		Note: 
			url_prefix and subdomain params should be handled in the respecting
			sub application (where module is kept). 
	
	Manual Loading:
		from myapp.apps.frontend.views import frontend_module
		app.register_module(frontend_module, url_prefix='/frontend')
		
		Setting of the url_prefix and subdomain params here will override
		the values set in the sub application module.
		
		Examples:
		
			app.register_module(app_module.module, url_prefix=app_prefix)
			app.register_module(app_module.module, subdomain=app_name)
			app.register_module(app_module.module, url_prefix=app_prefix, subdomain=app_name) 
    '''

    for app_name in settings.APPS:
        fq_app_name = ("myapp.apps.%s" % app_name) #TODO: dump myapp from settings
        app_module = __import__((fq_app_name), globals(), locals(), [ ("%s_module" % app_name) ])

        if hasattr(app_module, "module"):
            app.register_module(app_module.module)
        else:
            print("Missing attribute! Python object [%s.module] does not exist. Not registering app!" % fq_app_name)            

def createApp():
	if "MYAPP_DEBUG" not in os.environ or os.environ["MYAPP_DEBUG"] == "FALSE":
			app = _createFlaskApp()
	else:
			app = _createFlaskApp(True)

	_registerDebugToolbar(app)
	_registerAssets(app)
	_registerApps(app)

	return app

