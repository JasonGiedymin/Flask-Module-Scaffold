from myapp.apps.dummy import module

@module.route('/')
def index():
    return "Index Handler under dummy."