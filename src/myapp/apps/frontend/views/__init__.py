from myapp.apps.frontend import module

@module.route('/')
def index():
    return "Index Handler under frontend."