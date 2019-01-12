# custom-ipv4-dns-server
Custom-IPv4-DNS Server

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
