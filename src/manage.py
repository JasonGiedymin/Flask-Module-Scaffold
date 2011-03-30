import os

from flaskext.script import (Server, Manager)

from myapp import createApp
app = createApp()

manager = Manager(app)

#
# Here the manager should only be concerned with things related to managing.
# Leave the act of loading setting to be done within the app itself.
#
# We do use an environment setting to indicate the server should start in
# debug mode.
#
# Also note that virtualenv is required here.
#
if "MYAPP_DEBUG" not in os.environ or os.environ["MYAPP_DEBUG"] == "FALSE":
    print("Starting server in production mode.")
    print("Use 'fab start_dev_server' to start the dev server.")
    
    manager.add_command("runserver", Server(port=8080, use_reloader=False))
else:
    manager.add_command("runserver", Server(port=8080, use_reloader=True))

if __name__ == "__main__":
    if "VIRTUAL_ENV" not in os.environ:
        print("""
        Virtualenv has not been activated.
        
        Please activate it prior to running manage.py.
        This is for development stability.
        
        Typically you should use fabric to interact with manage.py as
        fabric will activate the environment automatically.
        
        If you would like to manually interact with manage.py please
        activate the environment by 'source'ing the activate file.
        """)
    else:
        manager.run()
