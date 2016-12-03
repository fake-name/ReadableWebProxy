
Overall data-flow:


+--------------+
|              |
|  Scheduled   |
|   trigger    +---------------------------------------------------+
|    system    |                                                   |
|              |                                                   |
+----+---------+                                                   |
     |                                                             |
+----v-----+   +----------------------+   +-------------------+    |
| Database +-->+                      +-->+                   |    |
+----^-----+   |   Retreive task.     |   |  Retreive remote  |    |
     |         |   Filter by          |   |  resource         |    |
     |         |    * Priority        |   |                   |    |    
     |         |    * Task source     |   +--------+----------+    |    +----------------------+
     |         |    * Predicted       |            |               |    | Raw filter           |
     |         |       content-Type   |            +---------------|--->+ plugins & parasitic  |
     |         |                      |            v               |    | export feeds         |
     |         +----------------------+   +--------+----------+    |    +----+-----------------+
     |         +----------------------+   |                   |    |         V
     |         |                      |   |  Process          |    |    +----+-------------+
     |         |  Generate update     |   |  retrieved        |    |    |    WLNUpdates    |
     +--(-)----+  based on processed  +<--+  content using    |    |    | Release parsing  |
         |     |  content.            |   |  plugin LUT       |    |    +----+-------------+
         |     |                      |   |                   |    |         |
         |     +----------------------+   +---------+---------+    |         |     
         |                                          ^              |         v     
         |                                          |              |     (  AMQP ) 
    +----+----+                             +-------+------+       |     ( Stuff ) 
    | Update  |                             |              |       |
    | Filter  |                             |   Build      |       |
    | System  |                             |   Plugin     +-------^
    +----+----+                             |    LUT       |        
         |                                  |              |        
         |                                  +------+-------+        
         v                                         ^           
     (  AMQP )                                     |           
     ( Stuff )                                     |           
                      +---------------+     +------+--------+   
                      |               |     |               |   
                      |      Rule     +---->+    Plugin     |   
                      |     files     |     |  Definitions  |   
                      |               |     |               |   
                      +---------------+     +---------------+   

Crawl limit is 1000000.
Shallow updates can be achived by upserting entries close to the limit. E.g. 
a distance limit of 2 can be achieved by upserting a url with a starting crawl 
distance of 999998.

Required directives:
 - badwords
 - decompose
 - baseUrl

Allowed directives:
 - decomposeBefore
 - feeds
 - feedPostfix
 - stripTitle
 - tld
 - FOLLOW_GOOGLE_LINKS
 - allImages
 - cloudflare
 - fileDomains
 - destyle
 - preserveAttrs
 - type
 - extraStartUrls

Planned directives:
 - TagReplace
 - TitleReplace
 - titleTweakLut