from myapp.apps.root import module

@module.route('/root-template')
def template():
    from flask import render_template
    return render_template("index.html")
