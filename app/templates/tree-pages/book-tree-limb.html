## -*- coding: utf-8 -*-


<%namespace name="ut"              file="/utilities.mako"/>
<%namespace name="sideBar"         file="/gensidebar.mako"/>
<%namespace name="feed_ut"         file="/feeds/render.mako"/>

<%!
import urllib.parse
import time
import uuid
import settings
import string

srcLut = dict(settings.bookSources)
from natsort import natsorted
def compact_trie(inKey, inDict):

	if len(inDict) == 0:
		raise ValueError("Wat? Item in dict with zero length!")
	elif len(inDict) == 1:

		curKey, curDict = inDict.popitem()

		# Don't munge the end key
		if curKey == "_end_":
			return inKey, {curKey : curDict}

		curKey, curDict = compact_trie(curKey, curDict)
		return inKey+curKey, curDict

	else:   # len(inDict) > 1

		ret = {}
		for key, value in inDict.items():
			if key != "_end_":
				key, value = compact_trie(key, value)
			ret[key] = value

		return inKey, ret


def build_trie(iterItem, getKey=lambda x: x):
	base = {}


	# Build a trie data structure that represents the strings passed using nested dicts
	scan = []
	for item in iterItem:
		scan.append((getKey(item).lower(), item))

	for key, item in scan:

		floating_dict = base
		for letter in key:
			floating_dict = floating_dict.setdefault(letter, {})
		floating_dict["_end_"] = item

	# Flatten cases where nested dicts have only one item. convert {"a": {"b" : sommat}} to {"ab" : sommat}
	key, val = compact_trie('', base)
	out = {key : val}

	return out


%>


<%def name="badId()">
	Error: Bad Page Reference!<br>
	Page either not archived, or invalid.
</%def>

<%def name="needId()">
	Treeview Requests require a valid source site key.
</%def>




<%def name="renderDirectory(inDict, name, keyBase, keyNum, isBase=False)">
	<%
	curBase = 'item-%s' % uuid.uuid1(0)

	childNum = 0

	keys = list(inDict.keys())
	keys.sort()
	%>

	<ul>

		% if not isBase:
			<li><input type="checkbox" id="${curBase}" checked="checked" /><label for="${curBase}">${'Baka-Tsuki' if not name else name}</label>
				<ul>
		% endif
				% for key in keys:
					% if "_end_" in key:
						<%
							url, dbId, title = inDict[key]
						%>

						<li>
							<div id='rowid'>${dbId}</div>
							<div id='rowLink'><a href='/books/render?url=${urllib.parse.quote(url)}'>${title}</a></div>
						</li>
					% else:
						<%
							renderDirectory(inDict[key], name+key, curBase, childNum)
							childNum += 1

						%>
					% endif
				% endfor
		% if not isBase:
			</ul>
		% endif
		</li>
	</ul>
</%def>


<%def name="renderTree(srcDomain, preload=False)">

	<%
	itemId = abs(hash(srcDomain))
	%>

	<div class="css-treeview">
		<ul>
			<li><input type="checkbox" id="id${itemId}" loaded=0 /><label for="id${itemId}">${srcDomain.title()}</label>
				<ul>
					<li id="id${itemId}"><img src='/js/loading.gif' /></li>
				</ul>
			</li>
		</ul>

		<script>
			function checkboxEvent(e)
			{
				input = $('input#id${itemId}');
				if (input.is(':checked') && input.attr("loaded") == 0)
				{
					input.attr("loaded", 1)
					$('li#id${itemId}').load("/books/render?root=${urllib.parse.quote(srcDomain)}")
				}
			}

			$('#id${itemId}').on('change', checkboxEvent);

			console.log("Item checked: ", $('input#id${itemId}').is(':checked'));

			% if preload:

				$('input#id${itemId}').trigger('click');


			% endif

		</script>



	</div>
	% if not preload:
		<hr>
	% endif

</%def>

<%def name="renderTreeRoot(srcDomain)">
	<%

	## rootKey, rootTitle

	cursor = sqlCon.cursor()
	## cur.execute("""SELECT DISTINCT(netloc) FROM book_items WHERE istext=TRUE;""", (srcDomain, ))

	ret = {}
	for char in string.punctuation + string.whitespace + string.ascii_letters + string.digits:

		# Escape the postgresql special chars in the like search.
		if char == "_" or char == "%":
			char = r"\\"+char

		cursor.execute("SELECT dbid FROM book_items WHERE title LIKE %s AND netloc=%s LIMIT 1;", ('{char}%'.format(char=char), srcDomain))
		ret[char] = cursor.fetchone()

	for key in string.ascii_lowercase:
		if ret[key]:
			ret[key.upper()] = ret[key]
			del(ret[key])
	have = list(set([key.upper() for key, val in ret.items() if val ]))
	have.sort()

	print("Query for '%s'" % srcDomain)
	if not have:
		return


	curBase = 'item-%s' % int(time.time()*1000)

	childNum = 0
	# print(trie)

	%>

	% for key in have:
		<li>
		${lazyTreeNode(srcDomain, key)}
		</li>
	% endfor


</%def>


<%def name="renderWholeBranch(rootKey, keyBase)">
	<%

		cur = sqlCon.cursor()
		cur.execute("SELECT url, dbid, title FROM book_items WHERE netloc = %s AND mimetype = %s AND lower(title) LIKE lower(%s) ORDER BY title;", (rootKey, 'text/html', keyBase+'%'))
		ret = cur.fetchall()

		if not ret:
			context.write("No items for key? Did something go wrong?")
			return ''

		items = []
		for item in ret:
			filter = item[2].lower()


			items.append(item)

		trie = build_trie(items, lambda x: x[2])


	%>

	${renderDirectory(trie, '', "item", 0, isBase=True)}

</%def>



<%def name="renderPage(dbid, dlstate, title, contents, itemUrl, src, distance, lastChecked=0)">
	<!DOCTYPE html>
	<html>
		<head>
			<title>${title}</title>
			${ut.headerBase()}
		</head>
		<body>
			${sideBar.getSideBar(sqlCon)}
			<div class="bookdiv">

				<div class="subdiv">
					<div class="contentdiv bookcontent">
						${contents}
					</div>
					<hr>

					<div>
						<%
						if src in srcLut:
							srcStr = srcLut[src]
						else:
							srcStr = "Source Key: '%s'" % src
						%>
						Src: ${srcStr} <br>
						<a href='/api?reset-book-download-state=${dbid}'>Retrigger download and reset distance ${dbid}</a><br>
						Crawl Distance: ${distance}<br>
						Last crawl time: ${lastChecked}<br>
						Download State: ${dlstate}<br>
						<%
							feedurl, itemHome = feed_ut.getBaseDomainUrl(itemUrl)
						%>
						<a href='${itemHome}'>${feedurl} content</a><br>
						<a href='${itemUrl}'>Original source: ${itemUrl}</a>
					</div>
				</div>
			</div>
		</body>
	</html>

</%def>

<%def name="renderId(itemUrl)">
	<%
	if request.matched_route.name == 'book-render-western':
		table = 'book_western_items'
	elif request.matched_route.name == 'book-render':
		table = 'book_items'
	else:
		badId()
		return

	cur = sqlCon.cursor()
	cur.execute("SELECT dbid, dlstate, src, title, series, mimetype, fsPath, contents, distance FROM {table} WHERE url=%s;".format(table=table), (itemUrl, ))
	page = cur.fetchall()
	if len(page) != 1:
		print("Bad URL", itemUrl)
		badId()
	else:
		dbid, dlstate, src, title, series, mimetype, fsPath, contents, distance = page.pop()
		print("title: '%s'" % title)
		renderPage(dbid, dlstate, title, contents, itemUrl, src, distance)
	%>

</%def>

<%def name="lazyTreeNode(rootKey, treeKey)">
	<%
	curBase = 'item-%s' % uuid.uuid1(0)

	childNum = 0
	# print(trie)

	%>

	<ul>

		<li><input type="checkbox" id="${curBase}" loaded=0 /><label for="${curBase}">${treeKey}</label>
			<ul>
				<li id="${curBase}"><img src='/js/loading.gif' /></li>
			</ul>
		</li>
	</ul>
	<script>
		function checkboxEvent(e)
		{
			input = $('input#${curBase}');
			if (input.is(':checked') && input.attr("loaded") == 0)
			{
				input.attr("loaded", 1)
				$('li#${curBase}').load("/books/render?key=${rootKey}&tree=${urllib.parse.quote(treeKey)}")
			}

		}

		$('#${curBase}').on('change', checkboxEvent);
	</script>

</%def>

<%def name="lazyTreeRender(rootKey, treeKey)">
	<%
	curBase = 'item-%s' % uuid.uuid1(0)

	childNum = 0
	# print(trie)
	cur = sqlCon.cursor()


	cur.execute("""SELECT DISTINCT(substring(title for {len})) FROM book_items WHERE lower(title) LIKE %s AND src=%s;""".format(len=len(treeKey)+1), (treeKey.lower()+'%', rootKey))
	ret = cur.fetchall()
	print("Dictinct = ", ret)

	ret = set([item[0].lower() for item in ret])
	ret = list(ret)

	ret = natsorted(ret, key=lambda x: x.replace("-", " "))
	%>
	## Fukkit, just render the entire branch
	## % if len(ret) > 1:
	## 	% for item in ret:
	## 		${lazyTreeNode(rootKey, item)}
	## 	% endfor
	## % else:
	## 	${renderWholeBranch(rootKey, treeKey)}
	## % endif

	${renderWholeBranch(rootKey, treeKey)}

</%def>



<%


print("Request params", request.params)



if "url" in request.params:
	url = urllib.parse.unquote(request.params["url"])
	print("Rendering ID", url)
	renderId(url)

elif "tree" in request.params:

	if not "key" in request.params:
		needId()
		return

	key = request.params['key']

	prefix = urllib.parse.unquote(request.params["tree"])
	lazyTreeRender(key, prefix)

elif "root" in request.params:

	domain = urllib.parse.unquote(request.params["root"])
	renderTreeRoot(domain)

else:
	badId()
%>




<%def name="genTrie(inInterable)">
	<%
	return build_trie(inInterable)
	%>

</%def>

