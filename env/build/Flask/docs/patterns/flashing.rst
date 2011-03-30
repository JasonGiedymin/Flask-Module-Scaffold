.. _message-flashing-pattern:

Message Flashing
================

Good applications and user interfaces are all about feedback.  If the user
does not get enough feedback he will probably end up hating the
application.  Flask provides a really simple way to give feedback to a
user with the flashing system.  The flashing system basically makes it
possible to record a message at the end of a request and access it next
request and only next request.  This is usually combined with a layout
template that does this.

Simple Flashing
---------------

So here a full example::

    from flask import flash, redirect, url_for, render_template

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        error = None
        if request.method == 'POST':
            if request.form['username'] != 'admin' or \
               request.form['password'] != 'secret':
                error = 'Invalid credentials'
            else:
                flash('You were sucessfully logged in')
                return redirect(url_for('index'))
        return render_template('login.html', error=error)

And here the ``layout.html`` template which does the magic:

.. sourcecode:: html+jinja

   <!doctype html>
   <title>My Application</title>
   {% with messages = get_flashed_messages() %}
     {% if messages %}
       <ul class=flashes>
       {% for message in messages %}
         <li>{{ message }}</li>
       {% endfor %}
       </ul>
     {% endif %}
   {% endwith %}
   {% block body %}{% endblock %}

And here the index.html template:

.. sourcecode:: html+jinja

   {% extends "layout.html" %}
   {% block body %}
     <h1>Overview</h1>
     <p>Do you want to <a href="{{ url_for('login') }}">log in?</a>
   {% endblock %}

And of course the login template:

.. sourcecode:: html+jinja

   {% extends "layout.html" %}
   {% block body %}
     <h1>Login</h1>
     {% if error %}
       <p class=error><strong>Error:</strong> {{ error }}
     {% endif %}
     <form action="" method=post>
       <dl>
         <dt>Username:
         <dd><input type=text name=username value="{{
             request.form.username }}">
         <dt>Password:
         <dd><input type=password name=password>
       </dl>
       <p><input type=submit value=Login>
     </form>
   {% endblock %}

Flashing With Categories
------------------------

.. versionadded:: 0.3

It is also possible to provide categories when flashing a message.  The
default category if nothing is provided is ``'message'``.  Alternative
categories can be used to give the user better feedback.  For example
error messages could be displayed with a red background.

To flash a message with a different category, just use the second argument
to the :func:`~flask.flash` function::

    flash(u'Invalid password provided', 'error')

Inside the template you then have to tell the
:func:`~flask.get_flashed_messages` function to also return the
categories.  The loop looks slighty different in that situation then:

.. sourcecode:: html+jinja

   {% with messages = get_flashed_messages(with_categories=true) %}
     {% if messages %}
       <ul class=flashes>
       {% for category, message in messages %}
         <li class="{{ category }}">{{ message }}</li>
       {% endfor %}
       </ul>
     {% endif %}
   {% endwith %}

This is just one example of how to render these flashed messages.  One
might also use the category to add a prefix such as
``<strong>Error:</strong>`` to the message.
