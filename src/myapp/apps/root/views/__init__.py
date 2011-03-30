from myapp.apps.root import module

@module.route('/hello')
def index():
    return "Hello World from under root subapp/module!"