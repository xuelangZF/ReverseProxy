This is a tiny [Reverse Proxy](https://en.wikipedia.org/wiki/Reverse_proxy) implement.  It taking requests from the Internet and forwarding them to real servers in network. Those making requests to the proxy may not be aware of the real network.

![Reverse Proxy](https://upload.wikimedia.org/wikipedia/commons/6/67/Reverse_proxy_h2g2bob.svg)

Reverse proxies can hide the existence and characteristics of an origin server or servers.  So we can bypass the Great Fire Wall to visit some blocked site.

# Main Feature

Feature available:

* Forward all the client's `GET` request to the backstage server.
* Change the response's content, move all the page's needed resource to the reverse server.
* Cache the pages for some custom expiry time in proxy server.

# How To Run

Firstly, you need to specify the domain and port used to act as a proxy and another domain and port from which we get the response.   All the config locates at `setting.conf`, and you just need to change the value.

Here is the demo setting,  when someone visits aaa.com, he actually visits v2ex.com.

    # All the configure of flask and reverse domain lists are put here.
    [flask]
    secret_key = 12345678!@#$%^&
    
    # Reverse Server domain = Proxy Domain
    [domain]
    server_domain = aaa.com
    server_port = 5000
    proxy_domain = v2ex.com
    proxy_port = 80
    
    [time]
    html_expired = 6400
    js_css_expired = 2592000
    img_expired = 2592000
    common_expired = 2592000

Then you can run the server simply using the following command:

    python manage.py runserver

Or in real product environment, you may need [gunicorn](http://gunicorn.org/) to manage the program.  Then you can start the service as follows:

    gunicorn manage:app runserver -b 0.0.0.0:5000

Make sure the program run at the port that we specify in setting.conf.

Once service starts, you can visit the `server_domain:server_port` in browser,  it may looks like:

![ReverseProxy][1]

If you can't access the site, you'd better check the DNS setting.  If you have not any domain available, you can also modify `hosts` to run the program on local machine.  If the proxy_domain has sub-domain, you need add the subdomain item to hosts too.

For example, if you want to make a proxy for `hupu.com` and its sub-domain: `soccer.hupu.com`, you need to add the following item to hosts:

    127.0.0.1 hupu.com
    127.0.0.1 soccer.hupu.com
 
If there are many sub-domains, you need to add them  one by one, because we can't use wildcard character in hosts.  Once you modify the hosts, you'd better refresh the system DNS cache.


[1]: http://o7l04issy.bkt.clouddn.com/ReverseProxy.png


