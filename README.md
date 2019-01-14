# custom-dns-server (Custom DNS Proxy, IPv4 only)
Custom DNS Server (IPv4 only)

This is a Custom DNS server. (IPv4 only)

I personally created it for testing mobile phone apps.

I wanted to make it possible for the app to connect to a specific IP address on my mobile phone.

By using this custom DNS server, I was able to connect a specific domain to a specific IP (my personal web server in my case).



Python 3.6

1. Add the domain and address you want to the source. (dns3.py)

2. Of the "CustomDNSResolver" class Modify the variable "customDomainDictionary".
<pre>
  ex)
      'mydomain.co.kr': &lt;YOUR_IPv4_ADDRESS&gt;,
      'mydomain.co.kr': '192.168.0.201',
      'yourdomain.co.kr': '192.168.0.205',
</pre>

3. Start the Custom-IPv4-DNS server.
<pre>
  usage: 
      python.exe dns3.py
</pre>
  
4. Test at Windows Command Prompt
<pre>
  c:\&gt; nslookup mydomain.co.kr 127.0.0.1
    Server:    UnKnown
    Address:  127.0.0.1

    Name:    mydomain.co.kr
    Addresses:  192.168.0.201
              192.168.0.201
</pre>


Enjoy.
