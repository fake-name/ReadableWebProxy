
Overall data-flow:

+----------+   +----------------------+   +-------------------+
| Database +-->+                      +-->+                   |
+----^-----+   |   Retreive task.     |   |  Retreive remote  |
     |         |   Filter by          |   |  resource         |
     |         |    * Priority        |   |                   |
     |         |    * Task source     |   +--------+----------+
     |         |    * Predicted       |            |           
     |         |       content-Type   |            |           
     |         |                      |            v           
     |         +----------------------+   +--------+----------+
     |         +----------------------+   |                   |
     |         |                      |   |  Process          |
     |         |  Generate update     |   |  retrieved        |
     +---------+  based on processed  +<--+  content using    |
               |  content.            |   |  plugin LUT       |
               |                      |   |                   |
               +----------------------+   +---------+---------+
                                                    ^          
                                                    |          
                                            +-------+------+   
                                            |              |   
                                            |   Build      |   
                                            |   Plugin     |   
                                            |    LUT       |   
                                            |              |   
                                            +------+-------+   
                                                   ^           
                                                   |           
                                                   |           
                                            +------+--------+   
                                            |               |   
                                            |    Plugin     |   
                                            |  Definitions  |   
                                            |               |   
                                            +---------------+   

Crawl limit is 1000000.
Shallow updates can be achived by upserting entries close to the limit. E.g. 
a distance limit of 2 can be achieved by upserting a url with a starting crawl 
distance of 999998.

Required directives:
 - badwords
 - decompose
 - baseUrl

Allowed directives:
 - feeds
 - feedPostfix
 - stripTitle
 - decomposeBefore
 - tld
 - baseUrl
 - FOLLOW_GOOGLE_LINKS
 - allImages
 - cloudflare
 - fileDomains

Planned directives:
 - TagReplace
 - TitleReplace

Ignored directives:
 - positive_keywords
 - negative_keywords

Disallowed directives:
 - wg
 - threads
 - startUrl
 - tableKey
 - pluginName
 - loggerPath