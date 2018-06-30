Nginx configuration
-------------------

1. Install Nginx:

    ::

        $ sudo apt-get install nginx

2. And then create the file ``/etc/nginx/sites-available/pih2o.conf`` with the following content:

    ::

        server {
            listen 80;
            server_name pih2o.com;

            root /path/to/pih2o;

            access_log /path/to/pih2o/access.log;
            error_log /path/to/pih2o/error.log;

            location /pih2o {
                proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
                proxy_set_header Host $http_host;
                proxy_redirect off;
                if (!-f $request_filename) {
                    proxy_pass http://127.0.0.1:5000;
                    break;
                }
            }
        }

3. Enable the site:

    ::

        $ sudo ln -s /etc/nginx/sites-available/pih2o.conf /etc/nginx/sites-enabled/

4. Remove default Nginx configuration:

   ::

        $ sudo rm /etc/nginx/sites-available/default

5. Check the configuration:

    ::

        $ sudo nginx -t


6. Reload the Nginx service:

    ::

        $ sudo service nginx reload
