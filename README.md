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

---

While the above was the original scope, the project has mutated heavily. At this 
point, it has a complete web spider and archives entire websites to local storage.
Additionally, multiple versions of each page are kept, with a overall rolling
refresh of the entire database at configurable intervals (configurable on a
per-domain, or global basis).

---

Quick installation overview:

 - Install Postgresql **>= 9.5.** 
 - Build the community extensions for Postgresql.
 - Create a database for the project.
 - In the project database, install the `pg_trgm` and `citext` extensions from the 
    community extensions modules.
 - Copy `settings.example.py` to `settings.py`.
 - Setup virtualhost by running `build-venv.sh`
 - Activate vhost: `source flask/bin/activate`
 - Bootstrap DB: `create_db.sh`
 - Run local fetch RPC server `run_local.sh` from 
 	https://github.com/fake-name/AutoTriever
 - Run server: `python3 run.py`
 - If you want to run the spider, it has a LOT more complicated components:
	 - Main scraper is started by `python runScrape.py`
	 - Scraper periodic scheduler is started by `python runScrape.py scheduler`
	 - The scraper requires substantial RPC infrastructure. You will need:
	 	+ A RabbitMQ instance with a public DNS address
	 	+ A machine running saltstack + salt-master with a public DNS address
	 		On the salt machine, run 
	 		https://github.com/fake-name/AutoTriever/tree/master/marshaller/salt_scheduler.py
	 	+ A variable number of RPC workers to execute fetch tasks. The 
	 		AutoTriever project can be used to manage these.
	 	+ A machine to run the RPC local agent (`run_agent.sh`)
	    The RPC agent allows multiple projects to use the RPC system 
	    simultaneously. Since the RPC system basically allows executing 
	    either predefined jobs, or arbitrary code on the worker swarm. This 
	    is fairly useful in general, so I've implemented it as a service
	    that multiple of my projects then use.
