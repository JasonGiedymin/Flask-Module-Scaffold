FastCGI
=======

A very popular deployment setup on servers like `lighttpd`_ and `nginx`_
is FastCGI.  To use your WSGI application with any of them you will need
a FastCGI server first.

The most popular one is `flup`_ which we will use for this guide.  Make
sure to have it installed.

.. admonition:: Watch Out

   Please make sure in advance that your ``app.run()`` call you might
   have in your application file, is inside an ``if __name__ ==
   '__main__':`` or moved to a separate file.  Just make sure it's not
   called because this will always start a local WSGI server which we do
   not want if we deploy that application to FastCGI.

Creating a `.fcgi` file
-----------------------

First you need to create the FastCGI server file.  Let's call it
`yourapplication.fcgi`::

    #!/usr/bin/python
    from flup.server.fcgi import WSGIServer
    from yourapplication import app

    WSGIServer(app).run()

This is enough for Apache to work, however lighttpd and nginx need a
socket to communicate with the FastCGI server.  For that to work you
need to pass the path to the socket to the
:class:`~flup.server.fcgi.WSGIServer`::

    WSGIServer(application, bindAddress='/path/to/fcgi.sock').run()

The path has to be the exact same path you define in the server
config.

Save the `yourapplication.fcgi` file somewhere you will find it again.
It makes sense to have that in `/var/www/yourapplication` or something
similar.

Make sure to set the executable bit on that file so that the servers
can execute it:

.. sourcecode:: text

    # chmod +x /var/www/yourapplication/yourapplication.fcgi

Configuring lighttpd
--------------------

A basic FastCGI configuration for lighttpd looks like that::

    fastcgi.server = ("/yourapplication" =>
        "yourapplication" => (
            "socket" => "/tmp/yourapplication-fcgi.sock",
            "bin-path" => "/var/www/yourapplication/yourapplication.fcgi",
            "check-local" => "disable"
        )
    )

This configuration binds the application to `/yourapplication`.  If you
want the application to work in the URL root you have to work around a
lighttpd bug with the :class:`~werkzeug.contrib.fixers.LighttpdCGIRootFix`
middleware.

Make sure to apply it only if you are mounting the application the URL
root.

Configuring nginx
-----------------

Installing FastCGI applications on nginx is a bit different because by default
no FastCGI parameters are forwarded.

A basic flask FastCGI configuration for nginx looks like this::

    location = /yourapplication { rewrite ^ /yourapplication/ last; }
    location /yourapplication { try_files $uri @yourapplication; }
    location @yourapplication {
        include fastcgi_params;
	fastcgi_split_path_info ^(/yourapplication)(.*)$;
        fastcgi_param PATH_INFO $fastcgi_path_info;
        fastcgi_param SCRIPT_NAME $fastcgi_script_name;
        fastcgi_pass unix:/tmp/yourapplication-fcgi.sock;
    }

This configuration binds the application to `/yourapplication`.  If you want
to have it in the URL root it's a bit simpler because you don't have to figure
out how to calculate `PATH_INFO` and `SCRIPT_NAME`::

    location / { try_files $uri @yourapplication; }
    location @yourapplication {
        include fastcgi_params;
        fastcgi_param PATH_INFO $fastcgi_script_name;
        fastcgi_param SCRIPT_NAME "";
        fastcgi_pass unix:/tmp/yourapplication-fcgi.sock;
    }

Since Nginx doesn't load FastCGI apps, you have to do it by yourself.  You
can either write an `init.d` script for that or execute it inside a screen
session::

    $ screen
    $ /var/www/yourapplication/yourapplication.fcgi

Debugging
---------

FastCGI deployments tend to be hard to debug on most webservers.  Very often the
only thing the server log tells you is something along the lines of "premature
end of headers".  In order to debug the application the only thing that can
really give you ideas why it breaks is switching to the correct user and
executing the application by hand.

This example assumes your application is called `application.fcgi` and that your
webserver user is `www-data`::

    $ su www-data
    $ cd /var/www/yourapplication
    $ python application.fcgi
    Traceback (most recent call last):
      File "yourapplication.fcg", line 4, in <module>
    ImportError: No module named yourapplication

In this case the error seems to be "yourapplication" not being on the python
path.  Common problems are:

-   relative paths being used.  Don't rely on the current working directory
-   the code depending on environment variables that are not set by the
    web server.
-   different python interpreters being used.

.. _lighttpd: http://www.lighttpd.net/
.. _nginx: http://nginx.net/
.. _flup: http://trac.saddi.com/flup
