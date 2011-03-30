from myapp.apps.frontend import module

@module.route('/template')
def template():
    from flask import render_template
    return render_template("frontend/index.html")

@module.route('/test')
def test():
    return "Test Handler under frontend."