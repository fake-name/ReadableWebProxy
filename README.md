## Readable-Web Proxy

Reading long-form content on the internet is a shitty experience.   
This is a web-proxy that tries to make it better.

This is a *rewriting proxy*. In other words, it proxies arbitrary web
content, while allowing the rewriting of the remote content as driven
by a set of rule-files. The goal is to effectively allow the complete
customization of any existing web-sites as driven by predefined rules.

Functionally, it's used for extracting just the actual content body
of a site and reproducing it in a clean layout. It also modifies
all links on the page to point to internal addresses, so following a
link points to the proxied version of the file, rather then the original.