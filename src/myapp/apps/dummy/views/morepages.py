from myapp.apps.dummy import module

@module.route('/template')
def template():
    from flask import render_template
    return render_template("dummy/index.html")

@module.route('/test')
def test():
    return "Test Handler under dummy."