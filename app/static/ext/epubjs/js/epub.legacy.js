(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("xmldom"), (function webpackLoadOptionalExternalModule() { try { return require("jszip"); } catch(e) {} }()));
	else if(typeof define === 'function' && define.amd)
		define(["xmldom", "jszip"], factory);
	else if(typeof exports === 'object')
		exports["ePub"] = factory(require("xmldom"), (function webpackLoadOptionalExternalModule() { try { return require("jszip"); } catch(e) {} }()));
	else
		root["ePub"] = factory(root["xmldom"], root["jszip"]);
})(typeof self !== 'undefined' ? self : this, function(__WEBPACK_EXTERNAL_MODULE_371__, __WEBPACK_EXTERNAL_MODULE_401__) {
return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "/dist/";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 148);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

var global = __webpack_require__(2);
var core = __webpack_require__(24);
var hide = __webpack_require__(13);
var redefine = __webpack_require__(14);
var ctx = __webpack_require__(19);
var PROTOTYPE = 'prototype';

var $export = function (type, name, source) {
  var IS_FORCED = type & $export.F;
  var IS_GLOBAL = type & $export.G;
  var IS_STATIC = type & $export.S;
  var IS_PROTO = type & $export.P;
  var IS_BIND = type & $export.B;
  var target = IS_GLOBAL ? global : IS_STATIC ? global[name] || (global[name] = {}) : (global[name] || {})[PROTOTYPE];
  var exports = IS_GLOBAL ? core : core[name] || (core[name] = {});
  var expProto = exports[PROTOTYPE] || (exports[PROTOTYPE] = {});
  var key, own, out, exp;
  if (IS_GLOBAL) source = name;
  for (key in source) {
    // contains in native
    own = !IS_FORCED && target && target[key] !== undefined;
    // export native or passed
    out = (own ? target : source)[key];
    // bind timers to global for call from export context
    exp = IS_BIND && own ? ctx(out, global) : IS_PROTO && typeof out == 'function' ? ctx(Function.call, out) : out;
    // extend global
    if (target) redefine(target, key, out, type & $export.U);
    // export
    if (exports[key] != out) hide(exports, key, exp);
    if (IS_PROTO && expProto[key] != out) expProto[key] = out;
  }
};
global.core = core;
// type bitmap
$export.F = 1;   // forced
$export.G = 2;   // global
$export.S = 4;   // static
$export.P = 8;   // proto
$export.B = 16;  // bind
$export.W = 32;  // wrap
$export.U = 64;  // safe
$export.R = 128; // real proto method for `library`
module.exports = $export;


/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

var isObject = __webpack_require__(4);
module.exports = function (it) {
  if (!isObject(it)) throw TypeError(it + ' is not an object!');
  return it;
};


/***/ }),
/* 2 */
/***/ (function(module, exports) {

// https://github.com/zloirock/core-js/issues/86#issuecomment-115759028
var global = module.exports = typeof window != 'undefined' && window.Math == Math
  ? window : typeof self != 'undefined' && self.Math == Math ? self
  // eslint-disable-next-line no-new-func
  : Function('return this')();
if (typeof __g == 'number') __g = global; // eslint-disable-line no-undef


/***/ }),
/* 3 */
/***/ (function(module, exports) {

module.exports = function (exec) {
  try {
    return !!exec();
  } catch (e) {
    return true;
  }
};


/***/ }),
/* 4 */
/***/ (function(module, exports) {

module.exports = function (it) {
  return typeof it === 'object' ? it !== null : typeof it === 'function';
};


/***/ }),
/* 5 */
/***/ (function(module, exports, __webpack_require__) {

var store = __webpack_require__(55)('wks');
var uid = __webpack_require__(37);
var Symbol = __webpack_require__(2).Symbol;
var USE_SYMBOL = typeof Symbol == 'function';

var $exports = module.exports = function (name) {
  return store[name] || (store[name] =
    USE_SYMBOL && Symbol[name] || (USE_SYMBOL ? Symbol : uid)('Symbol.' + name));
};

$exports.store = store;


/***/ }),
/* 6 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

exports.uuid = uuid;
exports.documentHeight = documentHeight;
exports.isElement = isElement;
exports.isNumber = isNumber;
exports.isFloat = isFloat;
exports.prefixed = prefixed;
exports.defaults = defaults;
exports.extend = extend;
exports.insert = insert;
exports.locationOf = locationOf;
exports.indexOfSorted = indexOfSorted;
exports.bounds = bounds;
exports.borders = borders;
exports.nodeBounds = nodeBounds;
exports.windowBounds = windowBounds;
exports.indexOfNode = indexOfNode;
exports.indexOfTextNode = indexOfTextNode;
exports.indexOfElementNode = indexOfElementNode;
exports.isXml = isXml;
exports.createBlob = createBlob;
exports.createBlobUrl = createBlobUrl;
exports.revokeBlobUrl = revokeBlobUrl;
exports.createBase64Url = createBase64Url;
exports.type = type;
exports.parse = parse;
exports.qs = qs;
exports.qsa = qsa;
exports.qsp = qsp;
exports.sprint = sprint;
exports.treeWalker = treeWalker;
exports.walk = walk;
exports.blob2base64 = blob2base64;
exports.defer = defer;
exports.querySelectorByType = querySelectorByType;
exports.findChildren = findChildren;
exports.parents = parents;
exports.filterChildren = filterChildren;
exports.getParentByTagName = getParentByTagName;

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Core Utilities and Helpers
 * @module Core
*/

/**
 * Vendor prefixed requestAnimationFrame
 * @returns {function} requestAnimationFrame
 * @memberof Core
 */
var requestAnimationFrame = exports.requestAnimationFrame = typeof window != "undefined" ? window.requestAnimationFrame || window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame || window.msRequestAnimationFrame : false;
var ELEMENT_NODE = 1;
var TEXT_NODE = 3;
var COMMENT_NODE = 8;
var DOCUMENT_NODE = 9;
var _URL = typeof URL != "undefined" ? URL : typeof window != "undefined" ? window.URL || window.webkitURL || window.mozURL : undefined;

/**
 * Generates a UUID
 * based on: http://stackoverflow.com/questions/105034/how-to-create-a-guid-uuid-in-javascript
 * @returns {string} uuid
 * @memberof Core
 */
function uuid() {
	var d = new Date().getTime();
	var uuid = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
		var r = (d + Math.random() * 16) % 16 | 0;
		d = Math.floor(d / 16);
		return (c == "x" ? r : r & 0x7 | 0x8).toString(16);
	});
	return uuid;
}

/**
 * Gets the height of a document
 * @returns {number} height
 * @memberof Core
 */
function documentHeight() {
	return Math.max(document.documentElement.clientHeight, document.body.scrollHeight, document.documentElement.scrollHeight, document.body.offsetHeight, document.documentElement.offsetHeight);
}

/**
 * Checks if a node is an element
 * @param {object} obj
 * @returns {boolean}
 * @memberof Core
 */
function isElement(obj) {
	return !!(obj && obj.nodeType == 1);
}

/**
 * @param {any} n
 * @returns {boolean}
 * @memberof Core
 */
function isNumber(n) {
	return !isNaN(parseFloat(n)) && isFinite(n);
}

/**
 * @param {any} n
 * @returns {boolean}
 * @memberof Core
 */
function isFloat(n) {
	var f = parseFloat(n);

	if (isNumber(n) === false) {
		return false;
	}

	if (typeof n === "string" && n.indexOf(".") > -1) {
		return true;
	}

	return Math.floor(f) !== f;
}

/**
 * Get a prefixed css property
 * @param {string} unprefixed
 * @returns {string}
 * @memberof Core
 */
function prefixed(unprefixed) {
	var vendors = ["Webkit", "webkit", "Moz", "O", "ms"];
	var prefixes = ["-webkit-", "-webkit-", "-moz-", "-o-", "-ms-"];
	var lower = unprefixed.toLowerCase();
	var length = vendors.length;

	if (typeof document === "undefined" || typeof document.body.style[lower] != "undefined") {
		return unprefixed;
	}

	for (var i = 0; i < length; i++) {
		if (typeof document.body.style[prefixes[i] + lower] != "undefined") {
			return prefixes[i] + lower;
		}
	}

	return unprefixed;
}

/**
 * Apply defaults to an object
 * @param {object} obj
 * @returns {object}
 * @memberof Core
 */
function defaults(obj) {
	for (var i = 1, length = arguments.length; i < length; i++) {
		var source = arguments[i];
		for (var prop in source) {
			if (obj[prop] === void 0) obj[prop] = source[prop];
		}
	}
	return obj;
}

/**
 * Extend properties of an object
 * @param {object} target
 * @returns {object}
 * @memberof Core
 */
function extend(target) {
	var sources = [].slice.call(arguments, 1);
	sources.forEach(function (source) {
		if (!source) return;
		Object.getOwnPropertyNames(source).forEach(function (propName) {
			Object.defineProperty(target, propName, Object.getOwnPropertyDescriptor(source, propName));
		});
	});
	return target;
}

/**
 * Fast quicksort insert for sorted array -- based on:
 *  http://stackoverflow.com/questions/1344500/efficient-way-to-insert-a-number-into-a-sorted-array-of-numbers
 * @param {any} item
 * @param {array} array
 * @param {function} [compareFunction]
 * @returns {number} location (in array)
 * @memberof Core
 */
function insert(item, array, compareFunction) {
	var location = locationOf(item, array, compareFunction);
	array.splice(location, 0, item);

	return location;
}

/**
 * Finds where something would fit into a sorted array
 * @param {any} item
 * @param {array} array
 * @param {function} [compareFunction]
 * @param {function} [_start]
 * @param {function} [_end]
 * @returns {number} location (in array)
 * @memberof Core
 */
function locationOf(item, array, compareFunction, _start, _end) {
	var start = _start || 0;
	var end = _end || array.length;
	var pivot = parseInt(start + (end - start) / 2);
	var compared;
	if (!compareFunction) {
		compareFunction = function compareFunction(a, b) {
			if (a > b) return 1;
			if (a < b) return -1;
			if (a == b) return 0;
		};
	}
	if (end - start <= 0) {
		return pivot;
	}

	compared = compareFunction(array[pivot], item);
	if (end - start === 1) {
		return compared >= 0 ? pivot : pivot + 1;
	}
	if (compared === 0) {
		return pivot;
	}
	if (compared === -1) {
		return locationOf(item, array, compareFunction, pivot, end);
	} else {
		return locationOf(item, array, compareFunction, start, pivot);
	}
}

/**
 * Finds index of something in a sorted array
 * Returns -1 if not found
 * @param {any} item
 * @param {array} array
 * @param {function} [compareFunction]
 * @param {function} [_start]
 * @param {function} [_end]
 * @returns {number} index (in array) or -1
 * @memberof Core
 */
function indexOfSorted(item, array, compareFunction, _start, _end) {
	var start = _start || 0;
	var end = _end || array.length;
	var pivot = parseInt(start + (end - start) / 2);
	var compared;
	if (!compareFunction) {
		compareFunction = function compareFunction(a, b) {
			if (a > b) return 1;
			if (a < b) return -1;
			if (a == b) return 0;
		};
	}
	if (end - start <= 0) {
		return -1; // Not found
	}

	compared = compareFunction(array[pivot], item);
	if (end - start === 1) {
		return compared === 0 ? pivot : -1;
	}
	if (compared === 0) {
		return pivot; // Found
	}
	if (compared === -1) {
		return indexOfSorted(item, array, compareFunction, pivot, end);
	} else {
		return indexOfSorted(item, array, compareFunction, start, pivot);
	}
}
/**
 * Find the bounds of an element
 * taking padding and margin into account
 * @param {element} el
 * @returns {{ width: Number, height: Number}}
 * @memberof Core
 */
function bounds(el) {

	var style = window.getComputedStyle(el);
	var widthProps = ["width", "paddingRight", "paddingLeft", "marginRight", "marginLeft", "borderRightWidth", "borderLeftWidth"];
	var heightProps = ["height", "paddingTop", "paddingBottom", "marginTop", "marginBottom", "borderTopWidth", "borderBottomWidth"];

	var width = 0;
	var height = 0;

	widthProps.forEach(function (prop) {
		width += parseFloat(style[prop]) || 0;
	});

	heightProps.forEach(function (prop) {
		height += parseFloat(style[prop]) || 0;
	});

	return {
		height: height,
		width: width
	};
}

/**
 * Find the bounds of an element
 * taking padding, margin and borders into account
 * @param {element} el
 * @returns {{ width: Number, height: Number}}
 * @memberof Core
 */
function borders(el) {

	var style = window.getComputedStyle(el);
	var widthProps = ["paddingRight", "paddingLeft", "marginRight", "marginLeft", "borderRightWidth", "borderLeftWidth"];
	var heightProps = ["paddingTop", "paddingBottom", "marginTop", "marginBottom", "borderTopWidth", "borderBottomWidth"];

	var width = 0;
	var height = 0;

	widthProps.forEach(function (prop) {
		width += parseFloat(style[prop]) || 0;
	});

	heightProps.forEach(function (prop) {
		height += parseFloat(style[prop]) || 0;
	});

	return {
		height: height,
		width: width
	};
}

/**
 * Find the bounds of any node
 * allows for getting bounds of text nodes by wrapping them in a range
 * @param {node} node
 * @returns {BoundingClientRect}
 * @memberof Core
 */
function nodeBounds(node) {
	var elPos = void 0;
	var doc = node.ownerDocument;
	if (node.nodeType == Node.TEXT_NODE) {
		var elRange = doc.createRange();
		elRange.selectNodeContents(node);
		elPos = elRange.getBoundingClientRect();
	} else {
		elPos = node.getBoundingClientRect();
	}
	return elPos;
}

/**
 * Find the equivelent of getBoundingClientRect of a browser window
 * @returns {{ width: Number, height: Number, top: Number, left: Number, right: Number, bottom: Number }}
 * @memberof Core
 */
function windowBounds() {

	var width = window.innerWidth;
	var height = window.innerHeight;

	return {
		top: 0,
		left: 0,
		right: width,
		bottom: height,
		width: width,
		height: height
	};
}

/**
 * Gets the index of a node in its parent
 * @param {Node} node
 * @param {string} typeId
 * @return {number} index
 * @memberof Core
 */
function indexOfNode(node, typeId) {
	var parent = node.parentNode;
	var children = parent.childNodes;
	var sib;
	var index = -1;
	for (var i = 0; i < children.length; i++) {
		sib = children[i];
		if (sib.nodeType === typeId) {
			index++;
		}
		if (sib == node) break;
	}

	return index;
}

/**
 * Gets the index of a text node in its parent
 * @param {node} textNode
 * @returns {number} index
 * @memberof Core
 */
function indexOfTextNode(textNode) {
	return indexOfNode(textNode, TEXT_NODE);
}

/**
 * Gets the index of an element node in its parent
 * @param {element} elementNode
 * @returns {number} index
 * @memberof Core
 */
function indexOfElementNode(elementNode) {
	return indexOfNode(elementNode, ELEMENT_NODE);
}

/**
 * Check if extension is xml
 * @param {string} ext
 * @returns {boolean}
 * @memberof Core
 */
function isXml(ext) {
	return ["xml", "opf", "ncx"].indexOf(ext) > -1;
}

/**
 * Create a new blob
 * @param {any} content
 * @param {string} mime
 * @returns {Blob}
 * @memberof Core
 */
function createBlob(content, mime) {
	return new Blob([content], { type: mime });
}

/**
 * Create a new blob url
 * @param {any} content
 * @param {string} mime
 * @returns {string} url
 * @memberof Core
 */
function createBlobUrl(content, mime) {
	var tempUrl;
	var blob = createBlob(content, mime);

	tempUrl = _URL.createObjectURL(blob);

	return tempUrl;
}

/**
 * Remove a blob url
 * @param {string} url
 * @memberof Core
 */
function revokeBlobUrl(url) {
	return _URL.revokeObjectURL(url);
}

/**
 * Create a new base64 encoded url
 * @param {any} content
 * @param {string} mime
 * @returns {string} url
 * @memberof Core
 */
function createBase64Url(content, mime) {
	var data;
	var datauri;

	if (typeof content !== "string") {
		// Only handles strings
		return;
	}

	data = btoa(encodeURIComponent(content));

	datauri = "data:" + mime + ";base64," + data;

	return datauri;
}

/**
 * Get type of an object
 * @param {object} obj
 * @returns {string} type
 * @memberof Core
 */
function type(obj) {
	return Object.prototype.toString.call(obj).slice(8, -1);
}

/**
 * Parse xml (or html) markup
 * @param {string} markup
 * @param {string} mime
 * @param {boolean} forceXMLDom force using xmlDom to parse instead of native parser
 * @returns {document} document
 * @memberof Core
 */
function parse(markup, mime, forceXMLDom) {
	var doc;
	var Parser;

	if (typeof DOMParser === "undefined" || forceXMLDom) {
		Parser = __webpack_require__(371).DOMParser;
	} else {
		Parser = DOMParser;
	}

	// Remove byte order mark before parsing
	// https://www.w3.org/International/questions/qa-byte-order-mark
	if (markup.charCodeAt(0) === 0xFEFF) {
		markup = markup.slice(1);
	}

	doc = new Parser().parseFromString(markup, mime);

	return doc;
}

/**
 * querySelector polyfill
 * @param {element} el
 * @param {string} sel selector string
 * @returns {element} element
 * @memberof Core
 */
function qs(el, sel) {
	var elements;
	if (!el) {
		throw new Error("No Element Provided");
	}

	if (typeof el.querySelector != "undefined") {
		return el.querySelector(sel);
	} else {
		elements = el.getElementsByTagName(sel);
		if (elements.length) {
			return elements[0];
		}
	}
}

/**
 * querySelectorAll polyfill
 * @param {element} el
 * @param {string} sel selector string
 * @returns {element[]} elements
 * @memberof Core
 */
function qsa(el, sel) {

	if (typeof el.querySelector != "undefined") {
		return el.querySelectorAll(sel);
	} else {
		return el.getElementsByTagName(sel);
	}
}

/**
 * querySelector by property
 * @param {element} el
 * @param {string} sel selector string
 * @param {object[]} props
 * @returns {element[]} elements
 * @memberof Core
 */
function qsp(el, sel, props) {
	var q, filtered;
	if (typeof el.querySelector != "undefined") {
		sel += "[";
		for (var prop in props) {
			sel += prop + "~='" + props[prop] + "'";
		}
		sel += "]";
		return el.querySelector(sel);
	} else {
		q = el.getElementsByTagName(sel);
		filtered = Array.prototype.slice.call(q, 0).filter(function (el) {
			for (var prop in props) {
				if (el.getAttribute(prop) === props[prop]) {
					return true;
				}
			}
			return false;
		});

		if (filtered) {
			return filtered[0];
		}
	}
}

/**
 * Sprint through all text nodes in a document
 * @memberof Core
 * @param  {element} root element to start with
 * @param  {function} func function to run on each element
 */
function sprint(root, func) {
	var doc = root.ownerDocument || root;
	if (typeof doc.createTreeWalker !== "undefined") {
		treeWalker(root, func, NodeFilter.SHOW_TEXT);
	} else {
		walk(root, function (node) {
			if (node && node.nodeType === 3) {
				// Node.TEXT_NODE
				func(node);
			}
		}, true);
	}
}

/**
 * Create a treeWalker
 * @memberof Core
 * @param  {element} root element to start with
 * @param  {function} func function to run on each element
 * @param  {function | object} filter funtion or object to filter with
 */
function treeWalker(root, func, filter) {
	var treeWalker = document.createTreeWalker(root, filter, null, false);
	var node = void 0;
	while (node = treeWalker.nextNode()) {
		func(node);
	}
}

/**
 * @memberof Core
 * @param {node} node
 * @param {callback} return false for continue,true for break inside callback
 */
function walk(node, callback) {
	if (callback(node)) {
		return true;
	}
	node = node.firstChild;
	if (node) {
		do {
			var walked = walk(node, callback);
			if (walked) {
				return true;
			}
			node = node.nextSibling;
		} while (node);
	}
}

/**
 * Convert a blob to a base64 encoded string
 * @param {Blog} blob
 * @returns {string}
 * @memberof Core
 */
function blob2base64(blob) {
	return new Promise(function (resolve, reject) {
		var reader = new FileReader();
		reader.readAsDataURL(blob);
		reader.onloadend = function () {
			resolve(reader.result);
		};
	});
}

/**
 * Creates a new pending promise and provides methods to resolve or reject it.
 * From: https://developer.mozilla.org/en-US/docs/Mozilla/JavaScript_code_modules/Promise.jsm/Deferred#backwards_forwards_compatible
 * @memberof Core
 */
function defer() {
	var _this = this;

	/* A method to resolve the associated Promise with the value passed.
  * If the promise is already settled it does nothing.
  *
  * @param {anything} value : This value is used to resolve the promise
  * If the value is a Promise then the associated promise assumes the state
  * of Promise passed as value.
  */
	this.resolve = null;

	/* A method to reject the assocaited Promise with the value passed.
  * If the promise is already settled it does nothing.
  *
  * @param {anything} reason: The reason for the rejection of the Promise.
  * Generally its an Error object. If however a Promise is passed, then the Promise
  * itself will be the reason for rejection no matter the state of the Promise.
  */
	this.reject = null;

	this.id = uuid();

	/* A newly created Pomise object.
  * Initially in pending state.
  */
	this.promise = new Promise(function (resolve, reject) {
		_this.resolve = resolve;
		_this.reject = reject;
	});
	Object.freeze(this);
}

/**
 * querySelector with filter by epub type
 * @param {element} html
 * @param {string} element element type to find
 * @param {string} type epub type to find
 * @returns {element[]} elements
 * @memberof Core
 */
function querySelectorByType(html, element, type) {
	var query;
	if (typeof html.querySelector != "undefined") {
		query = html.querySelector(element + "[*|type=\"" + type + "\"]");
	}
	// Handle IE not supporting namespaced epub:type in querySelector
	if (!query || query.length === 0) {
		query = qsa(html, element);
		for (var i = 0; i < query.length; i++) {
			if (query[i].getAttributeNS("http://www.idpf.org/2007/ops", "type") === type || query[i].getAttribute("epub:type") === type) {
				return query[i];
			}
		}
	} else {
		return query;
	}
}

/**
 * Find direct decendents of an element
 * @param {element} el
 * @returns {element[]} children
 * @memberof Core
 */
function findChildren(el) {
	var result = [];
	var childNodes = el.childNodes;
	for (var i = 0; i < childNodes.length; i++) {
		var node = childNodes[i];
		if (node.nodeType === 1) {
			result.push(node);
		}
	}
	return result;
}

/**
 * Find all parents (ancestors) of an element
 * @param {element} node
 * @returns {element[]} parents
 * @memberof Core
 */
function parents(node) {
	var nodes = [node];
	for (; node; node = node.parentNode) {
		nodes.unshift(node);
	}
	return nodes;
}

/**
 * Find all direct decendents of a specific type
 * @param {element} el
 * @param {string} nodeName
 * @param {boolean} [single]
 * @returns {element[]} children
 * @memberof Core
 */
function filterChildren(el, nodeName, single) {
	var result = [];
	var childNodes = el.childNodes;
	for (var i = 0; i < childNodes.length; i++) {
		var node = childNodes[i];
		if (node.nodeType === 1 && node.nodeName.toLowerCase() === nodeName) {
			if (single) {
				return node;
			} else {
				result.push(node);
			}
		}
	}
	if (!single) {
		return result;
	}
}

/**
 * Filter all parents (ancestors) with tag name
 * @param {element} node
 * @param {string} tagname
 * @returns {element[]} parents
 * @memberof Core
 */
function getParentByTagName(node, tagname) {
	var parent = void 0;
	if (node === null || tagname === '') return;
	parent = node.parentNode;
	while (parent.nodeType === 1) {
		if (parent.tagName.toLowerCase() === tagname) {
			return parent;
		}
		parent = parent.parentNode;
	}
}

/**
 * Lightweight Polyfill for DOM Range
 * @class
 * @memberof Core
 */

var RangeObject = exports.RangeObject = function () {
	function RangeObject() {
		_classCallCheck(this, RangeObject);

		this.collapsed = false;
		this.commonAncestorContainer = undefined;
		this.endContainer = undefined;
		this.endOffset = undefined;
		this.startContainer = undefined;
		this.startOffset = undefined;
	}

	_createClass(RangeObject, [{
		key: "setStart",
		value: function setStart(startNode, startOffset) {
			this.startContainer = startNode;
			this.startOffset = startOffset;

			if (!this.endContainer) {
				this.collapse(true);
			} else {
				this.commonAncestorContainer = this._commonAncestorContainer();
			}

			this._checkCollapsed();
		}
	}, {
		key: "setEnd",
		value: function setEnd(endNode, endOffset) {
			this.endContainer = endNode;
			this.endOffset = endOffset;

			if (!this.startContainer) {
				this.collapse(false);
			} else {
				this.collapsed = false;
				this.commonAncestorContainer = this._commonAncestorContainer();
			}

			this._checkCollapsed();
		}
	}, {
		key: "collapse",
		value: function collapse(toStart) {
			this.collapsed = true;
			if (toStart) {
				this.endContainer = this.startContainer;
				this.endOffset = this.startOffset;
				this.commonAncestorContainer = this.startContainer.parentNode;
			} else {
				this.startContainer = this.endContainer;
				this.startOffset = this.endOffset;
				this.commonAncestorContainer = this.endOffset.parentNode;
			}
		}
	}, {
		key: "selectNode",
		value: function selectNode(referenceNode) {
			var parent = referenceNode.parentNode;
			var index = Array.prototype.indexOf.call(parent.childNodes, referenceNode);
			this.setStart(parent, index);
			this.setEnd(parent, index + 1);
		}
	}, {
		key: "selectNodeContents",
		value: function selectNodeContents(referenceNode) {
			var end = referenceNode.childNodes[referenceNode.childNodes - 1];
			var endIndex = referenceNode.nodeType === 3 ? referenceNode.textContent.length : parent.childNodes.length;
			this.setStart(referenceNode, 0);
			this.setEnd(referenceNode, endIndex);
		}
	}, {
		key: "_commonAncestorContainer",
		value: function _commonAncestorContainer(startContainer, endContainer) {
			var startParents = parents(startContainer || this.startContainer);
			var endParents = parents(endContainer || this.endContainer);

			if (startParents[0] != endParents[0]) return undefined;

			for (var i = 0; i < startParents.length; i++) {
				if (startParents[i] != endParents[i]) {
					return startParents[i - 1];
				}
			}
		}
	}, {
		key: "_checkCollapsed",
		value: function _checkCollapsed() {
			if (this.startContainer === this.endContainer && this.startOffset === this.endOffset) {
				this.collapsed = true;
			} else {
				this.collapsed = false;
			}
		}
	}, {
		key: "toString",
		value: function toString() {
			// TODO: implement walking between start and end to find text
		}
	}]);

	return RangeObject;
}();

/***/ }),
/* 7 */
/***/ (function(module, exports, __webpack_require__) {

// Thank's IE8 for his funny defineProperty
module.exports = !__webpack_require__(3)(function () {
  return Object.defineProperty({}, 'a', { get: function () { return 7; } }).a != 7;
});


/***/ }),
/* 8 */
/***/ (function(module, exports, __webpack_require__) {

var anObject = __webpack_require__(1);
var IE8_DOM_DEFINE = __webpack_require__(107);
var toPrimitive = __webpack_require__(25);
var dP = Object.defineProperty;

exports.f = __webpack_require__(7) ? Object.defineProperty : function defineProperty(O, P, Attributes) {
  anObject(O);
  P = toPrimitive(P, true);
  anObject(Attributes);
  if (IE8_DOM_DEFINE) try {
    return dP(O, P, Attributes);
  } catch (e) { /* empty */ }
  if ('get' in Attributes || 'set' in Attributes) throw TypeError('Accessors not supported!');
  if ('value' in Attributes) O[P] = Attributes.value;
  return O;
};


/***/ }),
/* 9 */
/***/ (function(module, exports, __webpack_require__) {

// 7.1.15 ToLength
var toInteger = __webpack_require__(27);
var min = Math.min;
module.exports = function (it) {
  return it > 0 ? min(toInteger(it), 0x1fffffffffffff) : 0; // pow(2, 53) - 1 == 9007199254740991
};


/***/ }),
/* 10 */
/***/ (function(module, exports, __webpack_require__) {

// 7.1.13 ToObject(argument)
var defined = __webpack_require__(26);
module.exports = function (it) {
  return Object(defined(it));
};


/***/ }),
/* 11 */
/***/ (function(module, exports) {

module.exports = function (it) {
  if (typeof it != 'function') throw TypeError(it + ' is not a function!');
  return it;
};


/***/ }),
/* 12 */
/***/ (function(module, exports) {

var hasOwnProperty = {}.hasOwnProperty;
module.exports = function (it, key) {
  return hasOwnProperty.call(it, key);
};


/***/ }),
/* 13 */
/***/ (function(module, exports, __webpack_require__) {

var dP = __webpack_require__(8);
var createDesc = __webpack_require__(36);
module.exports = __webpack_require__(7) ? function (object, key, value) {
  return dP.f(object, key, createDesc(1, value));
} : function (object, key, value) {
  object[key] = value;
  return object;
};


/***/ }),
/* 14 */
/***/ (function(module, exports, __webpack_require__) {

var global = __webpack_require__(2);
var hide = __webpack_require__(13);
var has = __webpack_require__(12);
var SRC = __webpack_require__(37)('src');
var TO_STRING = 'toString';
var $toString = Function[TO_STRING];
var TPL = ('' + $toString).split(TO_STRING);

__webpack_require__(24).inspectSource = function (it) {
  return $toString.call(it);
};

(module.exports = function (O, key, val, safe) {
  var isFunction = typeof val == 'function';
  if (isFunction) has(val, 'name') || hide(val, 'name', key);
  if (O[key] === val) return;
  if (isFunction) has(val, SRC) || hide(val, SRC, O[key] ? '' + O[key] : TPL.join(String(key)));
  if (O === global) {
    O[key] = val;
  } else if (!safe) {
    delete O[key];
    hide(O, key, val);
  } else if (O[key]) {
    O[key] = val;
  } else {
    hide(O, key, val);
  }
// add fake Function#toString for correct work wrapped methods / constructors with methods like LoDash isNative
})(Function.prototype, TO_STRING, function toString() {
  return typeof this == 'function' && this[SRC] || $toString.call(this);
});


/***/ }),
/* 15 */
/***/ (function(module, exports, __webpack_require__) {

// to indexed object, toObject with fallback for non-array-like ES3 strings
var IObject = __webpack_require__(52);
var defined = __webpack_require__(26);
module.exports = function (it) {
  return IObject(defined(it));
};


/***/ }),
/* 16 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(0);
var fails = __webpack_require__(3);
var defined = __webpack_require__(26);
var quot = /"/g;
// B.2.3.2.1 CreateHTML(string, tag, attribute, value)
var createHTML = function (string, tag, attribute, value) {
  var S = String(defined(string));
  var p1 = '<' + tag;
  if (attribute !== '') p1 += ' ' + attribute + '="' + String(value).replace(quot, '&quot;') + '"';
  return p1 + '>' + S + '</' + tag + '>';
};
module.exports = function (NAME, exec) {
  var O = {};
  O[NAME] = exec(createHTML);
  $export($export.P + $export.F * fails(function () {
    var test = ''[NAME]('"');
    return test !== test.toLowerCase() || test.split('"').length > 3;
  }), 'String', O);
};


/***/ }),
/* 17 */
/***/ (function(module, exports, __webpack_require__) {

var pIE = __webpack_require__(53);
var createDesc = __webpack_require__(36);
var toIObject = __webpack_require__(15);
var toPrimitive = __webpack_require__(25);
var has = __webpack_require__(12);
var IE8_DOM_DEFINE = __webpack_require__(107);
var gOPD = Object.getOwnPropertyDescriptor;

exports.f = __webpack_require__(7) ? gOPD : function getOwnPropertyDescriptor(O, P) {
  O = toIObject(O);
  P = toPrimitive(P, true);
  if (IE8_DOM_DEFINE) try {
    return gOPD(O, P);
  } catch (e) { /* empty */ }
  if (has(O, P)) return createDesc(!pIE.f.call(O, P), O[P]);
};


/***/ }),
/* 18 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.9 / 15.2.3.2 Object.getPrototypeOf(O)
var has = __webpack_require__(12);
var toObject = __webpack_require__(10);
var IE_PROTO = __webpack_require__(76)('IE_PROTO');
var ObjectProto = Object.prototype;

module.exports = Object.getPrototypeOf || function (O) {
  O = toObject(O);
  if (has(O, IE_PROTO)) return O[IE_PROTO];
  if (typeof O.constructor == 'function' && O instanceof O.constructor) {
    return O.constructor.prototype;
  } return O instanceof Object ? ObjectProto : null;
};


/***/ }),
/* 19 */
/***/ (function(module, exports, __webpack_require__) {

// optional / simple context binding
var aFunction = __webpack_require__(11);
module.exports = function (fn, that, length) {
  aFunction(fn);
  if (that === undefined) return fn;
  switch (length) {
    case 1: return function (a) {
      return fn.call(that, a);
    };
    case 2: return function (a, b) {
      return fn.call(that, a, b);
    };
    case 3: return function (a, b, c) {
      return fn.call(that, a, b, c);
    };
  }
  return function (/* ...args */) {
    return fn.apply(that, arguments);
  };
};


/***/ }),
/* 20 */
/***/ (function(module, exports) {

var toString = {}.toString;

module.exports = function (it) {
  return toString.call(it).slice(8, -1);
};


/***/ }),
/* 21 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var fails = __webpack_require__(3);

module.exports = function (method, arg) {
  return !!method && fails(function () {
    // eslint-disable-next-line no-useless-call
    arg ? method.call(null, function () { /* empty */ }, 1) : method.call(null);
  });
};


/***/ }),
/* 22 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _core = __webpack_require__(6);

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var ELEMENT_NODE = 1;
var TEXT_NODE = 3;
var COMMENT_NODE = 8;
var DOCUMENT_NODE = 9;

/**
	* Parsing and creation of EpubCFIs: http://www.idpf.org/epub/linking/cfi/epub-cfi.html

	* Implements:
	* - Character Offset: epubcfi(/6/4[chap01ref]!/4[body01]/10[para05]/2/1:3)
	* - Simple Ranges : epubcfi(/6/4[chap01ref]!/4[body01]/10[para05],/2/1:1,/3:4)

	* Does Not Implement:
	* - Temporal Offset (~)
	* - Spatial Offset (@)
	* - Temporal-Spatial Offset (~ + @)
	* - Text Location Assertion ([)
	* @class
	@param {string | Range | Node } [cfiFrom]
	@param {string | object} [base]
	@param {string} [ignoreClass] class to ignore when parsing DOM
*/

var EpubCFI = function () {
	function EpubCFI(cfiFrom, base, ignoreClass) {
		_classCallCheck(this, EpubCFI);

		var type;

		this.str = "";

		this.base = {};
		this.spinePos = 0; // For compatibility

		this.range = false; // true || false;

		this.path = {};
		this.start = null;
		this.end = null;

		// Allow instantiation without the "new" keyword
		if (!(this instanceof EpubCFI)) {
			return new EpubCFI(cfiFrom, base, ignoreClass);
		}

		if (typeof base === "string") {
			this.base = this.parseComponent(base);
		} else if ((typeof base === "undefined" ? "undefined" : _typeof(base)) === "object" && base.steps) {
			this.base = base;
		}

		type = this.checkType(cfiFrom);

		if (type === "string") {
			this.str = cfiFrom;
			return (0, _core.extend)(this, this.parse(cfiFrom));
		} else if (type === "range") {
			return (0, _core.extend)(this, this.fromRange(cfiFrom, this.base, ignoreClass));
		} else if (type === "node") {
			return (0, _core.extend)(this, this.fromNode(cfiFrom, this.base, ignoreClass));
		} else if (type === "EpubCFI" && cfiFrom.path) {
			return cfiFrom;
		} else if (!cfiFrom) {
			return this;
		} else {
			throw new TypeError("not a valid argument for EpubCFI");
		}
	}

	/**
  * Check the type of constructor input
  * @private
  */


	_createClass(EpubCFI, [{
		key: "checkType",
		value: function checkType(cfi) {

			if (this.isCfiString(cfi)) {
				return "string";
				// Is a range object
			} else if (cfi && (typeof cfi === "undefined" ? "undefined" : _typeof(cfi)) === "object" && ((0, _core.type)(cfi) === "Range" || typeof cfi.startContainer != "undefined")) {
				return "range";
			} else if (cfi && (typeof cfi === "undefined" ? "undefined" : _typeof(cfi)) === "object" && typeof cfi.nodeType != "undefined") {
				// || typeof cfi === "function"
				return "node";
			} else if (cfi && (typeof cfi === "undefined" ? "undefined" : _typeof(cfi)) === "object" && cfi instanceof EpubCFI) {
				return "EpubCFI";
			} else {
				return false;
			}
		}

		/**
   * Parse a cfi string to a CFI object representation
   * @param {string} cfiStr
   * @returns {object} cfi
   */

	}, {
		key: "parse",
		value: function parse(cfiStr) {
			var cfi = {
				spinePos: -1,
				range: false,
				base: {},
				path: {},
				start: null,
				end: null
			};
			var baseComponent, pathComponent, range;

			if (typeof cfiStr !== "string") {
				return { spinePos: -1 };
			}

			if (cfiStr.indexOf("epubcfi(") === 0 && cfiStr[cfiStr.length - 1] === ")") {
				// Remove intial epubcfi( and ending )
				cfiStr = cfiStr.slice(8, cfiStr.length - 1);
			}

			baseComponent = this.getChapterComponent(cfiStr);

			// Make sure this is a valid cfi or return
			if (!baseComponent) {
				return { spinePos: -1 };
			}

			cfi.base = this.parseComponent(baseComponent);

			pathComponent = this.getPathComponent(cfiStr);
			cfi.path = this.parseComponent(pathComponent);

			range = this.getRange(cfiStr);

			if (range) {
				cfi.range = true;
				cfi.start = this.parseComponent(range[0]);
				cfi.end = this.parseComponent(range[1]);
			}

			// Get spine node position
			// cfi.spineSegment = cfi.base.steps[1];

			// Chapter segment is always the second step
			cfi.spinePos = cfi.base.steps[1].index;

			return cfi;
		}
	}, {
		key: "parseComponent",
		value: function parseComponent(componentStr) {
			var component = {
				steps: [],
				terminal: {
					offset: null,
					assertion: null
				}
			};
			var parts = componentStr.split(":");
			var steps = parts[0].split("/");
			var terminal;

			if (parts.length > 1) {
				terminal = parts[1];
				component.terminal = this.parseTerminal(terminal);
			}

			if (steps[0] === "") {
				steps.shift(); // Ignore the first slash
			}

			component.steps = steps.map(function (step) {
				return this.parseStep(step);
			}.bind(this));

			return component;
		}
	}, {
		key: "parseStep",
		value: function parseStep(stepStr) {
			var type, num, index, has_brackets, id;

			has_brackets = stepStr.match(/\[(.*)\]/);
			if (has_brackets && has_brackets[1]) {
				id = has_brackets[1];
			}

			//-- Check if step is a text node or element
			num = parseInt(stepStr);

			if (isNaN(num)) {
				return;
			}

			if (num % 2 === 0) {
				// Even = is an element
				type = "element";
				index = num / 2 - 1;
			} else {
				type = "text";
				index = (num - 1) / 2;
			}

			return {
				"type": type,
				"index": index,
				"id": id || null
			};
		}
	}, {
		key: "parseTerminal",
		value: function parseTerminal(termialStr) {
			var characterOffset, textLocationAssertion;
			var assertion = termialStr.match(/\[(.*)\]/);

			if (assertion && assertion[1]) {
				characterOffset = parseInt(termialStr.split("[")[0]);
				textLocationAssertion = assertion[1];
			} else {
				characterOffset = parseInt(termialStr);
			}

			if (!(0, _core.isNumber)(characterOffset)) {
				characterOffset = null;
			}

			return {
				"offset": characterOffset,
				"assertion": textLocationAssertion
			};
		}
	}, {
		key: "getChapterComponent",
		value: function getChapterComponent(cfiStr) {

			var indirection = cfiStr.split("!");

			return indirection[0];
		}
	}, {
		key: "getPathComponent",
		value: function getPathComponent(cfiStr) {

			var indirection = cfiStr.split("!");

			if (indirection[1]) {
				var ranges = indirection[1].split(",");
				return ranges[0];
			}
		}
	}, {
		key: "getRange",
		value: function getRange(cfiStr) {

			var ranges = cfiStr.split(",");

			if (ranges.length === 3) {
				return [ranges[1], ranges[2]];
			}

			return false;
		}
	}, {
		key: "getCharecterOffsetComponent",
		value: function getCharecterOffsetComponent(cfiStr) {
			var splitStr = cfiStr.split(":");
			return splitStr[1] || "";
		}
	}, {
		key: "joinSteps",
		value: function joinSteps(steps) {
			if (!steps) {
				return "";
			}

			return steps.map(function (part) {
				var segment = "";

				if (part.type === "element") {
					segment += (part.index + 1) * 2;
				}

				if (part.type === "text") {
					segment += 1 + 2 * part.index; // TODO: double check that this is odd
				}

				if (part.id) {
					segment += "[" + part.id + "]";
				}

				return segment;
			}).join("/");
		}
	}, {
		key: "segmentString",
		value: function segmentString(segment) {
			var segmentString = "/";

			segmentString += this.joinSteps(segment.steps);

			if (segment.terminal && segment.terminal.offset != null) {
				segmentString += ":" + segment.terminal.offset;
			}

			if (segment.terminal && segment.terminal.assertion != null) {
				segmentString += "[" + segment.terminal.assertion + "]";
			}

			return segmentString;
		}

		/**
   * Convert CFI to a epubcfi(...) string
   * @returns {string} epubcfi
   */

	}, {
		key: "toString",
		value: function toString() {
			var cfiString = "epubcfi(";

			cfiString += this.segmentString(this.base);

			cfiString += "!";
			cfiString += this.segmentString(this.path);

			// Add Range, if present
			if (this.range && this.start) {
				cfiString += ",";
				cfiString += this.segmentString(this.start);
			}

			if (this.range && this.end) {
				cfiString += ",";
				cfiString += this.segmentString(this.end);
			}

			cfiString += ")";

			return cfiString;
		}

		/**
   * Compare which of two CFIs is earlier in the text
   * @returns {number} First is earlier = -1, Second is earlier = 1, They are equal = 0
   */

	}, {
		key: "compare",
		value: function compare(cfiOne, cfiTwo) {
			var stepsA, stepsB;
			var terminalA, terminalB;

			var rangeAStartSteps, rangeAEndSteps;
			var rangeBEndSteps, rangeBEndSteps;
			var rangeAStartTerminal, rangeAEndTerminal;
			var rangeBStartTerminal, rangeBEndTerminal;

			if (typeof cfiOne === "string") {
				cfiOne = new EpubCFI(cfiOne);
			}
			if (typeof cfiTwo === "string") {
				cfiTwo = new EpubCFI(cfiTwo);
			}
			// Compare Spine Positions
			if (cfiOne.spinePos > cfiTwo.spinePos) {
				return 1;
			}
			if (cfiOne.spinePos < cfiTwo.spinePos) {
				return -1;
			}

			if (cfiOne.range) {
				stepsA = cfiOne.path.steps.concat(cfiOne.start.steps);
				terminalA = cfiOne.start.terminal;
			} else {
				stepsA = cfiOne.path.steps;
				terminalA = cfiOne.path.terminal;
			}

			if (cfiTwo.range) {
				stepsB = cfiTwo.path.steps.concat(cfiTwo.start.steps);
				terminalB = cfiTwo.start.terminal;
			} else {
				stepsB = cfiTwo.path.steps;
				terminalB = cfiTwo.path.terminal;
			}

			// Compare Each Step in the First item
			for (var i = 0; i < stepsA.length; i++) {
				if (!stepsA[i]) {
					return -1;
				}
				if (!stepsB[i]) {
					return 1;
				}
				if (stepsA[i].index > stepsB[i].index) {
					return 1;
				}
				if (stepsA[i].index < stepsB[i].index) {
					return -1;
				}
				// Otherwise continue checking
			}

			// All steps in First equal to Second and First is Less Specific
			if (stepsA.length < stepsB.length) {
				return -1;
			}

			// Compare the charecter offset of the text node
			if (terminalA.offset > terminalB.offset) {
				return 1;
			}
			if (terminalA.offset < terminalB.offset) {
				return -1;
			}

			// CFI's are equal
			return 0;
		}
	}, {
		key: "step",
		value: function step(node) {
			var nodeType = node.nodeType === TEXT_NODE ? "text" : "element";

			return {
				"id": node.id,
				"tagName": node.tagName,
				"type": nodeType,
				"index": this.position(node)
			};
		}
	}, {
		key: "filteredStep",
		value: function filteredStep(node, ignoreClass) {
			var filteredNode = this.filter(node, ignoreClass);
			var nodeType;

			// Node filtered, so ignore
			if (!filteredNode) {
				return;
			}

			// Otherwise add the filter node in
			nodeType = filteredNode.nodeType === TEXT_NODE ? "text" : "element";

			return {
				"id": filteredNode.id,
				"tagName": filteredNode.tagName,
				"type": nodeType,
				"index": this.filteredPosition(filteredNode, ignoreClass)
			};
		}
	}, {
		key: "pathTo",
		value: function pathTo(node, offset, ignoreClass) {
			var segment = {
				steps: [],
				terminal: {
					offset: null,
					assertion: null
				}
			};
			var currentNode = node;
			var step;

			while (currentNode && currentNode.parentNode && currentNode.parentNode.nodeType != DOCUMENT_NODE) {

				if (ignoreClass) {
					step = this.filteredStep(currentNode, ignoreClass);
				} else {
					step = this.step(currentNode);
				}

				if (step) {
					segment.steps.unshift(step);
				}

				currentNode = currentNode.parentNode;
			}

			if (offset != null && offset >= 0) {

				segment.terminal.offset = offset;

				// Make sure we are getting to a textNode if there is an offset
				if (segment.steps[segment.steps.length - 1].type != "text") {
					segment.steps.push({
						"type": "text",
						"index": 0
					});
				}
			}

			return segment;
		}
	}, {
		key: "equalStep",
		value: function equalStep(stepA, stepB) {
			if (!stepA || !stepB) {
				return false;
			}

			if (stepA.index === stepB.index && stepA.id === stepB.id && stepA.type === stepB.type) {
				return true;
			}

			return false;
		}

		/**
   * Create a CFI object from a Range
   * @param {Range} range
   * @param {string | object} base
   * @param {string} [ignoreClass]
   * @returns {object} cfi
   */

	}, {
		key: "fromRange",
		value: function fromRange(range, base, ignoreClass) {
			var cfi = {
				range: false,
				base: {},
				path: {},
				start: null,
				end: null
			};

			var start = range.startContainer;
			var end = range.endContainer;

			var startOffset = range.startOffset;
			var endOffset = range.endOffset;

			var needsIgnoring = false;

			if (ignoreClass) {
				// Tell pathTo if / what to ignore
				needsIgnoring = start.ownerDocument.querySelector("." + ignoreClass) != null;
			}

			if (typeof base === "string") {
				cfi.base = this.parseComponent(base);
				cfi.spinePos = cfi.base.steps[1].index;
			} else if ((typeof base === "undefined" ? "undefined" : _typeof(base)) === "object") {
				cfi.base = base;
			}

			if (range.collapsed) {
				if (needsIgnoring) {
					startOffset = this.patchOffset(start, startOffset, ignoreClass);
				}
				cfi.path = this.pathTo(start, startOffset, ignoreClass);
			} else {
				cfi.range = true;

				if (needsIgnoring) {
					startOffset = this.patchOffset(start, startOffset, ignoreClass);
				}

				cfi.start = this.pathTo(start, startOffset, ignoreClass);
				if (needsIgnoring) {
					endOffset = this.patchOffset(end, endOffset, ignoreClass);
				}

				cfi.end = this.pathTo(end, endOffset, ignoreClass);

				// Create a new empty path
				cfi.path = {
					steps: [],
					terminal: null
				};

				// Push steps that are shared between start and end to the common path
				var len = cfi.start.steps.length;
				var i;

				for (i = 0; i < len; i++) {
					if (this.equalStep(cfi.start.steps[i], cfi.end.steps[i])) {
						if (i === len - 1) {
							// Last step is equal, check terminals
							if (cfi.start.terminal === cfi.end.terminal) {
								// CFI's are equal
								cfi.path.steps.push(cfi.start.steps[i]);
								// Not a range
								cfi.range = false;
							}
						} else {
							cfi.path.steps.push(cfi.start.steps[i]);
						}
					} else {
						break;
					}
				}

				cfi.start.steps = cfi.start.steps.slice(cfi.path.steps.length);
				cfi.end.steps = cfi.end.steps.slice(cfi.path.steps.length);

				// TODO: Add Sanity check to make sure that the end if greater than the start
			}

			return cfi;
		}

		/**
   * Create a CFI object from a Node
   * @param {Node} anchor
   * @param {string | object} base
   * @param {string} [ignoreClass]
   * @returns {object} cfi
   */

	}, {
		key: "fromNode",
		value: function fromNode(anchor, base, ignoreClass) {
			var cfi = {
				range: false,
				base: {},
				path: {},
				start: null,
				end: null
			};

			if (typeof base === "string") {
				cfi.base = this.parseComponent(base);
				cfi.spinePos = cfi.base.steps[1].index;
			} else if ((typeof base === "undefined" ? "undefined" : _typeof(base)) === "object") {
				cfi.base = base;
			}

			cfi.path = this.pathTo(anchor, null, ignoreClass);

			return cfi;
		}
	}, {
		key: "filter",
		value: function filter(anchor, ignoreClass) {
			var needsIgnoring;
			var sibling; // to join with
			var parent, previousSibling, nextSibling;
			var isText = false;

			if (anchor.nodeType === TEXT_NODE) {
				isText = true;
				parent = anchor.parentNode;
				needsIgnoring = anchor.parentNode.classList.contains(ignoreClass);
			} else {
				isText = false;
				needsIgnoring = anchor.classList.contains(ignoreClass);
			}

			if (needsIgnoring && isText) {
				previousSibling = parent.previousSibling;
				nextSibling = parent.nextSibling;

				// If the sibling is a text node, join the nodes
				if (previousSibling && previousSibling.nodeType === TEXT_NODE) {
					sibling = previousSibling;
				} else if (nextSibling && nextSibling.nodeType === TEXT_NODE) {
					sibling = nextSibling;
				}

				if (sibling) {
					return sibling;
				} else {
					// Parent will be ignored on next step
					return anchor;
				}
			} else if (needsIgnoring && !isText) {
				// Otherwise just skip the element node
				return false;
			} else {
				// No need to filter
				return anchor;
			}
		}
	}, {
		key: "patchOffset",
		value: function patchOffset(anchor, offset, ignoreClass) {
			if (anchor.nodeType != TEXT_NODE) {
				throw new Error("Anchor must be a text node");
			}

			var curr = anchor;
			var totalOffset = offset;

			// If the parent is a ignored node, get offset from it's start
			if (anchor.parentNode.classList.contains(ignoreClass)) {
				curr = anchor.parentNode;
			}

			while (curr.previousSibling) {
				if (curr.previousSibling.nodeType === ELEMENT_NODE) {
					// Originally a text node, so join
					if (curr.previousSibling.classList.contains(ignoreClass)) {
						totalOffset += curr.previousSibling.textContent.length;
					} else {
						break; // Normal node, dont join
					}
				} else {
					// If the previous sibling is a text node, join the nodes
					totalOffset += curr.previousSibling.textContent.length;
				}

				curr = curr.previousSibling;
			}

			return totalOffset;
		}
	}, {
		key: "normalizedMap",
		value: function normalizedMap(children, nodeType, ignoreClass) {
			var output = {};
			var prevIndex = -1;
			var i,
			    len = children.length;
			var currNodeType;
			var prevNodeType;

			for (i = 0; i < len; i++) {

				currNodeType = children[i].nodeType;

				// Check if needs ignoring
				if (currNodeType === ELEMENT_NODE && children[i].classList.contains(ignoreClass)) {
					currNodeType = TEXT_NODE;
				}

				if (i > 0 && currNodeType === TEXT_NODE && prevNodeType === TEXT_NODE) {
					// join text nodes
					output[i] = prevIndex;
				} else if (nodeType === currNodeType) {
					prevIndex = prevIndex + 1;
					output[i] = prevIndex;
				}

				prevNodeType = currNodeType;
			}

			return output;
		}
	}, {
		key: "position",
		value: function position(anchor) {
			var children, index;
			if (anchor.nodeType === ELEMENT_NODE) {
				children = anchor.parentNode.children;
				if (!children) {
					children = (0, _core.findChildren)(anchor.parentNode);
				}
				index = Array.prototype.indexOf.call(children, anchor);
			} else {
				children = this.textNodes(anchor.parentNode);
				index = children.indexOf(anchor);
			}

			return index;
		}
	}, {
		key: "filteredPosition",
		value: function filteredPosition(anchor, ignoreClass) {
			var children, index, map;

			if (anchor.nodeType === ELEMENT_NODE) {
				children = anchor.parentNode.children;
				map = this.normalizedMap(children, ELEMENT_NODE, ignoreClass);
			} else {
				children = anchor.parentNode.childNodes;
				// Inside an ignored node
				if (anchor.parentNode.classList.contains(ignoreClass)) {
					anchor = anchor.parentNode;
					children = anchor.parentNode.childNodes;
				}
				map = this.normalizedMap(children, TEXT_NODE, ignoreClass);
			}

			index = Array.prototype.indexOf.call(children, anchor);

			return map[index];
		}
	}, {
		key: "stepsToXpath",
		value: function stepsToXpath(steps) {
			var xpath = [".", "*"];

			steps.forEach(function (step) {
				var position = step.index + 1;

				if (step.id) {
					xpath.push("*[position()=" + position + " and @id='" + step.id + "']");
				} else if (step.type === "text") {
					xpath.push("text()[" + position + "]");
				} else {
					xpath.push("*[" + position + "]");
				}
			});

			return xpath.join("/");
		}

		/*
  	To get the last step if needed:
  	// Get the terminal step
  lastStep = steps[steps.length-1];
  // Get the query string
  query = this.stepsToQuery(steps);
  // Find the containing element
  startContainerParent = doc.querySelector(query);
  // Find the text node within that element
  if(startContainerParent && lastStep.type == "text") {
  	container = startContainerParent.childNodes[lastStep.index];
  }
  */

	}, {
		key: "stepsToQuerySelector",
		value: function stepsToQuerySelector(steps) {
			var query = ["html"];

			steps.forEach(function (step) {
				var position = step.index + 1;

				if (step.id) {
					query.push("#" + step.id);
				} else if (step.type === "text") {
					// unsupported in querySelector
					// query.push("text()[" + position + "]");
				} else {
					query.push("*:nth-child(" + position + ")");
				}
			});

			return query.join(">");
		}
	}, {
		key: "textNodes",
		value: function textNodes(container, ignoreClass) {
			return Array.prototype.slice.call(container.childNodes).filter(function (node) {
				if (node.nodeType === TEXT_NODE) {
					return true;
				} else if (ignoreClass && node.classList.contains(ignoreClass)) {
					return true;
				}
				return false;
			});
		}
	}, {
		key: "walkToNode",
		value: function walkToNode(steps, _doc, ignoreClass) {
			var doc = _doc || document;
			var container = doc.documentElement;
			var children;
			var step;
			var len = steps.length;
			var i;

			for (i = 0; i < len; i++) {
				step = steps[i];

				if (step.type === "element") {
					//better to get a container using id as some times step.index may not be correct
					//For ex.https://github.com/futurepress/epub.js/issues/561
					if (step.id) {
						container = doc.getElementById(step.id);
					} else {
						children = container.children || (0, _core.findChildren)(container);
						container = children[step.index];
					}
				} else if (step.type === "text") {
					container = this.textNodes(container, ignoreClass)[step.index];
				}
				if (!container) {
					//Break the for loop as due to incorrect index we can get error if
					//container is undefined so that other functionailties works fine
					//like navigation
					break;
				}
			}

			return container;
		}
	}, {
		key: "findNode",
		value: function findNode(steps, _doc, ignoreClass) {
			var doc = _doc || document;
			var container;
			var xpath;

			if (!ignoreClass && typeof doc.evaluate != "undefined") {
				xpath = this.stepsToXpath(steps);
				container = doc.evaluate(xpath, doc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
			} else if (ignoreClass) {
				container = this.walkToNode(steps, doc, ignoreClass);
			} else {
				container = this.walkToNode(steps, doc);
			}

			return container;
		}
	}, {
		key: "fixMiss",
		value: function fixMiss(steps, offset, _doc, ignoreClass) {
			var container = this.findNode(steps.slice(0, -1), _doc, ignoreClass);
			var children = container.childNodes;
			var map = this.normalizedMap(children, TEXT_NODE, ignoreClass);
			var child;
			var len;
			var lastStepIndex = steps[steps.length - 1].index;

			for (var childIndex in map) {
				if (!map.hasOwnProperty(childIndex)) return;

				if (map[childIndex] === lastStepIndex) {
					child = children[childIndex];
					len = child.textContent.length;
					if (offset > len) {
						offset = offset - len;
					} else {
						if (child.nodeType === ELEMENT_NODE) {
							container = child.childNodes[0];
						} else {
							container = child;
						}
						break;
					}
				}
			}

			return {
				container: container,
				offset: offset
			};
		}

		/**
   * Creates a DOM range representing a CFI
   * @param {document} _doc document referenced in the base
   * @param {string} [ignoreClass]
   * @return {Range}
   */

	}, {
		key: "toRange",
		value: function toRange(_doc, ignoreClass) {
			var doc = _doc || document;
			var range;
			var start, end, startContainer, endContainer;
			var cfi = this;
			var startSteps, endSteps;
			var needsIgnoring = ignoreClass ? doc.querySelector("." + ignoreClass) != null : false;
			var missed;

			if (typeof doc.createRange !== "undefined") {
				range = doc.createRange();
			} else {
				range = new _core.RangeObject();
			}

			if (cfi.range) {
				start = cfi.start;
				startSteps = cfi.path.steps.concat(start.steps);
				startContainer = this.findNode(startSteps, doc, needsIgnoring ? ignoreClass : null);
				end = cfi.end;
				endSteps = cfi.path.steps.concat(end.steps);
				endContainer = this.findNode(endSteps, doc, needsIgnoring ? ignoreClass : null);
			} else {
				start = cfi.path;
				startSteps = cfi.path.steps;
				startContainer = this.findNode(cfi.path.steps, doc, needsIgnoring ? ignoreClass : null);
			}

			if (startContainer) {
				try {

					if (start.terminal.offset != null) {
						range.setStart(startContainer, start.terminal.offset);
					} else {
						range.setStart(startContainer, 0);
					}
				} catch (e) {
					missed = this.fixMiss(startSteps, start.terminal.offset, doc, needsIgnoring ? ignoreClass : null);
					range.setStart(missed.container, missed.offset);
				}
			} else {
				console.log("No startContainer found for", this.toString());
				// No start found
				return null;
			}

			if (endContainer) {
				try {

					if (end.terminal.offset != null) {
						range.setEnd(endContainer, end.terminal.offset);
					} else {
						range.setEnd(endContainer, 0);
					}
				} catch (e) {
					missed = this.fixMiss(endSteps, cfi.end.terminal.offset, doc, needsIgnoring ? ignoreClass : null);
					range.setEnd(missed.container, missed.offset);
				}
			}

			// doc.defaultView.getSelection().addRange(range);
			return range;
		}

		/**
   * Check if a string is wrapped with "epubcfi()"
   * @param {string} str
   * @returns {boolean}
   */

	}, {
		key: "isCfiString",
		value: function isCfiString(str) {
			if (typeof str === "string" && str.indexOf("epubcfi(") === 0 && str[str.length - 1] === ")") {
				return true;
			}

			return false;
		}
	}, {
		key: "generateChapterComponent",
		value: function generateChapterComponent(_spineNodeIndex, _pos, id) {
			var pos = parseInt(_pos),
			    spineNodeIndex = (_spineNodeIndex + 1) * 2,
			    cfi = "/" + spineNodeIndex + "/";

			cfi += (pos + 1) * 2;

			if (id) {
				cfi += "[" + id + "]";
			}

			return cfi;
		}

		/**
   * Collapse a CFI Range to a single CFI Position
   * @param {boolean} [toStart=false]
   */

	}, {
		key: "collapse",
		value: function collapse(toStart) {
			if (!this.range) {
				return;
			}

			this.range = false;

			if (toStart) {
				this.path.steps = this.path.steps.concat(this.start.steps);
				this.path.terminal = this.start.terminal;
			} else {
				this.path.steps = this.path.steps.concat(this.end.steps);
				this.path.terminal = this.end.terminal;
			}
		}
	}]);

	return EpubCFI;
}();

exports.default = EpubCFI;
module.exports = exports["default"];

/***/ }),
/* 23 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
var EPUBJS_VERSION = exports.EPUBJS_VERSION = "0.3";

// Dom events to listen for
var DOM_EVENTS = exports.DOM_EVENTS = ["keydown", "keyup", "keypressed", "mouseup", "mousedown", "click", "touchend", "touchstart", "touchmove"];

var EVENTS = exports.EVENTS = {
  BOOK: {
    OPEN_FAILED: "openFailed"
  },
  CONTENTS: {
    EXPAND: "expand",
    RESIZE: "resize",
    SELECTED: "selected",
    SELECTED_RANGE: "selectedRange",
    LINK_CLICKED: "linkClicked"
  },
  LOCATIONS: {
    CHANGED: "changed"
  },
  MANAGERS: {
    RESIZE: "resize",
    RESIZED: "resized",
    ORIENTATION_CHANGE: "orientationchange",
    ADDED: "added",
    SCROLL: "scroll",
    SCROLLED: "scrolled",
    REMOVED: "removed"
  },
  VIEWS: {
    AXIS: "axis",
    LOAD_ERROR: "loaderror",
    RENDERED: "rendered",
    RESIZED: "resized",
    DISPLAYED: "displayed",
    SHOWN: "shown",
    HIDDEN: "hidden",
    MARK_CLICKED: "markClicked"
  },
  RENDITION: {
    STARTED: "started",
    ATTACHED: "attached",
    DISPLAYED: "displayed",
    DISPLAY_ERROR: "displayerror",
    RENDERED: "rendered",
    REMOVED: "removed",
    RESIZED: "resized",
    ORIENTATION_CHANGE: "orientationchange",
    LOCATION_CHANGED: "locationChanged",
    RELOCATED: "relocated",
    MARK_CLICKED: "markClicked",
    SELECTED: "selected",
    LAYOUT: "layout"
  },
  LAYOUT: {
    UPDATED: "updated"
  },
  ANNOTATION: {
    ATTACH: "attach",
    DETACH: "detach"
  }
};

/***/ }),
/* 24 */
/***/ (function(module, exports) {

var core = module.exports = { version: '2.5.0' };
if (typeof __e == 'number') __e = core; // eslint-disable-line no-undef


/***/ }),
/* 25 */
/***/ (function(module, exports, __webpack_require__) {

// 7.1.1 ToPrimitive(input [, PreferredType])
var isObject = __webpack_require__(4);
// instead of the ES6 spec version, we didn't implement @@toPrimitive case
// and the second argument - flag - preferred type is a string
module.exports = function (it, S) {
  if (!isObject(it)) return it;
  var fn, val;
  if (S && typeof (fn = it.toString) == 'function' && !isObject(val = fn.call(it))) return val;
  if (typeof (fn = it.valueOf) == 'function' && !isObject(val = fn.call(it))) return val;
  if (!S && typeof (fn = it.toString) == 'function' && !isObject(val = fn.call(it))) return val;
  throw TypeError("Can't convert object to primitive value");
};


/***/ }),
/* 26 */
/***/ (function(module, exports) {

// 7.2.1 RequireObjectCoercible(argument)
module.exports = function (it) {
  if (it == undefined) throw TypeError("Can't call method on  " + it);
  return it;
};


/***/ }),
/* 27 */
/***/ (function(module, exports) {

// 7.1.4 ToInteger
var ceil = Math.ceil;
var floor = Math.floor;
module.exports = function (it) {
  return isNaN(it = +it) ? 0 : (it > 0 ? floor : ceil)(it);
};


/***/ }),
/* 28 */
/***/ (function(module, exports, __webpack_require__) {

// most Object methods by ES6 should accept primitives
var $export = __webpack_require__(0);
var core = __webpack_require__(24);
var fails = __webpack_require__(3);
module.exports = function (KEY, exec) {
  var fn = (core.Object || {})[KEY] || Object[KEY];
  var exp = {};
  exp[KEY] = exec(fn);
  $export($export.S + $export.F * fails(function () { fn(1); }), 'Object', exp);
};


/***/ }),
/* 29 */
/***/ (function(module, exports, __webpack_require__) {

// 0 -> Array#forEach
// 1 -> Array#map
// 2 -> Array#filter
// 3 -> Array#some
// 4 -> Array#every
// 5 -> Array#find
// 6 -> Array#findIndex
var ctx = __webpack_require__(19);
var IObject = __webpack_require__(52);
var toObject = __webpack_require__(10);
var toLength = __webpack_require__(9);
var asc = __webpack_require__(93);
module.exports = function (TYPE, $create) {
  var IS_MAP = TYPE == 1;
  var IS_FILTER = TYPE == 2;
  var IS_SOME = TYPE == 3;
  var IS_EVERY = TYPE == 4;
  var IS_FIND_INDEX = TYPE == 6;
  var NO_HOLES = TYPE == 5 || IS_FIND_INDEX;
  var create = $create || asc;
  return function ($this, callbackfn, that) {
    var O = toObject($this);
    var self = IObject(O);
    var f = ctx(callbackfn, that, 3);
    var length = toLength(self.length);
    var index = 0;
    var result = IS_MAP ? create($this, length) : IS_FILTER ? create($this, 0) : undefined;
    var val, res;
    for (;length > index; index++) if (NO_HOLES || index in self) {
      val = self[index];
      res = f(val, index, O);
      if (TYPE) {
        if (IS_MAP) result[index] = res;   // map
        else if (res) switch (TYPE) {
          case 3: return true;             // some
          case 5: return val;              // find
          case 6: return index;            // findIndex
          case 2: result.push(val);        // filter
        } else if (IS_EVERY) return false; // every
      }
    }
    return IS_FIND_INDEX ? -1 : IS_SOME || IS_EVERY ? IS_EVERY : result;
  };
};


/***/ }),
/* 30 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var d        = __webpack_require__(356)
  , callable = __webpack_require__(370)

  , apply = Function.prototype.apply, call = Function.prototype.call
  , create = Object.create, defineProperty = Object.defineProperty
  , defineProperties = Object.defineProperties
  , hasOwnProperty = Object.prototype.hasOwnProperty
  , descriptor = { configurable: true, enumerable: false, writable: true }

  , on, once, off, emit, methods, descriptors, base;

on = function (type, listener) {
	var data;

	callable(listener);

	if (!hasOwnProperty.call(this, '__ee__')) {
		data = descriptor.value = create(null);
		defineProperty(this, '__ee__', descriptor);
		descriptor.value = null;
	} else {
		data = this.__ee__;
	}
	if (!data[type]) data[type] = listener;
	else if (typeof data[type] === 'object') data[type].push(listener);
	else data[type] = [data[type], listener];

	return this;
};

once = function (type, listener) {
	var once, self;

	callable(listener);
	self = this;
	on.call(this, type, once = function () {
		off.call(self, type, once);
		apply.call(listener, this, arguments);
	});

	once.__eeOnceListener__ = listener;
	return this;
};

off = function (type, listener) {
	var data, listeners, candidate, i;

	callable(listener);

	if (!hasOwnProperty.call(this, '__ee__')) return this;
	data = this.__ee__;
	if (!data[type]) return this;
	listeners = data[type];

	if (typeof listeners === 'object') {
		for (i = 0; (candidate = listeners[i]); ++i) {
			if ((candidate === listener) ||
					(candidate.__eeOnceListener__ === listener)) {
				if (listeners.length === 2) data[type] = listeners[i ? 0 : 1];
				else listeners.splice(i, 1);
			}
		}
	} else {
		if ((listeners === listener) ||
				(listeners.__eeOnceListener__ === listener)) {
			delete data[type];
		}
	}

	return this;
};

emit = function (type) {
	var i, l, listener, listeners, args;

	if (!hasOwnProperty.call(this, '__ee__')) return;
	listeners = this.__ee__[type];
	if (!listeners) return;

	if (typeof listeners === 'object') {
		l = arguments.length;
		args = new Array(l - 1);
		for (i = 1; i < l; ++i) args[i - 1] = arguments[i];

		listeners = listeners.slice();
		for (i = 0; (listener = listeners[i]); ++i) {
			apply.call(listener, this, args);
		}
	} else {
		switch (arguments.length) {
		case 1:
			call.call(listeners, this);
			break;
		case 2:
			call.call(listeners, this, arguments[1]);
			break;
		case 3:
			call.call(listeners, this, arguments[1], arguments[2]);
			break;
		default:
			l = arguments.length;
			args = new Array(l - 1);
			for (i = 1; i < l; ++i) {
				args[i - 1] = arguments[i];
			}
			apply.call(listeners, this, args);
		}
	}
};

methods = {
	on: on,
	once: once,
	off: off,
	emit: emit
};

descriptors = {
	on: d(on),
	once: d(once),
	off: d(off),
	emit: d(emit)
};

base = defineProperties({}, descriptors);

module.exports = exports = function (o) {
	return (o == null) ? create(base) : defineProperties(Object(o), descriptors);
};
exports.methods = methods;


/***/ }),
/* 31 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

if (__webpack_require__(7)) {
  var LIBRARY = __webpack_require__(38);
  var global = __webpack_require__(2);
  var fails = __webpack_require__(3);
  var $export = __webpack_require__(0);
  var $typed = __webpack_require__(66);
  var $buffer = __webpack_require__(99);
  var ctx = __webpack_require__(19);
  var anInstance = __webpack_require__(43);
  var propertyDesc = __webpack_require__(36);
  var hide = __webpack_require__(13);
  var redefineAll = __webpack_require__(45);
  var toInteger = __webpack_require__(27);
  var toLength = __webpack_require__(9);
  var toIndex = __webpack_require__(132);
  var toAbsoluteIndex = __webpack_require__(39);
  var toPrimitive = __webpack_require__(25);
  var has = __webpack_require__(12);
  var classof = __webpack_require__(54);
  var isObject = __webpack_require__(4);
  var toObject = __webpack_require__(10);
  var isArrayIter = __webpack_require__(90);
  var create = __webpack_require__(40);
  var getPrototypeOf = __webpack_require__(18);
  var gOPN = __webpack_require__(41).f;
  var getIterFn = __webpack_require__(92);
  var uid = __webpack_require__(37);
  var wks = __webpack_require__(5);
  var createArrayMethod = __webpack_require__(29);
  var createArrayIncludes = __webpack_require__(56);
  var speciesConstructor = __webpack_require__(64);
  var ArrayIterators = __webpack_require__(95);
  var Iterators = __webpack_require__(50);
  var $iterDetect = __webpack_require__(61);
  var setSpecies = __webpack_require__(42);
  var arrayFill = __webpack_require__(94);
  var arrayCopyWithin = __webpack_require__(122);
  var $DP = __webpack_require__(8);
  var $GOPD = __webpack_require__(17);
  var dP = $DP.f;
  var gOPD = $GOPD.f;
  var RangeError = global.RangeError;
  var TypeError = global.TypeError;
  var Uint8Array = global.Uint8Array;
  var ARRAY_BUFFER = 'ArrayBuffer';
  var SHARED_BUFFER = 'Shared' + ARRAY_BUFFER;
  var BYTES_PER_ELEMENT = 'BYTES_PER_ELEMENT';
  var PROTOTYPE = 'prototype';
  var ArrayProto = Array[PROTOTYPE];
  var $ArrayBuffer = $buffer.ArrayBuffer;
  var $DataView = $buffer.DataView;
  var arrayForEach = createArrayMethod(0);
  var arrayFilter = createArrayMethod(2);
  var arraySome = createArrayMethod(3);
  var arrayEvery = createArrayMethod(4);
  var arrayFind = createArrayMethod(5);
  var arrayFindIndex = createArrayMethod(6);
  var arrayIncludes = createArrayIncludes(true);
  var arrayIndexOf = createArrayIncludes(false);
  var arrayValues = ArrayIterators.values;
  var arrayKeys = ArrayIterators.keys;
  var arrayEntries = ArrayIterators.entries;
  var arrayLastIndexOf = ArrayProto.lastIndexOf;
  var arrayReduce = ArrayProto.reduce;
  var arrayReduceRight = ArrayProto.reduceRight;
  var arrayJoin = ArrayProto.join;
  var arraySort = ArrayProto.sort;
  var arraySlice = ArrayProto.slice;
  var arrayToString = ArrayProto.toString;
  var arrayToLocaleString = ArrayProto.toLocaleString;
  var ITERATOR = wks('iterator');
  var TAG = wks('toStringTag');
  var TYPED_CONSTRUCTOR = uid('typed_constructor');
  var DEF_CONSTRUCTOR = uid('def_constructor');
  var ALL_CONSTRUCTORS = $typed.CONSTR;
  var TYPED_ARRAY = $typed.TYPED;
  var VIEW = $typed.VIEW;
  var WRONG_LENGTH = 'Wrong length!';

  var $map = createArrayMethod(1, function (O, length) {
    return allocate(speciesConstructor(O, O[DEF_CONSTRUCTOR]), length);
  });

  var LITTLE_ENDIAN = fails(function () {
    // eslint-disable-next-line no-undef
    return new Uint8Array(new Uint16Array([1]).buffer)[0] === 1;
  });

  var FORCED_SET = !!Uint8Array && !!Uint8Array[PROTOTYPE].set && fails(function () {
    new Uint8Array(1).set({});
  });

  var toOffset = function (it, BYTES) {
    var offset = toInteger(it);
    if (offset < 0 || offset % BYTES) throw RangeError('Wrong offset!');
    return offset;
  };

  var validate = function (it) {
    if (isObject(it) && TYPED_ARRAY in it) return it;
    throw TypeError(it + ' is not a typed array!');
  };

  var allocate = function (C, length) {
    if (!(isObject(C) && TYPED_CONSTRUCTOR in C)) {
      throw TypeError('It is not a typed array constructor!');
    } return new C(length);
  };

  var speciesFromList = function (O, list) {
    return fromList(speciesConstructor(O, O[DEF_CONSTRUCTOR]), list);
  };

  var fromList = function (C, list) {
    var index = 0;
    var length = list.length;
    var result = allocate(C, length);
    while (length > index) result[index] = list[index++];
    return result;
  };

  var addGetter = function (it, key, internal) {
    dP(it, key, { get: function () { return this._d[internal]; } });
  };

  var $from = function from(source /* , mapfn, thisArg */) {
    var O = toObject(source);
    var aLen = arguments.length;
    var mapfn = aLen > 1 ? arguments[1] : undefined;
    var mapping = mapfn !== undefined;
    var iterFn = getIterFn(O);
    var i, length, values, result, step, iterator;
    if (iterFn != undefined && !isArrayIter(iterFn)) {
      for (iterator = iterFn.call(O), values = [], i = 0; !(step = iterator.next()).done; i++) {
        values.push(step.value);
      } O = values;
    }
    if (mapping && aLen > 2) mapfn = ctx(mapfn, arguments[2], 2);
    for (i = 0, length = toLength(O.length), result = allocate(this, length); length > i; i++) {
      result[i] = mapping ? mapfn(O[i], i) : O[i];
    }
    return result;
  };

  var $of = function of(/* ...items */) {
    var index = 0;
    var length = arguments.length;
    var result = allocate(this, length);
    while (length > index) result[index] = arguments[index++];
    return result;
  };

  // iOS Safari 6.x fails here
  var TO_LOCALE_BUG = !!Uint8Array && fails(function () { arrayToLocaleString.call(new Uint8Array(1)); });

  var $toLocaleString = function toLocaleString() {
    return arrayToLocaleString.apply(TO_LOCALE_BUG ? arraySlice.call(validate(this)) : validate(this), arguments);
  };

  var proto = {
    copyWithin: function copyWithin(target, start /* , end */) {
      return arrayCopyWithin.call(validate(this), target, start, arguments.length > 2 ? arguments[2] : undefined);
    },
    every: function every(callbackfn /* , thisArg */) {
      return arrayEvery(validate(this), callbackfn, arguments.length > 1 ? arguments[1] : undefined);
    },
    fill: function fill(value /* , start, end */) { // eslint-disable-line no-unused-vars
      return arrayFill.apply(validate(this), arguments);
    },
    filter: function filter(callbackfn /* , thisArg */) {
      return speciesFromList(this, arrayFilter(validate(this), callbackfn,
        arguments.length > 1 ? arguments[1] : undefined));
    },
    find: function find(predicate /* , thisArg */) {
      return arrayFind(validate(this), predicate, arguments.length > 1 ? arguments[1] : undefined);
    },
    findIndex: function findIndex(predicate /* , thisArg */) {
      return arrayFindIndex(validate(this), predicate, arguments.length > 1 ? arguments[1] : undefined);
    },
    forEach: function forEach(callbackfn /* , thisArg */) {
      arrayForEach(validate(this), callbackfn, arguments.length > 1 ? arguments[1] : undefined);
    },
    indexOf: function indexOf(searchElement /* , fromIndex */) {
      return arrayIndexOf(validate(this), searchElement, arguments.length > 1 ? arguments[1] : undefined);
    },
    includes: function includes(searchElement /* , fromIndex */) {
      return arrayIncludes(validate(this), searchElement, arguments.length > 1 ? arguments[1] : undefined);
    },
    join: function join(separator) { // eslint-disable-line no-unused-vars
      return arrayJoin.apply(validate(this), arguments);
    },
    lastIndexOf: function lastIndexOf(searchElement /* , fromIndex */) { // eslint-disable-line no-unused-vars
      return arrayLastIndexOf.apply(validate(this), arguments);
    },
    map: function map(mapfn /* , thisArg */) {
      return $map(validate(this), mapfn, arguments.length > 1 ? arguments[1] : undefined);
    },
    reduce: function reduce(callbackfn /* , initialValue */) { // eslint-disable-line no-unused-vars
      return arrayReduce.apply(validate(this), arguments);
    },
    reduceRight: function reduceRight(callbackfn /* , initialValue */) { // eslint-disable-line no-unused-vars
      return arrayReduceRight.apply(validate(this), arguments);
    },
    reverse: function reverse() {
      var that = this;
      var length = validate(that).length;
      var middle = Math.floor(length / 2);
      var index = 0;
      var value;
      while (index < middle) {
        value = that[index];
        that[index++] = that[--length];
        that[length] = value;
      } return that;
    },
    some: function some(callbackfn /* , thisArg */) {
      return arraySome(validate(this), callbackfn, arguments.length > 1 ? arguments[1] : undefined);
    },
    sort: function sort(comparefn) {
      return arraySort.call(validate(this), comparefn);
    },
    subarray: function subarray(begin, end) {
      var O = validate(this);
      var length = O.length;
      var $begin = toAbsoluteIndex(begin, length);
      return new (speciesConstructor(O, O[DEF_CONSTRUCTOR]))(
        O.buffer,
        O.byteOffset + $begin * O.BYTES_PER_ELEMENT,
        toLength((end === undefined ? length : toAbsoluteIndex(end, length)) - $begin)
      );
    }
  };

  var $slice = function slice(start, end) {
    return speciesFromList(this, arraySlice.call(validate(this), start, end));
  };

  var $set = function set(arrayLike /* , offset */) {
    validate(this);
    var offset = toOffset(arguments[1], 1);
    var length = this.length;
    var src = toObject(arrayLike);
    var len = toLength(src.length);
    var index = 0;
    if (len + offset > length) throw RangeError(WRONG_LENGTH);
    while (index < len) this[offset + index] = src[index++];
  };

  var $iterators = {
    entries: function entries() {
      return arrayEntries.call(validate(this));
    },
    keys: function keys() {
      return arrayKeys.call(validate(this));
    },
    values: function values() {
      return arrayValues.call(validate(this));
    }
  };

  var isTAIndex = function (target, key) {
    return isObject(target)
      && target[TYPED_ARRAY]
      && typeof key != 'symbol'
      && key in target
      && String(+key) == String(key);
  };
  var $getDesc = function getOwnPropertyDescriptor(target, key) {
    return isTAIndex(target, key = toPrimitive(key, true))
      ? propertyDesc(2, target[key])
      : gOPD(target, key);
  };
  var $setDesc = function defineProperty(target, key, desc) {
    if (isTAIndex(target, key = toPrimitive(key, true))
      && isObject(desc)
      && has(desc, 'value')
      && !has(desc, 'get')
      && !has(desc, 'set')
      // TODO: add validation descriptor w/o calling accessors
      && !desc.configurable
      && (!has(desc, 'writable') || desc.writable)
      && (!has(desc, 'enumerable') || desc.enumerable)
    ) {
      target[key] = desc.value;
      return target;
    } return dP(target, key, desc);
  };

  if (!ALL_CONSTRUCTORS) {
    $GOPD.f = $getDesc;
    $DP.f = $setDesc;
  }

  $export($export.S + $export.F * !ALL_CONSTRUCTORS, 'Object', {
    getOwnPropertyDescriptor: $getDesc,
    defineProperty: $setDesc
  });

  if (fails(function () { arrayToString.call({}); })) {
    arrayToString = arrayToLocaleString = function toString() {
      return arrayJoin.call(this);
    };
  }

  var $TypedArrayPrototype$ = redefineAll({}, proto);
  redefineAll($TypedArrayPrototype$, $iterators);
  hide($TypedArrayPrototype$, ITERATOR, $iterators.values);
  redefineAll($TypedArrayPrototype$, {
    slice: $slice,
    set: $set,
    constructor: function () { /* noop */ },
    toString: arrayToString,
    toLocaleString: $toLocaleString
  });
  addGetter($TypedArrayPrototype$, 'buffer', 'b');
  addGetter($TypedArrayPrototype$, 'byteOffset', 'o');
  addGetter($TypedArrayPrototype$, 'byteLength', 'l');
  addGetter($TypedArrayPrototype$, 'length', 'e');
  dP($TypedArrayPrototype$, TAG, {
    get: function () { return this[TYPED_ARRAY]; }
  });

  // eslint-disable-next-line max-statements
  module.exports = function (KEY, BYTES, wrapper, CLAMPED) {
    CLAMPED = !!CLAMPED;
    var NAME = KEY + (CLAMPED ? 'Clamped' : '') + 'Array';
    var GETTER = 'get' + KEY;
    var SETTER = 'set' + KEY;
    var TypedArray = global[NAME];
    var Base = TypedArray || {};
    var TAC = TypedArray && getPrototypeOf(TypedArray);
    var FORCED = !TypedArray || !$typed.ABV;
    var O = {};
    var TypedArrayPrototype = TypedArray && TypedArray[PROTOTYPE];
    var getter = function (that, index) {
      var data = that._d;
      return data.v[GETTER](index * BYTES + data.o, LITTLE_ENDIAN);
    };
    var setter = function (that, index, value) {
      var data = that._d;
      if (CLAMPED) value = (value = Math.round(value)) < 0 ? 0 : value > 0xff ? 0xff : value & 0xff;
      data.v[SETTER](index * BYTES + data.o, value, LITTLE_ENDIAN);
    };
    var addElement = function (that, index) {
      dP(that, index, {
        get: function () {
          return getter(this, index);
        },
        set: function (value) {
          return setter(this, index, value);
        },
        enumerable: true
      });
    };
    if (FORCED) {
      TypedArray = wrapper(function (that, data, $offset, $length) {
        anInstance(that, TypedArray, NAME, '_d');
        var index = 0;
        var offset = 0;
        var buffer, byteLength, length, klass;
        if (!isObject(data)) {
          length = toIndex(data);
          byteLength = length * BYTES;
          buffer = new $ArrayBuffer(byteLength);
        } else if (data instanceof $ArrayBuffer || (klass = classof(data)) == ARRAY_BUFFER || klass == SHARED_BUFFER) {
          buffer = data;
          offset = toOffset($offset, BYTES);
          var $len = data.byteLength;
          if ($length === undefined) {
            if ($len % BYTES) throw RangeError(WRONG_LENGTH);
            byteLength = $len - offset;
            if (byteLength < 0) throw RangeError(WRONG_LENGTH);
          } else {
            byteLength = toLength($length) * BYTES;
            if (byteLength + offset > $len) throw RangeError(WRONG_LENGTH);
          }
          length = byteLength / BYTES;
        } else if (TYPED_ARRAY in data) {
          return fromList(TypedArray, data);
        } else {
          return $from.call(TypedArray, data);
        }
        hide(that, '_d', {
          b: buffer,
          o: offset,
          l: byteLength,
          e: length,
          v: new $DataView(buffer)
        });
        while (index < length) addElement(that, index++);
      });
      TypedArrayPrototype = TypedArray[PROTOTYPE] = create($TypedArrayPrototype$);
      hide(TypedArrayPrototype, 'constructor', TypedArray);
    } else if (!fails(function () {
      TypedArray(1);
    }) || !fails(function () {
      new TypedArray(-1); // eslint-disable-line no-new
    }) || !$iterDetect(function (iter) {
      new TypedArray(); // eslint-disable-line no-new
      new TypedArray(null); // eslint-disable-line no-new
      new TypedArray(1.5); // eslint-disable-line no-new
      new TypedArray(iter); // eslint-disable-line no-new
    }, true)) {
      TypedArray = wrapper(function (that, data, $offset, $length) {
        anInstance(that, TypedArray, NAME);
        var klass;
        // `ws` module bug, temporarily remove validation length for Uint8Array
        // https://github.com/websockets/ws/pull/645
        if (!isObject(data)) return new Base(toIndex(data));
        if (data instanceof $ArrayBuffer || (klass = classof(data)) == ARRAY_BUFFER || klass == SHARED_BUFFER) {
          return $length !== undefined
            ? new Base(data, toOffset($offset, BYTES), $length)
            : $offset !== undefined
              ? new Base(data, toOffset($offset, BYTES))
              : new Base(data);
        }
        if (TYPED_ARRAY in data) return fromList(TypedArray, data);
        return $from.call(TypedArray, data);
      });
      arrayForEach(TAC !== Function.prototype ? gOPN(Base).concat(gOPN(TAC)) : gOPN(Base), function (key) {
        if (!(key in TypedArray)) hide(TypedArray, key, Base[key]);
      });
      TypedArray[PROTOTYPE] = TypedArrayPrototype;
      if (!LIBRARY) TypedArrayPrototype.constructor = TypedArray;
    }
    var $nativeIterator = TypedArrayPrototype[ITERATOR];
    var CORRECT_ITER_NAME = !!$nativeIterator
      && ($nativeIterator.name == 'values' || $nativeIterator.name == undefined);
    var $iterator = $iterators.values;
    hide(TypedArray, TYPED_CONSTRUCTOR, true);
    hide(TypedArrayPrototype, TYPED_ARRAY, NAME);
    hide(TypedArrayPrototype, VIEW, true);
    hide(TypedArrayPrototype, DEF_CONSTRUCTOR, TypedArray);

    if (CLAMPED ? new TypedArray(1)[TAG] != NAME : !(TAG in TypedArrayPrototype)) {
      dP(TypedArrayPrototype, TAG, {
        get: function () { return NAME; }
      });
    }

    O[NAME] = TypedArray;

    $export($export.G + $export.W + $export.F * (TypedArray != Base), O);

    $export($export.S, NAME, {
      BYTES_PER_ELEMENT: BYTES
    });

    $export($export.S + $export.F * fails(function () { Base.of.call(TypedArray, 1); }), NAME, {
      from: $from,
      of: $of
    });

    if (!(BYTES_PER_ELEMENT in TypedArrayPrototype)) hide(TypedArrayPrototype, BYTES_PER_ELEMENT, BYTES);

    $export($export.P, NAME, proto);

    setSpecies(NAME);

    $export($export.P + $export.F * FORCED_SET, NAME, { set: $set });

    $export($export.P + $export.F * !CORRECT_ITER_NAME, NAME, $iterators);

    if (!LIBRARY && TypedArrayPrototype.toString != arrayToString) TypedArrayPrototype.toString = arrayToString;

    $export($export.P + $export.F * fails(function () {
      new TypedArray(1).slice();
    }), NAME, { slice: $slice });

    $export($export.P + $export.F * (fails(function () {
      return [1, 2].toLocaleString() != new TypedArray([1, 2]).toLocaleString();
    }) || !fails(function () {
      TypedArrayPrototype.toLocaleString.call([1, 2]);
    })), NAME, { toLocaleString: $toLocaleString });

    Iterators[NAME] = CORRECT_ITER_NAME ? $nativeIterator : $iterator;
    if (!LIBRARY && !CORRECT_ITER_NAME) hide(TypedArrayPrototype, ITERATOR, $iterator);
  };
} else module.exports = function () { /* empty */ };


/***/ }),
/* 32 */
/***/ (function(module, exports, __webpack_require__) {

var Map = __webpack_require__(127);
var $export = __webpack_require__(0);
var shared = __webpack_require__(55)('metadata');
var store = shared.store || (shared.store = new (__webpack_require__(130))());

var getOrCreateMetadataMap = function (target, targetKey, create) {
  var targetMetadata = store.get(target);
  if (!targetMetadata) {
    if (!create) return undefined;
    store.set(target, targetMetadata = new Map());
  }
  var keyMetadata = targetMetadata.get(targetKey);
  if (!keyMetadata) {
    if (!create) return undefined;
    targetMetadata.set(targetKey, keyMetadata = new Map());
  } return keyMetadata;
};
var ordinaryHasOwnMetadata = function (MetadataKey, O, P) {
  var metadataMap = getOrCreateMetadataMap(O, P, false);
  return metadataMap === undefined ? false : metadataMap.has(MetadataKey);
};
var ordinaryGetOwnMetadata = function (MetadataKey, O, P) {
  var metadataMap = getOrCreateMetadataMap(O, P, false);
  return metadataMap === undefined ? undefined : metadataMap.get(MetadataKey);
};
var ordinaryDefineOwnMetadata = function (MetadataKey, MetadataValue, O, P) {
  getOrCreateMetadataMap(O, P, true).set(MetadataKey, MetadataValue);
};
var ordinaryOwnMetadataKeys = function (target, targetKey) {
  var metadataMap = getOrCreateMetadataMap(target, targetKey, false);
  var keys = [];
  if (metadataMap) metadataMap.forEach(function (_, key) { keys.push(key); });
  return keys;
};
var toMetaKey = function (it) {
  return it === undefined || typeof it == 'symbol' ? it : String(it);
};
var exp = function (O) {
  $export($export.S, 'Reflect', O);
};

module.exports = {
  store: store,
  map: getOrCreateMetadataMap,
  has: ordinaryHasOwnMetadata,
  get: ordinaryGetOwnMetadata,
  set: ordinaryDefineOwnMetadata,
  keys: ordinaryOwnMetadataKeys,
  key: toMetaKey,
  exp: exp
};


/***/ }),
/* 33 */
/***/ (function(module, exports, __webpack_require__) {

var META = __webpack_require__(37)('meta');
var isObject = __webpack_require__(4);
var has = __webpack_require__(12);
var setDesc = __webpack_require__(8).f;
var id = 0;
var isExtensible = Object.isExtensible || function () {
  return true;
};
var FREEZE = !__webpack_require__(3)(function () {
  return isExtensible(Object.preventExtensions({}));
});
var setMeta = function (it) {
  setDesc(it, META, { value: {
    i: 'O' + ++id, // object ID
    w: {}          // weak collections IDs
  } });
};
var fastKey = function (it, create) {
  // return primitive with prefix
  if (!isObject(it)) return typeof it == 'symbol' ? it : (typeof it == 'string' ? 'S' : 'P') + it;
  if (!has(it, META)) {
    // can't set metadata to uncaught frozen object
    if (!isExtensible(it)) return 'F';
    // not necessary to add metadata
    if (!create) return 'E';
    // add missing metadata
    setMeta(it);
  // return object ID
  } return it[META].i;
};
var getWeak = function (it, create) {
  if (!has(it, META)) {
    // can't set metadata to uncaught frozen object
    if (!isExtensible(it)) return true;
    // not necessary to add metadata
    if (!create) return false;
    // add missing metadata
    setMeta(it);
  // return hash weak collections IDs
  } return it[META].w;
};
// add metadata on freeze-family methods calling
var onFreeze = function (it) {
  if (FREEZE && meta.NEED && isExtensible(it) && !has(it, META)) setMeta(it);
  return it;
};
var meta = module.exports = {
  KEY: META,
  NEED: false,
  fastKey: fastKey,
  getWeak: getWeak,
  onFreeze: onFreeze
};


/***/ }),
/* 34 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.14 / 15.2.3.14 Object.keys(O)
var $keys = __webpack_require__(109);
var enumBugKeys = __webpack_require__(77);

module.exports = Object.keys || function keys(O) {
  return $keys(O, enumBugKeys);
};


/***/ }),
/* 35 */
/***/ (function(module, exports, __webpack_require__) {

// 22.1.3.31 Array.prototype[@@unscopables]
var UNSCOPABLES = __webpack_require__(5)('unscopables');
var ArrayProto = Array.prototype;
if (ArrayProto[UNSCOPABLES] == undefined) __webpack_require__(13)(ArrayProto, UNSCOPABLES, {});
module.exports = function (key) {
  ArrayProto[UNSCOPABLES][key] = true;
};


/***/ }),
/* 36 */
/***/ (function(module, exports) {

module.exports = function (bitmap, value) {
  return {
    enumerable: !(bitmap & 1),
    configurable: !(bitmap & 2),
    writable: !(bitmap & 4),
    value: value
  };
};


/***/ }),
/* 37 */
/***/ (function(module, exports) {

var id = 0;
var px = Math.random();
module.exports = function (key) {
  return 'Symbol('.concat(key === undefined ? '' : key, ')_', (++id + px).toString(36));
};


/***/ }),
/* 38 */
/***/ (function(module, exports) {

module.exports = false;


/***/ }),
/* 39 */
/***/ (function(module, exports, __webpack_require__) {

var toInteger = __webpack_require__(27);
var max = Math.max;
var min = Math.min;
module.exports = function (index, length) {
  index = toInteger(index);
  return index < 0 ? max(index + length, 0) : min(index, length);
};


/***/ }),
/* 40 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.2 / 15.2.3.5 Object.create(O [, Properties])
var anObject = __webpack_require__(1);
var dPs = __webpack_require__(110);
var enumBugKeys = __webpack_require__(77);
var IE_PROTO = __webpack_require__(76)('IE_PROTO');
var Empty = function () { /* empty */ };
var PROTOTYPE = 'prototype';

// Create object with fake `null` prototype: use iframe Object with cleared prototype
var createDict = function () {
  // Thrash, waste and sodomy: IE GC bug
  var iframe = __webpack_require__(74)('iframe');
  var i = enumBugKeys.length;
  var lt = '<';
  var gt = '>';
  var iframeDocument;
  iframe.style.display = 'none';
  __webpack_require__(78).appendChild(iframe);
  iframe.src = 'javascript:'; // eslint-disable-line no-script-url
  // createDict = iframe.contentWindow.Object;
  // html.removeChild(iframe);
  iframeDocument = iframe.contentWindow.document;
  iframeDocument.open();
  iframeDocument.write(lt + 'script' + gt + 'document.F=Object' + lt + '/script' + gt);
  iframeDocument.close();
  createDict = iframeDocument.F;
  while (i--) delete createDict[PROTOTYPE][enumBugKeys[i]];
  return createDict();
};

module.exports = Object.create || function create(O, Properties) {
  var result;
  if (O !== null) {
    Empty[PROTOTYPE] = anObject(O);
    result = new Empty();
    Empty[PROTOTYPE] = null;
    // add "__proto__" for Object.getPrototypeOf polyfill
    result[IE_PROTO] = O;
  } else result = createDict();
  return Properties === undefined ? result : dPs(result, Properties);
};


/***/ }),
/* 41 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.7 / 15.2.3.4 Object.getOwnPropertyNames(O)
var $keys = __webpack_require__(109);
var hiddenKeys = __webpack_require__(77).concat('length', 'prototype');

exports.f = Object.getOwnPropertyNames || function getOwnPropertyNames(O) {
  return $keys(O, hiddenKeys);
};


/***/ }),
/* 42 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var global = __webpack_require__(2);
var dP = __webpack_require__(8);
var DESCRIPTORS = __webpack_require__(7);
var SPECIES = __webpack_require__(5)('species');

module.exports = function (KEY) {
  var C = global[KEY];
  if (DESCRIPTORS && C && !C[SPECIES]) dP.f(C, SPECIES, {
    configurable: true,
    get: function () { return this; }
  });
};


/***/ }),
/* 43 */
/***/ (function(module, exports) {

module.exports = function (it, Constructor, name, forbiddenField) {
  if (!(it instanceof Constructor) || (forbiddenField !== undefined && forbiddenField in it)) {
    throw TypeError(name + ': incorrect invocation!');
  } return it;
};


/***/ }),
/* 44 */
/***/ (function(module, exports, __webpack_require__) {

var ctx = __webpack_require__(19);
var call = __webpack_require__(120);
var isArrayIter = __webpack_require__(90);
var anObject = __webpack_require__(1);
var toLength = __webpack_require__(9);
var getIterFn = __webpack_require__(92);
var BREAK = {};
var RETURN = {};
var exports = module.exports = function (iterable, entries, fn, that, ITERATOR) {
  var iterFn = ITERATOR ? function () { return iterable; } : getIterFn(iterable);
  var f = ctx(fn, that, entries ? 2 : 1);
  var index = 0;
  var length, step, iterator, result;
  if (typeof iterFn != 'function') throw TypeError(iterable + ' is not iterable!');
  // fast case for arrays with default iterator
  if (isArrayIter(iterFn)) for (length = toLength(iterable.length); length > index; index++) {
    result = entries ? f(anObject(step = iterable[index])[0], step[1]) : f(iterable[index]);
    if (result === BREAK || result === RETURN) return result;
  } else for (iterator = iterFn.call(iterable); !(step = iterator.next()).done;) {
    result = call(iterator, f, step.value, entries);
    if (result === BREAK || result === RETURN) return result;
  }
};
exports.BREAK = BREAK;
exports.RETURN = RETURN;


/***/ }),
/* 45 */
/***/ (function(module, exports, __webpack_require__) {

var redefine = __webpack_require__(14);
module.exports = function (target, src, safe) {
  for (var key in src) redefine(target, key, src[key], safe);
  return target;
};


/***/ }),
/* 46 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _pathWebpack = __webpack_require__(71);

var _pathWebpack2 = _interopRequireDefault(_pathWebpack);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Creates a Path object for parsing and manipulation of a path strings
 *
 * Uses a polyfill for Nodejs path: https://nodejs.org/api/path.html
 * @param	{string} pathString	a url string (relative or absolute)
 * @class
 */
var Path = function () {
	function Path(pathString) {
		_classCallCheck(this, Path);

		var protocol;
		var parsed;

		protocol = pathString.indexOf("://");
		if (protocol > -1) {
			pathString = new URL(pathString).pathname;
		}

		parsed = this.parse(pathString);

		this.path = pathString;

		if (this.isDirectory(pathString)) {
			this.directory = pathString;
		} else {
			this.directory = parsed.dir + "/";
		}

		this.filename = parsed.base;
		this.extension = parsed.ext.slice(1);
	}

	/**
  * Parse the path: https://nodejs.org/api/path.html#path_path_parse_path
  * @param	{string} what
  * @returns {object}
  */


	_createClass(Path, [{
		key: "parse",
		value: function parse(what) {
			return _pathWebpack2.default.parse(what);
		}

		/**
   * @param	{string} what
   * @returns {boolean}
   */

	}, {
		key: "isAbsolute",
		value: function isAbsolute(what) {
			return _pathWebpack2.default.isAbsolute(what || this.path);
		}

		/**
   * Check if path ends with a directory
   * @param	{string} what
   * @returns {boolean}
   */

	}, {
		key: "isDirectory",
		value: function isDirectory(what) {
			return what.charAt(what.length - 1) === "/";
		}

		/**
   * Resolve a path against the directory of the Path
   *
   * https://nodejs.org/api/path.html#path_path_resolve_paths
   * @param	{string} what
   * @returns {string} resolved
   */

	}, {
		key: "resolve",
		value: function resolve(what) {
			return _pathWebpack2.default.resolve(this.directory, what);
		}

		/**
   * Resolve a path relative to the directory of the Path
   *
   * https://nodejs.org/api/path.html#path_path_relative_from_to
   * @param	{string} what
   * @returns {string} relative
   */

	}, {
		key: "relative",
		value: function relative(what) {
			var isAbsolute = what && what.indexOf("://") > -1;

			if (isAbsolute) {
				return what;
			}

			return _pathWebpack2.default.relative(this.directory, what);
		}
	}, {
		key: "splitPath",
		value: function splitPath(filename) {
			return this.splitPathRe.exec(filename).slice(1);
		}

		/**
   * Return the path string
   * @returns {string} path
   */

	}, {
		key: "toString",
		value: function toString() {
			return this.path;
		}
	}]);

	return Path;
}();

exports.default = Path;
module.exports = exports["default"];

/***/ }),
/* 47 */
/***/ (function(module, exports) {

var g;

// This works in non-strict mode
g = (function() {
	return this;
})();

try {
	// This works if eval is allowed (see CSP)
	g = g || Function("return this")() || (1,eval)("this");
} catch(e) {
	// This works if the window reference is available
	if(typeof window === "object")
		g = window;
}

// g can still be undefined, but nothing to do about it...
// We return undefined, instead of nothing here, so it's
// easier to handle this case. if(!global) { ...}

module.exports = g;


/***/ }),
/* 48 */
/***/ (function(module, exports, __webpack_require__) {

var def = __webpack_require__(8).f;
var has = __webpack_require__(12);
var TAG = __webpack_require__(5)('toStringTag');

module.exports = function (it, tag, stat) {
  if (it && !has(it = stat ? it : it.prototype, TAG)) def(it, TAG, { configurable: true, value: tag });
};


/***/ }),
/* 49 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(0);
var defined = __webpack_require__(26);
var fails = __webpack_require__(3);
var spaces = __webpack_require__(80);
var space = '[' + spaces + ']';
var non = '\u200b\u0085';
var ltrim = RegExp('^' + space + space + '*');
var rtrim = RegExp(space + space + '*$');

var exporter = function (KEY, exec, ALIAS) {
  var exp = {};
  var FORCE = fails(function () {
    return !!spaces[KEY]() || non[KEY]() != non;
  });
  var fn = exp[KEY] = FORCE ? exec(trim) : spaces[KEY];
  if (ALIAS) exp[ALIAS] = fn;
  $export($export.P + $export.F * FORCE, 'String', exp);
};

// 1 -> String#trimLeft
// 2 -> String#trimRight
// 3 -> String#trim
var trim = exporter.trim = function (string, TYPE) {
  string = String(defined(string));
  if (TYPE & 1) string = string.replace(ltrim, '');
  if (TYPE & 2) string = string.replace(rtrim, '');
  return string;
};

module.exports = exporter;


/***/ }),
/* 50 */
/***/ (function(module, exports) {

module.exports = {};


/***/ }),
/* 51 */
/***/ (function(module, exports, __webpack_require__) {

var isObject = __webpack_require__(4);
module.exports = function (it, TYPE) {
  if (!isObject(it) || it._t !== TYPE) throw TypeError('Incompatible receiver, ' + TYPE + ' required!');
  return it;
};


/***/ }),
/* 52 */
/***/ (function(module, exports, __webpack_require__) {

// fallback for non-array-like ES3 and non-enumerable old V8 strings
var cof = __webpack_require__(20);
// eslint-disable-next-line no-prototype-builtins
module.exports = Object('z').propertyIsEnumerable(0) ? Object : function (it) {
  return cof(it) == 'String' ? it.split('') : Object(it);
};


/***/ }),
/* 53 */
/***/ (function(module, exports) {

exports.f = {}.propertyIsEnumerable;


/***/ }),
/* 54 */
/***/ (function(module, exports, __webpack_require__) {

// getting tag from 19.1.3.6 Object.prototype.toString()
var cof = __webpack_require__(20);
var TAG = __webpack_require__(5)('toStringTag');
// ES3 wrong here
var ARG = cof(function () { return arguments; }()) == 'Arguments';

// fallback for IE11 Script Access Denied error
var tryGet = function (it, key) {
  try {
    return it[key];
  } catch (e) { /* empty */ }
};

module.exports = function (it) {
  var O, T, B;
  return it === undefined ? 'Undefined' : it === null ? 'Null'
    // @@toStringTag case
    : typeof (T = tryGet(O = Object(it), TAG)) == 'string' ? T
    // builtinTag case
    : ARG ? cof(O)
    // ES3 arguments fallback
    : (B = cof(O)) == 'Object' && typeof O.callee == 'function' ? 'Arguments' : B;
};


/***/ }),
/* 55 */
/***/ (function(module, exports, __webpack_require__) {

var global = __webpack_require__(2);
var SHARED = '__core-js_shared__';
var store = global[SHARED] || (global[SHARED] = {});
module.exports = function (key) {
  return store[key] || (store[key] = {});
};


/***/ }),
/* 56 */
/***/ (function(module, exports, __webpack_require__) {

// false -> Array#indexOf
// true  -> Array#includes
var toIObject = __webpack_require__(15);
var toLength = __webpack_require__(9);
var toAbsoluteIndex = __webpack_require__(39);
module.exports = function (IS_INCLUDES) {
  return function ($this, el, fromIndex) {
    var O = toIObject($this);
    var length = toLength(O.length);
    var index = toAbsoluteIndex(fromIndex, length);
    var value;
    // Array#includes uses SameValueZero equality algorithm
    // eslint-disable-next-line no-self-compare
    if (IS_INCLUDES && el != el) while (length > index) {
      value = O[index++];
      // eslint-disable-next-line no-self-compare
      if (value != value) return true;
    // Array#indexOf ignores holes, Array#includes - not
    } else for (;length > index; index++) if (IS_INCLUDES || index in O) {
      if (O[index] === el) return IS_INCLUDES || index || 0;
    } return !IS_INCLUDES && -1;
  };
};


/***/ }),
/* 57 */
/***/ (function(module, exports) {

exports.f = Object.getOwnPropertySymbols;


/***/ }),
/* 58 */
/***/ (function(module, exports, __webpack_require__) {

// 7.2.2 IsArray(argument)
var cof = __webpack_require__(20);
module.exports = Array.isArray || function isArray(arg) {
  return cof(arg) == 'Array';
};


/***/ }),
/* 59 */
/***/ (function(module, exports) {

// fast apply, http://jsperf.lnkit.com/fast-apply/5
module.exports = function (fn, args, that) {
  var un = that === undefined;
  switch (args.length) {
    case 0: return un ? fn()
                      : fn.call(that);
    case 1: return un ? fn(args[0])
                      : fn.call(that, args[0]);
    case 2: return un ? fn(args[0], args[1])
                      : fn.call(that, args[0], args[1]);
    case 3: return un ? fn(args[0], args[1], args[2])
                      : fn.call(that, args[0], args[1], args[2]);
    case 4: return un ? fn(args[0], args[1], args[2], args[3])
                      : fn.call(that, args[0], args[1], args[2], args[3]);
  } return fn.apply(that, args);
};


/***/ }),
/* 60 */
/***/ (function(module, exports, __webpack_require__) {

// 7.2.8 IsRegExp(argument)
var isObject = __webpack_require__(4);
var cof = __webpack_require__(20);
var MATCH = __webpack_require__(5)('match');
module.exports = function (it) {
  var isRegExp;
  return isObject(it) && ((isRegExp = it[MATCH]) !== undefined ? !!isRegExp : cof(it) == 'RegExp');
};


/***/ }),
/* 61 */
/***/ (function(module, exports, __webpack_require__) {

var ITERATOR = __webpack_require__(5)('iterator');
var SAFE_CLOSING = false;

try {
  var riter = [7][ITERATOR]();
  riter['return'] = function () { SAFE_CLOSING = true; };
  // eslint-disable-next-line no-throw-literal
  Array.from(riter, function () { throw 2; });
} catch (e) { /* empty */ }

module.exports = function (exec, skipClosing) {
  if (!skipClosing && !SAFE_CLOSING) return false;
  var safe = false;
  try {
    var arr = [7];
    var iter = arr[ITERATOR]();
    iter.next = function () { return { done: safe = true }; };
    arr[ITERATOR] = function () { return iter; };
    exec(arr);
  } catch (e) { /* empty */ }
  return safe;
};


/***/ }),
/* 62 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// 21.2.5.3 get RegExp.prototype.flags
var anObject = __webpack_require__(1);
module.exports = function () {
  var that = anObject(this);
  var result = '';
  if (that.global) result += 'g';
  if (that.ignoreCase) result += 'i';
  if (that.multiline) result += 'm';
  if (that.unicode) result += 'u';
  if (that.sticky) result += 'y';
  return result;
};


/***/ }),
/* 63 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var hide = __webpack_require__(13);
var redefine = __webpack_require__(14);
var fails = __webpack_require__(3);
var defined = __webpack_require__(26);
var wks = __webpack_require__(5);

module.exports = function (KEY, length, exec) {
  var SYMBOL = wks(KEY);
  var fns = exec(defined, SYMBOL, ''[KEY]);
  var strfn = fns[0];
  var rxfn = fns[1];
  if (fails(function () {
    var O = {};
    O[SYMBOL] = function () { return 7; };
    return ''[KEY](O) != 7;
  })) {
    redefine(String.prototype, KEY, strfn);
    hide(RegExp.prototype, SYMBOL, length == 2
      // 21.2.5.8 RegExp.prototype[@@replace](string, replaceValue)
      // 21.2.5.11 RegExp.prototype[@@split](string, limit)
      ? function (string, arg) { return rxfn.call(string, this, arg); }
      // 21.2.5.6 RegExp.prototype[@@match](string)
      // 21.2.5.9 RegExp.prototype[@@search](string)
      : function (string) { return rxfn.call(string, this); }
    );
  }
};


/***/ }),
/* 64 */
/***/ (function(module, exports, __webpack_require__) {

// 7.3.20 SpeciesConstructor(O, defaultConstructor)
var anObject = __webpack_require__(1);
var aFunction = __webpack_require__(11);
var SPECIES = __webpack_require__(5)('species');
module.exports = function (O, D) {
  var C = anObject(O).constructor;
  var S;
  return C === undefined || (S = anObject(C)[SPECIES]) == undefined ? D : aFunction(S);
};


/***/ }),
/* 65 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var global = __webpack_require__(2);
var $export = __webpack_require__(0);
var redefine = __webpack_require__(14);
var redefineAll = __webpack_require__(45);
var meta = __webpack_require__(33);
var forOf = __webpack_require__(44);
var anInstance = __webpack_require__(43);
var isObject = __webpack_require__(4);
var fails = __webpack_require__(3);
var $iterDetect = __webpack_require__(61);
var setToStringTag = __webpack_require__(48);
var inheritIfRequired = __webpack_require__(81);

module.exports = function (NAME, wrapper, methods, common, IS_MAP, IS_WEAK) {
  var Base = global[NAME];
  var C = Base;
  var ADDER = IS_MAP ? 'set' : 'add';
  var proto = C && C.prototype;
  var O = {};
  var fixMethod = function (KEY) {
    var fn = proto[KEY];
    redefine(proto, KEY,
      KEY == 'delete' ? function (a) {
        return IS_WEAK && !isObject(a) ? false : fn.call(this, a === 0 ? 0 : a);
      } : KEY == 'has' ? function has(a) {
        return IS_WEAK && !isObject(a) ? false : fn.call(this, a === 0 ? 0 : a);
      } : KEY == 'get' ? function get(a) {
        return IS_WEAK && !isObject(a) ? undefined : fn.call(this, a === 0 ? 0 : a);
      } : KEY == 'add' ? function add(a) { fn.call(this, a === 0 ? 0 : a); return this; }
        : function set(a, b) { fn.call(this, a === 0 ? 0 : a, b); return this; }
    );
  };
  if (typeof C != 'function' || !(IS_WEAK || proto.forEach && !fails(function () {
    new C().entries().next();
  }))) {
    // create collection constructor
    C = common.getConstructor(wrapper, NAME, IS_MAP, ADDER);
    redefineAll(C.prototype, methods);
    meta.NEED = true;
  } else {
    var instance = new C();
    // early implementations not supports chaining
    var HASNT_CHAINING = instance[ADDER](IS_WEAK ? {} : -0, 1) != instance;
    // V8 ~  Chromium 40- weak-collections throws on primitives, but should return false
    var THROWS_ON_PRIMITIVES = fails(function () { instance.has(1); });
    // most early implementations doesn't supports iterables, most modern - not close it correctly
    var ACCEPT_ITERABLES = $iterDetect(function (iter) { new C(iter); }); // eslint-disable-line no-new
    // for early implementations -0 and +0 not the same
    var BUGGY_ZERO = !IS_WEAK && fails(function () {
      // V8 ~ Chromium 42- fails only with 5+ elements
      var $instance = new C();
      var index = 5;
      while (index--) $instance[ADDER](index, index);
      return !$instance.has(-0);
    });
    if (!ACCEPT_ITERABLES) {
      C = wrapper(function (target, iterable) {
        anInstance(target, C, NAME);
        var that = inheritIfRequired(new Base(), target, C);
        if (iterable != undefined) forOf(iterable, IS_MAP, that[ADDER], that);
        return that;
      });
      C.prototype = proto;
      proto.constructor = C;
    }
    if (THROWS_ON_PRIMITIVES || BUGGY_ZERO) {
      fixMethod('delete');
      fixMethod('has');
      IS_MAP && fixMethod('get');
    }
    if (BUGGY_ZERO || HASNT_CHAINING) fixMethod(ADDER);
    // weak collections should not contains .clear method
    if (IS_WEAK && proto.clear) delete proto.clear;
  }

  setToStringTag(C, NAME);

  O[NAME] = C;
  $export($export.G + $export.W + $export.F * (C != Base), O);

  if (!IS_WEAK) common.setStrong(C, NAME, IS_MAP);

  return C;
};


/***/ }),
/* 66 */
/***/ (function(module, exports, __webpack_require__) {

var global = __webpack_require__(2);
var hide = __webpack_require__(13);
var uid = __webpack_require__(37);
var TYPED = uid('typed_array');
var VIEW = uid('view');
var ABV = !!(global.ArrayBuffer && global.DataView);
var CONSTR = ABV;
var i = 0;
var l = 9;
var Typed;

var TypedArrayConstructors = (
  'Int8Array,Uint8Array,Uint8ClampedArray,Int16Array,Uint16Array,Int32Array,Uint32Array,Float32Array,Float64Array'
).split(',');

while (i < l) {
  if (Typed = global[TypedArrayConstructors[i++]]) {
    hide(Typed.prototype, TYPED, true);
    hide(Typed.prototype, VIEW, true);
  } else CONSTR = false;
}

module.exports = {
  ABV: ABV,
  CONSTR: CONSTR,
  TYPED: TYPED,
  VIEW: VIEW
};


/***/ }),
/* 67 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// Forced replacement prototype accessors methods
module.exports = __webpack_require__(38) || !__webpack_require__(3)(function () {
  var K = Math.random();
  // In FF throws only define methods
  // eslint-disable-next-line no-undef, no-useless-call
  __defineSetter__.call(null, K, function () { /* empty */ });
  delete __webpack_require__(2)[K];
});


/***/ }),
/* 68 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// https://tc39.github.io/proposal-setmap-offrom/
var $export = __webpack_require__(0);

module.exports = function (COLLECTION) {
  $export($export.S, COLLECTION, { of: function of() {
    var length = arguments.length;
    var A = Array(length);
    while (length--) A[length] = arguments[length];
    return new this(A);
  } });
};


/***/ }),
/* 69 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// https://tc39.github.io/proposal-setmap-offrom/
var $export = __webpack_require__(0);
var aFunction = __webpack_require__(11);
var ctx = __webpack_require__(19);
var forOf = __webpack_require__(44);

module.exports = function (COLLECTION) {
  $export($export.S, COLLECTION, { from: function from(source /* , mapFn, thisArg */) {
    var mapFn = arguments[1];
    var mapping, A, n, cb;
    aFunction(this);
    mapping = mapFn !== undefined;
    if (mapping) aFunction(mapFn);
    if (source == undefined) return new this();
    A = [];
    if (mapping) {
      n = 0;
      cb = ctx(mapFn, arguments[2], 2);
      forOf(source, false, function (nextItem) {
        A.push(cb(nextItem, n++));
      });
    } else {
      forOf(source, false, A.push, A);
    }
    return new this(A);
  } });
};


/***/ }),
/* 70 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _path = __webpack_require__(46);

var _path2 = _interopRequireDefault(_path);

var _pathWebpack = __webpack_require__(71);

var _pathWebpack2 = _interopRequireDefault(_pathWebpack);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * creates a Url object for parsing and manipulation of a url string
 * @param	{string} urlString	a url string (relative or absolute)
 * @param	{string} [baseString] optional base for the url,
 * default to window.location.href
 */
var Url = function () {
	function Url(urlString, baseString) {
		_classCallCheck(this, Url);

		var absolute = urlString.indexOf("://") > -1;
		var pathname = urlString;
		var basePath;

		this.Url = undefined;
		this.href = urlString;
		this.protocol = "";
		this.origin = "";
		this.hash = "";
		this.hash = "";
		this.search = "";
		this.base = baseString;

		if (!absolute && baseString !== false && typeof baseString !== "string" && window && window.location) {
			this.base = window.location.href;
		}

		// URL Polyfill doesn't throw an error if base is empty
		if (absolute || this.base) {
			try {
				if (this.base) {
					// Safari doesn't like an undefined base
					this.Url = new URL(urlString, this.base);
				} else {
					this.Url = new URL(urlString);
				}
				this.href = this.Url.href;

				this.protocol = this.Url.protocol;
				this.origin = this.Url.origin;
				this.hash = this.Url.hash;
				this.search = this.Url.search;

				pathname = this.Url.pathname;
			} catch (e) {
				// Skip URL parsing
				this.Url = undefined;
				// resolve the pathname from the base
				if (this.base) {
					basePath = new _path2.default(this.base);
					pathname = basePath.resolve(pathname);
				}
			}
		}

		this.Path = new _path2.default(pathname);

		this.directory = this.Path.directory;
		this.filename = this.Path.filename;
		this.extension = this.Path.extension;
	}

	/**
  * @returns {Path}
  */


	_createClass(Url, [{
		key: "path",
		value: function path() {
			return this.Path;
		}

		/**
   * Resolves a relative path to a absolute url
   * @param {string} what
   * @returns {string} url
   */

	}, {
		key: "resolve",
		value: function resolve(what) {
			var isAbsolute = what.indexOf("://") > -1;
			var fullpath;

			if (isAbsolute) {
				return what;
			}

			fullpath = _pathWebpack2.default.resolve(this.directory, what);
			return this.origin + fullpath;
		}

		/**
   * Resolve a path relative to the url
   * @param {string} what
   * @returns {string} path
   */

	}, {
		key: "relative",
		value: function relative(what) {
			return _pathWebpack2.default.relative(what, this.directory);
		}

		/**
   * @returns {string}
   */

	}, {
		key: "toString",
		value: function toString() {
			return this.href;
		}
	}]);

	return Url;
}();

exports.default = Url;
module.exports = exports["default"];

/***/ }),
/* 71 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


if (!process) {
  var process = {
    "cwd" : function () { return '/' }
  };
}

function assertPath(path) {
  if (typeof path !== 'string') {
    throw new TypeError('Path must be a string. Received ' + path);
  }
}

// Resolves . and .. elements in a path with directory names
function normalizeStringPosix(path, allowAboveRoot) {
  var res = '';
  var lastSlash = -1;
  var dots = 0;
  var code;
  for (var i = 0; i <= path.length; ++i) {
    if (i < path.length)
      code = path.charCodeAt(i);
    else if (code === 47/*/*/)
      break;
    else
      code = 47/*/*/;
    if (code === 47/*/*/) {
      if (lastSlash === i - 1 || dots === 1) {
        // NOOP
      } else if (lastSlash !== i - 1 && dots === 2) {
        if (res.length < 2 ||
            res.charCodeAt(res.length - 1) !== 46/*.*/ ||
            res.charCodeAt(res.length - 2) !== 46/*.*/) {
          if (res.length > 2) {
            var start = res.length - 1;
            var j = start;
            for (; j >= 0; --j) {
              if (res.charCodeAt(j) === 47/*/*/)
                break;
            }
            if (j !== start) {
              if (j === -1)
                res = '';
              else
                res = res.slice(0, j);
              lastSlash = i;
              dots = 0;
              continue;
            }
          } else if (res.length === 2 || res.length === 1) {
            res = '';
            lastSlash = i;
            dots = 0;
            continue;
          }
        }
        if (allowAboveRoot) {
          if (res.length > 0)
            res += '/..';
          else
            res = '..';
        }
      } else {
        if (res.length > 0)
          res += '/' + path.slice(lastSlash + 1, i);
        else
          res = path.slice(lastSlash + 1, i);
      }
      lastSlash = i;
      dots = 0;
    } else if (code === 46/*.*/ && dots !== -1) {
      ++dots;
    } else {
      dots = -1;
    }
  }
  return res;
}

function _format(sep, pathObject) {
  var dir = pathObject.dir || pathObject.root;
  var base = pathObject.base ||
    ((pathObject.name || '') + (pathObject.ext || ''));
  if (!dir) {
    return base;
  }
  if (dir === pathObject.root) {
    return dir + base;
  }
  return dir + sep + base;
}

var posix = {
  // path.resolve([from ...], to)
  resolve: function resolve() {
    var resolvedPath = '';
    var resolvedAbsolute = false;
    var cwd;

    for (var i = arguments.length - 1; i >= -1 && !resolvedAbsolute; i--) {
      var path;
      if (i >= 0)
        path = arguments[i];
      else {
        if (cwd === undefined)
          cwd = process.cwd();
        path = cwd;
      }

      assertPath(path);

      // Skip empty entries
      if (path.length === 0) {
        continue;
      }

      resolvedPath = path + '/' + resolvedPath;
      resolvedAbsolute = path.charCodeAt(0) === 47/*/*/;
    }

    // At this point the path should be resolved to a full absolute path, but
    // handle relative paths to be safe (might happen when process.cwd() fails)

    // Normalize the path
    resolvedPath = normalizeStringPosix(resolvedPath, !resolvedAbsolute);

    if (resolvedAbsolute) {
      if (resolvedPath.length > 0)
        return '/' + resolvedPath;
      else
        return '/';
    } else if (resolvedPath.length > 0) {
      return resolvedPath;
    } else {
      return '.';
    }
  },


  normalize: function normalize(path) {
    assertPath(path);

    if (path.length === 0)
      return '.';

    var isAbsolute = path.charCodeAt(0) === 47/*/*/;
    var trailingSeparator = path.charCodeAt(path.length - 1) === 47/*/*/;

    // Normalize the path
    path = normalizeStringPosix(path, !isAbsolute);

    if (path.length === 0 && !isAbsolute)
      path = '.';
    if (path.length > 0 && trailingSeparator)
      path += '/';

    if (isAbsolute)
      return '/' + path;
    return path;
  },


  isAbsolute: function isAbsolute(path) {
    assertPath(path);
    return path.length > 0 && path.charCodeAt(0) === 47/*/*/;
  },


  join: function join() {
    if (arguments.length === 0)
      return '.';
    var joined;
    for (var i = 0; i < arguments.length; ++i) {
      var arg = arguments[i];
      assertPath(arg);
      if (arg.length > 0) {
        if (joined === undefined)
          joined = arg;
        else
          joined += '/' + arg;
      }
    }
    if (joined === undefined)
      return '.';
    return posix.normalize(joined);
  },


  relative: function relative(from, to) {
    assertPath(from);
    assertPath(to);

    if (from === to)
      return '';

    from = posix.resolve(from);
    to = posix.resolve(to);

    if (from === to)
      return '';

    // Trim any leading backslashes
    var fromStart = 1;
    for (; fromStart < from.length; ++fromStart) {
      if (from.charCodeAt(fromStart) !== 47/*/*/)
        break;
    }
    var fromEnd = from.length;
    var fromLen = (fromEnd - fromStart);

    // Trim any leading backslashes
    var toStart = 1;
    for (; toStart < to.length; ++toStart) {
      if (to.charCodeAt(toStart) !== 47/*/*/)
        break;
    }
    var toEnd = to.length;
    var toLen = (toEnd - toStart);

    // Compare paths to find the longest common path from root
    var length = (fromLen < toLen ? fromLen : toLen);
    var lastCommonSep = -1;
    var i = 0;
    for (; i <= length; ++i) {
      if (i === length) {
        if (toLen > length) {
          if (to.charCodeAt(toStart + i) === 47/*/*/) {
            // We get here if `from` is the exact base path for `to`.
            // For example: from='/foo/bar'; to='/foo/bar/baz'
            return to.slice(toStart + i + 1);
          } else if (i === 0) {
            // We get here if `from` is the root
            // For example: from='/'; to='/foo'
            return to.slice(toStart + i);
          }
        } else if (fromLen > length) {
          if (from.charCodeAt(fromStart + i) === 47/*/*/) {
            // We get here if `to` is the exact base path for `from`.
            // For example: from='/foo/bar/baz'; to='/foo/bar'
            lastCommonSep = i;
          } else if (i === 0) {
            // We get here if `to` is the root.
            // For example: from='/foo'; to='/'
            lastCommonSep = 0;
          }
        }
        break;
      }
      var fromCode = from.charCodeAt(fromStart + i);
      var toCode = to.charCodeAt(toStart + i);
      if (fromCode !== toCode)
        break;
      else if (fromCode === 47/*/*/)
        lastCommonSep = i;
    }

    var out = '';
    // Generate the relative path based on the path difference between `to`
    // and `from`
    for (i = fromStart + lastCommonSep + 1; i <= fromEnd; ++i) {
      if (i === fromEnd || from.charCodeAt(i) === 47/*/*/) {
        if (out.length === 0)
          out += '..';
        else
          out += '/..';
      }
    }

    // Lastly, append the rest of the destination (`to`) path that comes after
    // the common path parts
    if (out.length > 0)
      return out + to.slice(toStart + lastCommonSep);
    else {
      toStart += lastCommonSep;
      if (to.charCodeAt(toStart) === 47/*/*/)
        ++toStart;
      return to.slice(toStart);
    }
  },


  _makeLong: function _makeLong(path) {
    return path;
  },


  dirname: function dirname(path) {
    assertPath(path);
    if (path.length === 0)
      return '.';
    var code = path.charCodeAt(0);
    var hasRoot = (code === 47/*/*/);
    var end = -1;
    var matchedSlash = true;
    for (var i = path.length - 1; i >= 1; --i) {
      code = path.charCodeAt(i);
      if (code === 47/*/*/) {
        if (!matchedSlash) {
          end = i;
          break;
        }
      } else {
        // We saw the first non-path separator
        matchedSlash = false;
      }
    }

    if (end === -1)
      return hasRoot ? '/' : '.';
    if (hasRoot && end === 1)
      return '//';
    return path.slice(0, end);
  },


  basename: function basename(path, ext) {
    if (ext !== undefined && typeof ext !== 'string')
      throw new TypeError('"ext" argument must be a string');
    assertPath(path);

    var start = 0;
    var end = -1;
    var matchedSlash = true;
    var i;

    if (ext !== undefined && ext.length > 0 && ext.length <= path.length) {
      if (ext.length === path.length && ext === path)
        return '';
      var extIdx = ext.length - 1;
      var firstNonSlashEnd = -1;
      for (i = path.length - 1; i >= 0; --i) {
        var code = path.charCodeAt(i);
        if (code === 47/*/*/) {
          // If we reached a path separator that was not part of a set of path
          // separators at the end of the string, stop now
          if (!matchedSlash) {
            start = i + 1;
            break;
          }
        } else {
          if (firstNonSlashEnd === -1) {
            // We saw the first non-path separator, remember this index in case
            // we need it if the extension ends up not matching
            matchedSlash = false;
            firstNonSlashEnd = i + 1;
          }
          if (extIdx >= 0) {
            // Try to match the explicit extension
            if (code === ext.charCodeAt(extIdx)) {
              if (--extIdx === -1) {
                // We matched the extension, so mark this as the end of our path
                // component
                end = i;
              }
            } else {
              // Extension does not match, so our result is the entire path
              // component
              extIdx = -1;
              end = firstNonSlashEnd;
            }
          }
        }
      }

      if (start === end)
        end = firstNonSlashEnd;
      else if (end === -1)
        end = path.length;
      return path.slice(start, end);
    } else {
      for (i = path.length - 1; i >= 0; --i) {
        if (path.charCodeAt(i) === 47/*/*/) {
          // If we reached a path separator that was not part of a set of path
          // separators at the end of the string, stop now
          if (!matchedSlash) {
            start = i + 1;
            break;
          }
        } else if (end === -1) {
          // We saw the first non-path separator, mark this as the end of our
          // path component
          matchedSlash = false;
          end = i + 1;
        }
      }

      if (end === -1)
        return '';
      return path.slice(start, end);
    }
  },


  extname: function extname(path) {
    assertPath(path);
    var startDot = -1;
    var startPart = 0;
    var end = -1;
    var matchedSlash = true;
    // Track the state of characters (if any) we see before our first dot and
    // after any path separator we find
    var preDotState = 0;
    for (var i = path.length - 1; i >= 0; --i) {
      var code = path.charCodeAt(i);
      if (code === 47/*/*/) {
        // If we reached a path separator that was not part of a set of path
        // separators at the end of the string, stop now
        if (!matchedSlash) {
          startPart = i + 1;
          break;
        }
        continue;
      }
      if (end === -1) {
        // We saw the first non-path separator, mark this as the end of our
        // extension
        matchedSlash = false;
        end = i + 1;
      }
      if (code === 46/*.*/) {
        // If this is our first dot, mark it as the start of our extension
        if (startDot === -1)
          startDot = i;
        else if (preDotState !== 1)
          preDotState = 1;
      } else if (startDot !== -1) {
        // We saw a non-dot and non-path separator before our dot, so we should
        // have a good chance at having a non-empty extension
        preDotState = -1;
      }
    }

    if (startDot === -1 ||
        end === -1 ||
        // We saw a non-dot character immediately before the dot
        preDotState === 0 ||
        // The (right-most) trimmed path component is exactly '..'
        (preDotState === 1 &&
         startDot === end - 1 &&
         startDot === startPart + 1)) {
      return '';
    }
    return path.slice(startDot, end);
  },


  format: function format(pathObject) {
    if (pathObject === null || typeof pathObject !== 'object') {
      throw new TypeError(
        'Parameter "pathObject" must be an object, not ' + typeof(pathObject)
      );
    }
    return _format('/', pathObject);
  },


  parse: function parse(path) {
    assertPath(path);

    var ret = { root: '', dir: '', base: '', ext: '', name: '' };
    if (path.length === 0)
      return ret;
    var code = path.charCodeAt(0);
    var isAbsolute = (code === 47/*/*/);
    var start;
    if (isAbsolute) {
      ret.root = '/';
      start = 1;
    } else {
      start = 0;
    }
    var startDot = -1;
    var startPart = 0;
    var end = -1;
    var matchedSlash = true;
    var i = path.length - 1;

    // Track the state of characters (if any) we see before our first dot and
    // after any path separator we find
    var preDotState = 0;

    // Get non-dir info
    for (; i >= start; --i) {
      code = path.charCodeAt(i);
      if (code === 47/*/*/) {
        // If we reached a path separator that was not part of a set of path
        // separators at the end of the string, stop now
        if (!matchedSlash) {
          startPart = i + 1;
          break;
        }
        continue;
      }
      if (end === -1) {
        // We saw the first non-path separator, mark this as the end of our
        // extension
        matchedSlash = false;
        end = i + 1;
      }
      if (code === 46/*.*/) {
        // If this is our first dot, mark it as the start of our extension
        if (startDot === -1)
          startDot = i;
        else if (preDotState !== 1)
          preDotState = 1;
      } else if (startDot !== -1) {
        // We saw a non-dot and non-path separator before our dot, so we should
        // have a good chance at having a non-empty extension
        preDotState = -1;
      }
    }

    if (startDot === -1 ||
        end === -1 ||
        // We saw a non-dot character immediately before the dot
        preDotState === 0 ||
        // The (right-most) trimmed path component is exactly '..'
        (preDotState === 1 &&
         startDot === end - 1 &&
         startDot === startPart + 1)) {
      if (end !== -1) {
        if (startPart === 0 && isAbsolute)
          ret.base = ret.name = path.slice(1, end);
        else
          ret.base = ret.name = path.slice(startPart, end);
      }
    } else {
      if (startPart === 0 && isAbsolute) {
        ret.name = path.slice(1, startDot);
        ret.base = path.slice(1, end);
      } else {
        ret.name = path.slice(startPart, startDot);
        ret.base = path.slice(startPart, end);
      }
      ret.ext = path.slice(startDot, end);
    }

    if (startPart > 0)
      ret.dir = path.slice(0, startPart - 1);
    else if (isAbsolute)
      ret.dir = '/';

    return ret;
  },


  sep: '/',
  delimiter: ':',
  posix: null
};


module.exports = posix;


/***/ }),
/* 72 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});
exports.replaceBase = replaceBase;
exports.replaceCanonical = replaceCanonical;
exports.replaceMeta = replaceMeta;
exports.replaceLinks = replaceLinks;
exports.substitute = substitute;

var _core = __webpack_require__(6);

var _url = __webpack_require__(70);

var _url2 = _interopRequireDefault(_url);

var _path = __webpack_require__(46);

var _path2 = _interopRequireDefault(_path);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function replaceBase(doc, section) {
	var base;
	var head;
	var url = section.url;
	var absolute = url.indexOf("://") > -1;

	if (!doc) {
		return;
	}

	head = (0, _core.qs)(doc, "head");
	base = (0, _core.qs)(head, "base");

	if (!base) {
		base = doc.createElement("base");
		head.insertBefore(base, head.firstChild);
	}

	// Fix for Safari crashing if the url doesn't have an origin
	if (!absolute && window && window.location) {
		url = window.location.origin + url;
	}

	base.setAttribute("href", url);
}

function replaceCanonical(doc, section) {
	var head;
	var link;
	var url = section.canonical;

	if (!doc) {
		return;
	}

	head = (0, _core.qs)(doc, "head");
	link = (0, _core.qs)(head, "link[rel='canonical']");

	if (link) {
		link.setAttribute("href", url);
	} else {
		link = doc.createElement("link");
		link.setAttribute("rel", "canonical");
		link.setAttribute("href", url);
		head.appendChild(link);
	}
}

function replaceMeta(doc, section) {
	var head;
	var meta;
	var id = section.idref;
	if (!doc) {
		return;
	}

	head = (0, _core.qs)(doc, "head");
	meta = (0, _core.qs)(head, "link[property='dc.identifier']");

	if (meta) {
		meta.setAttribute("content", id);
	} else {
		meta = doc.createElement("meta");
		meta.setAttribute("name", "dc.identifier");
		meta.setAttribute("content", id);
		head.appendChild(meta);
	}
}

// TODO: move me to Contents
function replaceLinks(contents, fn) {

	var links = contents.querySelectorAll("a[href]");

	if (!links.length) {
		return;
	}

	var base = (0, _core.qs)(contents.ownerDocument, "base");
	var location = base ? base.getAttribute("href") : undefined;
	var replaceLink = function (link) {
		var href = link.getAttribute("href");

		if (href.indexOf("mailto:") === 0) {
			return;
		}

		var absolute = href.indexOf("://") > -1;

		if (absolute) {

			link.setAttribute("target", "_blank");
		} else {
			var linkUrl;
			try {
				linkUrl = new _url2.default(href, location);
			} catch (error) {
				// NOOP
			}

			link.onclick = function () {

				if (linkUrl && linkUrl.hash) {
					fn(linkUrl.Path.path + linkUrl.hash);
				} else if (linkUrl) {
					fn(linkUrl.Path.path);
				} else {
					fn(href);
				}

				return false;
			};
		}
	}.bind(this);

	for (var i = 0; i < links.length; i++) {
		replaceLink(links[i]);
	}
}

function substitute(content, urls, replacements) {
	urls.forEach(function (url, i) {
		if (url && replacements[i]) {
			content = content.replace(new RegExp(url, "g"), replacements[i]);
		}
	});
	return content;
}

/***/ }),
/* 73 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _core = __webpack_require__(6);

var _path = __webpack_require__(46);

var _path2 = _interopRequireDefault(_path);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function request(url, type, withCredentials, headers) {
	var supportsURL = typeof window != "undefined" ? window.URL : false; // TODO: fallback for url if window isn't defined
	var BLOB_RESPONSE = supportsURL ? "blob" : "arraybuffer";

	var deferred = new _core.defer();

	var xhr = new XMLHttpRequest();

	//-- Check from PDF.js:
	//   https://github.com/mozilla/pdf.js/blob/master/web/compatibility.js
	var xhrPrototype = XMLHttpRequest.prototype;

	var header;

	if (!("overrideMimeType" in xhrPrototype)) {
		// IE10 might have response, but not overrideMimeType
		Object.defineProperty(xhrPrototype, "overrideMimeType", {
			value: function xmlHttpRequestOverrideMimeType() {}
		});
	}

	if (withCredentials) {
		xhr.withCredentials = true;
	}

	xhr.onreadystatechange = handler;
	xhr.onerror = err;

	xhr.open("GET", url, true);

	for (header in headers) {
		xhr.setRequestHeader(header, headers[header]);
	}

	if (type == "json") {
		xhr.setRequestHeader("Accept", "application/json");
	}

	// If type isn"t set, determine it from the file extension
	if (!type) {
		type = new _path2.default(url).extension;
	}

	if (type == "blob") {
		xhr.responseType = BLOB_RESPONSE;
	}

	if ((0, _core.isXml)(type)) {
		// xhr.responseType = "document";
		xhr.overrideMimeType("text/xml"); // for OPF parsing
	}

	if (type == "xhtml") {
		// xhr.responseType = "document";
	}

	if (type == "html" || type == "htm") {
		// xhr.responseType = "document";
	}

	if (type == "binary") {
		xhr.responseType = "arraybuffer";
	}

	xhr.send();

	function err(e) {
		deferred.reject(e);
	}

	function handler() {
		if (this.readyState === XMLHttpRequest.DONE) {
			var responseXML = false;

			if (this.responseType === "" || this.responseType === "document") {
				responseXML = this.responseXML;
			}

			if (this.status === 200 || this.status === 0 || responseXML) {
				//-- Firefox is reporting 0 for blob urls
				var r;

				if (!this.response && !responseXML) {
					deferred.reject({
						status: this.status,
						message: "Empty Response",
						stack: new Error().stack
					});
					return deferred.promise;
				}

				if (this.status === 403) {
					deferred.reject({
						status: this.status,
						response: this.response,
						message: "Forbidden",
						stack: new Error().stack
					});
					return deferred.promise;
				}
				if (responseXML) {
					r = this.responseXML;
				} else if ((0, _core.isXml)(type)) {
					// xhr.overrideMimeType("text/xml"); // for OPF parsing
					// If this.responseXML wasn't set, try to parse using a DOMParser from text
					r = (0, _core.parse)(this.response, "text/xml");
				} else if (type == "xhtml") {
					r = (0, _core.parse)(this.response, "application/xhtml+xml");
				} else if (type == "html" || type == "htm") {
					r = (0, _core.parse)(this.response, "text/html");
				} else if (type == "json") {
					r = JSON.parse(this.response);
				} else if (type == "blob") {

					if (supportsURL) {
						r = this.response;
					} else {
						//-- Safari doesn't support responseType blob, so create a blob from arraybuffer
						r = new Blob([this.response]);
					}
				} else {
					r = this.response;
				}

				deferred.resolve(r);
			} else {

				deferred.reject({
					status: this.status,
					message: this.response,
					stack: new Error().stack
				});
			}
		}
	}

	return deferred.promise;
}

exports.default = request;
module.exports = exports["default"];

/***/ }),
/* 74 */
/***/ (function(module, exports, __webpack_require__) {

var isObject = __webpack_require__(4);
var document = __webpack_require__(2).document;
// typeof document.createElement is 'object' in old IE
var is = isObject(document) && isObject(document.createElement);
module.exports = function (it) {
  return is ? document.createElement(it) : {};
};


/***/ }),
/* 75 */
/***/ (function(module, exports, __webpack_require__) {

var global = __webpack_require__(2);
var core = __webpack_require__(24);
var LIBRARY = __webpack_require__(38);
var wksExt = __webpack_require__(108);
var defineProperty = __webpack_require__(8).f;
module.exports = function (name) {
  var $Symbol = core.Symbol || (core.Symbol = LIBRARY ? {} : global.Symbol || {});
  if (name.charAt(0) != '_' && !(name in $Symbol)) defineProperty($Symbol, name, { value: wksExt.f(name) });
};


/***/ }),
/* 76 */
/***/ (function(module, exports, __webpack_require__) {

var shared = __webpack_require__(55)('keys');
var uid = __webpack_require__(37);
module.exports = function (key) {
  return shared[key] || (shared[key] = uid(key));
};


/***/ }),
/* 77 */
/***/ (function(module, exports) {

// IE 8- don't enum bug keys
module.exports = (
  'constructor,hasOwnProperty,isPrototypeOf,propertyIsEnumerable,toLocaleString,toString,valueOf'
).split(',');


/***/ }),
/* 78 */
/***/ (function(module, exports, __webpack_require__) {

var document = __webpack_require__(2).document;
module.exports = document && document.documentElement;


/***/ }),
/* 79 */
/***/ (function(module, exports, __webpack_require__) {

// Works with __proto__ only. Old v8 can't work with null proto objects.
/* eslint-disable no-proto */
var isObject = __webpack_require__(4);
var anObject = __webpack_require__(1);
var check = function (O, proto) {
  anObject(O);
  if (!isObject(proto) && proto !== null) throw TypeError(proto + ": can't set as prototype!");
};
module.exports = {
  set: Object.setPrototypeOf || ('__proto__' in {} ? // eslint-disable-line
    function (test, buggy, set) {
      try {
        set = __webpack_require__(19)(Function.call, __webpack_require__(17).f(Object.prototype, '__proto__').set, 2);
        set(test, []);
        buggy = !(test instanceof Array);
      } catch (e) { buggy = true; }
      return function setPrototypeOf(O, proto) {
        check(O, proto);
        if (buggy) O.__proto__ = proto;
        else set(O, proto);
        return O;
      };
    }({}, false) : undefined),
  check: check
};


/***/ }),
/* 80 */
/***/ (function(module, exports) {

module.exports = '\x09\x0A\x0B\x0C\x0D\x20\xA0\u1680\u180E\u2000\u2001\u2002\u2003' +
  '\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u202F\u205F\u3000\u2028\u2029\uFEFF';


/***/ }),
/* 81 */
/***/ (function(module, exports, __webpack_require__) {

var isObject = __webpack_require__(4);
var setPrototypeOf = __webpack_require__(79).set;
module.exports = function (that, target, C) {
  var S = target.constructor;
  var P;
  if (S !== C && typeof S == 'function' && (P = S.prototype) !== C.prototype && isObject(P) && setPrototypeOf) {
    setPrototypeOf(that, P);
  } return that;
};


/***/ }),
/* 82 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var toInteger = __webpack_require__(27);
var defined = __webpack_require__(26);

module.exports = function repeat(count) {
  var str = String(defined(this));
  var res = '';
  var n = toInteger(count);
  if (n < 0 || n == Infinity) throw RangeError("Count can't be negative");
  for (;n > 0; (n >>>= 1) && (str += str)) if (n & 1) res += str;
  return res;
};


/***/ }),
/* 83 */
/***/ (function(module, exports) {

// 20.2.2.28 Math.sign(x)
module.exports = Math.sign || function sign(x) {
  // eslint-disable-next-line no-self-compare
  return (x = +x) == 0 || x != x ? x : x < 0 ? -1 : 1;
};


/***/ }),
/* 84 */
/***/ (function(module, exports) {

// 20.2.2.14 Math.expm1(x)
var $expm1 = Math.expm1;
module.exports = (!$expm1
  // Old FF bug
  || $expm1(10) > 22025.465794806719 || $expm1(10) < 22025.4657948067165168
  // Tor Browser bug
  || $expm1(-2e-17) != -2e-17
) ? function expm1(x) {
  return (x = +x) == 0 ? x : x > -1e-6 && x < 1e-6 ? x + x * x / 2 : Math.exp(x) - 1;
} : $expm1;


/***/ }),
/* 85 */
/***/ (function(module, exports, __webpack_require__) {

var toInteger = __webpack_require__(27);
var defined = __webpack_require__(26);
// true  -> String#at
// false -> String#codePointAt
module.exports = function (TO_STRING) {
  return function (that, pos) {
    var s = String(defined(that));
    var i = toInteger(pos);
    var l = s.length;
    var a, b;
    if (i < 0 || i >= l) return TO_STRING ? '' : undefined;
    a = s.charCodeAt(i);
    return a < 0xd800 || a > 0xdbff || i + 1 === l || (b = s.charCodeAt(i + 1)) < 0xdc00 || b > 0xdfff
      ? TO_STRING ? s.charAt(i) : a
      : TO_STRING ? s.slice(i, i + 2) : (a - 0xd800 << 10) + (b - 0xdc00) + 0x10000;
  };
};


/***/ }),
/* 86 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var LIBRARY = __webpack_require__(38);
var $export = __webpack_require__(0);
var redefine = __webpack_require__(14);
var hide = __webpack_require__(13);
var has = __webpack_require__(12);
var Iterators = __webpack_require__(50);
var $iterCreate = __webpack_require__(87);
var setToStringTag = __webpack_require__(48);
var getPrototypeOf = __webpack_require__(18);
var ITERATOR = __webpack_require__(5)('iterator');
var BUGGY = !([].keys && 'next' in [].keys()); // Safari has buggy iterators w/o `next`
var FF_ITERATOR = '@@iterator';
var KEYS = 'keys';
var VALUES = 'values';

var returnThis = function () { return this; };

module.exports = function (Base, NAME, Constructor, next, DEFAULT, IS_SET, FORCED) {
  $iterCreate(Constructor, NAME, next);
  var getMethod = function (kind) {
    if (!BUGGY && kind in proto) return proto[kind];
    switch (kind) {
      case KEYS: return function keys() { return new Constructor(this, kind); };
      case VALUES: return function values() { return new Constructor(this, kind); };
    } return function entries() { return new Constructor(this, kind); };
  };
  var TAG = NAME + ' Iterator';
  var DEF_VALUES = DEFAULT == VALUES;
  var VALUES_BUG = false;
  var proto = Base.prototype;
  var $native = proto[ITERATOR] || proto[FF_ITERATOR] || DEFAULT && proto[DEFAULT];
  var $default = $native || getMethod(DEFAULT);
  var $entries = DEFAULT ? !DEF_VALUES ? $default : getMethod('entries') : undefined;
  var $anyNative = NAME == 'Array' ? proto.entries || $native : $native;
  var methods, key, IteratorPrototype;
  // Fix native
  if ($anyNative) {
    IteratorPrototype = getPrototypeOf($anyNative.call(new Base()));
    if (IteratorPrototype !== Object.prototype && IteratorPrototype.next) {
      // Set @@toStringTag to native iterators
      setToStringTag(IteratorPrototype, TAG, true);
      // fix for some old engines
      if (!LIBRARY && !has(IteratorPrototype, ITERATOR)) hide(IteratorPrototype, ITERATOR, returnThis);
    }
  }
  // fix Array#{values, @@iterator}.name in V8 / FF
  if (DEF_VALUES && $native && $native.name !== VALUES) {
    VALUES_BUG = true;
    $default = function values() { return $native.call(this); };
  }
  // Define iterator
  if ((!LIBRARY || FORCED) && (BUGGY || VALUES_BUG || !proto[ITERATOR])) {
    hide(proto, ITERATOR, $default);
  }
  // Plug for library
  Iterators[NAME] = $default;
  Iterators[TAG] = returnThis;
  if (DEFAULT) {
    methods = {
      values: DEF_VALUES ? $default : getMethod(VALUES),
      keys: IS_SET ? $default : getMethod(KEYS),
      entries: $entries
    };
    if (FORCED) for (key in methods) {
      if (!(key in proto)) redefine(proto, key, methods[key]);
    } else $export($export.P + $export.F * (BUGGY || VALUES_BUG), NAME, methods);
  }
  return methods;
};


/***/ }),
/* 87 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var create = __webpack_require__(40);
var descriptor = __webpack_require__(36);
var setToStringTag = __webpack_require__(48);
var IteratorPrototype = {};

// 25.1.2.1.1 %IteratorPrototype%[@@iterator]()
__webpack_require__(13)(IteratorPrototype, __webpack_require__(5)('iterator'), function () { return this; });

module.exports = function (Constructor, NAME, next) {
  Constructor.prototype = create(IteratorPrototype, { next: descriptor(1, next) });
  setToStringTag(Constructor, NAME + ' Iterator');
};


/***/ }),
/* 88 */
/***/ (function(module, exports, __webpack_require__) {

// helper for String#{startsWith, endsWith, includes}
var isRegExp = __webpack_require__(60);
var defined = __webpack_require__(26);

module.exports = function (that, searchString, NAME) {
  if (isRegExp(searchString)) throw TypeError('String#' + NAME + " doesn't accept regex!");
  return String(defined(that));
};


/***/ }),
/* 89 */
/***/ (function(module, exports, __webpack_require__) {

var MATCH = __webpack_require__(5)('match');
module.exports = function (KEY) {
  var re = /./;
  try {
    '/./'[KEY](re);
  } catch (e) {
    try {
      re[MATCH] = false;
      return !'/./'[KEY](re);
    } catch (f) { /* empty */ }
  } return true;
};


/***/ }),
/* 90 */
/***/ (function(module, exports, __webpack_require__) {

// check on default Array iterator
var Iterators = __webpack_require__(50);
var ITERATOR = __webpack_require__(5)('iterator');
var ArrayProto = Array.prototype;

module.exports = function (it) {
  return it !== undefined && (Iterators.Array === it || ArrayProto[ITERATOR] === it);
};


/***/ }),
/* 91 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $defineProperty = __webpack_require__(8);
var createDesc = __webpack_require__(36);

module.exports = function (object, index, value) {
  if (index in object) $defineProperty.f(object, index, createDesc(0, value));
  else object[index] = value;
};


/***/ }),
/* 92 */
/***/ (function(module, exports, __webpack_require__) {

var classof = __webpack_require__(54);
var ITERATOR = __webpack_require__(5)('iterator');
var Iterators = __webpack_require__(50);
module.exports = __webpack_require__(24).getIteratorMethod = function (it) {
  if (it != undefined) return it[ITERATOR]
    || it['@@iterator']
    || Iterators[classof(it)];
};


/***/ }),
/* 93 */
/***/ (function(module, exports, __webpack_require__) {

// 9.4.2.3 ArraySpeciesCreate(originalArray, length)
var speciesConstructor = __webpack_require__(242);

module.exports = function (original, length) {
  return new (speciesConstructor(original))(length);
};


/***/ }),
/* 94 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
// 22.1.3.6 Array.prototype.fill(value, start = 0, end = this.length)

var toObject = __webpack_require__(10);
var toAbsoluteIndex = __webpack_require__(39);
var toLength = __webpack_require__(9);
module.exports = function fill(value /* , start = 0, end = @length */) {
  var O = toObject(this);
  var length = toLength(O.length);
  var aLen = arguments.length;
  var index = toAbsoluteIndex(aLen > 1 ? arguments[1] : undefined, length);
  var end = aLen > 2 ? arguments[2] : undefined;
  var endPos = end === undefined ? length : toAbsoluteIndex(end, length);
  while (endPos > index) O[index++] = value;
  return O;
};


/***/ }),
/* 95 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var addToUnscopables = __webpack_require__(35);
var step = __webpack_require__(123);
var Iterators = __webpack_require__(50);
var toIObject = __webpack_require__(15);

// 22.1.3.4 Array.prototype.entries()
// 22.1.3.13 Array.prototype.keys()
// 22.1.3.29 Array.prototype.values()
// 22.1.3.30 Array.prototype[@@iterator]()
module.exports = __webpack_require__(86)(Array, 'Array', function (iterated, kind) {
  this._t = toIObject(iterated); // target
  this._i = 0;                   // next index
  this._k = kind;                // kind
// 22.1.5.2.1 %ArrayIteratorPrototype%.next()
}, function () {
  var O = this._t;
  var kind = this._k;
  var index = this._i++;
  if (!O || index >= O.length) {
    this._t = undefined;
    return step(1);
  }
  if (kind == 'keys') return step(0, index);
  if (kind == 'values') return step(0, O[index]);
  return step(0, [index, O[index]]);
}, 'values');

// argumentsList[@@iterator] is %ArrayProto_values% (9.4.4.6, 9.4.4.7)
Iterators.Arguments = Iterators.Array;

addToUnscopables('keys');
addToUnscopables('values');
addToUnscopables('entries');


/***/ }),
/* 96 */
/***/ (function(module, exports, __webpack_require__) {

var ctx = __webpack_require__(19);
var invoke = __webpack_require__(59);
var html = __webpack_require__(78);
var cel = __webpack_require__(74);
var global = __webpack_require__(2);
var process = global.process;
var setTask = global.setImmediate;
var clearTask = global.clearImmediate;
var MessageChannel = global.MessageChannel;
var Dispatch = global.Dispatch;
var counter = 0;
var queue = {};
var ONREADYSTATECHANGE = 'onreadystatechange';
var defer, channel, port;
var run = function () {
  var id = +this;
  // eslint-disable-next-line no-prototype-builtins
  if (queue.hasOwnProperty(id)) {
    var fn = queue[id];
    delete queue[id];
    fn();
  }
};
var listener = function (event) {
  run.call(event.data);
};
// Node.js 0.9+ & IE10+ has setImmediate, otherwise:
if (!setTask || !clearTask) {
  setTask = function setImmediate(fn) {
    var args = [];
    var i = 1;
    while (arguments.length > i) args.push(arguments[i++]);
    queue[++counter] = function () {
      // eslint-disable-next-line no-new-func
      invoke(typeof fn == 'function' ? fn : Function(fn), args);
    };
    defer(counter);
    return counter;
  };
  clearTask = function clearImmediate(id) {
    delete queue[id];
  };
  // Node.js 0.8-
  if (__webpack_require__(20)(process) == 'process') {
    defer = function (id) {
      process.nextTick(ctx(run, id, 1));
    };
  // Sphere (JS game engine) Dispatch API
  } else if (Dispatch && Dispatch.now) {
    defer = function (id) {
      Dispatch.now(ctx(run, id, 1));
    };
  // Browsers with MessageChannel, includes WebWorkers
  } else if (MessageChannel) {
    channel = new MessageChannel();
    port = channel.port2;
    channel.port1.onmessage = listener;
    defer = ctx(port.postMessage, port, 1);
  // Browsers with postMessage, skip WebWorkers
  // IE8 has postMessage, but it's sync & typeof its postMessage is 'object'
  } else if (global.addEventListener && typeof postMessage == 'function' && !global.importScripts) {
    defer = function (id) {
      global.postMessage(id + '', '*');
    };
    global.addEventListener('message', listener, false);
  // IE8-
  } else if (ONREADYSTATECHANGE in cel('script')) {
    defer = function (id) {
      html.appendChild(cel('script'))[ONREADYSTATECHANGE] = function () {
        html.removeChild(this);
        run.call(id);
      };
    };
  // Rest old browsers
  } else {
    defer = function (id) {
      setTimeout(ctx(run, id, 1), 0);
    };
  }
}
module.exports = {
  set: setTask,
  clear: clearTask
};


/***/ }),
/* 97 */
/***/ (function(module, exports, __webpack_require__) {

var global = __webpack_require__(2);
var macrotask = __webpack_require__(96).set;
var Observer = global.MutationObserver || global.WebKitMutationObserver;
var process = global.process;
var Promise = global.Promise;
var isNode = __webpack_require__(20)(process) == 'process';

module.exports = function () {
  var head, last, notify;

  var flush = function () {
    var parent, fn;
    if (isNode && (parent = process.domain)) parent.exit();
    while (head) {
      fn = head.fn;
      head = head.next;
      try {
        fn();
      } catch (e) {
        if (head) notify();
        else last = undefined;
        throw e;
      }
    } last = undefined;
    if (parent) parent.enter();
  };

  // Node.js
  if (isNode) {
    notify = function () {
      process.nextTick(flush);
    };
  // browsers with MutationObserver
  } else if (Observer) {
    var toggle = true;
    var node = document.createTextNode('');
    new Observer(flush).observe(node, { characterData: true }); // eslint-disable-line no-new
    notify = function () {
      node.data = toggle = !toggle;
    };
  // environments with maybe non-completely correct, but existent Promise
  } else if (Promise && Promise.resolve) {
    var promise = Promise.resolve();
    notify = function () {
      promise.then(flush);
    };
  // for other environments - macrotask based on:
  // - setImmediate
  // - MessageChannel
  // - window.postMessag
  // - onreadystatechange
  // - setTimeout
  } else {
    notify = function () {
      // strange IE + webpack dev server bug - use .call(global)
      macrotask.call(global, flush);
    };
  }

  return function (fn) {
    var task = { fn: fn, next: undefined };
    if (last) last.next = task;
    if (!head) {
      head = task;
      notify();
    } last = task;
  };
};


/***/ }),
/* 98 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// 25.4.1.5 NewPromiseCapability(C)
var aFunction = __webpack_require__(11);

function PromiseCapability(C) {
  var resolve, reject;
  this.promise = new C(function ($$resolve, $$reject) {
    if (resolve !== undefined || reject !== undefined) throw TypeError('Bad Promise constructor');
    resolve = $$resolve;
    reject = $$reject;
  });
  this.resolve = aFunction(resolve);
  this.reject = aFunction(reject);
}

module.exports.f = function (C) {
  return new PromiseCapability(C);
};


/***/ }),
/* 99 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var global = __webpack_require__(2);
var DESCRIPTORS = __webpack_require__(7);
var LIBRARY = __webpack_require__(38);
var $typed = __webpack_require__(66);
var hide = __webpack_require__(13);
var redefineAll = __webpack_require__(45);
var fails = __webpack_require__(3);
var anInstance = __webpack_require__(43);
var toInteger = __webpack_require__(27);
var toLength = __webpack_require__(9);
var toIndex = __webpack_require__(132);
var gOPN = __webpack_require__(41).f;
var dP = __webpack_require__(8).f;
var arrayFill = __webpack_require__(94);
var setToStringTag = __webpack_require__(48);
var ARRAY_BUFFER = 'ArrayBuffer';
var DATA_VIEW = 'DataView';
var PROTOTYPE = 'prototype';
var WRONG_LENGTH = 'Wrong length!';
var WRONG_INDEX = 'Wrong index!';
var $ArrayBuffer = global[ARRAY_BUFFER];
var $DataView = global[DATA_VIEW];
var Math = global.Math;
var RangeError = global.RangeError;
// eslint-disable-next-line no-shadow-restricted-names
var Infinity = global.Infinity;
var BaseBuffer = $ArrayBuffer;
var abs = Math.abs;
var pow = Math.pow;
var floor = Math.floor;
var log = Math.log;
var LN2 = Math.LN2;
var BUFFER = 'buffer';
var BYTE_LENGTH = 'byteLength';
var BYTE_OFFSET = 'byteOffset';
var $BUFFER = DESCRIPTORS ? '_b' : BUFFER;
var $LENGTH = DESCRIPTORS ? '_l' : BYTE_LENGTH;
var $OFFSET = DESCRIPTORS ? '_o' : BYTE_OFFSET;

// IEEE754 conversions based on https://github.com/feross/ieee754
function packIEEE754(value, mLen, nBytes) {
  var buffer = Array(nBytes);
  var eLen = nBytes * 8 - mLen - 1;
  var eMax = (1 << eLen) - 1;
  var eBias = eMax >> 1;
  var rt = mLen === 23 ? pow(2, -24) - pow(2, -77) : 0;
  var i = 0;
  var s = value < 0 || value === 0 && 1 / value < 0 ? 1 : 0;
  var e, m, c;
  value = abs(value);
  // eslint-disable-next-line no-self-compare
  if (value != value || value === Infinity) {
    // eslint-disable-next-line no-self-compare
    m = value != value ? 1 : 0;
    e = eMax;
  } else {
    e = floor(log(value) / LN2);
    if (value * (c = pow(2, -e)) < 1) {
      e--;
      c *= 2;
    }
    if (e + eBias >= 1) {
      value += rt / c;
    } else {
      value += rt * pow(2, 1 - eBias);
    }
    if (value * c >= 2) {
      e++;
      c /= 2;
    }
    if (e + eBias >= eMax) {
      m = 0;
      e = eMax;
    } else if (e + eBias >= 1) {
      m = (value * c - 1) * pow(2, mLen);
      e = e + eBias;
    } else {
      m = value * pow(2, eBias - 1) * pow(2, mLen);
      e = 0;
    }
  }
  for (; mLen >= 8; buffer[i++] = m & 255, m /= 256, mLen -= 8);
  e = e << mLen | m;
  eLen += mLen;
  for (; eLen > 0; buffer[i++] = e & 255, e /= 256, eLen -= 8);
  buffer[--i] |= s * 128;
  return buffer;
}
function unpackIEEE754(buffer, mLen, nBytes) {
  var eLen = nBytes * 8 - mLen - 1;
  var eMax = (1 << eLen) - 1;
  var eBias = eMax >> 1;
  var nBits = eLen - 7;
  var i = nBytes - 1;
  var s = buffer[i--];
  var e = s & 127;
  var m;
  s >>= 7;
  for (; nBits > 0; e = e * 256 + buffer[i], i--, nBits -= 8);
  m = e & (1 << -nBits) - 1;
  e >>= -nBits;
  nBits += mLen;
  for (; nBits > 0; m = m * 256 + buffer[i], i--, nBits -= 8);
  if (e === 0) {
    e = 1 - eBias;
  } else if (e === eMax) {
    return m ? NaN : s ? -Infinity : Infinity;
  } else {
    m = m + pow(2, mLen);
    e = e - eBias;
  } return (s ? -1 : 1) * m * pow(2, e - mLen);
}

function unpackI32(bytes) {
  return bytes[3] << 24 | bytes[2] << 16 | bytes[1] << 8 | bytes[0];
}
function packI8(it) {
  return [it & 0xff];
}
function packI16(it) {
  return [it & 0xff, it >> 8 & 0xff];
}
function packI32(it) {
  return [it & 0xff, it >> 8 & 0xff, it >> 16 & 0xff, it >> 24 & 0xff];
}
function packF64(it) {
  return packIEEE754(it, 52, 8);
}
function packF32(it) {
  return packIEEE754(it, 23, 4);
}

function addGetter(C, key, internal) {
  dP(C[PROTOTYPE], key, { get: function () { return this[internal]; } });
}

function get(view, bytes, index, isLittleEndian) {
  var numIndex = +index;
  var intIndex = toIndex(numIndex);
  if (intIndex + bytes > view[$LENGTH]) throw RangeError(WRONG_INDEX);
  var store = view[$BUFFER]._b;
  var start = intIndex + view[$OFFSET];
  var pack = store.slice(start, start + bytes);
  return isLittleEndian ? pack : pack.reverse();
}
function set(view, bytes, index, conversion, value, isLittleEndian) {
  var numIndex = +index;
  var intIndex = toIndex(numIndex);
  if (intIndex + bytes > view[$LENGTH]) throw RangeError(WRONG_INDEX);
  var store = view[$BUFFER]._b;
  var start = intIndex + view[$OFFSET];
  var pack = conversion(+value);
  for (var i = 0; i < bytes; i++) store[start + i] = pack[isLittleEndian ? i : bytes - i - 1];
}

if (!$typed.ABV) {
  $ArrayBuffer = function ArrayBuffer(length) {
    anInstance(this, $ArrayBuffer, ARRAY_BUFFER);
    var byteLength = toIndex(length);
    this._b = arrayFill.call(Array(byteLength), 0);
    this[$LENGTH] = byteLength;
  };

  $DataView = function DataView(buffer, byteOffset, byteLength) {
    anInstance(this, $DataView, DATA_VIEW);
    anInstance(buffer, $ArrayBuffer, DATA_VIEW);
    var bufferLength = buffer[$LENGTH];
    var offset = toInteger(byteOffset);
    if (offset < 0 || offset > bufferLength) throw RangeError('Wrong offset!');
    byteLength = byteLength === undefined ? bufferLength - offset : toLength(byteLength);
    if (offset + byteLength > bufferLength) throw RangeError(WRONG_LENGTH);
    this[$BUFFER] = buffer;
    this[$OFFSET] = offset;
    this[$LENGTH] = byteLength;
  };

  if (DESCRIPTORS) {
    addGetter($ArrayBuffer, BYTE_LENGTH, '_l');
    addGetter($DataView, BUFFER, '_b');
    addGetter($DataView, BYTE_LENGTH, '_l');
    addGetter($DataView, BYTE_OFFSET, '_o');
  }

  redefineAll($DataView[PROTOTYPE], {
    getInt8: function getInt8(byteOffset) {
      return get(this, 1, byteOffset)[0] << 24 >> 24;
    },
    getUint8: function getUint8(byteOffset) {
      return get(this, 1, byteOffset)[0];
    },
    getInt16: function getInt16(byteOffset /* , littleEndian */) {
      var bytes = get(this, 2, byteOffset, arguments[1]);
      return (bytes[1] << 8 | bytes[0]) << 16 >> 16;
    },
    getUint16: function getUint16(byteOffset /* , littleEndian */) {
      var bytes = get(this, 2, byteOffset, arguments[1]);
      return bytes[1] << 8 | bytes[0];
    },
    getInt32: function getInt32(byteOffset /* , littleEndian */) {
      return unpackI32(get(this, 4, byteOffset, arguments[1]));
    },
    getUint32: function getUint32(byteOffset /* , littleEndian */) {
      return unpackI32(get(this, 4, byteOffset, arguments[1])) >>> 0;
    },
    getFloat32: function getFloat32(byteOffset /* , littleEndian */) {
      return unpackIEEE754(get(this, 4, byteOffset, arguments[1]), 23, 4);
    },
    getFloat64: function getFloat64(byteOffset /* , littleEndian */) {
      return unpackIEEE754(get(this, 8, byteOffset, arguments[1]), 52, 8);
    },
    setInt8: function setInt8(byteOffset, value) {
      set(this, 1, byteOffset, packI8, value);
    },
    setUint8: function setUint8(byteOffset, value) {
      set(this, 1, byteOffset, packI8, value);
    },
    setInt16: function setInt16(byteOffset, value /* , littleEndian */) {
      set(this, 2, byteOffset, packI16, value, arguments[2]);
    },
    setUint16: function setUint16(byteOffset, value /* , littleEndian */) {
      set(this, 2, byteOffset, packI16, value, arguments[2]);
    },
    setInt32: function setInt32(byteOffset, value /* , littleEndian */) {
      set(this, 4, byteOffset, packI32, value, arguments[2]);
    },
    setUint32: function setUint32(byteOffset, value /* , littleEndian */) {
      set(this, 4, byteOffset, packI32, value, arguments[2]);
    },
    setFloat32: function setFloat32(byteOffset, value /* , littleEndian */) {
      set(this, 4, byteOffset, packF32, value, arguments[2]);
    },
    setFloat64: function setFloat64(byteOffset, value /* , littleEndian */) {
      set(this, 8, byteOffset, packF64, value, arguments[2]);
    }
  });
} else {
  if (!fails(function () {
    $ArrayBuffer(1);
  }) || !fails(function () {
    new $ArrayBuffer(-1); // eslint-disable-line no-new
  }) || fails(function () {
    new $ArrayBuffer(); // eslint-disable-line no-new
    new $ArrayBuffer(1.5); // eslint-disable-line no-new
    new $ArrayBuffer(NaN); // eslint-disable-line no-new
    return $ArrayBuffer.name != ARRAY_BUFFER;
  })) {
    $ArrayBuffer = function ArrayBuffer(length) {
      anInstance(this, $ArrayBuffer);
      return new BaseBuffer(toIndex(length));
    };
    var ArrayBufferProto = $ArrayBuffer[PROTOTYPE] = BaseBuffer[PROTOTYPE];
    for (var keys = gOPN(BaseBuffer), j = 0, key; keys.length > j;) {
      if (!((key = keys[j++]) in $ArrayBuffer)) hide($ArrayBuffer, key, BaseBuffer[key]);
    }
    if (!LIBRARY) ArrayBufferProto.constructor = $ArrayBuffer;
  }
  // iOS Safari 7.x bug
  var view = new $DataView(new $ArrayBuffer(2));
  var $setInt8 = $DataView[PROTOTYPE].setInt8;
  view.setInt8(0, 2147483648);
  view.setInt8(1, 2147483649);
  if (view.getInt8(0) || !view.getInt8(1)) redefineAll($DataView[PROTOTYPE], {
    setInt8: function setInt8(byteOffset, value) {
      $setInt8.call(this, byteOffset, value << 24 >> 24);
    },
    setUint8: function setUint8(byteOffset, value) {
      $setInt8.call(this, byteOffset, value << 24 >> 24);
    }
  }, true);
}
setToStringTag($ArrayBuffer, ARRAY_BUFFER);
setToStringTag($DataView, DATA_VIEW);
hide($DataView[PROTOTYPE], $typed.VIEW, true);
exports[ARRAY_BUFFER] = $ArrayBuffer;
exports[DATA_VIEW] = $DataView;


/***/ }),
/* 100 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _undefined = __webpack_require__(363)(); // Support ES3 engines

module.exports = function (val) {
 return (val !== _undefined) && (val !== null);
};


/***/ }),
/* 101 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Hooks allow for injecting functions that must all complete in order before finishing
 * They will execute in parallel but all must finish before continuing
 * Functions may return a promise if they are asycn.
 * @param {any} context scope of this
 * @example this.content = new EPUBJS.Hook(this);
 */
var Hook = function () {
	function Hook(context) {
		_classCallCheck(this, Hook);

		this.context = context || this;
		this.hooks = [];
	}

	/**
  * Adds a function to be run before a hook completes
  * @example this.content.register(function(){...});
  */


	_createClass(Hook, [{
		key: "register",
		value: function register() {
			for (var i = 0; i < arguments.length; ++i) {
				if (typeof arguments[i] === "function") {
					this.hooks.push(arguments[i]);
				} else {
					// unpack array
					for (var j = 0; j < arguments[i].length; ++j) {
						this.hooks.push(arguments[i][j]);
					}
				}
			}
		}

		/**
   * Removes a function
   * @example this.content.deregister(function(){...});
   */

	}, {
		key: "deregister",
		value: function deregister(func) {
			var hook = void 0;
			for (var i = 0; i < this.hooks.length; i++) {
				hook = this.hooks[i];
				if (hook === func) {
					this.hooks.splice(i, 1);
					break;
				}
			}
		}

		/**
   * Triggers a hook to run all functions
   * @example this.content.trigger(args).then(function(){...});
   */

	}, {
		key: "trigger",
		value: function trigger() {
			var args = arguments;
			var context = this.context;
			var promises = [];

			this.hooks.forEach(function (task) {
				var executing = task.apply(context, args);

				if (executing && typeof executing["then"] === "function") {
					// Task is a function that returns a promise
					promises.push(executing);
				}
				// Otherwise Task resolves immediately, continue
			});

			return Promise.all(promises);
		}

		// Adds a function to be run before a hook completes

	}, {
		key: "list",
		value: function list() {
			return this.hooks;
		}
	}, {
		key: "clear",
		value: function clear() {
			return this.hooks = [];
		}
	}]);

	return Hook;
}();

exports.default = Hook;
module.exports = exports["default"];

/***/ }),
/* 102 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});
exports.Task = undefined;

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _core = __webpack_require__(6);

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Queue for handling tasks one at a time
 * @class
 * @param {scope} context what this will resolve to in the tasks
 */
var Queue = function () {
	function Queue(context) {
		_classCallCheck(this, Queue);

		this._q = [];
		this.context = context;
		this.tick = _core.requestAnimationFrame;
		this.running = false;
		this.paused = false;
	}

	/**
  * Add an item to the queue
  * @return {Promise}
  */


	_createClass(Queue, [{
		key: "enqueue",
		value: function enqueue() {
			var deferred, promise;
			var queued;
			var task = [].shift.call(arguments);
			var args = arguments;

			// Handle single args without context
			// if(args && !Array.isArray(args)) {
			//   args = [args];
			// }
			if (!task) {
				throw new Error("No Task Provided");
			}

			if (typeof task === "function") {

				deferred = new _core.defer();
				promise = deferred.promise;

				queued = {
					"task": task,
					"args": args,
					//"context"  : context,
					"deferred": deferred,
					"promise": promise
				};
			} else {
				// Task is a promise
				queued = {
					"promise": task
				};
			}

			this._q.push(queued);

			// Wait to start queue flush
			if (this.paused == false && !this.running) {
				// setTimeout(this.flush.bind(this), 0);
				// this.tick.call(window, this.run.bind(this));
				this.run();
			}

			return queued.promise;
		}

		/**
   * Run one item
   * @return {Promise}
   */

	}, {
		key: "dequeue",
		value: function dequeue() {
			var inwait, task, result;

			if (this._q.length && !this.paused) {
				inwait = this._q.shift();
				task = inwait.task;
				if (task) {
					// console.log(task)

					result = task.apply(this.context, inwait.args);

					if (result && typeof result["then"] === "function") {
						// Task is a function that returns a promise
						return result.then(function () {
							inwait.deferred.resolve.apply(this.context, arguments);
						}.bind(this), function () {
							inwait.deferred.reject.apply(this.context, arguments);
						}.bind(this));
					} else {
						// Task resolves immediately
						inwait.deferred.resolve.apply(this.context, result);
						return inwait.promise;
					}
				} else if (inwait.promise) {
					// Task is a promise
					return inwait.promise;
				}
			} else {
				inwait = new _core.defer();
				inwait.deferred.resolve();
				return inwait.promise;
			}
		}

		// Run All Immediately

	}, {
		key: "dump",
		value: function dump() {
			while (this._q.length) {
				this.dequeue();
			}
		}

		/**
   * Run all tasks sequentially, at convince
   * @return {Promise}
   */

	}, {
		key: "run",
		value: function run() {
			var _this = this;

			if (!this.running) {
				this.running = true;
				this.defered = new _core.defer();
			}

			this.tick.call(window, function () {

				if (_this._q.length) {

					_this.dequeue().then(function () {
						this.run();
					}.bind(_this));
				} else {
					_this.defered.resolve();
					_this.running = undefined;
				}
			});

			// Unpause
			if (this.paused == true) {
				this.paused = false;
			}

			return this.defered.promise;
		}

		/**
   * Flush all, as quickly as possible
   * @return {Promise}
   */

	}, {
		key: "flush",
		value: function flush() {

			if (this.running) {
				return this.running;
			}

			if (this._q.length) {
				this.running = this.dequeue().then(function () {
					this.running = undefined;
					return this.flush();
				}.bind(this));

				return this.running;
			}
		}

		/**
   * Clear all items in wait
   */

	}, {
		key: "clear",
		value: function clear() {
			this._q = [];
		}

		/**
   * Get the number of tasks in the queue
   * @return {number} tasks
   */

	}, {
		key: "length",
		value: function length() {
			return this._q.length;
		}

		/**
   * Pause a running queue
   */

	}, {
		key: "pause",
		value: function pause() {
			this.paused = true;
		}

		/**
   * End the queue
   */

	}, {
		key: "stop",
		value: function stop() {
			this._q = [];
			this.running = false;
			this.paused = true;
		}
	}]);

	return Queue;
}();

/**
 * Create a new task from a callback
 * @class
 * @private
 * @param {function} task
 * @param {array} args
 * @param {scope} context
 * @return {function} task
 */


var Task = function Task(task, args, context) {
	_classCallCheck(this, Task);

	return function () {
		var _this2 = this;

		var toApply = arguments || [];

		return new Promise(function (resolve, reject) {
			var callback = function callback(value, err) {
				if (!value && err) {
					reject(err);
				} else {
					resolve(value);
				}
			};
			// Add the callback to the arguments list
			toApply.push(callback);

			// Apply all arguments to the functions
			task.apply(context || _this2, toApply);
		});
	};
};

exports.default = Queue;
exports.Task = Task;

/***/ }),
/* 103 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


/*
 From Zip.js, by Gildas Lormeau
edited down
 */

var table = {
	"application": {
		"ecmascript": ["es", "ecma"],
		"javascript": "js",
		"ogg": "ogx",
		"pdf": "pdf",
		"postscript": ["ps", "ai", "eps", "epsi", "epsf", "eps2", "eps3"],
		"rdf+xml": "rdf",
		"smil": ["smi", "smil"],
		"xhtml+xml": ["xhtml", "xht"],
		"xml": ["xml", "xsl", "xsd", "opf", "ncx"],
		"zip": "zip",
		"x-httpd-eruby": "rhtml",
		"x-latex": "latex",
		"x-maker": ["frm", "maker", "frame", "fm", "fb", "book", "fbdoc"],
		"x-object": "o",
		"x-shockwave-flash": ["swf", "swfl"],
		"x-silverlight": "scr",
		"epub+zip": "epub",
		"font-tdpfr": "pfr",
		"inkml+xml": ["ink", "inkml"],
		"json": "json",
		"jsonml+json": "jsonml",
		"mathml+xml": "mathml",
		"metalink+xml": "metalink",
		"mp4": "mp4s",
		// "oebps-package+xml" : "opf",
		"omdoc+xml": "omdoc",
		"oxps": "oxps",
		"vnd.amazon.ebook": "azw",
		"widget": "wgt",
		// "x-dtbncx+xml" : "ncx",
		"x-dtbook+xml": "dtb",
		"x-dtbresource+xml": "res",
		"x-font-bdf": "bdf",
		"x-font-ghostscript": "gsf",
		"x-font-linux-psf": "psf",
		"x-font-otf": "otf",
		"x-font-pcf": "pcf",
		"x-font-snf": "snf",
		"x-font-ttf": ["ttf", "ttc"],
		"x-font-type1": ["pfa", "pfb", "pfm", "afm"],
		"x-font-woff": "woff",
		"x-mobipocket-ebook": ["prc", "mobi"],
		"x-mspublisher": "pub",
		"x-nzb": "nzb",
		"x-tgif": "obj",
		"xaml+xml": "xaml",
		"xml-dtd": "dtd",
		"xproc+xml": "xpl",
		"xslt+xml": "xslt",
		"internet-property-stream": "acx",
		"x-compress": "z",
		"x-compressed": "tgz",
		"x-gzip": "gz"
	},
	"audio": {
		"flac": "flac",
		"midi": ["mid", "midi", "kar", "rmi"],
		"mpeg": ["mpga", "mpega", "mp2", "mp3", "m4a", "mp2a", "m2a", "m3a"],
		"mpegurl": "m3u",
		"ogg": ["oga", "ogg", "spx"],
		"x-aiff": ["aif", "aiff", "aifc"],
		"x-ms-wma": "wma",
		"x-wav": "wav",
		"adpcm": "adp",
		"mp4": "mp4a",
		"webm": "weba",
		"x-aac": "aac",
		"x-caf": "caf",
		"x-matroska": "mka",
		"x-pn-realaudio-plugin": "rmp",
		"xm": "xm",
		"mid": ["mid", "rmi"]
	},
	"image": {
		"gif": "gif",
		"ief": "ief",
		"jpeg": ["jpeg", "jpg", "jpe"],
		"pcx": "pcx",
		"png": "png",
		"svg+xml": ["svg", "svgz"],
		"tiff": ["tiff", "tif"],
		"x-icon": "ico",
		"bmp": "bmp",
		"webp": "webp",
		"x-pict": ["pic", "pct"],
		"x-tga": "tga",
		"cis-cod": "cod"
	},
	"text": {
		"cache-manifest": ["manifest", "appcache"],
		"css": "css",
		"csv": "csv",
		"html": ["html", "htm", "shtml", "stm"],
		"mathml": "mml",
		"plain": ["txt", "text", "brf", "conf", "def", "list", "log", "in", "bas"],
		"richtext": "rtx",
		"tab-separated-values": "tsv",
		"x-bibtex": "bib"
	},
	"video": {
		"mpeg": ["mpeg", "mpg", "mpe", "m1v", "m2v", "mp2", "mpa", "mpv2"],
		"mp4": ["mp4", "mp4v", "mpg4"],
		"quicktime": ["qt", "mov"],
		"ogg": "ogv",
		"vnd.mpegurl": ["mxu", "m4u"],
		"x-flv": "flv",
		"x-la-asf": ["lsf", "lsx"],
		"x-mng": "mng",
		"x-ms-asf": ["asf", "asx", "asr"],
		"x-ms-wm": "wm",
		"x-ms-wmv": "wmv",
		"x-ms-wmx": "wmx",
		"x-ms-wvx": "wvx",
		"x-msvideo": "avi",
		"x-sgi-movie": "movie",
		"x-matroska": ["mpv", "mkv", "mk3d", "mks"],
		"3gpp2": "3g2",
		"h261": "h261",
		"h263": "h263",
		"h264": "h264",
		"jpeg": "jpgv",
		"jpm": ["jpm", "jpgm"],
		"mj2": ["mj2", "mjp2"],
		"vnd.ms-playready.media.pyv": "pyv",
		"vnd.uvvu.mp4": ["uvu", "uvvu"],
		"vnd.vivo": "viv",
		"webm": "webm",
		"x-f4v": "f4v",
		"x-m4v": "m4v",
		"x-ms-vob": "vob",
		"x-smv": "smv"
	}
};

var mimeTypes = function () {
	var type,
	    subtype,
	    val,
	    index,
	    mimeTypes = {};
	for (type in table) {
		if (table.hasOwnProperty(type)) {
			for (subtype in table[type]) {
				if (table[type].hasOwnProperty(subtype)) {
					val = table[type][subtype];
					if (typeof val == "string") {
						mimeTypes[val] = type + "/" + subtype;
					} else {
						for (index = 0; index < val.length; index++) {
							mimeTypes[val[index]] = type + "/" + subtype;
						}
					}
				}
			}
		}
	}
	return mimeTypes;
}();

var defaultValue = "text/plain"; //"application/octet-stream";

function lookup(filename) {
	return filename && mimeTypes[filename.split(".").pop().toLowerCase()] || defaultValue;
};

module.exports = {
	'lookup': lookup
};

/***/ }),
/* 104 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _eventEmitter = __webpack_require__(30);

var _eventEmitter2 = _interopRequireDefault(_eventEmitter);

var _core = __webpack_require__(6);

var _epubcfi = __webpack_require__(22);

var _epubcfi2 = _interopRequireDefault(_epubcfi);

var _mapping = __webpack_require__(142);

var _mapping2 = _interopRequireDefault(_mapping);

var _replacements = __webpack_require__(72);

var _constants = __webpack_require__(23);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var hasNavigator = typeof navigator !== "undefined";

var isChrome = hasNavigator && /Chrome/.test(navigator.userAgent);
var isWebkit = hasNavigator && !isChrome && /AppleWebKit/.test(navigator.userAgent);

var ELEMENT_NODE = 1;
var TEXT_NODE = 3;

/**
	* Handles DOM manipulation, queries and events for View contents
	* @class
	* @param {document} doc Document
	* @param {element} content Parent Element (typically Body)
	* @param {string} cfiBase Section component of CFIs
	* @param {number} sectionIndex Index in Spine of Conntent's Section
	*/

var Contents = function () {
	function Contents(doc, content, cfiBase, sectionIndex) {
		_classCallCheck(this, Contents);

		// Blank Cfi for Parsing
		this.epubcfi = new _epubcfi2.default();

		this.document = doc;
		this.documentElement = this.document.documentElement;
		this.content = content || this.document.body;
		this.window = this.document.defaultView;

		this._size = {
			width: 0,
			height: 0
		};

		this.sectionIndex = sectionIndex || 0;
		this.cfiBase = cfiBase || "";

		this.epubReadingSystem("epub.js", _constants.EPUBJS_VERSION);

		this.listeners();
	}

	/**
 	* Get DOM events that are listened for and passed along
 	*/


	_createClass(Contents, [{
		key: "width",


		/**
  	* Get or Set width
  	* @param {number} [w]
  	* @returns {number} width
  	*/
		value: function width(w) {
			// var frame = this.documentElement;
			var frame = this.content;

			if (w && (0, _core.isNumber)(w)) {
				w = w + "px";
			}

			if (w) {
				frame.style.width = w;
				// this.content.style.width = w;
			}

			return this.window.getComputedStyle(frame)["width"];
		}

		/**
  	* Get or Set height
  	* @param {number} [h]
  	* @returns {number} height
  	*/

	}, {
		key: "height",
		value: function height(h) {
			// var frame = this.documentElement;
			var frame = this.content;

			if (h && (0, _core.isNumber)(h)) {
				h = h + "px";
			}

			if (h) {
				frame.style.height = h;
				// this.content.style.height = h;
			}

			return this.window.getComputedStyle(frame)["height"];
		}

		/**
  	* Get or Set width of the contents
  	* @param {number} [w]
  	* @returns {number} width
  	*/

	}, {
		key: "contentWidth",
		value: function contentWidth(w) {

			var content = this.content || this.document.body;

			if (w && (0, _core.isNumber)(w)) {
				w = w + "px";
			}

			if (w) {
				content.style.width = w;
			}

			return this.window.getComputedStyle(content)["width"];
		}

		/**
  	* Get or Set height of the contents
  	* @param {number} [h]
  	* @returns {number} height
  	*/

	}, {
		key: "contentHeight",
		value: function contentHeight(h) {

			var content = this.content || this.document.body;

			if (h && (0, _core.isNumber)(h)) {
				h = h + "px";
			}

			if (h) {
				content.style.height = h;
			}

			return this.window.getComputedStyle(content)["height"];
		}

		/**
  	* Get the width of the text using Range
  	* @returns {number} width
  	*/

	}, {
		key: "textWidth",
		value: function textWidth() {
			var rect = void 0;
			var width = void 0;
			var range = this.document.createRange();
			var content = this.content || this.document.body;
			var border = (0, _core.borders)(content);

			// Select the contents of frame
			range.selectNodeContents(content);

			// get the width of the text content
			rect = range.getBoundingClientRect();
			width = rect.width;

			if (border && border.width) {
				width += border.width;
			}

			return Math.round(width);
		}

		/**
  	* Get the height of the text using Range
  	* @returns {number} height
  	*/

	}, {
		key: "textHeight",
		value: function textHeight() {
			var rect = void 0;
			var height = void 0;
			var range = this.document.createRange();
			var content = this.content || this.document.body;
			var border = (0, _core.borders)(content);

			range.selectNodeContents(content);

			rect = range.getBoundingClientRect();
			height = rect.height;

			if (height && border.height) {
				height += border.height;
			}

			if (height && rect.top) {
				height += rect.top;
			}

			return Math.round(height);
		}

		/**
  	* Get documentElement scrollWidth
  	* @returns {number} width
  	*/

	}, {
		key: "scrollWidth",
		value: function scrollWidth() {
			var width = this.documentElement.scrollWidth;

			return width;
		}

		/**
  	* Get documentElement scrollHeight
  	* @returns {number} height
  	*/

	}, {
		key: "scrollHeight",
		value: function scrollHeight() {
			var height = this.documentElement.scrollHeight;

			return height;
		}

		/**
  	* Set overflow css style of the contents
  	* @param {string} [overflow]
  	*/

	}, {
		key: "overflow",
		value: function overflow(_overflow) {

			if (_overflow) {
				this.documentElement.style.overflow = _overflow;
			}

			return this.window.getComputedStyle(this.documentElement)["overflow"];
		}

		/**
  	* Set overflowX css style of the documentElement
  	* @param {string} [overflow]
  	*/

	}, {
		key: "overflowX",
		value: function overflowX(overflow) {

			if (overflow) {
				this.documentElement.style.overflowX = overflow;
			}

			return this.window.getComputedStyle(this.documentElement)["overflowX"];
		}

		/**
  	* Set overflowY css style of the documentElement
  	* @param {string} [overflow]
  	*/

	}, {
		key: "overflowY",
		value: function overflowY(overflow) {

			if (overflow) {
				this.documentElement.style.overflowY = overflow;
			}

			return this.window.getComputedStyle(this.documentElement)["overflowY"];
		}

		/**
  	* Set Css styles on the contents element (typically Body)
  	* @param {string} property
  	* @param {string} value
  	* @param {boolean} [priority] set as "important"
  	*/

	}, {
		key: "css",
		value: function css(property, value, priority) {
			var content = this.content || this.document.body;

			if (value) {
				content.style.setProperty(property, value, priority ? "important" : "");
			}

			return this.window.getComputedStyle(content)[property];
		}

		/**
  	* Get or Set the viewport element
  	* @param {object} [options]
  	* @param {string} [options.width]
  	* @param {string} [options.height]
  	* @param {string} [options.scale]
  	* @param {string} [options.minimum]
  	* @param {string} [options.maximum]
  	* @param {string} [options.scalable]
  	*/

	}, {
		key: "viewport",
		value: function viewport(options) {
			var _width, _height, _scale, _minimum, _maximum, _scalable;
			// var width, height, scale, minimum, maximum, scalable;
			var $viewport = this.document.querySelector("meta[name='viewport']");
			var parsed = {
				"width": undefined,
				"height": undefined,
				"scale": undefined,
				"minimum": undefined,
				"maximum": undefined,
				"scalable": undefined
			};
			var newContent = [];
			var settings = {};

			/*
   * check for the viewport size
   * <meta name="viewport" content="width=1024,height=697" />
   */
			if ($viewport && $viewport.hasAttribute("content")) {
				var content = $viewport.getAttribute("content");
				var _width2 = content.match(/width\s*=\s*([^,]*)/);
				var _height2 = content.match(/height\s*=\s*([^,]*)/);
				var _scale2 = content.match(/initial-scale\s*=\s*([^,]*)/);
				var _minimum2 = content.match(/minimum-scale\s*=\s*([^,]*)/);
				var _maximum2 = content.match(/maximum-scale\s*=\s*([^,]*)/);
				var _scalable2 = content.match(/user-scalable\s*=\s*([^,]*)/);

				if (_width2 && _width2.length && typeof _width2[1] !== "undefined") {
					parsed.width = _width2[1];
				}
				if (_height2 && _height2.length && typeof _height2[1] !== "undefined") {
					parsed.height = _height2[1];
				}
				if (_scale2 && _scale2.length && typeof _scale2[1] !== "undefined") {
					parsed.scale = _scale2[1];
				}
				if (_minimum2 && _minimum2.length && typeof _minimum2[1] !== "undefined") {
					parsed.minimum = _minimum2[1];
				}
				if (_maximum2 && _maximum2.length && typeof _maximum2[1] !== "undefined") {
					parsed.maximum = _maximum2[1];
				}
				if (_scalable2 && _scalable2.length && typeof _scalable2[1] !== "undefined") {
					parsed.scalable = _scalable2[1];
				}
			}

			settings = (0, _core.defaults)(options || {}, parsed);

			if (options) {
				if (settings.width) {
					newContent.push("width=" + settings.width);
				}

				if (settings.height) {
					newContent.push("height=" + settings.height);
				}

				if (settings.scale) {
					newContent.push("initial-scale=" + settings.scale);
				}

				if (settings.scalable === "no") {
					newContent.push("minimum-scale=" + settings.scale);
					newContent.push("maximum-scale=" + settings.scale);
					newContent.push("user-scalable=" + settings.scalable);
				} else {

					if (settings.scalable) {
						newContent.push("user-scalable=" + settings.scalable);
					}

					if (settings.minimum) {
						newContent.push("minimum-scale=" + settings.minimum);
					}

					if (settings.maximum) {
						newContent.push("minimum-scale=" + settings.maximum);
					}
				}

				if (!$viewport) {
					$viewport = this.document.createElement("meta");
					$viewport.setAttribute("name", "viewport");
					this.document.querySelector("head").appendChild($viewport);
				}

				$viewport.setAttribute("content", newContent.join(", "));

				this.window.scrollTo(0, 0);
			}

			return settings;
		}

		/**
   * Event emitter for when the contents has expanded
   * @private
   */

	}, {
		key: "expand",
		value: function expand() {
			this.emit(_constants.EVENTS.CONTENTS.EXPAND);
		}

		/**
   * Add DOM listeners
   * @private
   */

	}, {
		key: "listeners",
		value: function listeners() {

			this.imageLoadListeners();

			this.mediaQueryListeners();

			// this.fontLoadListeners();

			this.addEventListeners();

			this.addSelectionListeners();

			// this.transitionListeners();

			this.resizeListeners();

			// this.resizeObservers();

			this.linksHandler();
		}

		/**
   * Remove DOM listeners
   * @private
   */

	}, {
		key: "removeListeners",
		value: function removeListeners() {

			this.removeEventListeners();

			this.removeSelectionListeners();

			clearTimeout(this.expanding);
		}

		/**
   * Check if size of contents has changed and
   * emit 'resize' event if it has.
   * @private
   */

	}, {
		key: "resizeCheck",
		value: function resizeCheck() {
			var width = this.textWidth();
			var height = this.textHeight();

			if (width != this._size.width || height != this._size.height) {

				this._size = {
					width: width,
					height: height
				};

				this.onResize && this.onResize(this._size);
				this.emit(_constants.EVENTS.CONTENTS.RESIZE, this._size);
			}
		}

		/**
   * Poll for resize detection
   * @private
   */

	}, {
		key: "resizeListeners",
		value: function resizeListeners() {
			var width, height;
			// Test size again
			clearTimeout(this.expanding);

			requestAnimationFrame(this.resizeCheck.bind(this));
			this.expanding = setTimeout(this.resizeListeners.bind(this), 350);
		}

		/**
   * Use css transitions to detect resize
   * @private
   */

	}, {
		key: "transitionListeners",
		value: function transitionListeners() {
			var body = this.content;

			body.style['transitionProperty'] = "font, font-size, font-size-adjust, font-stretch, font-variation-settings, font-weight, width, height";
			body.style['transitionDuration'] = "0.001ms";
			body.style['transitionTimingFunction'] = "linear";
			body.style['transitionDelay'] = "0";

			this._resizeCheck = this.resizeCheck.bind(this);
			this.document.addEventListener('transitionend', this._resizeCheck);
		}

		/**
   * Listen for media query changes and emit 'expand' event
   * Adapted from: https://github.com/tylergaw/media-query-events/blob/master/js/mq-events.js
   * @private
   */

	}, {
		key: "mediaQueryListeners",
		value: function mediaQueryListeners() {
			var sheets = this.document.styleSheets;
			var mediaChangeHandler = function (m) {
				if (m.matches && !this._expanding) {
					setTimeout(this.expand.bind(this), 1);
				}
			}.bind(this);

			for (var i = 0; i < sheets.length; i += 1) {
				var rules;
				// Firefox errors if we access cssRules cross-domain
				try {
					rules = sheets[i].cssRules;
				} catch (e) {
					return;
				}
				if (!rules) return; // Stylesheets changed
				for (var j = 0; j < rules.length; j += 1) {
					//if (rules[j].constructor === CSSMediaRule) {
					if (rules[j].media) {
						var mql = this.window.matchMedia(rules[j].media.mediaText);
						mql.addListener(mediaChangeHandler);
						//mql.onchange = mediaChangeHandler;
					}
				}
			}
		}

		/**
   * Use MutationObserver to listen for changes in the DOM and check for resize
   * @private
   */

	}, {
		key: "resizeObservers",
		value: function resizeObservers() {
			var _this = this;

			// create an observer instance
			this.observer = new MutationObserver(function (mutations) {
				_this.resizeCheck();
			});

			// configuration of the observer:
			var config = { attributes: true, childList: true, characterData: true, subtree: true };

			// pass in the target node, as well as the observer options
			this.observer.observe(this.document, config);
		}

		/**
   * Test if images are loaded or add listener for when they load
   * @private
   */

	}, {
		key: "imageLoadListeners",
		value: function imageLoadListeners() {
			var images = this.document.querySelectorAll("img");
			var img;
			for (var i = 0; i < images.length; i++) {
				img = images[i];

				if (typeof img.naturalWidth !== "undefined" && img.naturalWidth === 0) {
					img.onload = this.expand.bind(this);
				}
			}
		}

		/**
   * Listen for font load and check for resize when loaded
   * @private
   */

	}, {
		key: "fontLoadListeners",
		value: function fontLoadListeners() {
			if (!this.document || !this.document.fonts) {
				return;
			}

			this.document.fonts.ready.then(function () {
				this.resizeCheck();
			}.bind(this));
		}

		/**
   * Get the documentElement
   * @returns {element} documentElement
   */

	}, {
		key: "root",
		value: function root() {
			if (!this.document) return null;
			return this.document.documentElement;
		}

		/**
   * Get the location offset of a EpubCFI or an #id
   * @param {string | EpubCFI} target
   * @param {string} [ignoreClass] for the cfi
   * @returns { {left: Number, top: Number }
   */

	}, {
		key: "locationOf",
		value: function locationOf(target, ignoreClass) {
			var position;
			var targetPos = { "left": 0, "top": 0 };

			if (!this.document) return targetPos;

			if (this.epubcfi.isCfiString(target)) {
				var range = new _epubcfi2.default(target).toRange(this.document, ignoreClass);

				if (range) {
					if (range.startContainer.nodeType === Node.ELEMENT_NODE) {
						position = range.startContainer.getBoundingClientRect();
						targetPos.left = position.left;
						targetPos.top = position.top;
					} else {
						// Webkit does not handle collapsed range bounds correctly
						// https://bugs.webkit.org/show_bug.cgi?id=138949

						// Construct a new non-collapsed range
						if (isWebkit) {
							var container = range.startContainer;
							var newRange = new Range();
							try {
								if (container.nodeType === ELEMENT_NODE) {
									position = container.getBoundingClientRect();
								} else if (range.startOffset + 2 < container.length) {
									newRange.setStart(container, range.startOffset);
									newRange.setEnd(container, range.startOffset + 2);
									position = newRange.getBoundingClientRect();
								} else if (range.startOffset - 2 > 0) {
									newRange.setStart(container, range.startOffset - 2);
									newRange.setEnd(container, range.startOffset);
									position = newRange.getBoundingClientRect();
								} else {
									// empty, return the parent element
									position = container.parentNode.getBoundingClientRect();
								}
							} catch (e) {
								console.error(e, e.stack);
							}
						} else {
							position = range.getBoundingClientRect();
						}
					}
				}
			} else if (typeof target === "string" && target.indexOf("#") > -1) {

				var id = target.substring(target.indexOf("#") + 1);
				var el = this.document.getElementById(id);
				if (el) {
					if (isWebkit) {
						// Webkit reports incorrect bounding rects in Columns
						var _newRange = new Range();
						_newRange.selectNode(el);
						position = _newRange.getBoundingClientRect();
					} else {
						position = el.getBoundingClientRect();
					}
				}
			}

			if (position) {
				targetPos.left = position.left;
				targetPos.top = position.top;
			}

			return targetPos;
		}

		/**
   * Append a stylesheet link to the document head
   * @param {string} src url
   */

	}, {
		key: "addStylesheet",
		value: function addStylesheet(src) {
			return new Promise(function (resolve, reject) {
				var $stylesheet;
				var ready = false;

				if (!this.document) {
					resolve(false);
					return;
				}

				// Check if link already exists
				$stylesheet = this.document.querySelector("link[href='" + src + "']");
				if ($stylesheet) {
					resolve(true);
					return; // already present
				}

				$stylesheet = this.document.createElement("link");
				$stylesheet.type = "text/css";
				$stylesheet.rel = "stylesheet";
				$stylesheet.href = src;
				$stylesheet.onload = $stylesheet.onreadystatechange = function () {
					if (!ready && (!this.readyState || this.readyState == "complete")) {
						ready = true;
						// Let apply
						setTimeout(function () {
							resolve(true);
						}, 1);
					}
				};

				this.document.head.appendChild($stylesheet);
			}.bind(this));
		}

		/**
   * Append stylesheet rules to a generate stylesheet
   * Array: https://developer.mozilla.org/en-US/docs/Web/API/CSSStyleSheet/insertRule
   * Object: https://github.com/desirable-objects/json-to-css
   * @param {array | object} rules
   */

	}, {
		key: "addStylesheetRules",
		value: function addStylesheetRules(rules) {
			var styleEl;
			var styleSheet;
			var key = "epubjs-inserted-css";

			if (!this.document || !rules || rules.length === 0) return;

			// Check if link already exists
			styleEl = this.document.getElementById("#" + key);
			if (!styleEl) {
				styleEl = this.document.createElement("style");
				styleEl.id = key;
			}

			// Append style element to head
			this.document.head.appendChild(styleEl);

			// Grab style sheet
			styleSheet = styleEl.sheet;

			if (Object.prototype.toString.call(rules) === "[object Array]") {
				for (var i = 0, rl = rules.length; i < rl; i++) {
					var j = 1,
					    rule = rules[i],
					    selector = rules[i][0],
					    propStr = "";
					// If the second argument of a rule is an array of arrays, correct our variables.
					if (Object.prototype.toString.call(rule[1][0]) === "[object Array]") {
						rule = rule[1];
						j = 0;
					}

					for (var pl = rule.length; j < pl; j++) {
						var prop = rule[j];
						propStr += prop[0] + ":" + prop[1] + (prop[2] ? " !important" : "") + ";\n";
					}

					// Insert CSS Rule
					styleSheet.insertRule(selector + "{" + propStr + "}", styleSheet.cssRules.length);
				}
			} else {
				var selectors = Object.keys(rules);
				selectors.forEach(function (selector) {
					var definition = rules[selector];
					if (Array.isArray(definition)) {
						definition.forEach(function (item) {
							var _rules = Object.keys(item);
							var result = _rules.map(function (rule) {
								return rule + ":" + item[rule];
							}).join(';');
							styleSheet.insertRule(selector + "{" + result + "}", styleSheet.cssRules.length);
						});
					} else {
						var _rules = Object.keys(definition);
						var result = _rules.map(function (rule) {
							return rule + ":" + definition[rule];
						}).join(';');
						styleSheet.insertRule(selector + "{" + result + "}", styleSheet.cssRules.length);
					}
				});
			}
		}

		/**
   * Append a script tag to the document head
   * @param {string} src url
   * @returns {Promise} loaded
   */

	}, {
		key: "addScript",
		value: function addScript(src) {

			return new Promise(function (resolve, reject) {
				var $script;
				var ready = false;

				if (!this.document) {
					resolve(false);
					return;
				}

				$script = this.document.createElement("script");
				$script.type = "text/javascript";
				$script.async = true;
				$script.src = src;
				$script.onload = $script.onreadystatechange = function () {
					if (!ready && (!this.readyState || this.readyState == "complete")) {
						ready = true;
						setTimeout(function () {
							resolve(true);
						}, 1);
					}
				};

				this.document.head.appendChild($script);
			}.bind(this));
		}

		/**
   * Add a class to the contents container
   * @param {string} className
   */

	}, {
		key: "addClass",
		value: function addClass(className) {
			var content;

			if (!this.document) return;

			content = this.content || this.document.body;

			if (content) {
				content.classList.add(className);
			}
		}

		/**
   * Remove a class from the contents container
   * @param {string} removeClass
   */

	}, {
		key: "removeClass",
		value: function removeClass(className) {
			var content;

			if (!this.document) return;

			content = this.content || this.document.body;

			if (content) {
				content.classList.remove(className);
			}
		}

		/**
   * Add DOM event listeners
   * @private
   */

	}, {
		key: "addEventListeners",
		value: function addEventListeners() {
			if (!this.document) {
				return;
			}

			this._triggerEvent = this.triggerEvent.bind(this);

			_constants.DOM_EVENTS.forEach(function (eventName) {
				this.document.addEventListener(eventName, this._triggerEvent, { passive: true });
			}, this);
		}

		/**
   * Remove DOM event listeners
   * @private
   */

	}, {
		key: "removeEventListeners",
		value: function removeEventListeners() {
			if (!this.document) {
				return;
			}
			_constants.DOM_EVENTS.forEach(function (eventName) {
				this.document.removeEventListener(eventName, this._triggerEvent, { passive: true });
			}, this);
			this._triggerEvent = undefined;
		}

		/**
   * Emit passed browser events
   * @private
   */

	}, {
		key: "triggerEvent",
		value: function triggerEvent(e) {
			this.emit(e.type, e);
		}

		/**
   * Add listener for text selection
   * @private
   */

	}, {
		key: "addSelectionListeners",
		value: function addSelectionListeners() {
			if (!this.document) {
				return;
			}
			this._onSelectionChange = this.onSelectionChange.bind(this);
			this.document.addEventListener("selectionchange", this._onSelectionChange, { passive: true });
		}

		/**
   * Remove listener for text selection
   * @private
   */

	}, {
		key: "removeSelectionListeners",
		value: function removeSelectionListeners() {
			if (!this.document) {
				return;
			}
			this.document.removeEventListener("selectionchange", this._onSelectionChange, { passive: true });
			this._onSelectionChange = undefined;
		}

		/**
   * Handle getting text on selection
   * @private
   */

	}, {
		key: "onSelectionChange",
		value: function onSelectionChange(e) {
			if (this.selectionEndTimeout) {
				clearTimeout(this.selectionEndTimeout);
			}
			this.selectionEndTimeout = setTimeout(function () {
				var selection = this.window.getSelection();
				this.triggerSelectedEvent(selection);
			}.bind(this), 250);
		}

		/**
   * Emit event on text selection
   * @private
   */

	}, {
		key: "triggerSelectedEvent",
		value: function triggerSelectedEvent(selection) {
			var range, cfirange;

			if (selection && selection.rangeCount > 0) {
				range = selection.getRangeAt(0);
				if (!range.collapsed) {
					// cfirange = this.section.cfiFromRange(range);
					cfirange = new _epubcfi2.default(range, this.cfiBase).toString();
					this.emit(_constants.EVENTS.CONTENTS.SELECTED, cfirange);
					this.emit(_constants.EVENTS.CONTENTS.SELECTED_RANGE, range);
				}
			}
		}

		/**
   * Get a Dom Range from EpubCFI
   * @param {EpubCFI} _cfi
   * @param {string} [ignoreClass]
   * @returns {Range} range
   */

	}, {
		key: "range",
		value: function range(_cfi, ignoreClass) {
			var cfi = new _epubcfi2.default(_cfi);
			return cfi.toRange(this.document, ignoreClass);
		}

		/**
   * Get an EpubCFI from a Dom Range
   * @param {Range} range
   * @param {string} [ignoreClass]
   * @returns {EpubCFI} cfi
   */

	}, {
		key: "cfiFromRange",
		value: function cfiFromRange(range, ignoreClass) {
			return new _epubcfi2.default(range, this.cfiBase, ignoreClass).toString();
		}

		/**
   * Get an EpubCFI from a Dom node
   * @param {node} node
   * @param {string} [ignoreClass]
   * @returns {EpubCFI} cfi
   */

	}, {
		key: "cfiFromNode",
		value: function cfiFromNode(node, ignoreClass) {
			return new _epubcfi2.default(node, this.cfiBase, ignoreClass).toString();
		}

		// TODO: find where this is used - remove?

	}, {
		key: "map",
		value: function map(layout) {
			var map = new _mapping2.default(layout);
			return map.section();
		}

		/**
   * Size the contents to a given width and height
   * @param {number} [width]
   * @param {number} [height]
   */

	}, {
		key: "size",
		value: function size(width, height) {
			var viewport = { scale: 1.0, scalable: "no" };

			this.layoutStyle("scrolling");

			if (width >= 0) {
				this.width(width);
				viewport.width = width;
				this.css("padding", "0 " + width / 12 + "px");
			}

			if (height >= 0) {
				this.height(height);
				viewport.height = height;
			}

			this.css("margin", "0");
			this.css("box-sizing", "border-box");

			this.viewport(viewport);
		}

		/**
   * Apply columns to the contents for pagination
   * @param {number} width
   * @param {number} height
   * @param {number} columnWidth
   * @param {number} gap
   */

	}, {
		key: "columns",
		value: function columns(width, height, columnWidth, gap) {
			var COLUMN_AXIS = (0, _core.prefixed)("column-axis");
			var COLUMN_GAP = (0, _core.prefixed)("column-gap");
			var COLUMN_WIDTH = (0, _core.prefixed)("column-width");
			var COLUMN_FILL = (0, _core.prefixed)("column-fill");

			var writingMode = this.writingMode();
			var axis = writingMode.indexOf("vertical") === 0 ? "vertical" : "horizontal";

			this.layoutStyle("paginated");

			// Fix body width issues if rtl is only set on body element
			if (this.content.dir === "rtl") {
				this.direction("rtl");
			}

			this.width(width);
			this.height(height);

			// Deal with Mobile trying to scale to viewport
			this.viewport({ width: width, height: height, scale: 1.0, scalable: "no" });

			// TODO: inline-block needs more testing
			// Fixes Safari column cut offs, but causes RTL issues
			// this.css("display", "inline-block");

			this.css("overflow-y", "hidden");
			this.css("margin", "0", true);

			if (axis === "vertical") {
				this.css("padding-top", gap / 2 + "px", true);
				this.css("padding-bottom", gap / 2 + "px", true);
				this.css("padding-left", "20px");
				this.css("padding-right", "20px");
			} else {
				this.css("padding-top", "20px");
				this.css("padding-bottom", "20px");
				this.css("padding-left", gap / 2 + "px", true);
				this.css("padding-right", gap / 2 + "px", true);
			}

			this.css("box-sizing", "border-box");
			this.css("max-width", "inherit");

			this.css(COLUMN_AXIS, "horizontal");
			this.css(COLUMN_FILL, "auto");

			this.css(COLUMN_GAP, gap + "px");
			this.css(COLUMN_WIDTH, columnWidth + "px");
		}

		/**
   * Scale contents from center
   * @param {number} scale
   * @param {number} offsetX
   * @param {number} offsetY
   */

	}, {
		key: "scaler",
		value: function scaler(scale, offsetX, offsetY) {
			var scaleStr = "scale(" + scale + ")";
			var translateStr = "";
			// this.css("position", "absolute"));
			this.css("transform-origin", "top left");

			if (offsetX >= 0 || offsetY >= 0) {
				translateStr = " translate(" + (offsetX || 0) + "px, " + (offsetY || 0) + "px )";
			}

			this.css("transform", scaleStr + translateStr);
		}

		/**
   * Fit contents into a fixed width and height
   * @param {number} width
   * @param {number} height
   */

	}, {
		key: "fit",
		value: function fit(width, height) {
			var viewport = this.viewport();
			var viewportWidth = parseInt(viewport.width);
			var viewportHeight = parseInt(viewport.height);
			var widthScale = width / viewportWidth;
			var heightScale = height / viewportHeight;
			var scale = widthScale < heightScale ? widthScale : heightScale;

			// the translate does not work as intended, elements can end up unaligned
			// var offsetY = (height - (viewportHeight * scale)) / 2;
			// var offsetX = 0;
			// if (this.sectionIndex % 2 === 1) {
			// 	offsetX = width - (viewportWidth * scale);
			// }

			this.layoutStyle("paginated");

			// scale needs width and height to be set
			this.width(viewportWidth);
			this.height(viewportHeight);
			this.overflow("hidden");

			// Scale to the correct size
			this.scaler(scale, 0, 0);
			// this.scaler(scale, offsetX > 0 ? offsetX : 0, offsetY);

			// background images are not scaled by transform
			this.css("background-size", viewportWidth * scale + "px " + viewportHeight * scale + "px");

			this.css("background-color", "transparent");
		}

		/**
   * Set the direction of the text
   * @param {string} [dir="ltr"] "rtl" | "ltr"
   */

	}, {
		key: "direction",
		value: function direction(dir) {
			if (this.documentElement) {
				this.documentElement.style["direction"] = dir;
			}
		}
	}, {
		key: "mapPage",
		value: function mapPage(cfiBase, layout, start, end, dev) {
			var mapping = new _mapping2.default(layout, dev);

			return mapping.page(this, cfiBase, start, end);
		}

		/**
   * Emit event when link in content is clicked
   * @private
   */

	}, {
		key: "linksHandler",
		value: function linksHandler() {
			var _this2 = this;

			(0, _replacements.replaceLinks)(this.content, function (href) {
				_this2.emit(_constants.EVENTS.CONTENTS.LINK_CLICKED, href);
			});
		}

		/**
   * Set the writingMode of the text
   * @param {string} [mode="horizontal-tb"] "horizontal-tb" | "vertical-rl" | "vertical-lr"
   */

	}, {
		key: "writingMode",
		value: function writingMode(mode) {
			var WRITING_MODE = (0, _core.prefixed)("writing-mode");

			if (mode && this.documentElement) {
				this.documentElement.style[WRITING_MODE] = mode;
			}

			return this.window.getComputedStyle(this.documentElement)[WRITING_MODE] || '';
		}

		/**
   * Set the layoutStyle of the content
   * @param {string} [style="paginated"] "scrolling" | "paginated"
   * @private
   */

	}, {
		key: "layoutStyle",
		value: function layoutStyle(style) {

			if (style) {
				this._layoutStyle = style;
				navigator.epubReadingSystem.layoutStyle = this._layoutStyle;
			}

			return this._layoutStyle || "paginated";
		}

		/**
   * Add the epubReadingSystem object to the navigator
   * @param {string} name
   * @param {string} version
   * @private
   */

	}, {
		key: "epubReadingSystem",
		value: function epubReadingSystem(name, version) {
			navigator.epubReadingSystem = {
				name: name,
				version: version,
				layoutStyle: this.layoutStyle(),
				hasFeature: function hasFeature(feature) {
					switch (feature) {
						case "dom-manipulation":
							return true;
						case "layout-changes":
							return true;
						case "touch-events":
							return true;
						case "mouse-events":
							return true;
						case "keyboard-events":
							return true;
						case "spine-scripting":
							return false;
						default:
							return false;
					}
				}
			};
			return navigator.epubReadingSystem;
		}
	}, {
		key: "destroy",
		value: function destroy() {
			// Stop observing
			if (this.observer) {
				this.observer.disconnect();
			}

			this.document.removeEventListener('transitionend', this._resizeCheck);

			this.removeListeners();
		}
	}], [{
		key: "listenedEvents",
		get: function get() {
			return _constants.DOM_EVENTS;
		}
	}]);

	return Contents;
}();

(0, _eventEmitter2.default)(Contents.prototype);

exports.default = Contents;
module.exports = exports["default"];

/***/ }),
/* 105 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _eventEmitter = __webpack_require__(30);

var _eventEmitter2 = _interopRequireDefault(_eventEmitter);

var _core = __webpack_require__(6);

var _mapping = __webpack_require__(142);

var _mapping2 = _interopRequireDefault(_mapping);

var _queue = __webpack_require__(102);

var _queue2 = _interopRequireDefault(_queue);

var _stage = __webpack_require__(388);

var _stage2 = _interopRequireDefault(_stage);

var _views = __webpack_require__(398);

var _views2 = _interopRequireDefault(_views);

var _constants = __webpack_require__(23);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var DefaultViewManager = function () {
	function DefaultViewManager(options) {
		_classCallCheck(this, DefaultViewManager);

		this.name = "default";
		this.optsSettings = options.settings;
		this.View = options.view;
		this.request = options.request;
		this.renditionQueue = options.queue;
		this.q = new _queue2.default(this);

		this.settings = (0, _core.extend)(this.settings || {}, {
			infinite: true,
			hidden: false,
			width: undefined,
			height: undefined,
			axis: undefined,
			flow: "scrolled",
			ignoreClass: "",
			fullsize: undefined
		});

		(0, _core.extend)(this.settings, options.settings || {});

		this.viewSettings = {
			ignoreClass: this.settings.ignoreClass,
			axis: this.settings.axis,
			flow: this.settings.flow,
			layout: this.layout,
			method: this.settings.method, // srcdoc, blobUrl, write
			width: 0,
			height: 0,
			forceEvenPages: true
		};

		this.rendered = false;
	}

	_createClass(DefaultViewManager, [{
		key: "render",
		value: function render(element, size) {
			var tag = element.tagName;

			if (typeof this.settings.fullsize === "undefined" && tag && (tag.toLowerCase() == "body" || tag.toLowerCase() == "html")) {
				this.settings.fullsize = true;
			}

			if (this.settings.fullsize) {
				this.settings.overflow = "visible";
				this.overflow = this.settings.overflow;
			}

			this.settings.size = size;

			// Save the stage
			this.stage = new _stage2.default({
				width: size.width,
				height: size.height,
				overflow: this.overflow,
				hidden: this.settings.hidden,
				axis: this.settings.axis,
				fullsize: this.settings.fullsize,
				direction: this.settings.direction
			});

			this.stage.attachTo(element);

			// Get this stage container div
			this.container = this.stage.getContainer();

			// Views array methods
			this.views = new _views2.default(this.container);

			// Calculate Stage Size
			this._bounds = this.bounds();
			this._stageSize = this.stage.size();

			// Set the dimensions for views
			this.viewSettings.width = this._stageSize.width;
			this.viewSettings.height = this._stageSize.height;

			// Function to handle a resize event.
			// Will only attach if width and height are both fixed.
			this.stage.onResize(this.onResized.bind(this));

			this.stage.onOrientationChange(this.onOrientationChange.bind(this));

			// Add Event Listeners
			this.addEventListeners();

			// Add Layout method
			// this.applyLayoutMethod();
			if (this.layout) {
				this.updateLayout();
			}

			this.rendered = true;
		}
	}, {
		key: "addEventListeners",
		value: function addEventListeners() {
			var scroller;

			window.addEventListener("unload", function (e) {
				this.destroy();
			}.bind(this));

			if (!this.settings.fullsize) {
				scroller = this.container;
			} else {
				scroller = window;
			}

			this._onScroll = this.onScroll.bind(this);
			scroller.addEventListener("scroll", this._onScroll);
		}
	}, {
		key: "removeEventListeners",
		value: function removeEventListeners() {
			var scroller;

			if (!this.settings.fullsize) {
				scroller = this.container;
			} else {
				scroller = window;
			}

			scroller.removeEventListener("scroll", this._onScroll);
			this._onScroll = undefined;
		}
	}, {
		key: "destroy",
		value: function destroy() {
			clearTimeout(this.orientationTimeout);
			clearTimeout(this.resizeTimeout);
			clearTimeout(this.afterScrolled);

			this.clear();

			this.removeEventListeners();

			this.stage.destroy();

			this.rendered = false;

			/*
   		clearTimeout(this.trimTimeout);
   	if(this.settings.hidden) {
   		this.element.removeChild(this.wrapper);
   	} else {
   		this.element.removeChild(this.container);
   	}
   */
		}
	}, {
		key: "onOrientationChange",
		value: function onOrientationChange(e) {
			var _window = window,
			    orientation = _window.orientation;


			if (this.optsSettings.resizeOnOrientationChange) {
				this.resize();
			}

			// Per ampproject:
			// In IOS 10.3, the measured size of an element is incorrect if the
			// element size depends on window size directly and the measurement
			// happens in window.resize event. Adding a timeout for correct
			// measurement. See https://github.com/ampproject/amphtml/issues/8479
			clearTimeout(this.orientationTimeout);
			this.orientationTimeout = setTimeout(function () {
				this.orientationTimeout = undefined;

				if (this.optsSettings.resizeOnOrientationChange) {
					this.resize();
				}

				this.emit(_constants.EVENTS.MANAGERS.ORIENTATION_CHANGE, orientation);
			}.bind(this), 500);
		}
	}, {
		key: "onResized",
		value: function onResized(e) {
			this.resize();
		}
	}, {
		key: "resize",
		value: function resize(width, height) {
			var stageSize = this.stage.size(width, height);

			// For Safari, wait for orientation to catch up
			// if the window is a square
			this.winBounds = (0, _core.windowBounds)();
			if (this.orientationTimeout && this.winBounds.width === this.winBounds.height) {
				// reset the stage size for next resize
				this._stageSize = undefined;
				return;
			}

			if (this._stageSize && this._stageSize.width === stageSize.width && this._stageSize.height === stageSize.height) {
				// Size is the same, no need to resize
				return;
			}

			this._stageSize = stageSize;

			this._bounds = this.bounds();

			// Clear current views
			this.clear();

			// Update for new views
			this.viewSettings.width = this._stageSize.width;
			this.viewSettings.height = this._stageSize.height;

			this.updateLayout();

			this.emit(_constants.EVENTS.MANAGERS.RESIZED, {
				width: this._stageSize.width,
				height: this._stageSize.height
			});
		}
	}, {
		key: "createView",
		value: function createView(section) {
			return new this.View(section, this.viewSettings);
		}
	}, {
		key: "display",
		value: function display(section, target) {

			var displaying = new _core.defer();
			var displayed = displaying.promise;

			// Check if moving to target is needed
			if (target === section.href || (0, _core.isNumber)(target)) {
				target = undefined;
			}

			// Check to make sure the section we want isn't already shown
			var visible = this.views.find(section);

			// View is already shown, just move to correct location in view
			if (visible && section) {
				var offset = visible.offset();

				if (this.settings.direction === "ltr") {
					this.scrollTo(offset.left, offset.top, true);
				} else {
					var width = visible.width();
					this.scrollTo(offset.left + width, offset.top, true);
				}

				if (target) {
					var _offset = visible.locationOf(target);
					this.moveTo(_offset);
				}

				displaying.resolve();
				return displayed;
			}

			// Hide all current views
			this.clear();

			this.add(section).then(function (view) {

				// Move to correct place within the section, if needed
				if (target) {
					var _offset2 = view.locationOf(target);
					this.moveTo(_offset2);
				}
			}.bind(this), function (err) {
				displaying.reject(err);
			}).then(function () {
				var next;
				if (this.layout.name === "pre-paginated" && this.layout.divisor > 1 && section.index > 0) {
					// First page (cover) should stand alone for pre-paginated books
					next = section.next();
					if (next) {
						return this.add(next);
					}
				}
			}.bind(this)).then(function () {

				this.views.show();

				displaying.resolve();
			}.bind(this));
			// .then(function(){
			// 	return this.hooks.display.trigger(view);
			// }.bind(this))
			// .then(function(){
			// 	this.views.show();
			// }.bind(this));
			return displayed;
		}
	}, {
		key: "afterDisplayed",
		value: function afterDisplayed(view) {
			this.emit(_constants.EVENTS.MANAGERS.ADDED, view);
		}
	}, {
		key: "afterResized",
		value: function afterResized(view) {
			this.emit(_constants.EVENTS.MANAGERS.RESIZE, view.section);
		}
	}, {
		key: "moveTo",
		value: function moveTo(offset) {
			var distX = 0,
			    distY = 0;

			if (!this.isPaginated) {
				distY = offset.top;
			} else {
				distX = Math.floor(offset.left / this.layout.delta) * this.layout.delta;

				if (distX + this.layout.delta > this.container.scrollWidth) {
					distX = this.container.scrollWidth - this.layout.delta;
				}
			}
			this.scrollTo(distX, distY, true);
		}
	}, {
		key: "add",
		value: function add(section) {
			var _this = this;

			var view = this.createView(section);

			this.views.append(view);

			// view.on(EVENTS.VIEWS.SHOWN, this.afterDisplayed.bind(this));
			view.onDisplayed = this.afterDisplayed.bind(this);
			view.onResize = this.afterResized.bind(this);

			view.on(_constants.EVENTS.VIEWS.AXIS, function (axis) {
				_this.updateAxis(axis);
			});

			return view.display(this.request);
		}
	}, {
		key: "append",
		value: function append(section) {
			var _this2 = this;

			var view = this.createView(section);
			this.views.append(view);

			view.onDisplayed = this.afterDisplayed.bind(this);
			view.onResize = this.afterResized.bind(this);

			view.on(_constants.EVENTS.VIEWS.AXIS, function (axis) {
				_this2.updateAxis(axis);
			});

			return view.display(this.request);
		}
	}, {
		key: "prepend",
		value: function prepend(section) {
			var _this3 = this;

			var view = this.createView(section);

			view.on(_constants.EVENTS.VIEWS.RESIZED, function (bounds) {
				_this3.counter(bounds);
			});

			this.views.prepend(view);

			view.onDisplayed = this.afterDisplayed.bind(this);
			view.onResize = this.afterResized.bind(this);

			view.on(_constants.EVENTS.VIEWS.AXIS, function (axis) {
				_this3.updateAxis(axis);
			});

			return view.display(this.request);
		}
	}, {
		key: "counter",
		value: function counter(bounds) {
			if (this.settings.axis === "vertical") {
				this.scrollBy(0, bounds.heightDelta, true);
			} else {
				this.scrollBy(bounds.widthDelta, 0, true);
			}
		}

		// resizeView(view) {
		//
		// 	if(this.settings.globalLayoutProperties.layout === "pre-paginated") {
		// 		view.lock("both", this.bounds.width, this.bounds.height);
		// 	} else {
		// 		view.lock("width", this.bounds.width, this.bounds.height);
		// 	}
		//
		// };

	}, {
		key: "next",
		value: function next() {
			var next;
			var left;

			var dir = this.settings.direction;

			if (!this.views.length) return;

			if (this.isPaginated && this.settings.axis === "horizontal" && (!dir || dir === "ltr")) {

				this.scrollLeft = this.container.scrollLeft;

				left = this.container.scrollLeft + this.container.offsetWidth + this.layout.delta;

				if (left <= this.container.scrollWidth) {
					this.scrollBy(this.layout.delta, 0, true);
				} else {
					next = this.views.last().section.next();
				}
			} else if (this.isPaginated && this.settings.axis === "horizontal" && dir === "rtl") {

				this.scrollLeft = this.container.scrollLeft;

				left = this.container.scrollLeft;

				if (left > 0) {
					this.scrollBy(this.layout.delta, 0, true);
				} else {
					next = this.views.last().section.next();
				}
			} else if (this.isPaginated && this.settings.axis === "vertical") {

				this.scrollTop = this.container.scrollTop;

				var top = this.container.scrollTop + this.container.offsetHeight;

				if (top < this.container.scrollHeight) {
					this.scrollBy(0, this.layout.height, true);
				} else {
					next = this.views.last().section.next();
				}
			} else {
				next = this.views.last().section.next();
			}

			if (next) {
				this.clear();

				return this.append(next).then(function () {
					var right;
					if (this.layout.name === "pre-paginated" && this.layout.divisor > 1) {
						right = next.next();
						if (right) {
							return this.append(right);
						}
					}
				}.bind(this), function (err) {
					return err;
				}).then(function () {
					this.views.show();
				}.bind(this));
			}
		}
	}, {
		key: "prev",
		value: function prev() {
			var prev;
			var left;
			var dir = this.settings.direction;

			if (!this.views.length) return;

			if (this.isPaginated && this.settings.axis === "horizontal" && (!dir || dir === "ltr")) {

				this.scrollLeft = this.container.scrollLeft;

				left = this.container.scrollLeft;

				if (left > 0) {
					this.scrollBy(-this.layout.delta, 0, true);
				} else {
					prev = this.views.first().section.prev();
				}
			} else if (this.isPaginated && this.settings.axis === "horizontal" && dir === "rtl") {

				this.scrollLeft = this.container.scrollLeft;

				left = this.container.scrollLeft + this.container.offsetWidth + this.layout.delta;

				if (left <= this.container.scrollWidth) {
					this.scrollBy(-this.layout.delta, 0, true);
				} else {
					prev = this.views.first().section.prev();
				}
			} else if (this.isPaginated && this.settings.axis === "vertical") {

				this.scrollTop = this.container.scrollTop;

				var top = this.container.scrollTop;

				if (top > 0) {
					this.scrollBy(0, -this.layout.height, true);
				} else {
					prev = this.views.first().section.prev();
				}
			} else {

				prev = this.views.first().section.prev();
			}

			if (prev) {
				this.clear();

				return this.prepend(prev).then(function () {
					var left;
					if (this.layout.name === "pre-paginated" && this.layout.divisor > 1) {
						left = prev.prev();
						if (left) {
							return this.prepend(left);
						}
					}
				}.bind(this), function (err) {
					return err;
				}).then(function () {
					if (this.isPaginated && this.settings.axis === "horizontal") {
						if (this.settings.direction === "rtl") {
							this.scrollTo(0, 0, true);
						} else {
							this.scrollTo(this.container.scrollWidth - this.layout.delta, 0, true);
						}
					}
					this.views.show();
				}.bind(this));
			}
		}
	}, {
		key: "current",
		value: function current() {
			var visible = this.visible();
			if (visible.length) {
				// Current is the last visible view
				return visible[visible.length - 1];
			}
			return null;
		}
	}, {
		key: "clear",
		value: function clear() {

			// this.q.clear();

			if (this.views) {
				this.views.hide();
				this.scrollTo(0, 0, true);
				this.views.clear();
			}
		}
	}, {
		key: "currentLocation",
		value: function currentLocation() {

			if (this.settings.axis === "vertical") {
				this.location = this.scrolledLocation();
			} else {
				this.location = this.paginatedLocation();
			}
			return this.location;
		}
	}, {
		key: "scrolledLocation",
		value: function scrolledLocation() {
			var _this4 = this;

			var visible = this.visible();
			var container = this.container.getBoundingClientRect();
			var pageHeight = container.height < window.innerHeight ? container.height : window.innerHeight;

			var offset = 0;
			var used = 0;

			if (this.settings.fullsize) {
				offset = window.scrollY;
			}

			var sections = visible.map(function (view) {
				var _view$section = view.section,
				    index = _view$section.index,
				    href = _view$section.href;

				var position = view.position();
				var height = view.height();

				var startPos = offset + container.top - position.top + used;
				var endPos = startPos + pageHeight - used;
				if (endPos > height) {
					endPos = height;
					used = endPos - startPos;
				}

				var totalPages = _this4.layout.count(height, pageHeight).pages;

				var currPage = Math.ceil(startPos / pageHeight);
				var pages = [];
				var endPage = Math.ceil(endPos / pageHeight);

				pages = [];
				for (var i = currPage; i <= endPage; i++) {
					var pg = i + 1;
					pages.push(pg);
				}

				var mapping = _this4.mapping.page(view.contents, view.section.cfiBase, startPos, endPos);

				return {
					index: index,
					href: href,
					pages: pages,
					totalPages: totalPages,
					mapping: mapping
				};
			});

			return sections;
		}
	}, {
		key: "paginatedLocation",
		value: function paginatedLocation() {
			var _this5 = this;

			var visible = this.visible();
			var container = this.container.getBoundingClientRect();

			var left = 0;
			var used = 0;

			if (this.settings.fullsize) {
				left = window.scrollX;
			}

			var sections = visible.map(function (view) {
				var _view$section2 = view.section,
				    index = _view$section2.index,
				    href = _view$section2.href;

				var offset = view.offset().left;
				var position = view.position().left;
				var width = view.width();

				// Find mapping
				var start = left + container.left - position + used;
				var end = start + _this5.layout.width - used;

				var mapping = _this5.mapping.page(view.contents, view.section.cfiBase, start, end);

				// Find displayed pages
				//console.log("pre", end, offset + width);
				// if (end > offset + width) {
				// 	end = offset + width;
				// 	used = this.layout.pageWidth;
				// }
				// console.log("post", end);

				var totalPages = _this5.layout.count(width).pages;
				var startPage = Math.floor(start / _this5.layout.pageWidth);
				var pages = [];
				var endPage = Math.floor(end / _this5.layout.pageWidth);

				// start page should not be negative
				if (startPage < 0) {
					startPage = 0;
					endPage = endPage + 1;
				}

				// Reverse page counts for rtl
				if (_this5.settings.direction === "rtl") {
					var tempStartPage = startPage;
					startPage = totalPages - endPage;
					endPage = totalPages - tempStartPage;
				}

				for (var i = startPage + 1; i <= endPage; i++) {
					var pg = i;
					pages.push(pg);
				}

				return {
					index: index,
					href: href,
					pages: pages,
					totalPages: totalPages,
					mapping: mapping
				};
			});

			return sections;
		}
	}, {
		key: "isVisible",
		value: function isVisible(view, offsetPrev, offsetNext, _container) {
			var position = view.position();
			var container = _container || this.bounds();

			if (this.settings.axis === "horizontal" && position.right > container.left - offsetPrev && position.left < container.right + offsetNext) {

				return true;
			} else if (this.settings.axis === "vertical" && position.bottom > container.top - offsetPrev && position.top < container.bottom + offsetNext) {

				return true;
			}

			return false;
		}
	}, {
		key: "visible",
		value: function visible() {
			var container = this.bounds();
			var views = this.views.displayed();
			var viewsLength = views.length;
			var visible = [];
			var isVisible;
			var view;

			for (var i = 0; i < viewsLength; i++) {
				view = views[i];
				isVisible = this.isVisible(view, 0, 0, container);

				if (isVisible === true) {
					visible.push(view);
				}
			}
			return visible;
		}
	}, {
		key: "scrollBy",
		value: function scrollBy(x, y, silent) {
			var dir = this.settings.direction === "rtl" ? -1 : 1;

			if (silent) {
				this.ignore = true;
			}

			if (!this.settings.fullsize) {
				if (x) this.container.scrollLeft += x * dir;
				if (y) this.container.scrollTop += y;
			} else {
				window.scrollBy(x * dir, y * dir);
			}
			this.scrolled = true;
		}
	}, {
		key: "scrollTo",
		value: function scrollTo(x, y, silent) {
			if (silent) {
				this.ignore = true;
			}

			if (!this.settings.fullsize) {
				this.container.scrollLeft = x;
				this.container.scrollTop = y;
			} else {
				window.scrollTo(x, y);
			}
			this.scrolled = true;
		}
	}, {
		key: "onScroll",
		value: function onScroll() {
			var scrollTop = void 0;
			var scrollLeft = void 0;

			if (!this.settings.fullsize) {
				scrollTop = this.container.scrollTop;
				scrollLeft = this.container.scrollLeft;
			} else {
				scrollTop = window.scrollY;
				scrollLeft = window.scrollX;
			}

			this.scrollTop = scrollTop;
			this.scrollLeft = scrollLeft;

			if (!this.ignore) {
				this.emit(_constants.EVENTS.MANAGERS.SCROLL, {
					top: scrollTop,
					left: scrollLeft
				});

				clearTimeout(this.afterScrolled);
				this.afterScrolled = setTimeout(function () {
					this.emit(_constants.EVENTS.MANAGERS.SCROLLED, {
						top: this.scrollTop,
						left: this.scrollLeft
					});
				}.bind(this), 20);
			} else {
				this.ignore = false;
			}
		}
	}, {
		key: "bounds",
		value: function bounds() {
			var bounds;

			bounds = this.stage.bounds();

			return bounds;
		}
	}, {
		key: "applyLayout",
		value: function applyLayout(layout) {

			this.layout = layout;
			this.updateLayout();
			// this.manager.layout(this.layout.format);
		}
	}, {
		key: "updateLayout",
		value: function updateLayout() {

			if (!this.stage) {
				return;
			}

			this._stageSize = this.stage.size();

			if (!this.isPaginated) {
				this.layout.calculate(this._stageSize.width, this._stageSize.height);
			} else {
				this.layout.calculate(this._stageSize.width, this._stageSize.height, this.settings.gap);

				// Set the look ahead offset for what is visible
				this.settings.offset = this.layout.delta;

				// this.stage.addStyleRules("iframe", [{"margin-right" : this.layout.gap + "px"}]);
			}

			// Set the dimensions for views
			this.viewSettings.width = this.layout.width;
			this.viewSettings.height = this.layout.height;

			this.setLayout(this.layout);
		}
	}, {
		key: "setLayout",
		value: function setLayout(layout) {

			this.viewSettings.layout = layout;

			this.mapping = new _mapping2.default(layout.props, this.settings.direction, this.settings.axis);

			if (this.views) {

				this.views.forEach(function (view) {
					if (view) {
						view.setLayout(layout);
					}
				});
			}
		}
	}, {
		key: "updateAxis",
		value: function updateAxis(axis, forceUpdate) {

			if (!this.isPaginated) {
				axis = "vertical";
			}

			if (!forceUpdate && axis === this.settings.axis) {
				return;
			}

			this.settings.axis = axis;

			this.stage && this.stage.axis(axis);

			this.viewSettings.axis = axis;

			if (this.mapping) {
				this.mapping = new _mapping2.default(this.layout.props, this.settings.direction, this.settings.axis);
			}

			if (this.layout) {
				if (axis === "vertical") {
					this.layout.spread("none");
				} else {
					this.layout.spread(this.layout.settings.spread);
				}
			}
		}
	}, {
		key: "updateFlow",
		value: function updateFlow(flow) {
			var defaultScrolledOverflow = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : "auto";

			var isPaginated = flow === "paginated" || flow === "auto";

			this.isPaginated = isPaginated;

			if (flow === "scrolled-doc" || flow === "scrolled-continuous" || flow === "scrolled") {
				this.updateAxis("vertical");
			} else {
				this.updateAxis("horizontal");
			}

			this.viewSettings.flow = flow;

			if (!this.settings.overflow) {
				this.overflow = isPaginated ? "hidden" : defaultScrolledOverflow;
			} else {
				this.overflow = this.settings.overflow;
			}

			this.stage && this.stage.overflow(this.overflow);

			this.updateLayout();
		}
	}, {
		key: "getContents",
		value: function getContents() {
			var contents = [];
			if (!this.views) {
				return contents;
			}
			this.views.forEach(function (view) {
				var viewContents = view && view.contents;
				if (viewContents) {
					contents.push(viewContents);
				}
			});
			return contents;
		}
	}, {
		key: "direction",
		value: function direction() {
			var dir = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : "ltr";

			this.settings.direction = dir;

			this.stage && this.stage.direction(dir);

			this.viewSettings.direction = dir;

			this.updateLayout();
		}
	}, {
		key: "isRendered",
		value: function isRendered() {
			return this.rendered;
		}
	}]);

	return DefaultViewManager;
}();

//-- Enable binding events to Manager


(0, _eventEmitter2.default)(DefaultViewManager.prototype);

exports.default = DefaultViewManager;
module.exports = exports["default"];

/***/ }),
/* 106 */
/***/ (function(module, exports) {

/**
 * Checks if `value` is the
 * [language type](http://www.ecma-international.org/ecma-262/7.0/#sec-ecmascript-language-types)
 * of `Object`. (e.g. arrays, functions, objects, regexes, `new Number(0)`, and `new String('')`)
 *
 * @static
 * @memberOf _
 * @since 0.1.0
 * @category Lang
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is an object, else `false`.
 * @example
 *
 * _.isObject({});
 * // => true
 *
 * _.isObject([1, 2, 3]);
 * // => true
 *
 * _.isObject(_.noop);
 * // => true
 *
 * _.isObject(null);
 * // => false
 */
function isObject(value) {
  var type = typeof value;
  return value != null && (type == 'object' || type == 'function');
}

module.exports = isObject;


/***/ }),
/* 107 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = !__webpack_require__(7) && !__webpack_require__(3)(function () {
  return Object.defineProperty(__webpack_require__(74)('div'), 'a', { get: function () { return 7; } }).a != 7;
});


/***/ }),
/* 108 */
/***/ (function(module, exports, __webpack_require__) {

exports.f = __webpack_require__(5);


/***/ }),
/* 109 */
/***/ (function(module, exports, __webpack_require__) {

var has = __webpack_require__(12);
var toIObject = __webpack_require__(15);
var arrayIndexOf = __webpack_require__(56)(false);
var IE_PROTO = __webpack_require__(76)('IE_PROTO');

module.exports = function (object, names) {
  var O = toIObject(object);
  var i = 0;
  var result = [];
  var key;
  for (key in O) if (key != IE_PROTO) has(O, key) && result.push(key);
  // Don't enum bug & hidden keys
  while (names.length > i) if (has(O, key = names[i++])) {
    ~arrayIndexOf(result, key) || result.push(key);
  }
  return result;
};


/***/ }),
/* 110 */
/***/ (function(module, exports, __webpack_require__) {

var dP = __webpack_require__(8);
var anObject = __webpack_require__(1);
var getKeys = __webpack_require__(34);

module.exports = __webpack_require__(7) ? Object.defineProperties : function defineProperties(O, Properties) {
  anObject(O);
  var keys = getKeys(Properties);
  var length = keys.length;
  var i = 0;
  var P;
  while (length > i) dP.f(O, P = keys[i++], Properties[P]);
  return O;
};


/***/ }),
/* 111 */
/***/ (function(module, exports, __webpack_require__) {

// fallback for IE11 buggy Object.getOwnPropertyNames with iframe and window
var toIObject = __webpack_require__(15);
var gOPN = __webpack_require__(41).f;
var toString = {}.toString;

var windowNames = typeof window == 'object' && window && Object.getOwnPropertyNames
  ? Object.getOwnPropertyNames(window) : [];

var getWindowNames = function (it) {
  try {
    return gOPN(it);
  } catch (e) {
    return windowNames.slice();
  }
};

module.exports.f = function getOwnPropertyNames(it) {
  return windowNames && toString.call(it) == '[object Window]' ? getWindowNames(it) : gOPN(toIObject(it));
};


/***/ }),
/* 112 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// 19.1.2.1 Object.assign(target, source, ...)
var getKeys = __webpack_require__(34);
var gOPS = __webpack_require__(57);
var pIE = __webpack_require__(53);
var toObject = __webpack_require__(10);
var IObject = __webpack_require__(52);
var $assign = Object.assign;

// should work with symbols and should have deterministic property order (V8 bug)
module.exports = !$assign || __webpack_require__(3)(function () {
  var A = {};
  var B = {};
  // eslint-disable-next-line no-undef
  var S = Symbol();
  var K = 'abcdefghijklmnopqrst';
  A[S] = 7;
  K.split('').forEach(function (k) { B[k] = k; });
  return $assign({}, A)[S] != 7 || Object.keys($assign({}, B)).join('') != K;
}) ? function assign(target, source) { // eslint-disable-line no-unused-vars
  var T = toObject(target);
  var aLen = arguments.length;
  var index = 1;
  var getSymbols = gOPS.f;
  var isEnum = pIE.f;
  while (aLen > index) {
    var S = IObject(arguments[index++]);
    var keys = getSymbols ? getKeys(S).concat(getSymbols(S)) : getKeys(S);
    var length = keys.length;
    var j = 0;
    var key;
    while (length > j) if (isEnum.call(S, key = keys[j++])) T[key] = S[key];
  } return T;
} : $assign;


/***/ }),
/* 113 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var aFunction = __webpack_require__(11);
var isObject = __webpack_require__(4);
var invoke = __webpack_require__(59);
var arraySlice = [].slice;
var factories = {};

var construct = function (F, len, args) {
  if (!(len in factories)) {
    for (var n = [], i = 0; i < len; i++) n[i] = 'a[' + i + ']';
    // eslint-disable-next-line no-new-func
    factories[len] = Function('F,a', 'return new F(' + n.join(',') + ')');
  } return factories[len](F, args);
};

module.exports = Function.bind || function bind(that /* , ...args */) {
  var fn = aFunction(this);
  var partArgs = arraySlice.call(arguments, 1);
  var bound = function (/* args... */) {
    var args = partArgs.concat(arraySlice.call(arguments));
    return this instanceof bound ? construct(fn, args.length, args) : invoke(fn, args, that);
  };
  if (isObject(fn.prototype)) bound.prototype = fn.prototype;
  return bound;
};


/***/ }),
/* 114 */
/***/ (function(module, exports, __webpack_require__) {

var $parseInt = __webpack_require__(2).parseInt;
var $trim = __webpack_require__(49).trim;
var ws = __webpack_require__(80);
var hex = /^[-+]?0[xX]/;

module.exports = $parseInt(ws + '08') !== 8 || $parseInt(ws + '0x16') !== 22 ? function parseInt(str, radix) {
  var string = $trim(String(str), 3);
  return $parseInt(string, (radix >>> 0) || (hex.test(string) ? 16 : 10));
} : $parseInt;


/***/ }),
/* 115 */
/***/ (function(module, exports, __webpack_require__) {

var $parseFloat = __webpack_require__(2).parseFloat;
var $trim = __webpack_require__(49).trim;

module.exports = 1 / $parseFloat(__webpack_require__(80) + '-0') !== -Infinity ? function parseFloat(str) {
  var string = $trim(String(str), 3);
  var result = $parseFloat(string);
  return result === 0 && string.charAt(0) == '-' ? -0 : result;
} : $parseFloat;


/***/ }),
/* 116 */
/***/ (function(module, exports, __webpack_require__) {

var cof = __webpack_require__(20);
module.exports = function (it, msg) {
  if (typeof it != 'number' && cof(it) != 'Number') throw TypeError(msg);
  return +it;
};


/***/ }),
/* 117 */
/***/ (function(module, exports, __webpack_require__) {

// 20.1.2.3 Number.isInteger(number)
var isObject = __webpack_require__(4);
var floor = Math.floor;
module.exports = function isInteger(it) {
  return !isObject(it) && isFinite(it) && floor(it) === it;
};


/***/ }),
/* 118 */
/***/ (function(module, exports) {

// 20.2.2.20 Math.log1p(x)
module.exports = Math.log1p || function log1p(x) {
  return (x = +x) > -1e-8 && x < 1e-8 ? x - x * x / 2 : Math.log(1 + x);
};


/***/ }),
/* 119 */
/***/ (function(module, exports, __webpack_require__) {

// 20.2.2.16 Math.fround(x)
var sign = __webpack_require__(83);
var pow = Math.pow;
var EPSILON = pow(2, -52);
var EPSILON32 = pow(2, -23);
var MAX32 = pow(2, 127) * (2 - EPSILON32);
var MIN32 = pow(2, -126);

var roundTiesToEven = function (n) {
  return n + 1 / EPSILON - 1 / EPSILON;
};

module.exports = Math.fround || function fround(x) {
  var $abs = Math.abs(x);
  var $sign = sign(x);
  var a, result;
  if ($abs < MIN32) return $sign * roundTiesToEven($abs / MIN32 / EPSILON32) * MIN32 * EPSILON32;
  a = (1 + EPSILON32 / EPSILON) * $abs;
  result = a - (a - $abs);
  // eslint-disable-next-line no-self-compare
  if (result > MAX32 || result != result) return $sign * Infinity;
  return $sign * result;
};


/***/ }),
/* 120 */
/***/ (function(module, exports, __webpack_require__) {

// call something on iterator step with safe closing on error
var anObject = __webpack_require__(1);
module.exports = function (iterator, fn, value, entries) {
  try {
    return entries ? fn(anObject(value)[0], value[1]) : fn(value);
  // 7.4.6 IteratorClose(iterator, completion)
  } catch (e) {
    var ret = iterator['return'];
    if (ret !== undefined) anObject(ret.call(iterator));
    throw e;
  }
};


/***/ }),
/* 121 */
/***/ (function(module, exports, __webpack_require__) {

var aFunction = __webpack_require__(11);
var toObject = __webpack_require__(10);
var IObject = __webpack_require__(52);
var toLength = __webpack_require__(9);

module.exports = function (that, callbackfn, aLen, memo, isRight) {
  aFunction(callbackfn);
  var O = toObject(that);
  var self = IObject(O);
  var length = toLength(O.length);
  var index = isRight ? length - 1 : 0;
  var i = isRight ? -1 : 1;
  if (aLen < 2) for (;;) {
    if (index in self) {
      memo = self[index];
      index += i;
      break;
    }
    index += i;
    if (isRight ? index < 0 : length <= index) {
      throw TypeError('Reduce of empty array with no initial value');
    }
  }
  for (;isRight ? index >= 0 : length > index; index += i) if (index in self) {
    memo = callbackfn(memo, self[index], index, O);
  }
  return memo;
};


/***/ }),
/* 122 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
// 22.1.3.3 Array.prototype.copyWithin(target, start, end = this.length)

var toObject = __webpack_require__(10);
var toAbsoluteIndex = __webpack_require__(39);
var toLength = __webpack_require__(9);

module.exports = [].copyWithin || function copyWithin(target /* = 0 */, start /* = 0, end = @length */) {
  var O = toObject(this);
  var len = toLength(O.length);
  var to = toAbsoluteIndex(target, len);
  var from = toAbsoluteIndex(start, len);
  var end = arguments.length > 2 ? arguments[2] : undefined;
  var count = Math.min((end === undefined ? len : toAbsoluteIndex(end, len)) - from, len - to);
  var inc = 1;
  if (from < to && to < from + count) {
    inc = -1;
    from += count - 1;
    to += count - 1;
  }
  while (count-- > 0) {
    if (from in O) O[to] = O[from];
    else delete O[to];
    to += inc;
    from += inc;
  } return O;
};


/***/ }),
/* 123 */
/***/ (function(module, exports) {

module.exports = function (done, value) {
  return { value: value, done: !!done };
};


/***/ }),
/* 124 */
/***/ (function(module, exports, __webpack_require__) {

// 21.2.5.3 get RegExp.prototype.flags()
if (__webpack_require__(7) && /./g.flags != 'g') __webpack_require__(8).f(RegExp.prototype, 'flags', {
  configurable: true,
  get: __webpack_require__(62)
});


/***/ }),
/* 125 */
/***/ (function(module, exports) {

module.exports = function (exec) {
  try {
    return { e: false, v: exec() };
  } catch (e) {
    return { e: true, v: e };
  }
};


/***/ }),
/* 126 */
/***/ (function(module, exports, __webpack_require__) {

var newPromiseCapability = __webpack_require__(98);

module.exports = function (C, x) {
  var promiseCapability = newPromiseCapability.f(C);
  var resolve = promiseCapability.resolve;
  resolve(x);
  return promiseCapability.promise;
};


/***/ }),
/* 127 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var strong = __webpack_require__(128);
var validate = __webpack_require__(51);
var MAP = 'Map';

// 23.1 Map Objects
module.exports = __webpack_require__(65)(MAP, function (get) {
  return function Map() { return get(this, arguments.length > 0 ? arguments[0] : undefined); };
}, {
  // 23.1.3.6 Map.prototype.get(key)
  get: function get(key) {
    var entry = strong.getEntry(validate(this, MAP), key);
    return entry && entry.v;
  },
  // 23.1.3.9 Map.prototype.set(key, value)
  set: function set(key, value) {
    return strong.def(validate(this, MAP), key === 0 ? 0 : key, value);
  }
}, strong, true);


/***/ }),
/* 128 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var dP = __webpack_require__(8).f;
var create = __webpack_require__(40);
var redefineAll = __webpack_require__(45);
var ctx = __webpack_require__(19);
var anInstance = __webpack_require__(43);
var forOf = __webpack_require__(44);
var $iterDefine = __webpack_require__(86);
var step = __webpack_require__(123);
var setSpecies = __webpack_require__(42);
var DESCRIPTORS = __webpack_require__(7);
var fastKey = __webpack_require__(33).fastKey;
var validate = __webpack_require__(51);
var SIZE = DESCRIPTORS ? '_s' : 'size';

var getEntry = function (that, key) {
  // fast case
  var index = fastKey(key);
  var entry;
  if (index !== 'F') return that._i[index];
  // frozen object case
  for (entry = that._f; entry; entry = entry.n) {
    if (entry.k == key) return entry;
  }
};

module.exports = {
  getConstructor: function (wrapper, NAME, IS_MAP, ADDER) {
    var C = wrapper(function (that, iterable) {
      anInstance(that, C, NAME, '_i');
      that._t = NAME;         // collection type
      that._i = create(null); // index
      that._f = undefined;    // first entry
      that._l = undefined;    // last entry
      that[SIZE] = 0;         // size
      if (iterable != undefined) forOf(iterable, IS_MAP, that[ADDER], that);
    });
    redefineAll(C.prototype, {
      // 23.1.3.1 Map.prototype.clear()
      // 23.2.3.2 Set.prototype.clear()
      clear: function clear() {
        for (var that = validate(this, NAME), data = that._i, entry = that._f; entry; entry = entry.n) {
          entry.r = true;
          if (entry.p) entry.p = entry.p.n = undefined;
          delete data[entry.i];
        }
        that._f = that._l = undefined;
        that[SIZE] = 0;
      },
      // 23.1.3.3 Map.prototype.delete(key)
      // 23.2.3.4 Set.prototype.delete(value)
      'delete': function (key) {
        var that = validate(this, NAME);
        var entry = getEntry(that, key);
        if (entry) {
          var next = entry.n;
          var prev = entry.p;
          delete that._i[entry.i];
          entry.r = true;
          if (prev) prev.n = next;
          if (next) next.p = prev;
          if (that._f == entry) that._f = next;
          if (that._l == entry) that._l = prev;
          that[SIZE]--;
        } return !!entry;
      },
      // 23.2.3.6 Set.prototype.forEach(callbackfn, thisArg = undefined)
      // 23.1.3.5 Map.prototype.forEach(callbackfn, thisArg = undefined)
      forEach: function forEach(callbackfn /* , that = undefined */) {
        validate(this, NAME);
        var f = ctx(callbackfn, arguments.length > 1 ? arguments[1] : undefined, 3);
        var entry;
        while (entry = entry ? entry.n : this._f) {
          f(entry.v, entry.k, this);
          // revert to the last existing entry
          while (entry && entry.r) entry = entry.p;
        }
      },
      // 23.1.3.7 Map.prototype.has(key)
      // 23.2.3.7 Set.prototype.has(value)
      has: function has(key) {
        return !!getEntry(validate(this, NAME), key);
      }
    });
    if (DESCRIPTORS) dP(C.prototype, 'size', {
      get: function () {
        return validate(this, NAME)[SIZE];
      }
    });
    return C;
  },
  def: function (that, key, value) {
    var entry = getEntry(that, key);
    var prev, index;
    // change existing entry
    if (entry) {
      entry.v = value;
    // create new entry
    } else {
      that._l = entry = {
        i: index = fastKey(key, true), // <- index
        k: key,                        // <- key
        v: value,                      // <- value
        p: prev = that._l,             // <- previous entry
        n: undefined,                  // <- next entry
        r: false                       // <- removed
      };
      if (!that._f) that._f = entry;
      if (prev) prev.n = entry;
      that[SIZE]++;
      // add to index
      if (index !== 'F') that._i[index] = entry;
    } return that;
  },
  getEntry: getEntry,
  setStrong: function (C, NAME, IS_MAP) {
    // add .keys, .values, .entries, [@@iterator]
    // 23.1.3.4, 23.1.3.8, 23.1.3.11, 23.1.3.12, 23.2.3.5, 23.2.3.8, 23.2.3.10, 23.2.3.11
    $iterDefine(C, NAME, function (iterated, kind) {
      this._t = validate(iterated, NAME); // target
      this._k = kind;                     // kind
      this._l = undefined;                // previous
    }, function () {
      var that = this;
      var kind = that._k;
      var entry = that._l;
      // revert to the last existing entry
      while (entry && entry.r) entry = entry.p;
      // get next entry
      if (!that._t || !(that._l = entry = entry ? entry.n : that._t._f)) {
        // or finish the iteration
        that._t = undefined;
        return step(1);
      }
      // return step by kind
      if (kind == 'keys') return step(0, entry.k);
      if (kind == 'values') return step(0, entry.v);
      return step(0, [entry.k, entry.v]);
    }, IS_MAP ? 'entries' : 'values', !IS_MAP, true);

    // add [@@species], 23.1.2.2, 23.2.2.2
    setSpecies(NAME);
  }
};


/***/ }),
/* 129 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var strong = __webpack_require__(128);
var validate = __webpack_require__(51);
var SET = 'Set';

// 23.2 Set Objects
module.exports = __webpack_require__(65)(SET, function (get) {
  return function Set() { return get(this, arguments.length > 0 ? arguments[0] : undefined); };
}, {
  // 23.2.3.1 Set.prototype.add(value)
  add: function add(value) {
    return strong.def(validate(this, SET), value = value === 0 ? 0 : value, value);
  }
}, strong);


/***/ }),
/* 130 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var each = __webpack_require__(29)(0);
var redefine = __webpack_require__(14);
var meta = __webpack_require__(33);
var assign = __webpack_require__(112);
var weak = __webpack_require__(131);
var isObject = __webpack_require__(4);
var fails = __webpack_require__(3);
var validate = __webpack_require__(51);
var WEAK_MAP = 'WeakMap';
var getWeak = meta.getWeak;
var isExtensible = Object.isExtensible;
var uncaughtFrozenStore = weak.ufstore;
var tmp = {};
var InternalMap;

var wrapper = function (get) {
  return function WeakMap() {
    return get(this, arguments.length > 0 ? arguments[0] : undefined);
  };
};

var methods = {
  // 23.3.3.3 WeakMap.prototype.get(key)
  get: function get(key) {
    if (isObject(key)) {
      var data = getWeak(key);
      if (data === true) return uncaughtFrozenStore(validate(this, WEAK_MAP)).get(key);
      return data ? data[this._i] : undefined;
    }
  },
  // 23.3.3.5 WeakMap.prototype.set(key, value)
  set: function set(key, value) {
    return weak.def(validate(this, WEAK_MAP), key, value);
  }
};

// 23.3 WeakMap Objects
var $WeakMap = module.exports = __webpack_require__(65)(WEAK_MAP, wrapper, methods, weak, true, true);

// IE11 WeakMap frozen keys fix
if (fails(function () { return new $WeakMap().set((Object.freeze || Object)(tmp), 7).get(tmp) != 7; })) {
  InternalMap = weak.getConstructor(wrapper, WEAK_MAP);
  assign(InternalMap.prototype, methods);
  meta.NEED = true;
  each(['delete', 'has', 'get', 'set'], function (key) {
    var proto = $WeakMap.prototype;
    var method = proto[key];
    redefine(proto, key, function (a, b) {
      // store frozen objects on internal weakmap shim
      if (isObject(a) && !isExtensible(a)) {
        if (!this._f) this._f = new InternalMap();
        var result = this._f[key](a, b);
        return key == 'set' ? this : result;
      // store all the rest on native weakmap
      } return method.call(this, a, b);
    });
  });
}


/***/ }),
/* 131 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var redefineAll = __webpack_require__(45);
var getWeak = __webpack_require__(33).getWeak;
var anObject = __webpack_require__(1);
var isObject = __webpack_require__(4);
var anInstance = __webpack_require__(43);
var forOf = __webpack_require__(44);
var createArrayMethod = __webpack_require__(29);
var $has = __webpack_require__(12);
var validate = __webpack_require__(51);
var arrayFind = createArrayMethod(5);
var arrayFindIndex = createArrayMethod(6);
var id = 0;

// fallback for uncaught frozen keys
var uncaughtFrozenStore = function (that) {
  return that._l || (that._l = new UncaughtFrozenStore());
};
var UncaughtFrozenStore = function () {
  this.a = [];
};
var findUncaughtFrozen = function (store, key) {
  return arrayFind(store.a, function (it) {
    return it[0] === key;
  });
};
UncaughtFrozenStore.prototype = {
  get: function (key) {
    var entry = findUncaughtFrozen(this, key);
    if (entry) return entry[1];
  },
  has: function (key) {
    return !!findUncaughtFrozen(this, key);
  },
  set: function (key, value) {
    var entry = findUncaughtFrozen(this, key);
    if (entry) entry[1] = value;
    else this.a.push([key, value]);
  },
  'delete': function (key) {
    var index = arrayFindIndex(this.a, function (it) {
      return it[0] === key;
    });
    if (~index) this.a.splice(index, 1);
    return !!~index;
  }
};

module.exports = {
  getConstructor: function (wrapper, NAME, IS_MAP, ADDER) {
    var C = wrapper(function (that, iterable) {
      anInstance(that, C, NAME, '_i');
      that._t = NAME;      // collection type
      that._i = id++;      // collection id
      that._l = undefined; // leak store for uncaught frozen objects
      if (iterable != undefined) forOf(iterable, IS_MAP, that[ADDER], that);
    });
    redefineAll(C.prototype, {
      // 23.3.3.2 WeakMap.prototype.delete(key)
      // 23.4.3.3 WeakSet.prototype.delete(value)
      'delete': function (key) {
        if (!isObject(key)) return false;
        var data = getWeak(key);
        if (data === true) return uncaughtFrozenStore(validate(this, NAME))['delete'](key);
        return data && $has(data, this._i) && delete data[this._i];
      },
      // 23.3.3.4 WeakMap.prototype.has(key)
      // 23.4.3.4 WeakSet.prototype.has(value)
      has: function has(key) {
        if (!isObject(key)) return false;
        var data = getWeak(key);
        if (data === true) return uncaughtFrozenStore(validate(this, NAME)).has(key);
        return data && $has(data, this._i);
      }
    });
    return C;
  },
  def: function (that, key, value) {
    var data = getWeak(anObject(key), true);
    if (data === true) uncaughtFrozenStore(that).set(key, value);
    else data[that._i] = value;
    return that;
  },
  ufstore: uncaughtFrozenStore
};


/***/ }),
/* 132 */
/***/ (function(module, exports, __webpack_require__) {

// https://tc39.github.io/ecma262/#sec-toindex
var toInteger = __webpack_require__(27);
var toLength = __webpack_require__(9);
module.exports = function (it) {
  if (it === undefined) return 0;
  var number = toInteger(it);
  var length = toLength(number);
  if (number !== length) throw RangeError('Wrong length!');
  return length;
};


/***/ }),
/* 133 */
/***/ (function(module, exports, __webpack_require__) {

// all object keys, includes non-enumerable and symbols
var gOPN = __webpack_require__(41);
var gOPS = __webpack_require__(57);
var anObject = __webpack_require__(1);
var Reflect = __webpack_require__(2).Reflect;
module.exports = Reflect && Reflect.ownKeys || function ownKeys(it) {
  var keys = gOPN.f(anObject(it));
  var getSymbols = gOPS.f;
  return getSymbols ? keys.concat(getSymbols(it)) : keys;
};


/***/ }),
/* 134 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// https://tc39.github.io/proposal-flatMap/#sec-FlattenIntoArray
var isArray = __webpack_require__(58);
var isObject = __webpack_require__(4);
var toLength = __webpack_require__(9);
var ctx = __webpack_require__(19);
var IS_CONCAT_SPREADABLE = __webpack_require__(5)('isConcatSpreadable');

function flattenIntoArray(target, original, source, sourceLen, start, depth, mapper, thisArg) {
  var targetIndex = start;
  var sourceIndex = 0;
  var mapFn = mapper ? ctx(mapper, thisArg, 3) : false;
  var element, spreadable;

  while (sourceIndex < sourceLen) {
    if (sourceIndex in source) {
      element = mapFn ? mapFn(source[sourceIndex], sourceIndex, original) : source[sourceIndex];

      spreadable = false;
      if (isObject(element)) {
        spreadable = element[IS_CONCAT_SPREADABLE];
        spreadable = spreadable !== undefined ? !!spreadable : isArray(element);
      }

      if (spreadable && depth > 0) {
        targetIndex = flattenIntoArray(target, original, element, toLength(element.length), targetIndex, depth - 1) - 1;
      } else {
        if (targetIndex >= 0x1fffffffffffff) throw TypeError();
        target[targetIndex] = element;
      }

      targetIndex++;
    }
    sourceIndex++;
  }
  return targetIndex;
}

module.exports = flattenIntoArray;


/***/ }),
/* 135 */
/***/ (function(module, exports, __webpack_require__) {

// https://github.com/tc39/proposal-string-pad-start-end
var toLength = __webpack_require__(9);
var repeat = __webpack_require__(82);
var defined = __webpack_require__(26);

module.exports = function (that, maxLength, fillString, left) {
  var S = String(defined(that));
  var stringLength = S.length;
  var fillStr = fillString === undefined ? ' ' : String(fillString);
  var intMaxLength = toLength(maxLength);
  if (intMaxLength <= stringLength || fillStr == '') return S;
  var fillLen = intMaxLength - stringLength;
  var stringFiller = repeat.call(fillStr, Math.ceil(fillLen / fillStr.length));
  if (stringFiller.length > fillLen) stringFiller = stringFiller.slice(0, fillLen);
  return left ? stringFiller + S : S + stringFiller;
};


/***/ }),
/* 136 */
/***/ (function(module, exports, __webpack_require__) {

var getKeys = __webpack_require__(34);
var toIObject = __webpack_require__(15);
var isEnum = __webpack_require__(53).f;
module.exports = function (isEntries) {
  return function (it) {
    var O = toIObject(it);
    var keys = getKeys(O);
    var length = keys.length;
    var i = 0;
    var result = [];
    var key;
    while (length > i) if (isEnum.call(O, key = keys[i++])) {
      result.push(isEntries ? [key, O[key]] : O[key]);
    } return result;
  };
};


/***/ }),
/* 137 */
/***/ (function(module, exports, __webpack_require__) {

// https://github.com/DavidBruant/Map-Set.prototype.toJSON
var classof = __webpack_require__(54);
var from = __webpack_require__(138);
module.exports = function (NAME) {
  return function toJSON() {
    if (classof(this) != NAME) throw TypeError(NAME + "#toJSON isn't generic");
    return from(this);
  };
};


/***/ }),
/* 138 */
/***/ (function(module, exports, __webpack_require__) {

var forOf = __webpack_require__(44);

module.exports = function (iter, ITERATOR) {
  var result = [];
  forOf(iter, false, result.push, result, ITERATOR);
  return result;
};


/***/ }),
/* 139 */
/***/ (function(module, exports) {

// https://rwaldron.github.io/proposal-math-extensions/
module.exports = Math.scale || function scale(x, inLow, inHigh, outLow, outHigh) {
  if (
    arguments.length === 0
      // eslint-disable-next-line no-self-compare
      || x != x
      // eslint-disable-next-line no-self-compare
      || inLow != inLow
      // eslint-disable-next-line no-self-compare
      || inHigh != inHigh
      // eslint-disable-next-line no-self-compare
      || outLow != outLow
      // eslint-disable-next-line no-self-compare
      || outHigh != outHigh
  ) return NaN;
  if (x === Infinity || x === -Infinity) return x;
  return (x - inLow) * (outHigh - outLow) / (inHigh - inLow) + outLow;
};


/***/ }),
/* 140 */
/***/ (function(module, exports) {

/*
 * DOM Level 2
 * Object DOMException
 * @see http://www.w3.org/TR/REC-DOM-Level-1/ecma-script-language-binding.html
 * @see http://www.w3.org/TR/2000/REC-DOM-Level-2-Core-20001113/ecma-script-binding.html
 */

function copy(src,dest){
	for(var p in src){
		dest[p] = src[p];
	}
}
/**
^\w+\.prototype\.([_\w]+)\s*=\s*((?:.*\{\s*?[\r\n][\s\S]*?^})|\S.*?(?=[;\r\n]));?
^\w+\.prototype\.([_\w]+)\s*=\s*(\S.*?(?=[;\r\n]));?
 */
function _extends(Class,Super){
	var pt = Class.prototype;
	if(Object.create){
		var ppt = Object.create(Super.prototype)
		pt.__proto__ = ppt;
	}
	if(!(pt instanceof Super)){
		function t(){};
		t.prototype = Super.prototype;
		t = new t();
		copy(pt,t);
		Class.prototype = pt = t;
	}
	if(pt.constructor != Class){
		if(typeof Class != 'function'){
			console.error("unknow Class:"+Class)
		}
		pt.constructor = Class
	}
}
var htmlns = 'http://www.w3.org/1999/xhtml' ;
// Node Types
var NodeType = {}
var ELEMENT_NODE                = NodeType.ELEMENT_NODE                = 1;
var ATTRIBUTE_NODE              = NodeType.ATTRIBUTE_NODE              = 2;
var TEXT_NODE                   = NodeType.TEXT_NODE                   = 3;
var CDATA_SECTION_NODE          = NodeType.CDATA_SECTION_NODE          = 4;
var ENTITY_REFERENCE_NODE       = NodeType.ENTITY_REFERENCE_NODE       = 5;
var ENTITY_NODE                 = NodeType.ENTITY_NODE                 = 6;
var PROCESSING_INSTRUCTION_NODE = NodeType.PROCESSING_INSTRUCTION_NODE = 7;
var COMMENT_NODE                = NodeType.COMMENT_NODE                = 8;
var DOCUMENT_NODE               = NodeType.DOCUMENT_NODE               = 9;
var DOCUMENT_TYPE_NODE          = NodeType.DOCUMENT_TYPE_NODE          = 10;
var DOCUMENT_FRAGMENT_NODE      = NodeType.DOCUMENT_FRAGMENT_NODE      = 11;
var NOTATION_NODE               = NodeType.NOTATION_NODE               = 12;

// ExceptionCode
var ExceptionCode = {}
var ExceptionMessage = {};
var INDEX_SIZE_ERR              = ExceptionCode.INDEX_SIZE_ERR              = ((ExceptionMessage[1]="Index size error"),1);
var DOMSTRING_SIZE_ERR          = ExceptionCode.DOMSTRING_SIZE_ERR          = ((ExceptionMessage[2]="DOMString size error"),2);
var HIERARCHY_REQUEST_ERR       = ExceptionCode.HIERARCHY_REQUEST_ERR       = ((ExceptionMessage[3]="Hierarchy request error"),3);
var WRONG_DOCUMENT_ERR          = ExceptionCode.WRONG_DOCUMENT_ERR          = ((ExceptionMessage[4]="Wrong document"),4);
var INVALID_CHARACTER_ERR       = ExceptionCode.INVALID_CHARACTER_ERR       = ((ExceptionMessage[5]="Invalid character"),5);
var NO_DATA_ALLOWED_ERR         = ExceptionCode.NO_DATA_ALLOWED_ERR         = ((ExceptionMessage[6]="No data allowed"),6);
var NO_MODIFICATION_ALLOWED_ERR = ExceptionCode.NO_MODIFICATION_ALLOWED_ERR = ((ExceptionMessage[7]="No modification allowed"),7);
var NOT_FOUND_ERR               = ExceptionCode.NOT_FOUND_ERR               = ((ExceptionMessage[8]="Not found"),8);
var NOT_SUPPORTED_ERR           = ExceptionCode.NOT_SUPPORTED_ERR           = ((ExceptionMessage[9]="Not supported"),9);
var INUSE_ATTRIBUTE_ERR         = ExceptionCode.INUSE_ATTRIBUTE_ERR         = ((ExceptionMessage[10]="Attribute in use"),10);
//level2
var INVALID_STATE_ERR        	= ExceptionCode.INVALID_STATE_ERR        	= ((ExceptionMessage[11]="Invalid state"),11);
var SYNTAX_ERR               	= ExceptionCode.SYNTAX_ERR               	= ((ExceptionMessage[12]="Syntax error"),12);
var INVALID_MODIFICATION_ERR 	= ExceptionCode.INVALID_MODIFICATION_ERR 	= ((ExceptionMessage[13]="Invalid modification"),13);
var NAMESPACE_ERR            	= ExceptionCode.NAMESPACE_ERR           	= ((ExceptionMessage[14]="Invalid namespace"),14);
var INVALID_ACCESS_ERR       	= ExceptionCode.INVALID_ACCESS_ERR      	= ((ExceptionMessage[15]="Invalid access"),15);


function DOMException(code, message) {
	if(message instanceof Error){
		var error = message;
	}else{
		error = this;
		Error.call(this, ExceptionMessage[code]);
		this.message = ExceptionMessage[code];
		if(Error.captureStackTrace) Error.captureStackTrace(this, DOMException);
	}
	error.code = code;
	if(message) this.message = this.message + ": " + message;
	return error;
};
DOMException.prototype = Error.prototype;
copy(ExceptionCode,DOMException)
/**
 * @see http://www.w3.org/TR/2000/REC-DOM-Level-2-Core-20001113/core.html#ID-536297177
 * The NodeList interface provides the abstraction of an ordered collection of nodes, without defining or constraining how this collection is implemented. NodeList objects in the DOM are live.
 * The items in the NodeList are accessible via an integral index, starting from 0.
 */
function NodeList() {
};
NodeList.prototype = {
	/**
	 * The number of nodes in the list. The range of valid child node indices is 0 to length-1 inclusive.
	 * @standard level1
	 */
	length:0,
	/**
	 * Returns the indexth item in the collection. If index is greater than or equal to the number of nodes in the list, this returns null.
	 * @standard level1
	 * @param index  unsigned long
	 *   Index into the collection.
	 * @return Node
	 * 	The node at the indexth position in the NodeList, or null if that is not a valid index.
	 */
	item: function(index) {
		return this[index] || null;
	},
	toString:function(isHTML,nodeFilter){
		for(var buf = [], i = 0;i<this.length;i++){
			serializeToString(this[i],buf,isHTML,nodeFilter);
		}
		return buf.join('');
	}
};
function LiveNodeList(node,refresh){
	this._node = node;
	this._refresh = refresh
	_updateLiveList(this);
}
function _updateLiveList(list){
	var inc = list._node._inc || list._node.ownerDocument._inc;
	if(list._inc != inc){
		var ls = list._refresh(list._node);
		//console.log(ls.length)
		__set__(list,'length',ls.length);
		copy(ls,list);
		list._inc = inc;
	}
}
LiveNodeList.prototype.item = function(i){
	_updateLiveList(this);
	return this[i];
}

_extends(LiveNodeList,NodeList);
/**
 *
 * Objects implementing the NamedNodeMap interface are used to represent collections of nodes that can be accessed by name. Note that NamedNodeMap does not inherit from NodeList; NamedNodeMaps are not maintained in any particular order. Objects contained in an object implementing NamedNodeMap may also be accessed by an ordinal index, but this is simply to allow convenient enumeration of the contents of a NamedNodeMap, and does not imply that the DOM specifies an order to these Nodes.
 * NamedNodeMap objects in the DOM are live.
 * used for attributes or DocumentType entities
 */
function NamedNodeMap() {
};

function _findNodeIndex(list,node){
	var i = list.length;
	while(i--){
		if(list[i] === node){return i}
	}
}

function _addNamedNode(el,list,newAttr,oldAttr){
	if(oldAttr){
		list[_findNodeIndex(list,oldAttr)] = newAttr;
	}else{
		list[list.length++] = newAttr;
	}
	if(el){
		newAttr.ownerElement = el;
		var doc = el.ownerDocument;
		if(doc){
			oldAttr && _onRemoveAttribute(doc,el,oldAttr);
			_onAddAttribute(doc,el,newAttr);
		}
	}
}
function _removeNamedNode(el,list,attr){
	//console.log('remove attr:'+attr)
	var i = _findNodeIndex(list,attr);
	if(i>=0){
		var lastIndex = list.length-1
		while(i<lastIndex){
			list[i] = list[++i]
		}
		list.length = lastIndex;
		if(el){
			var doc = el.ownerDocument;
			if(doc){
				_onRemoveAttribute(doc,el,attr);
				attr.ownerElement = null;
			}
		}
	}else{
		throw DOMException(NOT_FOUND_ERR,new Error(el.tagName+'@'+attr))
	}
}
NamedNodeMap.prototype = {
	length:0,
	item:NodeList.prototype.item,
	getNamedItem: function(key) {
//		if(key.indexOf(':')>0 || key == 'xmlns'){
//			return null;
//		}
		//console.log()
		var i = this.length;
		while(i--){
			var attr = this[i];
			//console.log(attr.nodeName,key)
			if(attr.nodeName == key){
				return attr;
			}
		}
	},
	setNamedItem: function(attr) {
		var el = attr.ownerElement;
		if(el && el!=this._ownerElement){
			throw new DOMException(INUSE_ATTRIBUTE_ERR);
		}
		var oldAttr = this.getNamedItem(attr.nodeName);
		_addNamedNode(this._ownerElement,this,attr,oldAttr);
		return oldAttr;
	},
	/* returns Node */
	setNamedItemNS: function(attr) {// raises: WRONG_DOCUMENT_ERR,NO_MODIFICATION_ALLOWED_ERR,INUSE_ATTRIBUTE_ERR
		var el = attr.ownerElement, oldAttr;
		if(el && el!=this._ownerElement){
			throw new DOMException(INUSE_ATTRIBUTE_ERR);
		}
		oldAttr = this.getNamedItemNS(attr.namespaceURI,attr.localName);
		_addNamedNode(this._ownerElement,this,attr,oldAttr);
		return oldAttr;
	},

	/* returns Node */
	removeNamedItem: function(key) {
		var attr = this.getNamedItem(key);
		_removeNamedNode(this._ownerElement,this,attr);
		return attr;


	},// raises: NOT_FOUND_ERR,NO_MODIFICATION_ALLOWED_ERR

	//for level2
	removeNamedItemNS:function(namespaceURI,localName){
		var attr = this.getNamedItemNS(namespaceURI,localName);
		_removeNamedNode(this._ownerElement,this,attr);
		return attr;
	},
	getNamedItemNS: function(namespaceURI, localName) {
		var i = this.length;
		while(i--){
			var node = this[i];
			if(node.localName == localName && node.namespaceURI == namespaceURI){
				return node;
			}
		}
		return null;
	}
};
/**
 * @see http://www.w3.org/TR/REC-DOM-Level-1/level-one-core.html#ID-102161490
 */
function DOMImplementation(/* Object */ features) {
	this._features = {};
	if (features) {
		for (var feature in features) {
			 this._features = features[feature];
		}
	}
};

DOMImplementation.prototype = {
	hasFeature: function(/* string */ feature, /* string */ version) {
		var versions = this._features[feature.toLowerCase()];
		if (versions && (!version || version in versions)) {
			return true;
		} else {
			return false;
		}
	},
	// Introduced in DOM Level 2:
	createDocument:function(namespaceURI,  qualifiedName, doctype){// raises:INVALID_CHARACTER_ERR,NAMESPACE_ERR,WRONG_DOCUMENT_ERR
		var doc = new Document();
		doc.implementation = this;
		doc.childNodes = new NodeList();
		doc.doctype = doctype;
		if(doctype){
			doc.appendChild(doctype);
		}
		if(qualifiedName){
			var root = doc.createElementNS(namespaceURI,qualifiedName);
			doc.appendChild(root);
		}
		return doc;
	},
	// Introduced in DOM Level 2:
	createDocumentType:function(qualifiedName, publicId, systemId){// raises:INVALID_CHARACTER_ERR,NAMESPACE_ERR
		var node = new DocumentType();
		node.name = qualifiedName;
		node.nodeName = qualifiedName;
		node.publicId = publicId;
		node.systemId = systemId;
		// Introduced in DOM Level 2:
		//readonly attribute DOMString        internalSubset;

		//TODO:..
		//  readonly attribute NamedNodeMap     entities;
		//  readonly attribute NamedNodeMap     notations;
		return node;
	}
};


/**
 * @see http://www.w3.org/TR/2000/REC-DOM-Level-2-Core-20001113/core.html#ID-1950641247
 */

function Node() {
};

Node.prototype = {
	firstChild : null,
	lastChild : null,
	previousSibling : null,
	nextSibling : null,
	attributes : null,
	parentNode : null,
	childNodes : null,
	ownerDocument : null,
	nodeValue : null,
	namespaceURI : null,
	prefix : null,
	localName : null,
	// Modified in DOM Level 2:
	insertBefore:function(newChild, refChild){//raises
		return _insertBefore(this,newChild,refChild);
	},
	replaceChild:function(newChild, oldChild){//raises
		this.insertBefore(newChild,oldChild);
		if(oldChild){
			this.removeChild(oldChild);
		}
	},
	removeChild:function(oldChild){
		return _removeChild(this,oldChild);
	},
	appendChild:function(newChild){
		return this.insertBefore(newChild,null);
	},
	hasChildNodes:function(){
		return this.firstChild != null;
	},
	cloneNode:function(deep){
		return cloneNode(this.ownerDocument||this,this,deep);
	},
	// Modified in DOM Level 2:
	normalize:function(){
		var child = this.firstChild;
		while(child){
			var next = child.nextSibling;
			if(next && next.nodeType == TEXT_NODE && child.nodeType == TEXT_NODE){
				this.removeChild(next);
				child.appendData(next.data);
			}else{
				child.normalize();
				child = next;
			}
		}
	},
  	// Introduced in DOM Level 2:
	isSupported:function(feature, version){
		return this.ownerDocument.implementation.hasFeature(feature,version);
	},
    // Introduced in DOM Level 2:
    hasAttributes:function(){
    	return this.attributes.length>0;
    },
    lookupPrefix:function(namespaceURI){
    	var el = this;
    	while(el){
    		var map = el._nsMap;
    		//console.dir(map)
    		if(map){
    			for(var n in map){
    				if(map[n] == namespaceURI){
    					return n;
    				}
    			}
    		}
    		el = el.nodeType == ATTRIBUTE_NODE?el.ownerDocument : el.parentNode;
    	}
    	return null;
    },
    // Introduced in DOM Level 3:
    lookupNamespaceURI:function(prefix){
    	var el = this;
    	while(el){
    		var map = el._nsMap;
    		//console.dir(map)
    		if(map){
    			if(prefix in map){
    				return map[prefix] ;
    			}
    		}
    		el = el.nodeType == ATTRIBUTE_NODE?el.ownerDocument : el.parentNode;
    	}
    	return null;
    },
    // Introduced in DOM Level 3:
    isDefaultNamespace:function(namespaceURI){
    	var prefix = this.lookupPrefix(namespaceURI);
    	return prefix == null;
    }
};


function _xmlEncoder(c){
	return c == '<' && '&lt;' ||
         c == '>' && '&gt;' ||
         c == '&' && '&amp;' ||
         c == '"' && '&quot;' ||
         '&#'+c.charCodeAt()+';'
}


copy(NodeType,Node);
copy(NodeType,Node.prototype);

/**
 * @param callback return true for continue,false for break
 * @return boolean true: break visit;
 */
function _visitNode(node,callback){
	if(callback(node)){
		return true;
	}
	if(node = node.firstChild){
		do{
			if(_visitNode(node,callback)){return true}
        }while(node=node.nextSibling)
    }
}



function Document(){
}
function _onAddAttribute(doc,el,newAttr){
	doc && doc._inc++;
	var ns = newAttr.namespaceURI ;
	if(ns == 'http://www.w3.org/2000/xmlns/'){
		//update namespace
		el._nsMap[newAttr.prefix?newAttr.localName:''] = newAttr.value
	}
}
function _onRemoveAttribute(doc,el,newAttr,remove){
	doc && doc._inc++;
	var ns = newAttr.namespaceURI ;
	if(ns == 'http://www.w3.org/2000/xmlns/'){
		//update namespace
		delete el._nsMap[newAttr.prefix?newAttr.localName:'']
	}
}
function _onUpdateChild(doc,el,newChild){
	if(doc && doc._inc){
		doc._inc++;
		//update childNodes
		var cs = el.childNodes;
		if(newChild){
			cs[cs.length++] = newChild;
		}else{
			//console.log(1)
			var child = el.firstChild;
			var i = 0;
			while(child){
				cs[i++] = child;
				child =child.nextSibling;
			}
			cs.length = i;
		}
	}
}

/**
 * attributes;
 * children;
 *
 * writeable properties:
 * nodeValue,Attr:value,CharacterData:data
 * prefix
 */
function _removeChild(parentNode,child){
	var previous = child.previousSibling;
	var next = child.nextSibling;
	if(previous){
		previous.nextSibling = next;
	}else{
		parentNode.firstChild = next
	}
	if(next){
		next.previousSibling = previous;
	}else{
		parentNode.lastChild = previous;
	}
	_onUpdateChild(parentNode.ownerDocument,parentNode);
	return child;
}
/**
 * preformance key(refChild == null)
 */
function _insertBefore(parentNode,newChild,nextChild){
	var cp = newChild.parentNode;
	if(cp){
		cp.removeChild(newChild);//remove and update
	}
	if(newChild.nodeType === DOCUMENT_FRAGMENT_NODE){
		var newFirst = newChild.firstChild;
		if (newFirst == null) {
			return newChild;
		}
		var newLast = newChild.lastChild;
	}else{
		newFirst = newLast = newChild;
	}
	var pre = nextChild ? nextChild.previousSibling : parentNode.lastChild;

	newFirst.previousSibling = pre;
	newLast.nextSibling = nextChild;


	if(pre){
		pre.nextSibling = newFirst;
	}else{
		parentNode.firstChild = newFirst;
	}
	if(nextChild == null){
		parentNode.lastChild = newLast;
	}else{
		nextChild.previousSibling = newLast;
	}
	do{
		newFirst.parentNode = parentNode;
	}while(newFirst !== newLast && (newFirst= newFirst.nextSibling))
	_onUpdateChild(parentNode.ownerDocument||parentNode,parentNode);
	//console.log(parentNode.lastChild.nextSibling == null)
	if (newChild.nodeType == DOCUMENT_FRAGMENT_NODE) {
		newChild.firstChild = newChild.lastChild = null;
	}
	return newChild;
}
function _appendSingleChild(parentNode,newChild){
	var cp = newChild.parentNode;
	if(cp){
		var pre = parentNode.lastChild;
		cp.removeChild(newChild);//remove and update
		var pre = parentNode.lastChild;
	}
	var pre = parentNode.lastChild;
	newChild.parentNode = parentNode;
	newChild.previousSibling = pre;
	newChild.nextSibling = null;
	if(pre){
		pre.nextSibling = newChild;
	}else{
		parentNode.firstChild = newChild;
	}
	parentNode.lastChild = newChild;
	_onUpdateChild(parentNode.ownerDocument,parentNode,newChild);
	return newChild;
	//console.log("__aa",parentNode.lastChild.nextSibling == null)
}
Document.prototype = {
	//implementation : null,
	nodeName :  '#document',
	nodeType :  DOCUMENT_NODE,
	doctype :  null,
	documentElement :  null,
	_inc : 1,

	insertBefore :  function(newChild, refChild){//raises
		if(newChild.nodeType == DOCUMENT_FRAGMENT_NODE){
			var child = newChild.firstChild;
			while(child){
				var next = child.nextSibling;
				this.insertBefore(child,refChild);
				child = next;
			}
			return newChild;
		}
		if(this.documentElement == null && newChild.nodeType == ELEMENT_NODE){
			this.documentElement = newChild;
		}

		return _insertBefore(this,newChild,refChild),(newChild.ownerDocument = this),newChild;
	},
	removeChild :  function(oldChild){
		if(this.documentElement == oldChild){
			this.documentElement = null;
		}
		return _removeChild(this,oldChild);
	},
	// Introduced in DOM Level 2:
	importNode : function(importedNode,deep){
		return importNode(this,importedNode,deep);
	},
	// Introduced in DOM Level 2:
	getElementById :	function(id){
		var rtv = null;
		_visitNode(this.documentElement,function(node){
			if(node.nodeType == ELEMENT_NODE){
				if(node.getAttribute('id') == id){
					rtv = node;
					return true;
				}
			}
		})
		return rtv;
	},

	//document factory method:
	createElement :	function(tagName){
		var node = new Element();
		node.ownerDocument = this;
		node.nodeName = tagName;
		node.tagName = tagName;
		node.childNodes = new NodeList();
		var attrs	= node.attributes = new NamedNodeMap();
		attrs._ownerElement = node;
		return node;
	},
	createDocumentFragment :	function(){
		var node = new DocumentFragment();
		node.ownerDocument = this;
		node.childNodes = new NodeList();
		return node;
	},
	createTextNode :	function(data){
		var node = new Text();
		node.ownerDocument = this;
		node.appendData(data)
		return node;
	},
	createComment :	function(data){
		var node = new Comment();
		node.ownerDocument = this;
		node.appendData(data)
		return node;
	},
	createCDATASection :	function(data){
		var node = new CDATASection();
		node.ownerDocument = this;
		node.appendData(data)
		return node;
	},
	createProcessingInstruction :	function(target,data){
		var node = new ProcessingInstruction();
		node.ownerDocument = this;
		node.tagName = node.target = target;
		node.nodeValue= node.data = data;
		return node;
	},
	createAttribute :	function(name){
		var node = new Attr();
		node.ownerDocument	= this;
		node.name = name;
		node.nodeName	= name;
		node.localName = name;
		node.specified = true;
		return node;
	},
	createEntityReference :	function(name){
		var node = new EntityReference();
		node.ownerDocument	= this;
		node.nodeName	= name;
		return node;
	},
	// Introduced in DOM Level 2:
	createElementNS :	function(namespaceURI,qualifiedName){
		var node = new Element();
		var pl = qualifiedName.split(':');
		var attrs	= node.attributes = new NamedNodeMap();
		node.childNodes = new NodeList();
		node.ownerDocument = this;
		node.nodeName = qualifiedName;
		node.tagName = qualifiedName;
		node.namespaceURI = namespaceURI;
		if(pl.length == 2){
			node.prefix = pl[0];
			node.localName = pl[1];
		}else{
			//el.prefix = null;
			node.localName = qualifiedName;
		}
		attrs._ownerElement = node;
		return node;
	},
	// Introduced in DOM Level 2:
	createAttributeNS :	function(namespaceURI,qualifiedName){
		var node = new Attr();
		var pl = qualifiedName.split(':');
		node.ownerDocument = this;
		node.nodeName = qualifiedName;
		node.name = qualifiedName;
		node.namespaceURI = namespaceURI;
		node.specified = true;
		if(pl.length == 2){
			node.prefix = pl[0];
			node.localName = pl[1];
		}else{
			//el.prefix = null;
			node.localName = qualifiedName;
		}
		return node;
	}
};
_extends(Document,Node);


function Element() {
	this._nsMap = {};
};
Element.prototype = {
	nodeType : ELEMENT_NODE,
	hasAttribute : function(name){
		return this.getAttributeNode(name)!=null;
	},
	getAttribute : function(name){
		var attr = this.getAttributeNode(name);
		return attr && attr.value || '';
	},
	getAttributeNode : function(name){
		return this.attributes.getNamedItem(name);
	},
	setAttribute : function(name, value){
		var attr = this.ownerDocument.createAttribute(name);
		attr.value = attr.nodeValue = "" + value;
		this.setAttributeNode(attr)
	},
	removeAttribute : function(name){
		var attr = this.getAttributeNode(name)
		attr && this.removeAttributeNode(attr);
	},

	//four real opeartion method
	appendChild:function(newChild){
		if(newChild.nodeType === DOCUMENT_FRAGMENT_NODE){
			return this.insertBefore(newChild,null);
		}else{
			return _appendSingleChild(this,newChild);
		}
	},
	setAttributeNode : function(newAttr){
		return this.attributes.setNamedItem(newAttr);
	},
	setAttributeNodeNS : function(newAttr){
		return this.attributes.setNamedItemNS(newAttr);
	},
	removeAttributeNode : function(oldAttr){
		//console.log(this == oldAttr.ownerElement)
		return this.attributes.removeNamedItem(oldAttr.nodeName);
	},
	//get real attribute name,and remove it by removeAttributeNode
	removeAttributeNS : function(namespaceURI, localName){
		var old = this.getAttributeNodeNS(namespaceURI, localName);
		old && this.removeAttributeNode(old);
	},

	hasAttributeNS : function(namespaceURI, localName){
		return this.getAttributeNodeNS(namespaceURI, localName)!=null;
	},
	getAttributeNS : function(namespaceURI, localName){
		var attr = this.getAttributeNodeNS(namespaceURI, localName);
		return attr && attr.value || '';
	},
	setAttributeNS : function(namespaceURI, qualifiedName, value){
		var attr = this.ownerDocument.createAttributeNS(namespaceURI, qualifiedName);
		attr.value = attr.nodeValue = "" + value;
		this.setAttributeNode(attr)
	},
	getAttributeNodeNS : function(namespaceURI, localName){
		return this.attributes.getNamedItemNS(namespaceURI, localName);
	},

	getElementsByTagName : function(tagName){
		return new LiveNodeList(this,function(base){
			var ls = [];
			_visitNode(base,function(node){
				if(node !== base && node.nodeType == ELEMENT_NODE && (tagName === '*' || node.tagName == tagName)){
					ls.push(node);
				}
			});
			return ls;
		});
	},
	getElementsByTagNameNS : function(namespaceURI, localName){
		return new LiveNodeList(this,function(base){
			var ls = [];
			_visitNode(base,function(node){
				if(node !== base && node.nodeType === ELEMENT_NODE && (namespaceURI === '*' || node.namespaceURI === namespaceURI) && (localName === '*' || node.localName == localName)){
					ls.push(node);
				}
			});
			return ls;

		});
	}
};
Document.prototype.getElementsByTagName = Element.prototype.getElementsByTagName;
Document.prototype.getElementsByTagNameNS = Element.prototype.getElementsByTagNameNS;


_extends(Element,Node);
function Attr() {
};
Attr.prototype.nodeType = ATTRIBUTE_NODE;
_extends(Attr,Node);


function CharacterData() {
};
CharacterData.prototype = {
	data : '',
	substringData : function(offset, count) {
		return this.data.substring(offset, offset+count);
	},
	appendData: function(text) {
		text = this.data+text;
		this.nodeValue = this.data = text;
		this.length = text.length;
	},
	insertData: function(offset,text) {
		this.replaceData(offset,0,text);

	},
	appendChild:function(newChild){
		throw new Error(ExceptionMessage[HIERARCHY_REQUEST_ERR])
	},
	deleteData: function(offset, count) {
		this.replaceData(offset,count,"");
	},
	replaceData: function(offset, count, text) {
		var start = this.data.substring(0,offset);
		var end = this.data.substring(offset+count);
		text = start + text + end;
		this.nodeValue = this.data = text;
		this.length = text.length;
	}
}
_extends(CharacterData,Node);
function Text() {
};
Text.prototype = {
	nodeName : "#text",
	nodeType : TEXT_NODE,
	splitText : function(offset) {
		var text = this.data;
		var newText = text.substring(offset);
		text = text.substring(0, offset);
		this.data = this.nodeValue = text;
		this.length = text.length;
		var newNode = this.ownerDocument.createTextNode(newText);
		if(this.parentNode){
			this.parentNode.insertBefore(newNode, this.nextSibling);
		}
		return newNode;
	}
}
_extends(Text,CharacterData);
function Comment() {
};
Comment.prototype = {
	nodeName : "#comment",
	nodeType : COMMENT_NODE
}
_extends(Comment,CharacterData);

function CDATASection() {
};
CDATASection.prototype = {
	nodeName : "#cdata-section",
	nodeType : CDATA_SECTION_NODE
}
_extends(CDATASection,CharacterData);


function DocumentType() {
};
DocumentType.prototype.nodeType = DOCUMENT_TYPE_NODE;
_extends(DocumentType,Node);

function Notation() {
};
Notation.prototype.nodeType = NOTATION_NODE;
_extends(Notation,Node);

function Entity() {
};
Entity.prototype.nodeType = ENTITY_NODE;
_extends(Entity,Node);

function EntityReference() {
};
EntityReference.prototype.nodeType = ENTITY_REFERENCE_NODE;
_extends(EntityReference,Node);

function DocumentFragment() {
};
DocumentFragment.prototype.nodeName =	"#document-fragment";
DocumentFragment.prototype.nodeType =	DOCUMENT_FRAGMENT_NODE;
_extends(DocumentFragment,Node);


function ProcessingInstruction() {
}
ProcessingInstruction.prototype.nodeType = PROCESSING_INSTRUCTION_NODE;
_extends(ProcessingInstruction,Node);
function XMLSerializer(){}
XMLSerializer.prototype.serializeToString = function(node,isHtml,nodeFilter){
	return nodeSerializeToString.call(node,isHtml,nodeFilter);
}
Node.prototype.toString = nodeSerializeToString;
function nodeSerializeToString(isHtml,nodeFilter){
	var buf = [];
	var refNode = this.nodeType == 9?this.documentElement:this;
	var prefix = refNode.prefix;
	var uri = refNode.namespaceURI;

	if(uri && prefix == null){
		//console.log(prefix)
		var prefix = refNode.lookupPrefix(uri);
		if(prefix == null){
			//isHTML = true;
			var visibleNamespaces=[
			{namespace:uri,prefix:null}
			//{namespace:uri,prefix:''}
			]
		}
	}
	serializeToString(this,buf,isHtml,nodeFilter,visibleNamespaces);
	//console.log('###',this.nodeType,uri,prefix,buf.join(''))
	return buf.join('');
}
function needNamespaceDefine(node,isHTML, visibleNamespaces) {
	var prefix = node.prefix||'';
	var uri = node.namespaceURI;
	if (!prefix && !uri){
		return false;
	}
	if (prefix === "xml" && uri === "http://www.w3.org/XML/1998/namespace"
		|| uri == 'http://www.w3.org/2000/xmlns/'){
		return false;
	}

	var i = visibleNamespaces.length
	//console.log('@@@@',node.tagName,prefix,uri,visibleNamespaces)
	while (i--) {
		var ns = visibleNamespaces[i];
		// get namespace prefix
		//console.log(node.nodeType,node.tagName,ns.prefix,prefix)
		if (ns.prefix == prefix){
			return ns.namespace != uri;
		}
	}
	//console.log(isHTML,uri,prefix=='')
	//if(isHTML && prefix ==null && uri == 'http://www.w3.org/1999/xhtml'){
	//	return false;
	//}
	//node.flag = '11111'
	//console.error(3,true,node.flag,node.prefix,node.namespaceURI)
	return true;
}
function serializeToString(node,buf,isHTML,nodeFilter,visibleNamespaces){
	if(nodeFilter){
		node = nodeFilter(node);
		if(node){
			if(typeof node == 'string'){
				buf.push(node);
				return;
			}
		}else{
			return;
		}
		//buf.sort.apply(attrs, attributeSorter);
	}
	switch(node.nodeType){
	case ELEMENT_NODE:
		if (!visibleNamespaces) visibleNamespaces = [];
		var startVisibleNamespaces = visibleNamespaces.length;
		var attrs = node.attributes;
		var len = attrs.length;
		var child = node.firstChild;
		var nodeName = node.tagName;

		isHTML =  (htmlns === node.namespaceURI) ||isHTML
		buf.push('<',nodeName);



		for(var i=0;i<len;i++){
			// add namespaces for attributes
			var attr = attrs.item(i);
			if (attr.prefix == 'xmlns') {
				visibleNamespaces.push({ prefix: attr.localName, namespace: attr.value });
			}else if(attr.nodeName == 'xmlns'){
				visibleNamespaces.push({ prefix: '', namespace: attr.value });
			}
		}
		for(var i=0;i<len;i++){
			var attr = attrs.item(i);
			if (needNamespaceDefine(attr,isHTML, visibleNamespaces)) {
				var prefix = attr.prefix||'';
				var uri = attr.namespaceURI;
				var ns = prefix ? ' xmlns:' + prefix : " xmlns";
				buf.push(ns, '="' , uri , '"');
				visibleNamespaces.push({ prefix: prefix, namespace:uri });
			}
			serializeToString(attr,buf,isHTML,nodeFilter,visibleNamespaces);
		}
		// add namespace for current node
		if (needNamespaceDefine(node,isHTML, visibleNamespaces)) {
			var prefix = node.prefix||'';
			var uri = node.namespaceURI;
			var ns = prefix ? ' xmlns:' + prefix : " xmlns";
			buf.push(ns, '="' , uri , '"');
			visibleNamespaces.push({ prefix: prefix, namespace:uri });
		}

		if(child || isHTML && !/^(?:meta|link|img|br|hr|input)$/i.test(nodeName)){
			buf.push('>');
			//if is cdata child node
			if(isHTML && /^script$/i.test(nodeName)){
				while(child){
					if(child.data){
						buf.push(child.data);
					}else{
						serializeToString(child,buf,isHTML,nodeFilter,visibleNamespaces);
					}
					child = child.nextSibling;
				}
			}else
			{
				while(child){
					serializeToString(child,buf,isHTML,nodeFilter,visibleNamespaces);
					child = child.nextSibling;
				}
			}
			buf.push('</',nodeName,'>');
		}else{
			buf.push('/>');
		}
		// remove added visible namespaces
		//visibleNamespaces.length = startVisibleNamespaces;
		return;
	case DOCUMENT_NODE:
	case DOCUMENT_FRAGMENT_NODE:
		var child = node.firstChild;
		while(child){
			serializeToString(child,buf,isHTML,nodeFilter,visibleNamespaces);
			child = child.nextSibling;
		}
		return;
	case ATTRIBUTE_NODE:
		return buf.push(' ',node.name,'="',node.value.replace(/[<&"]/g,_xmlEncoder),'"');
	case TEXT_NODE:
		return buf.push(node.data.replace(/[<&]/g,_xmlEncoder));
	case CDATA_SECTION_NODE:
		return buf.push( '<![CDATA[',node.data,']]>');
	case COMMENT_NODE:
		return buf.push( "<!--",node.data,"-->");
	case DOCUMENT_TYPE_NODE:
		var pubid = node.publicId;
		var sysid = node.systemId;
		buf.push('<!DOCTYPE ',node.name);
		if(pubid){
			buf.push(' PUBLIC "',pubid);
			if (sysid && sysid!='.') {
				buf.push( '" "',sysid);
			}
			buf.push('">');
		}else if(sysid && sysid!='.'){
			buf.push(' SYSTEM "',sysid,'">');
		}else{
			var sub = node.internalSubset;
			if(sub){
				buf.push(" [",sub,"]");
			}
			buf.push(">");
		}
		return;
	case PROCESSING_INSTRUCTION_NODE:
		return buf.push( "<?",node.target," ",node.data,"?>");
	case ENTITY_REFERENCE_NODE:
		return buf.push( '&',node.nodeName,';');
	//case ENTITY_NODE:
	//case NOTATION_NODE:
	default:
		buf.push('??',node.nodeName);
	}
}
function importNode(doc,node,deep){
	var node2;
	switch (node.nodeType) {
	case ELEMENT_NODE:
		node2 = node.cloneNode(false);
		node2.ownerDocument = doc;
		//var attrs = node2.attributes;
		//var len = attrs.length;
		//for(var i=0;i<len;i++){
			//node2.setAttributeNodeNS(importNode(doc,attrs.item(i),deep));
		//}
	case DOCUMENT_FRAGMENT_NODE:
		break;
	case ATTRIBUTE_NODE:
		deep = true;
		break;
	//case ENTITY_REFERENCE_NODE:
	//case PROCESSING_INSTRUCTION_NODE:
	////case TEXT_NODE:
	//case CDATA_SECTION_NODE:
	//case COMMENT_NODE:
	//	deep = false;
	//	break;
	//case DOCUMENT_NODE:
	//case DOCUMENT_TYPE_NODE:
	//cannot be imported.
	//case ENTITY_NODE:
	//case NOTATION_NODE：
	//can not hit in level3
	//default:throw e;
	}
	if(!node2){
		node2 = node.cloneNode(false);//false
	}
	node2.ownerDocument = doc;
	node2.parentNode = null;
	if(deep){
		var child = node.firstChild;
		while(child){
			node2.appendChild(importNode(doc,child,deep));
			child = child.nextSibling;
		}
	}
	return node2;
}
//
//var _relationMap = {firstChild:1,lastChild:1,previousSibling:1,nextSibling:1,
//					attributes:1,childNodes:1,parentNode:1,documentElement:1,doctype,};
function cloneNode(doc,node,deep){
	var node2 = new node.constructor();
	for(var n in node){
		var v = node[n];
		if(typeof v != 'object' ){
			if(v != node2[n]){
				node2[n] = v;
			}
		}
	}
	if(node.childNodes){
		node2.childNodes = new NodeList();
	}
	node2.ownerDocument = doc;
	switch (node2.nodeType) {
	case ELEMENT_NODE:
		var attrs	= node.attributes;
		var attrs2	= node2.attributes = new NamedNodeMap();
		var len = attrs.length
		attrs2._ownerElement = node2;
		for(var i=0;i<len;i++){
			node2.setAttributeNode(cloneNode(doc,attrs.item(i),true));
		}
		break;;
	case ATTRIBUTE_NODE:
		deep = true;
	}
	if(deep){
		var child = node.firstChild;
		while(child){
			node2.appendChild(cloneNode(doc,child,deep));
			child = child.nextSibling;
		}
	}
	return node2;
}

function __set__(object,key,value){
	object[key] = value
}
//do dynamic
try{
	if(Object.defineProperty){
		Object.defineProperty(LiveNodeList.prototype,'length',{
			get:function(){
				_updateLiveList(this);
				return this.$$length;
			}
		});
		Object.defineProperty(Node.prototype,'textContent',{
			get:function(){
				return getTextContent(this);
			},
			set:function(data){
				switch(this.nodeType){
				case ELEMENT_NODE:
				case DOCUMENT_FRAGMENT_NODE:
					while(this.firstChild){
						this.removeChild(this.firstChild);
					}
					if(data || String(data)){
						this.appendChild(this.ownerDocument.createTextNode(data));
					}
					break;
				default:
					//TODO:
					this.data = data;
					this.value = data;
					this.nodeValue = data;
				}
			}
		})

		function getTextContent(node){
			switch(node.nodeType){
			case ELEMENT_NODE:
			case DOCUMENT_FRAGMENT_NODE:
				var buf = [];
				node = node.firstChild;
				while(node){
					if(node.nodeType!==7 && node.nodeType !==8){
						buf.push(getTextContent(node));
					}
					node = node.nextSibling;
				}
				return buf.join('');
			default:
				return node.nodeValue;
			}
		}
		__set__ = function(object,key,value){
			//console.log(value)
			object['$$'+key] = value
		}
	}
}catch(e){//ie8
}

//if(typeof require == 'function'){
	exports.DOMImplementation = DOMImplementation;
	exports.XMLSerializer = XMLSerializer;
//}


/***/ }),
/* 141 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();
// import Mapping from "./mapping";


// Default Views


// Default View Managers


var _eventEmitter = __webpack_require__(30);

var _eventEmitter2 = _interopRequireDefault(_eventEmitter);

var _core = __webpack_require__(6);

var _hook = __webpack_require__(101);

var _hook2 = _interopRequireDefault(_hook);

var _epubcfi = __webpack_require__(22);

var _epubcfi2 = _interopRequireDefault(_epubcfi);

var _queue = __webpack_require__(102);

var _queue2 = _interopRequireDefault(_queue);

var _layout = __webpack_require__(382);

var _layout2 = _interopRequireDefault(_layout);

var _themes = __webpack_require__(383);

var _themes2 = _interopRequireDefault(_themes);

var _contents = __webpack_require__(104);

var _contents2 = _interopRequireDefault(_contents);

var _annotations = __webpack_require__(384);

var _annotations2 = _interopRequireDefault(_annotations);

var _constants = __webpack_require__(23);

var _iframe = __webpack_require__(143);

var _iframe2 = _interopRequireDefault(_iframe);

var _index = __webpack_require__(105);

var _index2 = _interopRequireDefault(_index);

var _index3 = __webpack_require__(147);

var _index4 = _interopRequireDefault(_index3);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Displays an Epub as a series of Views for each Section.
 * Requires Manager and View class to handle specifics of rendering
 * the section content.
 * @class
 * @param {Book} book
 * @param {object} [options]
 * @param {number} [options.width]
 * @param {number} [options.height]
 * @param {string} [options.ignoreClass] class for the cfi parser to ignore
 * @param {string | function | object} [options.manager='default']
 * @param {string | function} [options.view='iframe']
 * @param {string} [options.layout] layout to force
 * @param {string} [options.spread] force spread value
 * @param {number} [options.minSpreadWidth] overridden by spread: none (never) / both (always)
 * @param {string} [options.stylesheet] url of stylesheet to be injected
 * @param {boolean} [options.resizeOnOrientationChange] false to disable orientation events
 * @param {string} [options.script] url of script to be injected
 * @param {boolean | object} [options.snap=false] use snap scrolling
 */
var Rendition = function () {
	function Rendition(book, options) {
		_classCallCheck(this, Rendition);

		this.settings = (0, _core.extend)(this.settings || {}, {
			width: null,
			height: null,
			ignoreClass: "",
			manager: "default",
			view: "iframe",
			flow: null,
			layout: null,
			spread: null,
			minSpreadWidth: 800,
			stylesheet: null,
			resizeOnOrientationChange: true,
			script: null,
			snap: false
		});

		(0, _core.extend)(this.settings, options);

		if (_typeof(this.settings.manager) === "object") {
			this.manager = this.settings.manager;
		}

		this.book = book;

		/**
   * Adds Hook methods to the Rendition prototype
   * @member {object} hooks
   * @property {Hook} hooks.content
   * @memberof Rendition
   */
		this.hooks = {};
		this.hooks.display = new _hook2.default(this);
		this.hooks.serialize = new _hook2.default(this);
		this.hooks.content = new _hook2.default(this);
		this.hooks.unloaded = new _hook2.default(this);
		this.hooks.layout = new _hook2.default(this);
		this.hooks.render = new _hook2.default(this);
		this.hooks.show = new _hook2.default(this);

		this.hooks.content.register(this.handleLinks.bind(this));
		this.hooks.content.register(this.passEvents.bind(this));
		this.hooks.content.register(this.adjustImages.bind(this));

		this.book.spine.hooks.content.register(this.injectIdentifier.bind(this));

		if (this.settings.stylesheet) {
			this.book.spine.hooks.content.register(this.injectStylesheet.bind(this));
		}

		if (this.settings.script) {
			this.book.spine.hooks.content.register(this.injectScript.bind(this));
		}

		/**
   * @member {Themes} themes
   * @memberof Rendition
   */
		this.themes = new _themes2.default(this);

		/**
   * @member {Annotations} annotations
   * @memberof Rendition
   */
		this.annotations = new _annotations2.default(this);

		this.epubcfi = new _epubcfi2.default();

		this.q = new _queue2.default(this);

		/**
   * A Rendered Location Range
   * @typedef location
   * @type {Object}
   * @property {object} start
   * @property {string} start.index
   * @property {string} start.href
   * @property {object} start.displayed
   * @property {EpubCFI} start.cfi
   * @property {number} start.location
   * @property {number} start.percentage
   * @property {number} start.displayed.page
   * @property {number} start.displayed.total
   * @property {object} end
   * @property {string} end.index
   * @property {string} end.href
   * @property {object} end.displayed
   * @property {EpubCFI} end.cfi
   * @property {number} end.location
   * @property {number} end.percentage
   * @property {number} end.displayed.page
   * @property {number} end.displayed.total
   * @property {boolean} atStart
   * @property {boolean} atEnd
   * @memberof Rendition
   */
		this.location = undefined;

		// Hold queue until book is opened
		this.q.enqueue(this.book.opened);

		this.starting = new _core.defer();
		/**
   * @member {promise} started returns after the rendition has started
   * @memberof Rendition
   */
		this.started = this.starting.promise;
		// Block the queue until rendering is started
		this.q.enqueue(this.start);
	}

	/**
  * Set the manager function
  * @param {function} manager
  */


	_createClass(Rendition, [{
		key: "setManager",
		value: function setManager(manager) {
			this.manager = manager;
		}

		/**
   * Require the manager from passed string, or as a class function
   * @param  {string|object} manager [description]
   * @return {method}
   */

	}, {
		key: "requireManager",
		value: function requireManager(manager) {
			var viewManager;

			// If manager is a string, try to load from imported managers
			if (typeof manager === "string" && manager === "default") {
				viewManager = _index2.default;
			} else if (typeof manager === "string" && manager === "continuous") {
				viewManager = _index4.default;
			} else {
				// otherwise, assume we were passed a class function
				viewManager = manager;
			}

			return viewManager;
		}

		/**
   * Require the view from passed string, or as a class function
   * @param  {string|object} view
   * @return {view}
   */

	}, {
		key: "requireView",
		value: function requireView(view) {
			var View;

			// If view is a string, try to load from imported views,
			if (typeof view == "string" && view === "iframe") {
				View = _iframe2.default;
			} else {
				// otherwise, assume we were passed a class function
				View = view;
			}

			return View;
		}

		/**
   * Start the rendering
   * @return {Promise} rendering has started
   */

	}, {
		key: "start",
		value: function start() {
			if (!this.settings.layout && (this.book.package.metadata.layout === "pre-paginated" || this.book.displayOptions.fixedLayout === "true")) {
				this.settings.layout = "pre-paginated";
			}

			if (!this.manager) {
				this.ViewManager = this.requireManager(this.settings.manager);
				this.View = this.requireView(this.settings.view);

				this.manager = new this.ViewManager({
					view: this.View,
					queue: this.q,
					request: this.book.load.bind(this.book),
					settings: this.settings
				});
			}

			this.direction(this.book.package.metadata.direction);

			// Parse metadata to get layout props
			this.settings.globalLayoutProperties = this.determineLayoutProperties(this.book.package.metadata);

			this.flow(this.settings.globalLayoutProperties.flow);

			this.layout(this.settings.globalLayoutProperties);

			// Listen for displayed views
			this.manager.on(_constants.EVENTS.MANAGERS.ADDED, this.afterDisplayed.bind(this));
			this.manager.on(_constants.EVENTS.MANAGERS.REMOVED, this.afterRemoved.bind(this));

			// Listen for resizing
			this.manager.on(_constants.EVENTS.MANAGERS.RESIZED, this.onResized.bind(this));

			// Listen for rotation
			this.manager.on(_constants.EVENTS.MANAGERS.ORIENTATION_CHANGE, this.onOrientationChange.bind(this));

			// Listen for scroll changes
			this.manager.on(_constants.EVENTS.MANAGERS.SCROLLED, this.reportLocation.bind(this));

			/**
    * Emit that rendering has started
    * @event started
    * @memberof Rendition
    */
			this.emit(_constants.EVENTS.RENDITION.STARTED);

			// Start processing queue
			this.starting.resolve();
		}

		/**
   * Call to attach the container to an element in the dom
   * Container must be attached before rendering can begin
   * @param  {element} element to attach to
   * @return {Promise}
   */

	}, {
		key: "attachTo",
		value: function attachTo(element) {

			return this.q.enqueue(function () {

				// Start rendering
				this.manager.render(element, {
					"width": this.settings.width,
					"height": this.settings.height
				});

				/**
     * Emit that rendering has attached to an element
     * @event attached
     * @memberof Rendition
     */
				this.emit(_constants.EVENTS.RENDITION.ATTACHED);
			}.bind(this));
		}

		/**
   * Display a point in the book
   * The request will be added to the rendering Queue,
   * so it will wait until book is opened, rendering started
   * and all other rendering tasks have finished to be called.
   * @param  {string} target Url or EpubCFI
   * @return {Promise}
   */

	}, {
		key: "display",
		value: function display(target) {
			if (this.displaying) {
				this.displaying.resolve();
			}
			return this.q.enqueue(this._display, target);
		}

		/**
   * Tells the manager what to display immediately
   * @private
   * @param  {string} target Url or EpubCFI
   * @return {Promise}
   */

	}, {
		key: "_display",
		value: function _display(target) {
			var _this = this;

			if (!this.book) {
				return;
			}
			var isCfiString = this.epubcfi.isCfiString(target);
			var displaying = new _core.defer();
			var displayed = displaying.promise;
			var section;
			var moveTo;

			this.displaying = displaying;

			// Check if this is a book percentage
			if (this.book.locations.length() && (0, _core.isFloat)(target)) {
				target = this.book.locations.cfiFromPercentage(parseFloat(target));
			}

			section = this.book.spine.get(target);

			if (!section) {
				displaying.reject(new Error("No Section Found"));
				return displayed;
			}

			this.manager.display(section, target).then(function () {
				displaying.resolve(section);
				_this.displaying = undefined;

				/**
     * Emit that a section has been displayed
     * @event displayed
     * @param {Section} section
     * @memberof Rendition
     */
				_this.emit(_constants.EVENTS.RENDITION.DISPLAYED, section);
				_this.reportLocation();
			}, function (err) {
				/**
     * Emit that has been an error displaying
     * @event displayError
     * @param {Section} section
     * @memberof Rendition
     */
				_this.emit(_constants.EVENTS.RENDITION.DISPLAY_ERROR, err);
			});

			return displayed;
		}

		/*
  render(view, show) {
  		// view.onLayout = this.layout.format.bind(this.layout);
  	view.create();
  		// Fit to size of the container, apply padding
  	this.manager.resizeView(view);
  		// Render Chain
  	return view.section.render(this.book.request)
  		.then(function(contents){
  			return view.load(contents);
  		}.bind(this))
  		.then(function(doc){
  			return this.hooks.content.trigger(view, this);
  		}.bind(this))
  		.then(function(){
  			this.layout.format(view.contents);
  			return this.hooks.layout.trigger(view, this);
  		}.bind(this))
  		.then(function(){
  			return view.display();
  		}.bind(this))
  		.then(function(){
  			return this.hooks.render.trigger(view, this);
  		}.bind(this))
  		.then(function(){
  			if(show !== false) {
  				this.q.enqueue(function(view){
  					view.show();
  				}, view);
  			}
  			// this.map = new Map(view, this.layout);
  			this.hooks.show.trigger(view, this);
  			this.trigger("rendered", view.section);
  			}.bind(this))
  		.catch(function(e){
  			this.trigger("loaderror", e);
  		}.bind(this));
  	}
  */

		/**
   * Report what section has been displayed
   * @private
   * @param  {*} view
   */

	}, {
		key: "afterDisplayed",
		value: function afterDisplayed(view) {
			var _this2 = this;

			view.on(_constants.EVENTS.VIEWS.MARK_CLICKED, function (cfiRange, data) {
				return _this2.triggerMarkEvent(cfiRange, data, view.contents);
			});

			this.hooks.render.trigger(view, this).then(function () {
				if (view.contents) {
					_this2.hooks.content.trigger(view.contents, _this2).then(function () {
						/**
       * Emit that a section has been rendered
       * @event rendered
       * @param {Section} section
       * @param {View} view
       * @memberof Rendition
       */
						_this2.emit(_constants.EVENTS.RENDITION.RENDERED, view.section, view);
					});
				} else {
					_this2.emit(_constants.EVENTS.RENDITION.RENDERED, view.section, view);
				}
			});
		}

		/**
   * Report what has been removed
   * @private
   * @param  {*} view
   */

	}, {
		key: "afterRemoved",
		value: function afterRemoved(view) {
			var _this3 = this;

			this.hooks.unloaded.trigger(view, this).then(function () {
				/**
     * Emit that a section has been removed
     * @event removed
     * @param {Section} section
     * @param {View} view
     * @memberof Rendition
     */
				_this3.emit(_constants.EVENTS.RENDITION.REMOVED, view.section, view);
			});
		}

		/**
   * Report resize events and display the last seen location
   * @private
   */

	}, {
		key: "onResized",
		value: function onResized(size) {

			/**
    * Emit that the rendition has been resized
    * @event resized
    * @param {number} width
    * @param {height} height
    * @memberof Rendition
    */
			this.emit(_constants.EVENTS.RENDITION.RESIZED, {
				width: size.width,
				height: size.height
			});

			if (this.location && this.location.start) {
				this.display(this.location.start.cfi);
			}
		}

		/**
   * Report orientation events and display the last seen location
   * @private
   */

	}, {
		key: "onOrientationChange",
		value: function onOrientationChange(orientation) {
			/**
    * Emit that the rendition has been rotated
    * @event orientationchange
    * @param {string} orientation
    * @memberof Rendition
    */
			this.emit(_constants.EVENTS.RENDITION.ORIENTATION_CHANGE, orientation);
		}

		/**
   * Move the Rendition to a specific offset
   * Usually you would be better off calling display()
   * @param {object} offset
   */

	}, {
		key: "moveTo",
		value: function moveTo(offset) {
			this.manager.moveTo(offset);
		}

		/**
   * Trigger a resize of the views
   * @param {number} [width]
   * @param {number} [height]
   */

	}, {
		key: "resize",
		value: function resize(width, height) {
			if (width) {
				this.settings.width = width;
			}
			if (height) {
				this.settings.height = height;
			}
			this.manager.resize(width, height);
		}

		/**
   * Clear all rendered views
   */

	}, {
		key: "clear",
		value: function clear() {
			this.manager.clear();
		}

		/**
   * Go to the next "page" in the rendition
   * @return {Promise}
   */

	}, {
		key: "next",
		value: function next() {
			return this.q.enqueue(this.manager.next.bind(this.manager)).then(this.reportLocation.bind(this));
		}

		/**
   * Go to the previous "page" in the rendition
   * @return {Promise}
   */

	}, {
		key: "prev",
		value: function prev() {
			return this.q.enqueue(this.manager.prev.bind(this.manager)).then(this.reportLocation.bind(this));
		}

		//-- http://www.idpf.org/epub/301/spec/epub-publications.html#meta-properties-rendering
		/**
   * Determine the Layout properties from metadata and settings
   * @private
   * @param  {object} metadata
   * @return {object} properties
   */

	}, {
		key: "determineLayoutProperties",
		value: function determineLayoutProperties(metadata) {
			var properties;
			var layout = this.settings.layout || metadata.layout || "reflowable";
			var spread = this.settings.spread || metadata.spread || "auto";
			var orientation = this.settings.orientation || metadata.orientation || "auto";
			var flow = this.settings.flow || metadata.flow || "auto";
			var viewport = metadata.viewport || "";
			var minSpreadWidth = this.settings.minSpreadWidth || metadata.minSpreadWidth || 800;
			var direction = this.settings.direction || metadata.direction || "ltr";

			if ((this.settings.width === 0 || this.settings.width > 0) && (this.settings.height === 0 || this.settings.height > 0)) {
				// viewport = "width="+this.settings.width+", height="+this.settings.height+"";
			}

			properties = {
				layout: layout,
				spread: spread,
				orientation: orientation,
				flow: flow,
				viewport: viewport,
				minSpreadWidth: minSpreadWidth,
				direction: direction
			};

			return properties;
		}

		/**
   * Adjust the flow of the rendition to paginated or scrolled
   * (scrolled-continuous vs scrolled-doc are handled by different view managers)
   * @param  {string} flow
   */

	}, {
		key: "flow",
		value: function flow(_flow2) {
			var _flow = _flow2;
			if (_flow2 === "scrolled" || _flow2 === "scrolled-doc" || _flow2 === "scrolled-continuous") {
				_flow = "scrolled";
			}

			if (_flow2 === "auto" || _flow2 === "paginated") {
				_flow = "paginated";
			}

			this.settings.flow = _flow2;

			if (this._layout) {
				this._layout.flow(_flow);
			}

			if (this.manager && this._layout) {
				this.manager.applyLayout(this._layout);
			}

			if (this.manager) {
				this.manager.updateFlow(_flow);
			}

			if (this.manager && this.manager.isRendered() && this.location) {
				this.manager.clear();
				this.display(this.location.start.cfi);
			}
		}

		/**
   * Adjust the layout of the rendition to reflowable or pre-paginated
   * @param  {object} settings
   */

	}, {
		key: "layout",
		value: function layout(settings) {
			var _this4 = this;

			if (settings) {
				this._layout = new _layout2.default(settings);
				this._layout.spread(settings.spread, this.settings.minSpreadWidth);

				// this.mapping = new Mapping(this._layout.props);

				this._layout.on(_constants.EVENTS.LAYOUT.UPDATED, function (props, changed) {
					_this4.emit(_constants.EVENTS.RENDITION.LAYOUT, props, changed);
				});
			}

			if (this.manager && this._layout) {
				this.manager.applyLayout(this._layout);
			}

			return this._layout;
		}

		/**
   * Adjust if the rendition uses spreads
   * @param  {string} spread none | auto (TODO: implement landscape, portrait, both)
   * @param  {int} [min] min width to use spreads at
   */

	}, {
		key: "spread",
		value: function spread(_spread, min) {

			this.settings.spread = _spread;

			if (min) {
				this.settings.minSpreadWidth = min;
			}

			if (this._layout) {
				this._layout.spread(_spread, min);
			}

			if (this.manager && this.manager.isRendered()) {
				this.manager.updateLayout();
			}
		}

		/**
   * Adjust the direction of the rendition
   * @param  {string} dir
   */

	}, {
		key: "direction",
		value: function direction(dir) {

			this.settings.direction = dir || "ltr";

			if (this.manager) {
				this.manager.direction(this.settings.direction);
			}

			if (this.manager && this.manager.isRendered() && this.location) {
				this.manager.clear();
				this.display(this.location.start.cfi);
			}
		}

		/**
   * Report the current location
   * @fires relocated
   * @fires locationChanged
   */

	}, {
		key: "reportLocation",
		value: function reportLocation() {
			return this.q.enqueue(function reportedLocation() {
				requestAnimationFrame(function reportedLocationAfterRAF() {
					var location = this.manager.currentLocation();
					if (location && location.then && typeof location.then === "function") {
						location.then(function (result) {
							var located = this.located(result);

							if (!located || !located.start || !located.end) {
								return;
							}

							this.location = located;

							this.emit(_constants.EVENTS.RENDITION.LOCATION_CHANGED, {
								index: this.location.start.index,
								href: this.location.start.href,
								start: this.location.start.cfi,
								end: this.location.end.cfi,
								percentage: this.location.start.percentage
							});

							this.emit(_constants.EVENTS.RENDITION.RELOCATED, this.location);
						}.bind(this));
					} else if (location) {
						var located = this.located(location);

						if (!located || !located.start || !located.end) {
							return;
						}

						this.location = located;

						/**
       * @event locationChanged
       * @deprecated
       * @type {object}
       * @property {number} index
       * @property {string} href
       * @property {EpubCFI} start
       * @property {EpubCFI} end
       * @property {number} percentage
       * @memberof Rendition
       */
						this.emit(_constants.EVENTS.RENDITION.LOCATION_CHANGED, {
							index: this.location.start.index,
							href: this.location.start.href,
							start: this.location.start.cfi,
							end: this.location.end.cfi,
							percentage: this.location.start.percentage
						});

						/**
       * @event relocated
       * @type {displayedLocation}
       * @memberof Rendition
       */
						this.emit(_constants.EVENTS.RENDITION.RELOCATED, this.location);
					}
				}.bind(this));
			}.bind(this));
		}

		/**
   * Get the Current Location object
   * @return {displayedLocation | promise} location (may be a promise)
   */

	}, {
		key: "currentLocation",
		value: function currentLocation() {
			var location = this.manager.currentLocation();
			if (location && location.then && typeof location.then === "function") {
				location.then(function (result) {
					var located = this.located(result);
					return located;
				}.bind(this));
			} else if (location) {
				var located = this.located(location);
				return located;
			}
		}

		/**
   * Creates a Rendition#locationRange from location
   * passed by the Manager
   * @returns {displayedLocation}
   * @private
   */

	}, {
		key: "located",
		value: function located(location) {
			if (!location.length) {
				return {};
			}
			var start = location[0];
			var end = location[location.length - 1];

			var located = {
				start: {
					index: start.index,
					href: start.href,
					cfi: start.mapping.start,
					displayed: {
						page: start.pages[0] || 1,
						total: start.totalPages
					}
				},
				end: {
					index: end.index,
					href: end.href,
					cfi: end.mapping.end,
					displayed: {
						page: end.pages[end.pages.length - 1] || 1,
						total: end.totalPages
					}
				}
			};

			var locationStart = this.book.locations.locationFromCfi(start.mapping.start);
			var locationEnd = this.book.locations.locationFromCfi(end.mapping.end);

			if (locationStart != null) {
				located.start.location = locationStart;
				located.start.percentage = this.book.locations.percentageFromLocation(locationStart);
			}
			if (locationEnd != null) {
				located.end.location = locationEnd;
				located.end.percentage = this.book.locations.percentageFromLocation(locationEnd);
			}

			var pageStart = this.book.pageList.pageFromCfi(start.mapping.start);
			var pageEnd = this.book.pageList.pageFromCfi(end.mapping.end);

			if (pageStart != -1) {
				located.start.page = pageStart;
			}
			if (pageEnd != -1) {
				located.end.page = pageEnd;
			}

			if (end.index === this.book.spine.last().index && located.end.displayed.page >= located.end.displayed.total) {
				located.atEnd = true;
			}

			if (start.index === this.book.spine.first().index && located.start.displayed.page === 1) {
				located.atStart = true;
			}

			return located;
		}

		/**
   * Remove and Clean Up the Rendition
   */

	}, {
		key: "destroy",
		value: function destroy() {
			// Clear the queue
			// this.q.clear();
			// this.q = undefined;

			this.manager && this.manager.destroy();

			this.book = undefined;

			// this.views = null;

			// this.hooks.display.clear();
			// this.hooks.serialize.clear();
			// this.hooks.content.clear();
			// this.hooks.layout.clear();
			// this.hooks.render.clear();
			// this.hooks.show.clear();
			// this.hooks = {};

			// this.themes.destroy();
			// this.themes = undefined;

			// this.epubcfi = undefined;

			// this.starting = undefined;
			// this.started = undefined;

		}

		/**
   * Pass the events from a view's Contents
   * @private
   * @param  {Contents} view contents
   */

	}, {
		key: "passEvents",
		value: function passEvents(contents) {
			var _this5 = this;

			_constants.DOM_EVENTS.forEach(function (e) {
				contents.on(e, function (ev) {
					return _this5.triggerViewEvent(ev, contents);
				});
			});

			contents.on(_constants.EVENTS.CONTENTS.SELECTED, function (e) {
				return _this5.triggerSelectedEvent(e, contents);
			});
		}

		/**
   * Emit events passed by a view
   * @private
   * @param  {event} e
   */

	}, {
		key: "triggerViewEvent",
		value: function triggerViewEvent(e, contents) {
			this.emit(e.type, e, contents);
		}

		/**
   * Emit a selection event's CFI Range passed from a a view
   * @private
   * @param  {EpubCFI} cfirange
   */

	}, {
		key: "triggerSelectedEvent",
		value: function triggerSelectedEvent(cfirange, contents) {
			/**
    * Emit that a text selection has occured
    * @event selected
    * @param {EpubCFI} cfirange
    * @param {Contents} contents
    * @memberof Rendition
    */
			this.emit(_constants.EVENTS.RENDITION.SELECTED, cfirange, contents);
		}

		/**
   * Emit a markClicked event with the cfiRange and data from a mark
   * @private
   * @param  {EpubCFI} cfirange
   */

	}, {
		key: "triggerMarkEvent",
		value: function triggerMarkEvent(cfiRange, data, contents) {
			/**
    * Emit that a mark was clicked
    * @event markClicked
    * @param {EpubCFI} cfirange
    * @param {object} data
    * @param {Contents} contents
    * @memberof Rendition
    */
			this.emit(_constants.EVENTS.RENDITION.MARK_CLICKED, cfiRange, data, contents);
		}

		/**
   * Get a Range from a Visible CFI
   * @param  {string} cfi EpubCfi String
   * @param  {string} ignoreClass
   * @return {range}
   */

	}, {
		key: "getRange",
		value: function getRange(cfi, ignoreClass) {
			var _cfi = new _epubcfi2.default(cfi);
			var found = this.manager.visible().filter(function (view) {
				if (_cfi.spinePos === view.index) return true;
			});

			// Should only every return 1 item
			if (found.length) {
				return found[0].contents.range(_cfi, ignoreClass);
			}
		}

		/**
   * Hook to adjust images to fit in columns
   * @param  {Contents} contents
   * @private
   */

	}, {
		key: "adjustImages",
		value: function adjustImages(contents) {

			if (this._layout.name === "pre-paginated") {
				return new Promise(function (resolve) {
					resolve();
				});
			}

			var computed = contents.window.getComputedStyle(contents.content, null);
			var height = (contents.content.offsetHeight - (parseFloat(computed.paddingTop) + parseFloat(computed.paddingBottom))) * .95;
			var verticalPadding = parseFloat(computed.verticalPadding);

			contents.addStylesheetRules({
				"img": {
					"max-width": (this._layout.columnWidth ? this._layout.columnWidth - verticalPadding + "px" : "100%") + "!important",
					"max-height": height + "px" + "!important",
					"object-fit": "contain",
					"page-break-inside": "avoid",
					"break-inside": "avoid",
					"box-sizing": "border-box"
				},
				"svg": {
					"max-width": (this._layout.columnWidth ? this._layout.columnWidth - verticalPadding + "px" : "100%") + "!important",
					"max-height": height + "px" + "!important",
					"page-break-inside": "avoid",
					"break-inside": "avoid"
				}
			});

			return new Promise(function (resolve, reject) {
				// Wait to apply
				setTimeout(function () {
					resolve();
				}, 1);
			});
		}

		/**
   * Get the Contents object of each rendered view
   * @returns {Contents[]}
   */

	}, {
		key: "getContents",
		value: function getContents() {
			return this.manager ? this.manager.getContents() : [];
		}

		/**
   * Get the views member from the manager
   * @returns {Views}
   */

	}, {
		key: "views",
		value: function views() {
			var views = this.manager ? this.manager.views : undefined;
			return views || [];
		}

		/**
   * Hook to handle link clicks in rendered content
   * @param  {Contents} contents
   * @private
   */

	}, {
		key: "handleLinks",
		value: function handleLinks(contents) {
			var _this6 = this;

			if (contents) {
				contents.on(_constants.EVENTS.CONTENTS.LINK_CLICKED, function (href) {
					var relative = _this6.book.path.relative(href);
					_this6.display(relative);
				});
			}
		}

		/**
   * Hook to handle injecting stylesheet before
   * a Section is serialized
   * @param  {document} doc
   * @param  {Section} section
   * @private
   */

	}, {
		key: "injectStylesheet",
		value: function injectStylesheet(doc, section) {
			var style = doc.createElement("link");
			style.setAttribute("type", "text/css");
			style.setAttribute("rel", "stylesheet");
			style.setAttribute("href", this.settings.stylesheet);
			doc.getElementsByTagName("head")[0].appendChild(style);
		}

		/**
   * Hook to handle injecting scripts before
   * a Section is serialized
   * @param  {document} doc
   * @param  {Section} section
   * @private
   */

	}, {
		key: "injectScript",
		value: function injectScript(doc, section) {
			var script = doc.createElement("script");
			script.setAttribute("type", "text/javascript");
			script.setAttribute("src", this.settings.script);
			script.textContent = " "; // Needed to prevent self closing tag
			doc.getElementsByTagName("head")[0].appendChild(script);
		}

		/**
   * Hook to handle the document identifier before
   * a Section is serialized
   * @param  {document} doc
   * @param  {Section} section
   * @private
   */

	}, {
		key: "injectIdentifier",
		value: function injectIdentifier(doc, section) {
			var ident = this.book.packaging.metadata.identifier;
			var meta = doc.createElement("meta");
			meta.setAttribute("name", "dc.relation.ispartof");
			if (ident) {
				meta.setAttribute("content", ident);
			}
			doc.getElementsByTagName("head")[0].appendChild(meta);
		}
	}]);

	return Rendition;
}();

//-- Enable binding events to Renderer


(0, _eventEmitter2.default)(Rendition.prototype);

exports.default = Rendition;
module.exports = exports["default"];

/***/ }),
/* 142 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _epubcfi = __webpack_require__(22);

var _epubcfi2 = _interopRequireDefault(_epubcfi);

var _core = __webpack_require__(6);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Map text locations to CFI ranges
 * @class
 * @param {Layout} layout Layout to apply
 * @param {string} [direction="ltr"] Text direction
 * @param {string} [axis="horizontal"] vertical or horizontal axis
 * @param {boolean} [dev] toggle developer highlighting
 */
var Mapping = function () {
	function Mapping(layout, direction, axis, dev) {
		_classCallCheck(this, Mapping);

		this.layout = layout;
		this.horizontal = axis === "horizontal" ? true : false;
		this.direction = direction || "ltr";
		this._dev = dev;
	}

	/**
  * Find CFI pairs for entire section at once
  */


	_createClass(Mapping, [{
		key: "section",
		value: function section(view) {
			var ranges = this.findRanges(view);
			var map = this.rangeListToCfiList(view.section.cfiBase, ranges);

			return map;
		}

		/**
   * Find CFI pairs for a page
   * @param {Contents} contents Contents from view
   * @param {string} cfiBase string of the base for a cfi
   * @param {number} start position to start at
   * @param {number} end position to end at
   */

	}, {
		key: "page",
		value: function page(contents, cfiBase, start, end) {
			var root = contents && contents.document ? contents.document.body : false;
			var result;

			if (!root) {
				return;
			}

			result = this.rangePairToCfiPair(cfiBase, {
				start: this.findStart(root, start, end),
				end: this.findEnd(root, start, end)
			});

			if (this._dev === true) {
				var doc = contents.document;
				var startRange = new _epubcfi2.default(result.start).toRange(doc);
				var endRange = new _epubcfi2.default(result.end).toRange(doc);

				var selection = doc.defaultView.getSelection();
				var r = doc.createRange();
				selection.removeAllRanges();
				r.setStart(startRange.startContainer, startRange.startOffset);
				r.setEnd(endRange.endContainer, endRange.endOffset);
				selection.addRange(r);
			}

			return result;
		}

		/**
   * Walk a node, preforming a function on each node it finds
   * @private
   * @param {Node} root Node to walkToNode
   * @param {function} func walk function
   * @return {*} returns the result of the walk function
   */

	}, {
		key: "walk",
		value: function walk(root, func) {
			// IE11 has strange issue, if root is text node IE throws exception on
			// calling treeWalker.nextNode(), saying
			// Unexpected call to method or property access instead of returing null value
			if (root && root.nodeType === Node.TEXT_NODE) {
				return;
			}
			// safeFilter is required so that it can work in IE as filter is a function for IE
			// and for other browser filter is an object.
			var filter = {
				acceptNode: function acceptNode(node) {
					if (node.data.trim().length > 0) {
						return NodeFilter.FILTER_ACCEPT;
					} else {
						return NodeFilter.FILTER_REJECT;
					}
				}
			};
			var safeFilter = filter.acceptNode;
			safeFilter.acceptNode = filter.acceptNode;

			var treeWalker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, safeFilter, false);
			var node;
			var result;
			while (node = treeWalker.nextNode()) {
				result = func(node);
				if (result) break;
			}

			return result;
		}
	}, {
		key: "findRanges",
		value: function findRanges(view) {
			var columns = [];
			var scrollWidth = view.contents.scrollWidth();
			var spreads = Math.ceil(scrollWidth / this.layout.spreadWidth);
			var count = spreads * this.layout.divisor;
			var columnWidth = this.layout.columnWidth;
			var gap = this.layout.gap;
			var start, end;

			for (var i = 0; i < count.pages; i++) {
				start = (columnWidth + gap) * i;
				end = columnWidth * (i + 1) + gap * i;
				columns.push({
					start: this.findStart(view.document.body, start, end),
					end: this.findEnd(view.document.body, start, end)
				});
			}

			return columns;
		}

		/**
   * Find Start Range
   * @private
   * @param {Node} root root node
   * @param {number} start position to start at
   * @param {number} end position to end at
   * @return {Range}
   */

	}, {
		key: "findStart",
		value: function findStart(root, start, end) {
			var _this = this;

			var stack = [root];
			var $el;
			var found;
			var $prev = root;

			while (stack.length) {

				$el = stack.shift();

				found = this.walk($el, function (node) {
					var left, right, top, bottom;
					var elPos;
					var elRange;

					elPos = (0, _core.nodeBounds)(node);

					if (_this.horizontal && _this.direction === "ltr") {

						left = _this.horizontal ? elPos.left : elPos.top;
						right = _this.horizontal ? elPos.right : elPos.bottom;

						if (left >= start && left <= end) {
							return node;
						} else if (right > start) {
							return node;
						} else {
							$prev = node;
							stack.push(node);
						}
					} else if (_this.horizontal && _this.direction === "rtl") {

						left = elPos.left;
						right = elPos.right;

						if (right <= end && right >= start) {
							return node;
						} else if (left < end) {
							return node;
						} else {
							$prev = node;
							stack.push(node);
						}
					} else {

						top = elPos.top;
						bottom = elPos.bottom;

						if (top >= start && top <= end) {
							return node;
						} else if (bottom > start) {
							return node;
						} else {
							$prev = node;
							stack.push(node);
						}
					}
				});

				if (found) {
					return this.findTextStartRange(found, start, end);
				}
			}

			// Return last element
			return this.findTextStartRange($prev, start, end);
		}

		/**
   * Find End Range
   * @private
   * @param {Node} root root node
   * @param {number} start position to start at
   * @param {number} end position to end at
   * @return {Range}
   */

	}, {
		key: "findEnd",
		value: function findEnd(root, start, end) {
			var _this2 = this;

			var stack = [root];
			var $el;
			var $prev = root;
			var found;

			while (stack.length) {

				$el = stack.shift();

				found = this.walk($el, function (node) {

					var left, right, top, bottom;
					var elPos;
					var elRange;

					elPos = (0, _core.nodeBounds)(node);

					if (_this2.horizontal && _this2.direction === "ltr") {

						left = Math.round(elPos.left);
						right = Math.round(elPos.right);

						if (left > end && $prev) {
							return $prev;
						} else if (right > end) {
							return node;
						} else {
							$prev = node;
							stack.push(node);
						}
					} else if (_this2.horizontal && _this2.direction === "rtl") {

						left = Math.round(_this2.horizontal ? elPos.left : elPos.top);
						right = Math.round(_this2.horizontal ? elPos.right : elPos.bottom);

						if (right < start && $prev) {
							return $prev;
						} else if (left < start) {
							return node;
						} else {
							$prev = node;
							stack.push(node);
						}
					} else {

						top = Math.round(elPos.top);
						bottom = Math.round(elPos.bottom);

						if (top > end && $prev) {
							return $prev;
						} else if (bottom > end) {
							return node;
						} else {
							$prev = node;
							stack.push(node);
						}
					}
				});

				if (found) {
					return this.findTextEndRange(found, start, end);
				}
			}

			// end of chapter
			return this.findTextEndRange($prev, start, end);
		}

		/**
   * Find Text Start Range
   * @private
   * @param {Node} root root node
   * @param {number} start position to start at
   * @param {number} end position to end at
   * @return {Range}
   */

	}, {
		key: "findTextStartRange",
		value: function findTextStartRange(node, start, end) {
			var ranges = this.splitTextNodeIntoRanges(node);
			var range;
			var pos;
			var left, top, right;

			for (var i = 0; i < ranges.length; i++) {
				range = ranges[i];

				pos = range.getBoundingClientRect();

				if (this.horizontal && this.direction === "ltr") {

					left = pos.left;
					if (left >= start) {
						return range;
					}
				} else if (this.horizontal && this.direction === "rtl") {

					right = pos.right;
					if (right <= end) {
						return range;
					}
				} else {

					top = pos.top;
					if (top >= start) {
						return range;
					}
				}

				// prev = range;
			}

			return ranges[0];
		}

		/**
   * Find Text End Range
   * @private
   * @param {Node} root root node
   * @param {number} start position to start at
   * @param {number} end position to end at
   * @return {Range}
   */

	}, {
		key: "findTextEndRange",
		value: function findTextEndRange(node, start, end) {
			var ranges = this.splitTextNodeIntoRanges(node);
			var prev;
			var range;
			var pos;
			var left, right, top, bottom;

			for (var i = 0; i < ranges.length; i++) {
				range = ranges[i];

				pos = range.getBoundingClientRect();

				if (this.horizontal && this.direction === "ltr") {

					left = pos.left;
					right = pos.right;

					if (left > end && prev) {
						return prev;
					} else if (right > end) {
						return range;
					}
				} else if (this.horizontal && this.direction === "rtl") {

					left = pos.left;
					right = pos.right;

					if (right < start && prev) {
						return prev;
					} else if (left < start) {
						return range;
					}
				} else {

					top = pos.top;
					bottom = pos.bottom;

					if (top > end && prev) {
						return prev;
					} else if (bottom > end) {
						return range;
					}
				}

				prev = range;
			}

			// Ends before limit
			return ranges[ranges.length - 1];
		}

		/**
   * Split up a text node into ranges for each word
   * @private
   * @param {Node} root root node
   * @param {string} [_splitter] what to split on
   * @return {Range[]}
   */

	}, {
		key: "splitTextNodeIntoRanges",
		value: function splitTextNodeIntoRanges(node, _splitter) {
			var ranges = [];
			var textContent = node.textContent || "";
			var text = textContent.trim();
			var range;
			var doc = node.ownerDocument;
			var splitter = _splitter || " ";

			var pos = text.indexOf(splitter);

			if (pos === -1 || node.nodeType != Node.TEXT_NODE) {
				range = doc.createRange();
				range.selectNodeContents(node);
				return [range];
			}

			range = doc.createRange();
			range.setStart(node, 0);
			range.setEnd(node, pos);
			ranges.push(range);
			range = false;

			while (pos != -1) {

				pos = text.indexOf(splitter, pos + 1);
				if (pos > 0) {

					if (range) {
						range.setEnd(node, pos);
						ranges.push(range);
					}

					range = doc.createRange();
					range.setStart(node, pos + 1);
				}
			}

			if (range) {
				range.setEnd(node, text.length);
				ranges.push(range);
			}

			return ranges;
		}

		/**
   * Turn a pair of ranges into a pair of CFIs
   * @private
   * @param {string} cfiBase base string for an EpubCFI
   * @param {object} rangePair { start: Range, end: Range }
   * @return {object} { start: "epubcfi(...)", end: "epubcfi(...)" }
   */

	}, {
		key: "rangePairToCfiPair",
		value: function rangePairToCfiPair(cfiBase, rangePair) {

			var startRange = rangePair.start;
			var endRange = rangePair.end;

			startRange.collapse(true);
			endRange.collapse(false);

			var startCfi = new _epubcfi2.default(startRange, cfiBase).toString();
			var endCfi = new _epubcfi2.default(endRange, cfiBase).toString();

			return {
				start: startCfi,
				end: endCfi
			};
		}
	}, {
		key: "rangeListToCfiList",
		value: function rangeListToCfiList(cfiBase, columns) {
			var map = [];
			var cifPair;

			for (var i = 0; i < columns.length; i++) {
				cifPair = this.rangePairToCfiPair(cfiBase, columns[i]);

				map.push(cifPair);
			}

			return map;
		}

		/**
   * Set the axis for mapping
   * @param {string} axis horizontal | vertical
   * @return {boolean} is it horizontal?
   */

	}, {
		key: "axis",
		value: function axis(_axis) {
			if (_axis) {
				this.horizontal = _axis === "horizontal" ? true : false;
			}
			return this.horizontal;
		}
	}]);

	return Mapping;
}();

exports.default = Mapping;
module.exports = exports["default"];

/***/ }),
/* 143 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _eventEmitter = __webpack_require__(30);

var _eventEmitter2 = _interopRequireDefault(_eventEmitter);

var _core = __webpack_require__(6);

var _epubcfi = __webpack_require__(22);

var _epubcfi2 = _interopRequireDefault(_epubcfi);

var _contents = __webpack_require__(104);

var _contents2 = _interopRequireDefault(_contents);

var _constants = __webpack_require__(23);

var _marksPane = __webpack_require__(385);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var IframeView = function () {
	function IframeView(section, options) {
		_classCallCheck(this, IframeView);

		this.settings = (0, _core.extend)({
			ignoreClass: "",
			axis: options.layout && options.layout.props.flow === "scrolled" ? "vertical" : "horizontal",
			direction: undefined,
			width: 0,
			height: 0,
			layout: undefined,
			globalLayoutProperties: {},
			method: undefined
		}, options || {});

		this.id = "epubjs-view-" + (0, _core.uuid)();
		this.section = section;
		this.index = section.index;

		this.element = this.container(this.settings.axis);

		this.added = false;
		this.displayed = false;
		this.rendered = false;

		// this.width  = this.settings.width;
		// this.height = this.settings.height;

		this.fixedWidth = 0;
		this.fixedHeight = 0;

		// Blank Cfi for Parsing
		this.epubcfi = new _epubcfi2.default();

		this.layout = this.settings.layout;
		// Dom events to listen for
		// this.listenedEvents = ["keydown", "keyup", "keypressed", "mouseup", "mousedown", "click", "touchend", "touchstart"];

		this.pane = undefined;
		this.highlights = {};
		this.underlines = {};
		this.marks = {};
	}

	_createClass(IframeView, [{
		key: "container",
		value: function container(axis) {
			var element = document.createElement("div");

			element.classList.add("epub-view");

			// this.element.style.minHeight = "100px";
			element.style.height = "0px";
			element.style.width = "0px";
			element.style.overflow = "hidden";
			element.style.position = "relative";
			element.style.display = "block";

			if (axis && axis == "horizontal") {
				element.style.flex = "none";
			} else {
				element.style.flex = "initial";
			}

			return element;
		}
	}, {
		key: "create",
		value: function create() {

			if (this.iframe) {
				return this.iframe;
			}

			if (!this.element) {
				this.element = this.createContainer();
			}

			this.iframe = document.createElement("iframe");
			this.iframe.id = this.id;
			this.iframe.scrolling = "no"; // Might need to be removed: breaks ios width calculations
			this.iframe.style.overflow = "hidden";
			this.iframe.seamless = "seamless";
			// Back up if seamless isn't supported
			this.iframe.style.border = "none";

			this.iframe.setAttribute("enable-annotation", "true");

			this.resizing = true;

			// this.iframe.style.display = "none";
			this.element.style.visibility = "hidden";
			this.iframe.style.visibility = "hidden";

			this.iframe.style.width = "0";
			this.iframe.style.height = "0";
			this._width = 0;
			this._height = 0;

			this.element.setAttribute("ref", this.index);

			this.added = true;

			this.elementBounds = (0, _core.bounds)(this.element);

			// if(width || height){
			//   this.resize(width, height);
			// } else if(this.width && this.height){
			//   this.resize(this.width, this.height);
			// } else {
			//   this.iframeBounds = bounds(this.iframe);
			// }


			if ("srcdoc" in this.iframe) {
				this.supportsSrcdoc = true;
			} else {
				this.supportsSrcdoc = false;
			}

			if (!this.settings.method) {
				this.settings.method = this.supportsSrcdoc ? "srcdoc" : "write";
			}

			return this.iframe;
		}
	}, {
		key: "render",
		value: function render(request, show) {

			// view.onLayout = this.layout.format.bind(this.layout);
			this.create();

			// Fit to size of the container, apply padding
			this.size();

			if (!this.sectionRender) {
				this.sectionRender = this.section.render(request);
			}

			// Render Chain
			return this.sectionRender.then(function (contents) {
				return this.load(contents);
			}.bind(this)).then(function () {
				var _this = this;

				// apply the layout function to the contents
				this.layout.format(this.contents);

				// find and report the writingMode axis
				var writingMode = this.contents.writingMode();
				var axis = writingMode.indexOf("vertical") === 0 ? "vertical" : "horizontal";

				this.setAxis(axis);
				this.emit(_constants.EVENTS.VIEWS.AXIS, axis);

				// Listen for events that require an expansion of the iframe
				this.addListeners();

				return new Promise(function (resolve, reject) {
					// Expand the iframe to the full size of the content
					_this.expand();
					resolve();
				});
			}.bind(this), function (e) {
				this.emit(_constants.EVENTS.VIEWS.LOAD_ERROR, e);
				return new Promise(function (resolve, reject) {
					reject(e);
				});
			}.bind(this)).then(function () {
				this.emit(_constants.EVENTS.VIEWS.RENDERED, this.section);
			}.bind(this));
		}
	}, {
		key: "reset",
		value: function reset() {
			if (this.iframe) {
				this.iframe.style.width = "0";
				this.iframe.style.height = "0";
				this._width = 0;
				this._height = 0;
				this._textWidth = undefined;
				this._contentWidth = undefined;
				this._textHeight = undefined;
				this._contentHeight = undefined;
			}
			this._needsReframe = true;
		}

		// Determine locks base on settings

	}, {
		key: "size",
		value: function size(_width, _height) {
			var width = _width || this.settings.width;
			var height = _height || this.settings.height;

			if (this.layout.name === "pre-paginated") {
				this.lock("both", width, height);
			} else if (this.settings.axis === "horizontal") {
				this.lock("height", width, height);
			} else {
				this.lock("width", width, height);
			}

			this.settings.width = width;
			this.settings.height = height;
		}

		// Lock an axis to element dimensions, taking borders into account

	}, {
		key: "lock",
		value: function lock(what, width, height) {
			var elBorders = (0, _core.borders)(this.element);
			var iframeBorders;

			if (this.iframe) {
				iframeBorders = (0, _core.borders)(this.iframe);
			} else {
				iframeBorders = { width: 0, height: 0 };
			}

			if (what == "width" && (0, _core.isNumber)(width)) {
				this.lockedWidth = width - elBorders.width - iframeBorders.width;
				// this.resize(this.lockedWidth, width); //  width keeps ratio correct
			}

			if (what == "height" && (0, _core.isNumber)(height)) {
				this.lockedHeight = height - elBorders.height - iframeBorders.height;
				// this.resize(width, this.lockedHeight);
			}

			if (what === "both" && (0, _core.isNumber)(width) && (0, _core.isNumber)(height)) {

				this.lockedWidth = width - elBorders.width - iframeBorders.width;
				this.lockedHeight = height - elBorders.height - iframeBorders.height;
				// this.resize(this.lockedWidth, this.lockedHeight);
			}

			if (this.displayed && this.iframe) {

				// this.contents.layout();
				this.expand();
			}
		}

		// Resize a single axis based on content dimensions

	}, {
		key: "expand",
		value: function expand(force) {
			var width = this.lockedWidth;
			var height = this.lockedHeight;
			var columns;

			var textWidth, textHeight;

			if (!this.iframe || this._expanding) return;

			this._expanding = true;

			if (this.layout.name === "pre-paginated") {
				width = this.layout.columnWidth;
				height = this.layout.height;
			}
			// Expand Horizontally
			else if (this.settings.axis === "horizontal") {
					// Get the width of the text
					width = this.contents.textWidth();

					if (width % this.layout.pageWidth > 0) {
						width = Math.ceil(width / this.layout.pageWidth) * this.layout.pageWidth;
					}

					if (this.settings.forceEvenPages) {
						columns = width / this.layout.pageWidth;
						if (this.layout.divisor > 1 && this.layout.name === "reflowable" && columns % 2 > 0) {
							// add a blank page
							width += this.layout.pageWidth;
						}
					}
				} // Expand Vertically
				else if (this.settings.axis === "vertical") {
						height = this.contents.textHeight();
					}

			// Only Resize if dimensions have changed or
			// if Frame is still hidden, so needs reframing
			if (this._needsReframe || width != this._width || height != this._height) {
				this.reframe(width, height);
			}

			this._expanding = false;
		}
	}, {
		key: "reframe",
		value: function reframe(width, height) {
			var _this2 = this;

			var size;

			if ((0, _core.isNumber)(width)) {
				this.element.style.width = width + "px";
				this.iframe.style.width = width + "px";
				this._width = width;
			}

			if ((0, _core.isNumber)(height)) {
				this.element.style.height = height + "px";
				this.iframe.style.height = height + "px";
				this._height = height;
			}

			var widthDelta = this.prevBounds ? width - this.prevBounds.width : width;
			var heightDelta = this.prevBounds ? height - this.prevBounds.height : height;

			size = {
				width: width,
				height: height,
				widthDelta: widthDelta,
				heightDelta: heightDelta
			};

			this.pane && this.pane.render();

			requestAnimationFrame(function () {
				var mark = void 0;
				for (var m in _this2.marks) {
					if (_this2.marks.hasOwnProperty(m)) {
						mark = _this2.marks[m];
						_this2.placeMark(mark.element, mark.range);
					}
				}
			});

			this.onResize(this, size);

			this.emit(_constants.EVENTS.VIEWS.RESIZED, size);

			this.prevBounds = size;

			this.elementBounds = (0, _core.bounds)(this.element);
		}
	}, {
		key: "load",
		value: function load(contents) {
			var loading = new _core.defer();
			var loaded = loading.promise;

			if (!this.iframe) {
				loading.reject(new Error("No Iframe Available"));
				return loaded;
			}

			this.iframe.onload = function (event) {

				this.onLoad(event, loading);
			}.bind(this);

			if (this.settings.method === "blobUrl") {
				this.blobUrl = (0, _core.createBlobUrl)(contents, "application/xhtml+xml");
				this.iframe.src = this.blobUrl;
				this.element.appendChild(this.iframe);
			} else if (this.settings.method === "srcdoc") {
				this.iframe.srcdoc = contents;
				this.element.appendChild(this.iframe);
			} else {

				this.element.appendChild(this.iframe);

				this.document = this.iframe.contentDocument;

				if (!this.document) {
					loading.reject(new Error("No Document Available"));
					return loaded;
				}

				this.iframe.contentDocument.open();
				this.iframe.contentDocument.write(contents);
				this.iframe.contentDocument.close();
			}

			return loaded;
		}
	}, {
		key: "onLoad",
		value: function onLoad(event, promise) {
			var _this3 = this;

			this.window = this.iframe.contentWindow;
			this.document = this.iframe.contentDocument;

			this.contents = new _contents2.default(this.document, this.document.body, this.section.cfiBase, this.section.index);

			this.rendering = false;

			var link = this.document.querySelector("link[rel='canonical']");
			if (link) {
				link.setAttribute("href", this.section.canonical);
			} else {
				link = this.document.createElement("link");
				link.setAttribute("rel", "canonical");
				link.setAttribute("href", this.section.canonical);
				this.document.querySelector("head").appendChild(link);
			}

			this.contents.on(_constants.EVENTS.CONTENTS.EXPAND, function () {
				if (_this3.displayed && _this3.iframe) {
					_this3.expand();
					if (_this3.contents) {
						_this3.layout.format(_this3.contents);
					}
				}
			});

			this.contents.on(_constants.EVENTS.CONTENTS.RESIZE, function (e) {
				if (_this3.displayed && _this3.iframe) {
					_this3.expand();
					if (_this3.contents) {
						_this3.layout.format(_this3.contents);
					}
				}
			});

			promise.resolve(this.contents);
		}
	}, {
		key: "setLayout",
		value: function setLayout(layout) {
			this.layout = layout;

			if (this.contents) {
				this.layout.format(this.contents);
				this.expand();
			}
		}
	}, {
		key: "setAxis",
		value: function setAxis(axis) {

			// Force vertical for scrolled
			if (this.layout.props.flow === "scrolled") {
				axis = "vertical";
			}

			this.settings.axis = axis;

			if (axis == "horizontal") {
				this.element.style.flex = "none";
			} else {
				this.element.style.flex = "initial";
			}

			this.size();
		}
	}, {
		key: "addListeners",
		value: function addListeners() {
			//TODO: Add content listeners for expanding
		}
	}, {
		key: "removeListeners",
		value: function removeListeners(layoutFunc) {
			//TODO: remove content listeners for expanding
		}
	}, {
		key: "display",
		value: function display(request) {
			var displayed = new _core.defer();

			if (!this.displayed) {

				this.render(request).then(function () {

					this.emit(_constants.EVENTS.VIEWS.DISPLAYED, this);
					this.onDisplayed(this);

					this.displayed = true;
					displayed.resolve(this);
				}.bind(this), function (err) {
					displayed.reject(err, this);
				});
			} else {
				displayed.resolve(this);
			}

			return displayed.promise;
		}
	}, {
		key: "show",
		value: function show() {

			this.element.style.visibility = "visible";

			if (this.iframe) {
				this.iframe.style.visibility = "visible";

				// Remind Safari to redraw the iframe
				this.iframe.style.transform = "translateZ(0)";
				this.iframe.offsetWidth;
				this.iframe.style.transform = null;
			}

			this.emit(_constants.EVENTS.VIEWS.SHOWN, this);
		}
	}, {
		key: "hide",
		value: function hide() {
			// this.iframe.style.display = "none";
			this.element.style.visibility = "hidden";
			this.iframe.style.visibility = "hidden";

			this.stopExpanding = true;
			this.emit(_constants.EVENTS.VIEWS.HIDDEN, this);
		}
	}, {
		key: "offset",
		value: function offset() {
			return {
				top: this.element.offsetTop,
				left: this.element.offsetLeft
			};
		}
	}, {
		key: "width",
		value: function width() {
			return this._width;
		}
	}, {
		key: "height",
		value: function height() {
			return this._height;
		}
	}, {
		key: "position",
		value: function position() {
			return this.element.getBoundingClientRect();
		}
	}, {
		key: "locationOf",
		value: function locationOf(target) {
			var parentPos = this.iframe.getBoundingClientRect();
			var targetPos = this.contents.locationOf(target, this.settings.ignoreClass);

			return {
				"left": targetPos.left,
				"top": targetPos.top
			};
		}
	}, {
		key: "onDisplayed",
		value: function onDisplayed(view) {
			// Stub, override with a custom functions
		}
	}, {
		key: "onResize",
		value: function onResize(view, e) {
			// Stub, override with a custom functions
		}
	}, {
		key: "bounds",
		value: function bounds(force) {
			if (force || !this.elementBounds) {
				this.elementBounds = (0, _core.bounds)(this.element);
			}

			return this.elementBounds;
		}
	}, {
		key: "highlight",
		value: function highlight(cfiRange) {
			var data = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};
			var cb = arguments[2];

			var _this4 = this;

			var className = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : "epubjs-hl";
			var styles = arguments.length > 4 && arguments[4] !== undefined ? arguments[4] : {};

			if (!this.contents) {
				return;
			}
			var attributes = Object.assign({ "fill": "yellow", "fill-opacity": "0.3", "mix-blend-mode": "multiply" }, styles);
			var range = this.contents.range(cfiRange);

			var emitter = function emitter() {
				_this4.emit(_constants.EVENTS.VIEWS.MARK_CLICKED, cfiRange, data);
			};

			data["epubcfi"] = cfiRange;

			if (!this.pane) {
				this.pane = new _marksPane.Pane(this.iframe, this.element);
			}

			var m = new _marksPane.Highlight(range, className, data, attributes);
			var h = this.pane.addMark(m);

			this.highlights[cfiRange] = { "mark": h, "element": h.element, "listeners": [emitter, cb] };

			h.element.setAttribute("ref", className);
			h.element.addEventListener("click", emitter);
			h.element.addEventListener("touchstart", emitter);

			if (cb) {
				h.element.addEventListener("click", cb);
				h.element.addEventListener("touchstart", cb);
			}
			return h;
		}
	}, {
		key: "underline",
		value: function underline(cfiRange) {
			var data = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};
			var cb = arguments[2];

			var _this5 = this;

			var className = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : "epubjs-ul";
			var styles = arguments.length > 4 && arguments[4] !== undefined ? arguments[4] : {};

			if (!this.contents) {
				return;
			}
			var attributes = Object.assign({ "stroke": "black", "stroke-opacity": "0.3", "mix-blend-mode": "multiply" }, styles);
			var range = this.contents.range(cfiRange);
			var emitter = function emitter() {
				_this5.emit(_constants.EVENTS.VIEWS.MARK_CLICKED, cfiRange, data);
			};

			data["epubcfi"] = cfiRange;

			if (!this.pane) {
				this.pane = new _marksPane.Pane(this.iframe, this.element);
			}

			var m = new _marksPane.Underline(range, className, data, attributes);
			var h = this.pane.addMark(m);

			this.underlines[cfiRange] = { "mark": h, "element": h.element, "listeners": [emitter, cb] };

			h.element.setAttribute("ref", className);
			h.element.addEventListener("click", emitter);
			h.element.addEventListener("touchstart", emitter);

			if (cb) {
				h.element.addEventListener("click", cb);
				h.element.addEventListener("touchstart", cb);
			}
			return h;
		}
	}, {
		key: "mark",
		value: function mark(cfiRange) {
			var _this6 = this;

			var data = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};
			var cb = arguments[2];

			if (!this.contents) {
				return;
			}

			if (cfiRange in this.marks) {
				var item = this.marks[cfiRange];
				return item;
			}

			var range = this.contents.range(cfiRange);
			if (!range) {
				return;
			}
			var container = range.commonAncestorContainer;
			var parent = container.nodeType === 1 ? container : container.parentNode;

			var emitter = function emitter(e) {
				_this6.emit(_constants.EVENTS.VIEWS.MARK_CLICKED, cfiRange, data);
			};

			if (range.collapsed && container.nodeType === 1) {
				range = new Range();
				range.selectNodeContents(container);
			} else if (range.collapsed) {
				// Webkit doesn't like collapsed ranges
				range = new Range();
				range.selectNodeContents(parent);
			}

			var mark = this.document.createElement("a");
			mark.setAttribute("ref", "epubjs-mk");
			mark.style.position = "absolute";

			mark.dataset["epubcfi"] = cfiRange;

			if (data) {
				Object.keys(data).forEach(function (key) {
					mark.dataset[key] = data[key];
				});
			}

			if (cb) {
				mark.addEventListener("click", cb);
				mark.addEventListener("touchstart", cb);
			}

			mark.addEventListener("click", emitter);
			mark.addEventListener("touchstart", emitter);

			this.placeMark(mark, range);

			this.element.appendChild(mark);

			this.marks[cfiRange] = { "element": mark, "range": range, "listeners": [emitter, cb] };

			return parent;
		}
	}, {
		key: "placeMark",
		value: function placeMark(element, range) {
			var top = void 0,
			    right = void 0,
			    left = void 0;

			if (this.layout.name === "pre-paginated" || this.settings.axis !== "horizontal") {
				var pos = range.getBoundingClientRect();
				top = pos.top;
				right = pos.right;
			} else {
				// Element might break columns, so find the left most element
				var rects = range.getClientRects();

				var rect = void 0;
				for (var i = 0; i != rects.length; i++) {
					rect = rects[i];
					if (!left || rect.left < left) {
						left = rect.left;
						// right = rect.right;
						right = Math.ceil(left / this.layout.props.pageWidth) * this.layout.props.pageWidth - this.layout.gap / 2;
						top = rect.top;
					}
				}
			}

			element.style.top = top + "px";
			element.style.left = right + "px";
		}
	}, {
		key: "unhighlight",
		value: function unhighlight(cfiRange) {
			var item = void 0;
			if (cfiRange in this.highlights) {
				item = this.highlights[cfiRange];

				this.pane.removeMark(item.mark);
				item.listeners.forEach(function (l) {
					if (l) {
						item.element.removeEventListener("click", l);
						item.element.removeEventListener("touchstart", l);
					};
				});
				delete this.highlights[cfiRange];
			}
		}
	}, {
		key: "ununderline",
		value: function ununderline(cfiRange) {
			var item = void 0;
			if (cfiRange in this.underlines) {
				item = this.underlines[cfiRange];
				this.pane.removeMark(item.mark);
				item.listeners.forEach(function (l) {
					if (l) {
						item.element.removeEventListener("click", l);
						item.element.removeEventListener("touchstart", l);
					};
				});
				delete this.underlines[cfiRange];
			}
		}
	}, {
		key: "unmark",
		value: function unmark(cfiRange) {
			var item = void 0;
			if (cfiRange in this.marks) {
				item = this.marks[cfiRange];
				this.element.removeChild(item.element);
				item.listeners.forEach(function (l) {
					if (l) {
						item.element.removeEventListener("click", l);
						item.element.removeEventListener("touchstart", l);
					};
				});
				delete this.marks[cfiRange];
			}
		}
	}, {
		key: "destroy",
		value: function destroy() {

			for (var cfiRange in this.highlights) {
				this.unhighlight(cfiRange);
			}

			for (var _cfiRange in this.underlines) {
				this.ununderline(_cfiRange);
			}

			for (var _cfiRange2 in this.marks) {
				this.unmark(_cfiRange2);
			}

			if (this.blobUrl) {
				(0, _core.revokeBlobUrl)(this.blobUrl);
			}

			if (this.displayed) {
				this.displayed = false;

				this.removeListeners();
				this.contents.destroy();

				this.stopExpanding = true;
				this.element.removeChild(this.iframe);

				this.iframe = undefined;
				this.contents = undefined;

				this._textWidth = null;
				this._textHeight = null;
				this._width = null;
				this._height = null;
			}

			// this.element.style.height = "0px";
			// this.element.style.width = "0px";
		}
	}]);

	return IframeView;
}();

(0, _eventEmitter2.default)(IframeView.prototype);

exports.default = IframeView;
module.exports = exports["default"];

/***/ }),
/* 144 */
/***/ (function(module, exports, __webpack_require__) {

var isObject = __webpack_require__(106),
    now = __webpack_require__(390),
    toNumber = __webpack_require__(392);

/** Error message constants. */
var FUNC_ERROR_TEXT = 'Expected a function';

/* Built-in method references for those with the same name as other `lodash` methods. */
var nativeMax = Math.max,
    nativeMin = Math.min;

/**
 * Creates a debounced function that delays invoking `func` until after `wait`
 * milliseconds have elapsed since the last time the debounced function was
 * invoked. The debounced function comes with a `cancel` method to cancel
 * delayed `func` invocations and a `flush` method to immediately invoke them.
 * Provide `options` to indicate whether `func` should be invoked on the
 * leading and/or trailing edge of the `wait` timeout. The `func` is invoked
 * with the last arguments provided to the debounced function. Subsequent
 * calls to the debounced function return the result of the last `func`
 * invocation.
 *
 * **Note:** If `leading` and `trailing` options are `true`, `func` is
 * invoked on the trailing edge of the timeout only if the debounced function
 * is invoked more than once during the `wait` timeout.
 *
 * If `wait` is `0` and `leading` is `false`, `func` invocation is deferred
 * until to the next tick, similar to `setTimeout` with a timeout of `0`.
 *
 * See [David Corbacho's article](https://css-tricks.com/debouncing-throttling-explained-examples/)
 * for details over the differences between `_.debounce` and `_.throttle`.
 *
 * @static
 * @memberOf _
 * @since 0.1.0
 * @category Function
 * @param {Function} func The function to debounce.
 * @param {number} [wait=0] The number of milliseconds to delay.
 * @param {Object} [options={}] The options object.
 * @param {boolean} [options.leading=false]
 *  Specify invoking on the leading edge of the timeout.
 * @param {number} [options.maxWait]
 *  The maximum time `func` is allowed to be delayed before it's invoked.
 * @param {boolean} [options.trailing=true]
 *  Specify invoking on the trailing edge of the timeout.
 * @returns {Function} Returns the new debounced function.
 * @example
 *
 * // Avoid costly calculations while the window size is in flux.
 * jQuery(window).on('resize', _.debounce(calculateLayout, 150));
 *
 * // Invoke `sendMail` when clicked, debouncing subsequent calls.
 * jQuery(element).on('click', _.debounce(sendMail, 300, {
 *   'leading': true,
 *   'trailing': false
 * }));
 *
 * // Ensure `batchLog` is invoked once after 1 second of debounced calls.
 * var debounced = _.debounce(batchLog, 250, { 'maxWait': 1000 });
 * var source = new EventSource('/stream');
 * jQuery(source).on('message', debounced);
 *
 * // Cancel the trailing debounced invocation.
 * jQuery(window).on('popstate', debounced.cancel);
 */
function debounce(func, wait, options) {
  var lastArgs,
      lastThis,
      maxWait,
      result,
      timerId,
      lastCallTime,
      lastInvokeTime = 0,
      leading = false,
      maxing = false,
      trailing = true;

  if (typeof func != 'function') {
    throw new TypeError(FUNC_ERROR_TEXT);
  }
  wait = toNumber(wait) || 0;
  if (isObject(options)) {
    leading = !!options.leading;
    maxing = 'maxWait' in options;
    maxWait = maxing ? nativeMax(toNumber(options.maxWait) || 0, wait) : maxWait;
    trailing = 'trailing' in options ? !!options.trailing : trailing;
  }

  function invokeFunc(time) {
    var args = lastArgs,
        thisArg = lastThis;

    lastArgs = lastThis = undefined;
    lastInvokeTime = time;
    result = func.apply(thisArg, args);
    return result;
  }

  function leadingEdge(time) {
    // Reset any `maxWait` timer.
    lastInvokeTime = time;
    // Start the timer for the trailing edge.
    timerId = setTimeout(timerExpired, wait);
    // Invoke the leading edge.
    return leading ? invokeFunc(time) : result;
  }

  function remainingWait(time) {
    var timeSinceLastCall = time - lastCallTime,
        timeSinceLastInvoke = time - lastInvokeTime,
        timeWaiting = wait - timeSinceLastCall;

    return maxing
      ? nativeMin(timeWaiting, maxWait - timeSinceLastInvoke)
      : timeWaiting;
  }

  function shouldInvoke(time) {
    var timeSinceLastCall = time - lastCallTime,
        timeSinceLastInvoke = time - lastInvokeTime;

    // Either this is the first call, activity has stopped and we're at the
    // trailing edge, the system time has gone backwards and we're treating
    // it as the trailing edge, or we've hit the `maxWait` limit.
    return (lastCallTime === undefined || (timeSinceLastCall >= wait) ||
      (timeSinceLastCall < 0) || (maxing && timeSinceLastInvoke >= maxWait));
  }

  function timerExpired() {
    var time = now();
    if (shouldInvoke(time)) {
      return trailingEdge(time);
    }
    // Restart the timer.
    timerId = setTimeout(timerExpired, remainingWait(time));
  }

  function trailingEdge(time) {
    timerId = undefined;

    // Only invoke if we have `lastArgs` which means `func` has been
    // debounced at least once.
    if (trailing && lastArgs) {
      return invokeFunc(time);
    }
    lastArgs = lastThis = undefined;
    return result;
  }

  function cancel() {
    if (timerId !== undefined) {
      clearTimeout(timerId);
    }
    lastInvokeTime = 0;
    lastArgs = lastCallTime = lastThis = timerId = undefined;
  }

  function flush() {
    return timerId === undefined ? result : trailingEdge(now());
  }

  function debounced() {
    var time = now(),
        isInvoking = shouldInvoke(time);

    lastArgs = arguments;
    lastThis = this;
    lastCallTime = time;

    if (isInvoking) {
      if (timerId === undefined) {
        return leadingEdge(lastCallTime);
      }
      if (maxing) {
        // Handle invocations in a tight loop.
        timerId = setTimeout(timerExpired, wait);
        return invokeFunc(lastCallTime);
      }
    }
    if (timerId === undefined) {
      timerId = setTimeout(timerExpired, wait);
    }
    return result;
  }
  debounced.cancel = cancel;
  debounced.flush = flush;
  return debounced;
}

module.exports = debounce;


/***/ }),
/* 145 */
/***/ (function(module, exports, __webpack_require__) {

var freeGlobal = __webpack_require__(391);

/** Detect free variable `self`. */
var freeSelf = typeof self == 'object' && self && self.Object === Object && self;

/** Used as a reference to the global object. */
var root = freeGlobal || freeSelf || Function('return this')();

module.exports = root;


/***/ }),
/* 146 */
/***/ (function(module, exports, __webpack_require__) {

var root = __webpack_require__(145);

/** Built-in value references. */
var Symbol = root.Symbol;

module.exports = Symbol;


/***/ }),
/* 147 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _core = __webpack_require__(6);

var _default = __webpack_require__(105);

var _default2 = _interopRequireDefault(_default);

var _snap = __webpack_require__(399);

var _snap2 = _interopRequireDefault(_snap);

var _constants = __webpack_require__(23);

var _debounce = __webpack_require__(144);

var _debounce2 = _interopRequireDefault(_debounce);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var ContinuousViewManager = function (_DefaultViewManager) {
	_inherits(ContinuousViewManager, _DefaultViewManager);

	function ContinuousViewManager(options) {
		_classCallCheck(this, ContinuousViewManager);

		var _this = _possibleConstructorReturn(this, (ContinuousViewManager.__proto__ || Object.getPrototypeOf(ContinuousViewManager)).call(this, options));

		_this.name = "continuous";

		_this.settings = (0, _core.extend)(_this.settings || {}, {
			infinite: true,
			overflow: undefined,
			axis: undefined,
			flow: "scrolled",
			offset: 500,
			offsetDelta: 250,
			width: undefined,
			height: undefined,
			snap: false,
			afterScrolledTimeout: 10
		});

		(0, _core.extend)(_this.settings, options.settings || {});

		// Gap can be 0, but defaults doesn't handle that
		if (options.settings.gap != "undefined" && options.settings.gap === 0) {
			_this.settings.gap = options.settings.gap;
		}

		_this.viewSettings = {
			ignoreClass: _this.settings.ignoreClass,
			axis: _this.settings.axis,
			flow: _this.settings.flow,
			layout: _this.layout,
			width: 0,
			height: 0,
			forceEvenPages: false
		};

		_this.scrollTop = 0;
		_this.scrollLeft = 0;
		return _this;
	}

	_createClass(ContinuousViewManager, [{
		key: "display",
		value: function display(section, target) {
			return _default2.default.prototype.display.call(this, section, target).then(function () {
				return this.fill();
			}.bind(this));
		}
	}, {
		key: "fill",
		value: function fill(_full) {
			var _this2 = this;

			var full = _full || new _core.defer();

			this.q.enqueue(function () {
				return _this2.check();
			}).then(function (result) {
				if (result) {
					_this2.fill(full);
				} else {
					full.resolve();
				}
			});

			return full.promise;
		}
	}, {
		key: "moveTo",
		value: function moveTo(offset) {
			// var bounds = this.stage.bounds();
			// var dist = Math.floor(offset.top / bounds.height) * bounds.height;
			var distX = 0,
			    distY = 0;

			var offsetX = 0,
			    offsetY = 0;

			if (!this.isPaginated) {
				distY = offset.top;
				offsetY = offset.top + this.settings.offsetDelta;
			} else {
				distX = Math.floor(offset.left / this.layout.delta) * this.layout.delta;
				offsetX = distX + this.settings.offsetDelta;
			}

			if (distX > 0 || distY > 0) {
				this.scrollBy(distX, distY, true);
			}
		}
	}, {
		key: "afterResized",
		value: function afterResized(view) {
			this.emit(_constants.EVENTS.MANAGERS.RESIZE, view.section);
		}

		// Remove Previous Listeners if present

	}, {
		key: "removeShownListeners",
		value: function removeShownListeners(view) {

			// view.off("shown", this.afterDisplayed);
			// view.off("shown", this.afterDisplayedAbove);
			view.onDisplayed = function () {};
		}
	}, {
		key: "add",
		value: function add(section) {
			var _this3 = this;

			var view = this.createView(section);

			this.views.append(view);

			view.on(_constants.EVENTS.VIEWS.RESIZED, function (bounds) {
				view.expanded = true;
			});

			view.on(_constants.EVENTS.VIEWS.AXIS, function (axis) {
				_this3.updateAxis(axis);
			});

			// view.on(EVENTS.VIEWS.SHOWN, this.afterDisplayed.bind(this));
			view.onDisplayed = this.afterDisplayed.bind(this);
			view.onResize = this.afterResized.bind(this);

			return view.display(this.request);
		}
	}, {
		key: "append",
		value: function append(section) {
			var _this4 = this;

			var view = this.createView(section);

			view.on(_constants.EVENTS.VIEWS.RESIZED, function (bounds) {
				view.expanded = true;
			});

			view.on(_constants.EVENTS.VIEWS.AXIS, function (axis) {
				_this4.updateAxis(axis);
			});

			this.views.append(view);

			view.onDisplayed = this.afterDisplayed.bind(this);

			return view;
		}
	}, {
		key: "prepend",
		value: function prepend(section) {
			var _this5 = this;

			var view = this.createView(section);

			view.on(_constants.EVENTS.VIEWS.RESIZED, function (bounds) {
				_this5.counter(bounds);
				view.expanded = true;
			});

			view.on(_constants.EVENTS.VIEWS.AXIS, function (axis) {
				_this5.updateAxis(axis);
			});

			this.views.prepend(view);

			view.onDisplayed = this.afterDisplayed.bind(this);

			return view;
		}
	}, {
		key: "counter",
		value: function counter(bounds) {
			if (this.settings.axis === "vertical") {
				this.scrollBy(0, bounds.heightDelta, true);
			} else {
				this.scrollBy(bounds.widthDelta, 0, true);
			}
		}
	}, {
		key: "update",
		value: function update(_offset) {
			var container = this.bounds();
			var views = this.views.all();
			var viewsLength = views.length;
			var visible = [];
			var offset = typeof _offset != "undefined" ? _offset : this.settings.offset || 0;
			var isVisible;
			var view;

			var updating = new _core.defer();
			var promises = [];
			for (var i = 0; i < viewsLength; i++) {
				view = views[i];

				isVisible = this.isVisible(view, offset, offset, container);

				if (isVisible === true) {
					// console.log("visible " + view.index);

					if (!view.displayed) {
						var displayed = view.display(this.request).then(function (view) {
							view.show();
						}, function (err) {
							view.hide();
						});
						promises.push(displayed);
					} else {
						view.show();
					}
					visible.push(view);
				} else {
					this.q.enqueue(view.destroy.bind(view));
					// console.log("hidden " + view.index);

					clearTimeout(this.trimTimeout);
					this.trimTimeout = setTimeout(function () {
						this.q.enqueue(this.trim.bind(this));
					}.bind(this), 250);
				}
			}

			if (promises.length) {
				return Promise.all(promises).catch(function (err) {
					updating.reject(err);
				});
			} else {
				updating.resolve();
				return updating.promise;
			}
		}
	}, {
		key: "check",
		value: function check(_offsetLeft, _offsetTop) {
			var _this6 = this;

			var checking = new _core.defer();
			var newViews = [];

			var horizontal = this.settings.axis === "horizontal";
			var delta = this.settings.offset || 0;

			if (_offsetLeft && horizontal) {
				delta = _offsetLeft;
			}

			if (_offsetTop && !horizontal) {
				delta = _offsetTop;
			}

			var bounds = this._bounds; // bounds saved this until resize

			var rtl = this.settings.direction === "rtl";
			var dir = horizontal && rtl ? -1 : 1; //RTL reverses scrollTop

			var offset = horizontal ? this.scrollLeft : this.scrollTop * dir;
			var visibleLength = horizontal ? Math.floor(bounds.width) : bounds.height;
			var contentLength = horizontal ? this.container.scrollWidth : this.container.scrollHeight;

			var prepend = function prepend() {
				var first = _this6.views.first();
				var prev = first && first.section.prev();

				if (prev) {
					newViews.push(_this6.prepend(prev));
				}
			};

			var append = function append() {
				var last = _this6.views.last();
				var next = last && last.section.next();

				if (next) {
					newViews.push(_this6.append(next));
				}
			};

			if (offset + visibleLength + delta >= contentLength) {
				if (horizontal && rtl) {
					prepend();
				} else {
					append();
				}
			}

			if (offset - delta < 0) {
				if (horizontal && rtl) {
					append();
				} else {
					prepend();
				}
			}

			var promises = newViews.map(function (view) {
				return view.displayed;
			});

			if (newViews.length) {
				return Promise.all(promises).then(function () {
					if (_this6.layout.name === "pre-paginated" && _this6.layout.props.spread) {
						return _this6.check();
					}
				}).then(function () {
					// Check to see if anything new is on screen after rendering
					return _this6.update(delta);
				}, function (err) {
					return err;
				});
			} else {
				this.q.enqueue(function () {
					this.update();
				}.bind(this));
				checking.resolve(false);
				return checking.promise;
			}
		}
	}, {
		key: "trim",
		value: function trim() {
			var task = new _core.defer();
			var displayed = this.views.displayed();
			var first = displayed[0];
			var last = displayed[displayed.length - 1];
			var firstIndex = this.views.indexOf(first);
			var lastIndex = this.views.indexOf(last);
			var above = this.views.slice(0, firstIndex);
			var below = this.views.slice(lastIndex + 1);

			// Erase all but last above
			for (var i = 0; i < above.length - 1; i++) {
				this.erase(above[i], above);
			}

			// Erase all except first below
			for (var j = 1; j < below.length; j++) {
				this.erase(below[j]);
			}

			task.resolve();
			return task.promise;
		}
	}, {
		key: "erase",
		value: function erase(view, above) {
			//Trim

			var prevTop;
			var prevLeft;

			if (!this.settings.fullsize) {
				prevTop = this.container.scrollTop;
				prevLeft = this.container.scrollLeft;
			} else {
				prevTop = window.scrollY;
				prevLeft = window.scrollX;
			}

			var bounds = view.bounds();

			this.views.remove(view);

			if (above) {
				if (this.settings.axis === "vertical") {
					this.scrollTo(0, prevTop - bounds.height, true);
				} else {
					this.scrollTo(prevLeft - Math.floor(bounds.width), 0, true);
				}
			}
		}
	}, {
		key: "addEventListeners",
		value: function addEventListeners(stage) {

			window.addEventListener("unload", function (e) {
				this.ignore = true;
				// this.scrollTo(0,0);
				this.destroy();
			}.bind(this));

			this.addScrollListeners();

			if (this.isPaginated && this.settings.snap) {
				this.snapper = new _snap2.default(this, this.settings.snap && _typeof(this.settings.snap) === "object" && this.settings.snap);
			}
		}
	}, {
		key: "addScrollListeners",
		value: function addScrollListeners() {
			var scroller;

			this.tick = _core.requestAnimationFrame;

			if (!this.settings.fullsize) {
				this.prevScrollTop = this.container.scrollTop;
				this.prevScrollLeft = this.container.scrollLeft;
			} else {
				this.prevScrollTop = window.scrollY;
				this.prevScrollLeft = window.scrollX;
			}

			this.scrollDeltaVert = 0;
			this.scrollDeltaHorz = 0;

			if (!this.settings.fullsize) {
				scroller = this.container;
				this.scrollTop = this.container.scrollTop;
				this.scrollLeft = this.container.scrollLeft;
			} else {
				scroller = window;
				this.scrollTop = window.scrollY;
				this.scrollLeft = window.scrollX;
			}

			this._onScroll = this.onScroll.bind(this);
			scroller.addEventListener("scroll", this._onScroll);
			this._scrolled = (0, _debounce2.default)(this.scrolled.bind(this), 30);
			// this.tick.call(window, this.onScroll.bind(this));

			this.didScroll = false;
		}
	}, {
		key: "removeEventListeners",
		value: function removeEventListeners() {
			var scroller;

			if (!this.settings.fullsize) {
				scroller = this.container;
			} else {
				scroller = window;
			}

			scroller.removeEventListener("scroll", this._onScroll);
			this._onScroll = undefined;
		}
	}, {
		key: "onScroll",
		value: function onScroll() {
			var scrollTop = void 0;
			var scrollLeft = void 0;
			var dir = this.settings.direction === "rtl" ? -1 : 1;

			if (!this.settings.fullsize) {
				scrollTop = this.container.scrollTop;
				scrollLeft = this.container.scrollLeft;
			} else {
				scrollTop = window.scrollY * dir;
				scrollLeft = window.scrollX * dir;
			}

			this.scrollTop = scrollTop;
			this.scrollLeft = scrollLeft;

			if (!this.ignore) {

				this._scrolled();
			} else {
				this.ignore = false;
			}

			this.scrollDeltaVert += Math.abs(scrollTop - this.prevScrollTop);
			this.scrollDeltaHorz += Math.abs(scrollLeft - this.prevScrollLeft);

			this.prevScrollTop = scrollTop;
			this.prevScrollLeft = scrollLeft;

			clearTimeout(this.scrollTimeout);
			this.scrollTimeout = setTimeout(function () {
				this.scrollDeltaVert = 0;
				this.scrollDeltaHorz = 0;
			}.bind(this), 150);

			clearTimeout(this.afterScrolled);

			this.didScroll = false;
		}
	}, {
		key: "scrolled",
		value: function scrolled() {

			this.q.enqueue(function () {
				this.check();
			}.bind(this));

			this.emit(_constants.EVENTS.MANAGERS.SCROLL, {
				top: this.scrollTop,
				left: this.scrollLeft
			});

			clearTimeout(this.afterScrolled);
			this.afterScrolled = setTimeout(function () {

				// Don't report scroll if we are about the snap
				if (this.snapper && this.snapper.supportsTouch && this.snapper.needsSnap()) {
					return;
				}

				this.emit(_constants.EVENTS.MANAGERS.SCROLLED, {
					top: this.scrollTop,
					left: this.scrollLeft
				});
			}.bind(this), this.settings.afterScrolledTimeout);
		}
	}, {
		key: "next",
		value: function next() {

			var dir = this.settings.direction;
			var delta = this.layout.props.name === "pre-paginated" && this.layout.props.spread ? this.layout.props.delta * 2 : this.layout.props.delta;

			if (!this.views.length) return;

			if (this.isPaginated && this.settings.axis === "horizontal") {

				this.scrollBy(delta, 0, true);
			} else {

				this.scrollBy(0, this.layout.height, true);
			}

			this.q.enqueue(function () {
				this.check();
			}.bind(this));
		}
	}, {
		key: "prev",
		value: function prev() {

			var dir = this.settings.direction;
			var delta = this.layout.props.name === "pre-paginated" && this.layout.props.spread ? this.layout.props.delta * 2 : this.layout.props.delta;

			if (!this.views.length) return;

			if (this.isPaginated && this.settings.axis === "horizontal") {

				this.scrollBy(-delta, 0, true);
			} else {

				this.scrollBy(0, -this.layout.height, true);
			}

			this.q.enqueue(function () {
				this.check();
			}.bind(this));
		}

		// updateAxis(axis, forceUpdate){
		//
		// 	super.updateAxis(axis, forceUpdate);
		//
		// 	if (axis === "vertical") {
		// 		this.settings.infinite = true;
		// 	} else {
		// 		this.settings.infinite = false;
		// 	}
		// }

	}, {
		key: "updateFlow",
		value: function updateFlow(flow) {
			if (this.rendered && this.snapper) {
				this.snapper.destroy();
				this.snapper = undefined;
			}

			_get(ContinuousViewManager.prototype.__proto__ || Object.getPrototypeOf(ContinuousViewManager.prototype), "updateFlow", this).call(this, flow, "scroll");

			if (this.rendered && this.isPaginated && this.settings.snap) {
				this.snapper = new _snap2.default(this, this.settings.snap && _typeof(this.settings.snap) === "object" && this.settings.snap);
			}
		}
	}, {
		key: "destroy",
		value: function destroy() {
			_get(ContinuousViewManager.prototype.__proto__ || Object.getPrototypeOf(ContinuousViewManager.prototype), "destroy", this).call(this);

			if (this.snapper) {
				this.snapper.destroy();
			}
		}
	}]);

	return ContinuousViewManager;
}(_default2.default);

exports.default = ContinuousViewManager;
module.exports = exports["default"];

/***/ }),
/* 148 */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(149);
module.exports = __webpack_require__(354);


/***/ }),
/* 149 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(global) {

__webpack_require__(150);

__webpack_require__(350);

__webpack_require__(351);

if (global._babelPolyfill) {
  throw new Error("only one instance of babel-polyfill is allowed");
}
global._babelPolyfill = true;

var DEFINE_PROPERTY = "defineProperty";
function define(O, key, value) {
  O[key] || Object[DEFINE_PROPERTY](O, key, {
    writable: true,
    configurable: true,
    value: value
  });
}

define(String.prototype, "padLeft", "".padStart);
define(String.prototype, "padRight", "".padEnd);

"pop,reverse,shift,keys,values,entries,indexOf,every,some,forEach,map,filter,find,findIndex,includes,join,slice,concat,push,splice,unshift,sort,lastIndexOf,reduce,reduceRight,copyWithin,fill".split(",").forEach(function (key) {
  [][key] && define(Array, key, Function.call.bind([][key]));
});
/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(47)))

/***/ }),
/* 150 */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(151);
__webpack_require__(154);
__webpack_require__(155);
__webpack_require__(156);
__webpack_require__(157);
__webpack_require__(158);
__webpack_require__(159);
__webpack_require__(160);
__webpack_require__(161);
__webpack_require__(162);
__webpack_require__(163);
__webpack_require__(164);
__webpack_require__(165);
__webpack_require__(166);
__webpack_require__(167);
__webpack_require__(168);
__webpack_require__(170);
__webpack_require__(171);
__webpack_require__(172);
__webpack_require__(173);
__webpack_require__(174);
__webpack_require__(175);
__webpack_require__(176);
__webpack_require__(177);
__webpack_require__(178);
__webpack_require__(179);
__webpack_require__(180);
__webpack_require__(181);
__webpack_require__(182);
__webpack_require__(183);
__webpack_require__(184);
__webpack_require__(185);
__webpack_require__(186);
__webpack_require__(187);
__webpack_require__(188);
__webpack_require__(189);
__webpack_require__(190);
__webpack_require__(191);
__webpack_require__(192);
__webpack_require__(193);
__webpack_require__(194);
__webpack_require__(195);
__webpack_require__(196);
__webpack_require__(197);
__webpack_require__(198);
__webpack_require__(199);
__webpack_require__(200);
__webpack_require__(201);
__webpack_require__(202);
__webpack_require__(203);
__webpack_require__(204);
__webpack_require__(205);
__webpack_require__(206);
__webpack_require__(207);
__webpack_require__(208);
__webpack_require__(209);
__webpack_require__(210);
__webpack_require__(211);
__webpack_require__(212);
__webpack_require__(213);
__webpack_require__(214);
__webpack_require__(215);
__webpack_require__(216);
__webpack_require__(217);
__webpack_require__(218);
__webpack_require__(219);
__webpack_require__(220);
__webpack_require__(221);
__webpack_require__(222);
__webpack_require__(223);
__webpack_require__(224);
__webpack_require__(225);
__webpack_require__(226);
__webpack_require__(227);
__webpack_require__(228);
__webpack_require__(229);
__webpack_require__(230);
__webpack_require__(232);
__webpack_require__(233);
__webpack_require__(235);
__webpack_require__(236);
__webpack_require__(237);
__webpack_require__(238);
__webpack_require__(239);
__webpack_require__(240);
__webpack_require__(241);
__webpack_require__(243);
__webpack_require__(244);
__webpack_require__(245);
__webpack_require__(246);
__webpack_require__(247);
__webpack_require__(248);
__webpack_require__(249);
__webpack_require__(250);
__webpack_require__(251);
__webpack_require__(252);
__webpack_require__(253);
__webpack_require__(254);
__webpack_require__(255);
__webpack_require__(95);
__webpack_require__(256);
__webpack_require__(257);
__webpack_require__(124);
__webpack_require__(258);
__webpack_require__(259);
__webpack_require__(260);
__webpack_require__(261);
__webpack_require__(262);
__webpack_require__(127);
__webpack_require__(129);
__webpack_require__(130);
__webpack_require__(263);
__webpack_require__(264);
__webpack_require__(265);
__webpack_require__(266);
__webpack_require__(267);
__webpack_require__(268);
__webpack_require__(269);
__webpack_require__(270);
__webpack_require__(271);
__webpack_require__(272);
__webpack_require__(273);
__webpack_require__(274);
__webpack_require__(275);
__webpack_require__(276);
__webpack_require__(277);
__webpack_require__(278);
__webpack_require__(279);
__webpack_require__(280);
__webpack_require__(281);
__webpack_require__(282);
__webpack_require__(283);
__webpack_require__(284);
__webpack_require__(285);
__webpack_require__(286);
__webpack_require__(287);
__webpack_require__(288);
__webpack_require__(289);
__webpack_require__(290);
__webpack_require__(291);
__webpack_require__(292);
__webpack_require__(293);
__webpack_require__(294);
__webpack_require__(295);
__webpack_require__(296);
__webpack_require__(297);
__webpack_require__(298);
__webpack_require__(299);
__webpack_require__(300);
__webpack_require__(301);
__webpack_require__(302);
__webpack_require__(303);
__webpack_require__(304);
__webpack_require__(305);
__webpack_require__(306);
__webpack_require__(307);
__webpack_require__(308);
__webpack_require__(309);
__webpack_require__(310);
__webpack_require__(311);
__webpack_require__(312);
__webpack_require__(313);
__webpack_require__(314);
__webpack_require__(315);
__webpack_require__(316);
__webpack_require__(317);
__webpack_require__(318);
__webpack_require__(319);
__webpack_require__(320);
__webpack_require__(321);
__webpack_require__(322);
__webpack_require__(323);
__webpack_require__(324);
__webpack_require__(325);
__webpack_require__(326);
__webpack_require__(327);
__webpack_require__(328);
__webpack_require__(329);
__webpack_require__(330);
__webpack_require__(331);
__webpack_require__(332);
__webpack_require__(333);
__webpack_require__(334);
__webpack_require__(335);
__webpack_require__(336);
__webpack_require__(337);
__webpack_require__(338);
__webpack_require__(339);
__webpack_require__(340);
__webpack_require__(341);
__webpack_require__(342);
__webpack_require__(343);
__webpack_require__(344);
__webpack_require__(345);
__webpack_require__(348);
__webpack_require__(349);
module.exports = __webpack_require__(24);


/***/ }),
/* 151 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// ECMAScript 6 symbols shim
var global = __webpack_require__(2);
var has = __webpack_require__(12);
var DESCRIPTORS = __webpack_require__(7);
var $export = __webpack_require__(0);
var redefine = __webpack_require__(14);
var META = __webpack_require__(33).KEY;
var $fails = __webpack_require__(3);
var shared = __webpack_require__(55);
var setToStringTag = __webpack_require__(48);
var uid = __webpack_require__(37);
var wks = __webpack_require__(5);
var wksExt = __webpack_require__(108);
var wksDefine = __webpack_require__(75);
var keyOf = __webpack_require__(152);
var enumKeys = __webpack_require__(153);
var isArray = __webpack_require__(58);
var anObject = __webpack_require__(1);
var toIObject = __webpack_require__(15);
var toPrimitive = __webpack_require__(25);
var createDesc = __webpack_require__(36);
var _create = __webpack_require__(40);
var gOPNExt = __webpack_require__(111);
var $GOPD = __webpack_require__(17);
var $DP = __webpack_require__(8);
var $keys = __webpack_require__(34);
var gOPD = $GOPD.f;
var dP = $DP.f;
var gOPN = gOPNExt.f;
var $Symbol = global.Symbol;
var $JSON = global.JSON;
var _stringify = $JSON && $JSON.stringify;
var PROTOTYPE = 'prototype';
var HIDDEN = wks('_hidden');
var TO_PRIMITIVE = wks('toPrimitive');
var isEnum = {}.propertyIsEnumerable;
var SymbolRegistry = shared('symbol-registry');
var AllSymbols = shared('symbols');
var OPSymbols = shared('op-symbols');
var ObjectProto = Object[PROTOTYPE];
var USE_NATIVE = typeof $Symbol == 'function';
var QObject = global.QObject;
// Don't use setters in Qt Script, https://github.com/zloirock/core-js/issues/173
var setter = !QObject || !QObject[PROTOTYPE] || !QObject[PROTOTYPE].findChild;

// fallback for old Android, https://code.google.com/p/v8/issues/detail?id=687
var setSymbolDesc = DESCRIPTORS && $fails(function () {
  return _create(dP({}, 'a', {
    get: function () { return dP(this, 'a', { value: 7 }).a; }
  })).a != 7;
}) ? function (it, key, D) {
  var protoDesc = gOPD(ObjectProto, key);
  if (protoDesc) delete ObjectProto[key];
  dP(it, key, D);
  if (protoDesc && it !== ObjectProto) dP(ObjectProto, key, protoDesc);
} : dP;

var wrap = function (tag) {
  var sym = AllSymbols[tag] = _create($Symbol[PROTOTYPE]);
  sym._k = tag;
  return sym;
};

var isSymbol = USE_NATIVE && typeof $Symbol.iterator == 'symbol' ? function (it) {
  return typeof it == 'symbol';
} : function (it) {
  return it instanceof $Symbol;
};

var $defineProperty = function defineProperty(it, key, D) {
  if (it === ObjectProto) $defineProperty(OPSymbols, key, D);
  anObject(it);
  key = toPrimitive(key, true);
  anObject(D);
  if (has(AllSymbols, key)) {
    if (!D.enumerable) {
      if (!has(it, HIDDEN)) dP(it, HIDDEN, createDesc(1, {}));
      it[HIDDEN][key] = true;
    } else {
      if (has(it, HIDDEN) && it[HIDDEN][key]) it[HIDDEN][key] = false;
      D = _create(D, { enumerable: createDesc(0, false) });
    } return setSymbolDesc(it, key, D);
  } return dP(it, key, D);
};
var $defineProperties = function defineProperties(it, P) {
  anObject(it);
  var keys = enumKeys(P = toIObject(P));
  var i = 0;
  var l = keys.length;
  var key;
  while (l > i) $defineProperty(it, key = keys[i++], P[key]);
  return it;
};
var $create = function create(it, P) {
  return P === undefined ? _create(it) : $defineProperties(_create(it), P);
};
var $propertyIsEnumerable = function propertyIsEnumerable(key) {
  var E = isEnum.call(this, key = toPrimitive(key, true));
  if (this === ObjectProto && has(AllSymbols, key) && !has(OPSymbols, key)) return false;
  return E || !has(this, key) || !has(AllSymbols, key) || has(this, HIDDEN) && this[HIDDEN][key] ? E : true;
};
var $getOwnPropertyDescriptor = function getOwnPropertyDescriptor(it, key) {
  it = toIObject(it);
  key = toPrimitive(key, true);
  if (it === ObjectProto && has(AllSymbols, key) && !has(OPSymbols, key)) return;
  var D = gOPD(it, key);
  if (D && has(AllSymbols, key) && !(has(it, HIDDEN) && it[HIDDEN][key])) D.enumerable = true;
  return D;
};
var $getOwnPropertyNames = function getOwnPropertyNames(it) {
  var names = gOPN(toIObject(it));
  var result = [];
  var i = 0;
  var key;
  while (names.length > i) {
    if (!has(AllSymbols, key = names[i++]) && key != HIDDEN && key != META) result.push(key);
  } return result;
};
var $getOwnPropertySymbols = function getOwnPropertySymbols(it) {
  var IS_OP = it === ObjectProto;
  var names = gOPN(IS_OP ? OPSymbols : toIObject(it));
  var result = [];
  var i = 0;
  var key;
  while (names.length > i) {
    if (has(AllSymbols, key = names[i++]) && (IS_OP ? has(ObjectProto, key) : true)) result.push(AllSymbols[key]);
  } return result;
};

// 19.4.1.1 Symbol([description])
if (!USE_NATIVE) {
  $Symbol = function Symbol() {
    if (this instanceof $Symbol) throw TypeError('Symbol is not a constructor!');
    var tag = uid(arguments.length > 0 ? arguments[0] : undefined);
    var $set = function (value) {
      if (this === ObjectProto) $set.call(OPSymbols, value);
      if (has(this, HIDDEN) && has(this[HIDDEN], tag)) this[HIDDEN][tag] = false;
      setSymbolDesc(this, tag, createDesc(1, value));
    };
    if (DESCRIPTORS && setter) setSymbolDesc(ObjectProto, tag, { configurable: true, set: $set });
    return wrap(tag);
  };
  redefine($Symbol[PROTOTYPE], 'toString', function toString() {
    return this._k;
  });

  $GOPD.f = $getOwnPropertyDescriptor;
  $DP.f = $defineProperty;
  __webpack_require__(41).f = gOPNExt.f = $getOwnPropertyNames;
  __webpack_require__(53).f = $propertyIsEnumerable;
  __webpack_require__(57).f = $getOwnPropertySymbols;

  if (DESCRIPTORS && !__webpack_require__(38)) {
    redefine(ObjectProto, 'propertyIsEnumerable', $propertyIsEnumerable, true);
  }

  wksExt.f = function (name) {
    return wrap(wks(name));
  };
}

$export($export.G + $export.W + $export.F * !USE_NATIVE, { Symbol: $Symbol });

for (var es6Symbols = (
  // 19.4.2.2, 19.4.2.3, 19.4.2.4, 19.4.2.6, 19.4.2.8, 19.4.2.9, 19.4.2.10, 19.4.2.11, 19.4.2.12, 19.4.2.13, 19.4.2.14
  'hasInstance,isConcatSpreadable,iterator,match,replace,search,species,split,toPrimitive,toStringTag,unscopables'
).split(','), j = 0; es6Symbols.length > j;)wks(es6Symbols[j++]);

for (var wellKnownSymbols = $keys(wks.store), k = 0; wellKnownSymbols.length > k;) wksDefine(wellKnownSymbols[k++]);

$export($export.S + $export.F * !USE_NATIVE, 'Symbol', {
  // 19.4.2.1 Symbol.for(key)
  'for': function (key) {
    return has(SymbolRegistry, key += '')
      ? SymbolRegistry[key]
      : SymbolRegistry[key] = $Symbol(key);
  },
  // 19.4.2.5 Symbol.keyFor(sym)
  keyFor: function keyFor(key) {
    if (isSymbol(key)) return keyOf(SymbolRegistry, key);
    throw TypeError(key + ' is not a symbol!');
  },
  useSetter: function () { setter = true; },
  useSimple: function () { setter = false; }
});

$export($export.S + $export.F * !USE_NATIVE, 'Object', {
  // 19.1.2.2 Object.create(O [, Properties])
  create: $create,
  // 19.1.2.4 Object.defineProperty(O, P, Attributes)
  defineProperty: $defineProperty,
  // 19.1.2.3 Object.defineProperties(O, Properties)
  defineProperties: $defineProperties,
  // 19.1.2.6 Object.getOwnPropertyDescriptor(O, P)
  getOwnPropertyDescriptor: $getOwnPropertyDescriptor,
  // 19.1.2.7 Object.getOwnPropertyNames(O)
  getOwnPropertyNames: $getOwnPropertyNames,
  // 19.1.2.8 Object.getOwnPropertySymbols(O)
  getOwnPropertySymbols: $getOwnPropertySymbols
});

// 24.3.2 JSON.stringify(value [, replacer [, space]])
$JSON && $export($export.S + $export.F * (!USE_NATIVE || $fails(function () {
  var S = $Symbol();
  // MS Edge converts symbol values to JSON as {}
  // WebKit converts symbol values to JSON as null
  // V8 throws on boxed symbols
  return _stringify([S]) != '[null]' || _stringify({ a: S }) != '{}' || _stringify(Object(S)) != '{}';
})), 'JSON', {
  stringify: function stringify(it) {
    if (it === undefined || isSymbol(it)) return; // IE8 returns string on undefined
    var args = [it];
    var i = 1;
    var replacer, $replacer;
    while (arguments.length > i) args.push(arguments[i++]);
    replacer = args[1];
    if (typeof replacer == 'function') $replacer = replacer;
    if ($replacer || !isArray(replacer)) replacer = function (key, value) {
      if ($replacer) value = $replacer.call(this, key, value);
      if (!isSymbol(value)) return value;
    };
    args[1] = replacer;
    return _stringify.apply($JSON, args);
  }
});

// 19.4.3.4 Symbol.prototype[@@toPrimitive](hint)
$Symbol[PROTOTYPE][TO_PRIMITIVE] || __webpack_require__(13)($Symbol[PROTOTYPE], TO_PRIMITIVE, $Symbol[PROTOTYPE].valueOf);
// 19.4.3.5 Symbol.prototype[@@toStringTag]
setToStringTag($Symbol, 'Symbol');
// 20.2.1.9 Math[@@toStringTag]
setToStringTag(Math, 'Math', true);
// 24.3.3 JSON[@@toStringTag]
setToStringTag(global.JSON, 'JSON', true);


/***/ }),
/* 152 */
/***/ (function(module, exports, __webpack_require__) {

var getKeys = __webpack_require__(34);
var toIObject = __webpack_require__(15);
module.exports = function (object, el) {
  var O = toIObject(object);
  var keys = getKeys(O);
  var length = keys.length;
  var index = 0;
  var key;
  while (length > index) if (O[key = keys[index++]] === el) return key;
};


/***/ }),
/* 153 */
/***/ (function(module, exports, __webpack_require__) {

// all enumerable object keys, includes symbols
var getKeys = __webpack_require__(34);
var gOPS = __webpack_require__(57);
var pIE = __webpack_require__(53);
module.exports = function (it) {
  var result = getKeys(it);
  var getSymbols = gOPS.f;
  if (getSymbols) {
    var symbols = getSymbols(it);
    var isEnum = pIE.f;
    var i = 0;
    var key;
    while (symbols.length > i) if (isEnum.call(it, key = symbols[i++])) result.push(key);
  } return result;
};


/***/ }),
/* 154 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(0);
// 19.1.2.2 / 15.2.3.5 Object.create(O [, Properties])
$export($export.S, 'Object', { create: __webpack_require__(40) });


/***/ }),
/* 155 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(0);
// 19.1.2.4 / 15.2.3.6 Object.defineProperty(O, P, Attributes)
$export($export.S + $export.F * !__webpack_require__(7), 'Object', { defineProperty: __webpack_require__(8).f });


/***/ }),
/* 156 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(0);
// 19.1.2.3 / 15.2.3.7 Object.defineProperties(O, Properties)
$export($export.S + $export.F * !__webpack_require__(7), 'Object', { defineProperties: __webpack_require__(110) });


/***/ }),
/* 157 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.6 Object.getOwnPropertyDescriptor(O, P)
var toIObject = __webpack_require__(15);
var $getOwnPropertyDescriptor = __webpack_require__(17).f;

__webpack_require__(28)('getOwnPropertyDescriptor', function () {
  return function getOwnPropertyDescriptor(it, key) {
    return $getOwnPropertyDescriptor(toIObject(it), key);
  };
});


/***/ }),
/* 158 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.9 Object.getPrototypeOf(O)
var toObject = __webpack_require__(10);
var $getPrototypeOf = __webpack_require__(18);

__webpack_require__(28)('getPrototypeOf', function () {
  return function getPrototypeOf(it) {
    return $getPrototypeOf(toObject(it));
  };
});


/***/ }),
/* 159 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.14 Object.keys(O)
var toObject = __webpack_require__(10);
var $keys = __webpack_require__(34);

__webpack_require__(28)('keys', function () {
  return function keys(it) {
    return $keys(toObject(it));
  };
});


/***/ }),
/* 160 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.7 Object.getOwnPropertyNames(O)
__webpack_require__(28)('getOwnPropertyNames', function () {
  return __webpack_require__(111).f;
});


/***/ }),
/* 161 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.5 Object.freeze(O)
var isObject = __webpack_require__(4);
var meta = __webpack_require__(33).onFreeze;

__webpack_require__(28)('freeze', function ($freeze) {
  return function freeze(it) {
    return $freeze && isObject(it) ? $freeze(meta(it)) : it;
  };
});


/***/ }),
/* 162 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.17 Object.seal(O)
var isObject = __webpack_require__(4);
var meta = __webpack_require__(33).onFreeze;

__webpack_require__(28)('seal', function ($seal) {
  return function seal(it) {
    return $seal && isObject(it) ? $seal(meta(it)) : it;
  };
});


/***/ }),
/* 163 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.15 Object.preventExtensions(O)
var isObject = __webpack_require__(4);
var meta = __webpack_require__(33).onFreeze;

__webpack_require__(28)('preventExtensions', function ($preventExtensions) {
  return function preventExtensions(it) {
    return $preventExtensions && isObject(it) ? $preventExtensions(meta(it)) : it;
  };
});


/***/ }),
/* 164 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.12 Object.isFrozen(O)
var isObject = __webpack_require__(4);

__webpack_require__(28)('isFrozen', function ($isFrozen) {
  return function isFrozen(it) {
    return isObject(it) ? $isFrozen ? $isFrozen(it) : false : true;
  };
});


/***/ }),
/* 165 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.13 Object.isSealed(O)
var isObject = __webpack_require__(4);

__webpack_require__(28)('isSealed', function ($isSealed) {
  return function isSealed(it) {
    return isObject(it) ? $isSealed ? $isSealed(it) : false : true;
  };
});


/***/ }),
/* 166 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.11 Object.isExtensible(O)
var isObject = __webpack_require__(4);

__webpack_require__(28)('isExtensible', function ($isExtensible) {
  return function isExtensible(it) {
    return isObject(it) ? $isExtensible ? $isExtensible(it) : true : false;
  };
});


/***/ }),
/* 167 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.3.1 Object.assign(target, source)
var $export = __webpack_require__(0);

$export($export.S + $export.F, 'Object', { assign: __webpack_require__(112) });


/***/ }),
/* 168 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.3.10 Object.is(value1, value2)
var $export = __webpack_require__(0);
$export($export.S, 'Object', { is: __webpack_require__(169) });


/***/ }),
/* 169 */
/***/ (function(module, exports) {

// 7.2.9 SameValue(x, y)
module.exports = Object.is || function is(x, y) {
  // eslint-disable-next-line no-self-compare
  return x === y ? x !== 0 || 1 / x === 1 / y : x != x && y != y;
};


/***/ }),
/* 170 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.3.19 Object.setPrototypeOf(O, proto)
var $export = __webpack_require__(0);
$export($export.S, 'Object', { setPrototypeOf: __webpack_require__(79).set });


/***/ }),
/* 171 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// 19.1.3.6 Object.prototype.toString()
var classof = __webpack_require__(54);
var test = {};
test[__webpack_require__(5)('toStringTag')] = 'z';
if (test + '' != '[object z]') {
  __webpack_require__(14)(Object.prototype, 'toString', function toString() {
    return '[object ' + classof(this) + ']';
  }, true);
}


/***/ }),
/* 172 */
/***/ (function(module, exports, __webpack_require__) {

// 19.2.3.2 / 15.3.4.5 Function.prototype.bind(thisArg, args...)
var $export = __webpack_require__(0);

$export($export.P, 'Function', { bind: __webpack_require__(113) });


/***/ }),
/* 173 */
/***/ (function(module, exports, __webpack_require__) {

var dP = __webpack_require__(8).f;
var FProto = Function.prototype;
var nameRE = /^\s*function ([^ (]*)/;
var NAME = 'name';

// 19.2.4.2 name
NAME in FProto || __webpack_require__(7) && dP(FProto, NAME, {
  configurable: true,
  get: function () {
    try {
      return ('' + this).match(nameRE)[1];
    } catch (e) {
      return '';
    }
  }
});


/***/ }),
/* 174 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var isObject = __webpack_require__(4);
var getPrototypeOf = __webpack_require__(18);
var HAS_INSTANCE = __webpack_require__(5)('hasInstance');
var FunctionProto = Function.prototype;
// 19.2.3.6 Function.prototype[@@hasInstance](V)
if (!(HAS_INSTANCE in FunctionProto)) __webpack_require__(8).f(FunctionProto, HAS_INSTANCE, { value: function (O) {
  if (typeof this != 'function' || !isObject(O)) return false;
  if (!isObject(this.prototype)) return O instanceof this;
  // for environment w/o native `@@hasInstance` logic enough `instanceof`, but add this:
  while (O = getPrototypeOf(O)) if (this.prototype === O) return true;
  return false;
} });


/***/ }),
/* 175 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(0);
var $parseInt = __webpack_require__(114);
// 18.2.5 parseInt(string, radix)
$export($export.G + $export.F * (parseInt != $parseInt), { parseInt: $parseInt });


/***/ }),
/* 176 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(0);
var $parseFloat = __webpack_require__(115);
// 18.2.4 parseFloat(string)
$export($export.G + $export.F * (parseFloat != $parseFloat), { parseFloat: $parseFloat });


/***/ }),
/* 177 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var global = __webpack_require__(2);
var has = __webpack_require__(12);
var cof = __webpack_require__(20);
var inheritIfRequired = __webpack_require__(81);
var toPrimitive = __webpack_require__(25);
var fails = __webpack_require__(3);
var gOPN = __webpack_require__(41).f;
var gOPD = __webpack_require__(17).f;
var dP = __webpack_require__(8).f;
var $trim = __webpack_require__(49).trim;
var NUMBER = 'Number';
var $Number = global[NUMBER];
var Base = $Number;
var proto = $Number.prototype;
// Opera ~12 has broken Object#toString
var BROKEN_COF = cof(__webpack_require__(40)(proto)) == NUMBER;
var TRIM = 'trim' in String.prototype;

// 7.1.3 ToNumber(argument)
var toNumber = function (argument) {
  var it = toPrimitive(argument, false);
  if (typeof it == 'string' && it.length > 2) {
    it = TRIM ? it.trim() : $trim(it, 3);
    var first = it.charCodeAt(0);
    var third, radix, maxCode;
    if (first === 43 || first === 45) {
      third = it.charCodeAt(2);
      if (third === 88 || third === 120) return NaN; // Number('+0x1') should be NaN, old V8 fix
    } else if (first === 48) {
      switch (it.charCodeAt(1)) {
        case 66: case 98: radix = 2; maxCode = 49; break; // fast equal /^0b[01]+$/i
        case 79: case 111: radix = 8; maxCode = 55; break; // fast equal /^0o[0-7]+$/i
        default: return +it;
      }
      for (var digits = it.slice(2), i = 0, l = digits.length, code; i < l; i++) {
        code = digits.charCodeAt(i);
        // parseInt parses a string to a first unavailable symbol
        // but ToNumber should return NaN if a string contains unavailable symbols
        if (code < 48 || code > maxCode) return NaN;
      } return parseInt(digits, radix);
    }
  } return +it;
};

if (!$Number(' 0o1') || !$Number('0b1') || $Number('+0x1')) {
  $Number = function Number(value) {
    var it = arguments.length < 1 ? 0 : value;
    var that = this;
    return that instanceof $Number
      // check on 1..constructor(foo) case
      && (BROKEN_COF ? fails(function () { proto.valueOf.call(that); }) : cof(that) != NUMBER)
        ? inheritIfRequired(new Base(toNumber(it)), that, $Number) : toNumber(it);
  };
  for (var keys = __webpack_require__(7) ? gOPN(Base) : (
    // ES3:
    'MAX_VALUE,MIN_VALUE,NaN,NEGATIVE_INFINITY,POSITIVE_INFINITY,' +
    // ES6 (in case, if modules with ES6 Number statics required before):
    'EPSILON,isFinite,isInteger,isNaN,isSafeInteger,MAX_SAFE_INTEGER,' +
    'MIN_SAFE_INTEGER,parseFloat,parseInt,isInteger'
  ).split(','), j = 0, key; keys.length > j; j++) {
    if (has(Base, key = keys[j]) && !has($Number, key)) {
      dP($Number, key, gOPD(Base, key));
    }
  }
  $Number.prototype = proto;
  proto.constructor = $Number;
  __webpack_require__(14)(global, NUMBER, $Number);
}


/***/ }),
/* 178 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(0);
var toInteger = __webpack_require__(27);
var aNumberValue = __webpack_require__(116);
var repeat = __webpack_require__(82);
var $toFixed = 1.0.toFixed;
var floor = Math.floor;
var data = [0, 0, 0, 0, 0, 0];
var ERROR = 'Number.toFixed: incorrect invocation!';
var ZERO = '0';

var multiply = function (n, c) {
  var i = -1;
  var c2 = c;
  while (++i < 6) {
    c2 += n * data[i];
    data[i] = c2 % 1e7;
    c2 = floor(c2 / 1e7);
  }
};
var divide = function (n) {
  var i = 6;
  var c = 0;
  while (--i >= 0) {
    c += data[i];
    data[i] = floor(c / n);
    c = (c % n) * 1e7;
  }
};
var numToString = function () {
  var i = 6;
  var s = '';
  while (--i >= 0) {
    if (s !== '' || i === 0 || data[i] !== 0) {
      var t = String(data[i]);
      s = s === '' ? t : s + repeat.call(ZERO, 7 - t.length) + t;
    }
  } return s;
};
var pow = function (x, n, acc) {
  return n === 0 ? acc : n % 2 === 1 ? pow(x, n - 1, acc * x) : pow(x * x, n / 2, acc);
};
var log = function (x) {
  var n = 0;
  var x2 = x;
  while (x2 >= 4096) {
    n += 12;
    x2 /= 4096;
  }
  while (x2 >= 2) {
    n += 1;
    x2 /= 2;
  } return n;
};

$export($export.P + $export.F * (!!$toFixed && (
  0.00008.toFixed(3) !== '0.000' ||
  0.9.toFixed(0) !== '1' ||
  1.255.toFixed(2) !== '1.25' ||
  1000000000000000128.0.toFixed(0) !== '1000000000000000128'
) || !__webpack_require__(3)(function () {
  // V8 ~ Android 4.3-
  $toFixed.call({});
})), 'Number', {
  toFixed: function toFixed(fractionDigits) {
    var x = aNumberValue(this, ERROR);
    var f = toInteger(fractionDigits);
    var s = '';
    var m = ZERO;
    var e, z, j, k;
    if (f < 0 || f > 20) throw RangeError(ERROR);
    // eslint-disable-next-line no-self-compare
    if (x != x) return 'NaN';
    if (x <= -1e21 || x >= 1e21) return String(x);
    if (x < 0) {
      s = '-';
      x = -x;
    }
    if (x > 1e-21) {
      e = log(x * pow(2, 69, 1)) - 69;
      z = e < 0 ? x * pow(2, -e, 1) : x / pow(2, e, 1);
      z *= 0x10000000000000;
      e = 52 - e;
      if (e > 0) {
        multiply(0, z);
        j = f;
        while (j >= 7) {
          multiply(1e7, 0);
          j -= 7;
        }
        multiply(pow(10, j, 1), 0);
        j = e - 1;
        while (j >= 23) {
          divide(1 << 23);
          j -= 23;
        }
        divide(1 << j);
        multiply(1, 1);
        divide(2);
        m = numToString();
      } else {
        multiply(0, z);
        multiply(1 << -e, 0);
        m = numToString() + repeat.call(ZERO, f);
      }
    }
    if (f > 0) {
      k = m.length;
      m = s + (k <= f ? '0.' + repeat.call(ZERO, f - k) + m : m.slice(0, k - f) + '.' + m.slice(k - f));
    } else {
      m = s + m;
    } return m;
  }
});


/***/ }),
/* 179 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(0);
var $fails = __webpack_require__(3);
var aNumberValue = __webpack_require__(116);
var $toPrecision = 1.0.toPrecision;

$export($export.P + $export.F * ($fails(function () {
  // IE7-
  return $toPrecision.call(1, undefined) !== '1';
}) || !$fails(function () {
  // V8 ~ Android 4.3-
  $toPrecision.call({});
})), 'Number', {
  toPrecision: function toPrecision(precision) {
    var that = aNumberValue(this, 'Number#toPrecision: incorrect invocation!');
    return precision === undefined ? $toPrecision.call(that) : $toPrecision.call(that, precision);
  }
});


/***/ }),
/* 180 */
/***/ (function(module, exports, __webpack_require__) {

// 20.1.2.1 Number.EPSILON
var $export = __webpack_require__(0);

$export($export.S, 'Number', { EPSILON: Math.pow(2, -52) });


/***/ }),
/* 181 */
/***/ (function(module, exports, __webpack_require__) {

// 20.1.2.2 Number.isFinite(number)
var $export = __webpack_require__(0);
var _isFinite = __webpack_require__(2).isFinite;

$export($export.S, 'Number', {
  isFinite: function isFinite(it) {
    return typeof it == 'number' && _isFinite(it);
  }
});


/***/ }),
/* 182 */
/***/ (function(module, exports, __webpack_require__) {

// 20.1.2.3 Number.isInteger(number)
var $export = __webpack_require__(0);

$export($export.S, 'Number', { isInteger: __webpack_require__(117) });


/***/ }),
/* 183 */
/***/ (function(module, exports, __webpack_require__) {

// 20.1.2.4 Number.isNaN(number)
var $export = __webpack_require__(0);

$export($export.S, 'Number', {
  isNaN: function isNaN(number) {
    // eslint-disable-next-line no-self-compare
    return number != number;
  }
});


/***/ }),
/* 184 */
/***/ (function(module, exports, __webpack_require__) {

// 20.1.2.5 Number.isSafeInteger(number)
var $export = __webpack_require__(0);
var isInteger = __webpack_require__(117);
var abs = Math.abs;

$export($export.S, 'Number', {
  isSafeInteger: function isSafeInteger(number) {
    return isInteger(number) && abs(number) <= 0x1fffffffffffff;
  }
});


/***/ }),
/* 185 */
/***/ (function(module, exports, __webpack_require__) {

// 20.1.2.6 Number.MAX_SAFE_INTEGER
var $export = __webpack_require__(0);

$export($export.S, 'Number', { MAX_SAFE_INTEGER: 0x1fffffffffffff });


/***/ }),
/* 186 */
/***/ (function(module, exports, __webpack_require__) {

// 20.1.2.10 Number.MIN_SAFE_INTEGER
var $export = __webpack_require__(0);

$export($export.S, 'Number', { MIN_SAFE_INTEGER: -0x1fffffffffffff });


/***/ }),
/* 187 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(0);
var $parseFloat = __webpack_require__(115);
// 20.1.2.12 Number.parseFloat(string)
$export($export.S + $export.F * (Number.parseFloat != $parseFloat), 'Number', { parseFloat: $parseFloat });


/***/ }),
/* 188 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(0);
var $parseInt = __webpack_require__(114);
// 20.1.2.13 Number.parseInt(string, radix)
$export($export.S + $export.F * (Number.parseInt != $parseInt), 'Number', { parseInt: $parseInt });


/***/ }),
/* 189 */
/***/ (function(module, exports, __webpack_require__) {

// 20.2.2.3 Math.acosh(x)
var $export = __webpack_require__(0);
var log1p = __webpack_require__(118);
var sqrt = Math.sqrt;
var $acosh = Math.acosh;

$export($export.S + $export.F * !($acosh
  // V8 bug: https://code.google.com/p/v8/issues/detail?id=3509
  && Math.floor($acosh(Number.MAX_VALUE)) == 710
  // Tor Browser bug: Math.acosh(Infinity) -> NaN
  && $acosh(Infinity) == Infinity
), 'Math', {
  acosh: function acosh(x) {
    return (x = +x) < 1 ? NaN : x > 94906265.62425156
      ? Math.log(x) + Math.LN2
      : log1p(x - 1 + sqrt(x - 1) * sqrt(x + 1));
  }
});


/***/ }),
/* 190 */
/***/ (function(module, exports, __webpack_require__) {

// 20.2.2.5 Math.asinh(x)
var $export = __webpack_require__(0);
var $asinh = Math.asinh;

function asinh(x) {
  return !isFinite(x = +x) || x == 0 ? x : x < 0 ? -asinh(-x) : Math.log(x + Math.sqrt(x * x + 1));
}

// Tor Browser bug: Math.asinh(0) -> -0
$export($export.S + $export.F * !($asinh && 1 / $asinh(0) > 0), 'Math', { asinh: asinh });


/***/ }),
/* 191 */
/***/ (function(module, exports, __webpack_require__) {

// 20.2.2.7 Math.atanh(x)
var $export = __webpack_require__(0);
var $atanh = Math.atanh;

// Tor Browser bug: Math.atanh(-0) -> 0
$export($export.S + $export.F * !($atanh && 1 / $atanh(-0) < 0), 'Math', {
  atanh: function atanh(x) {
    return (x = +x) == 0 ? x : Math.log((1 + x) / (1 - x)) / 2;
  }
});


/***/ }),
/* 192 */
/***/ (function(module, exports, __webpack_require__) {

// 20.2.2.9 Math.cbrt(x)
var $export = __webpack_require__(0);
var sign = __webpack_require__(83);

$export($export.S, 'Math', {
  cbrt: function cbrt(x) {
    return sign(x = +x) * Math.pow(Math.abs(x), 1 / 3);
  }
});


/***/ }),
/* 193 */
/***/ (function(module, exports, __webpack_require__) {

// 20.2.2.11 Math.clz32(x)
var $export = __webpack_require__(0);

$export($export.S, 'Math', {
  clz32: function clz32(x) {
    return (x >>>= 0) ? 31 - Math.floor(Math.log(x + 0.5) * Math.LOG2E) : 32;
  }
});


/***/ }),
/* 194 */
/***/ (function(module, exports, __webpack_require__) {

// 20.2.2.12 Math.cosh(x)
var $export = __webpack_require__(0);
var exp = Math.exp;

$export($export.S, 'Math', {
  cosh: function cosh(x) {
    return (exp(x = +x) + exp(-x)) / 2;
  }
});


/***/ }),
/* 195 */
/***/ (function(module, exports, __webpack_require__) {

// 20.2.2.14 Math.expm1(x)
var $export = __webpack_require__(0);
var $expm1 = __webpack_require__(84);

$export($export.S + $export.F * ($expm1 != Math.expm1), 'Math', { expm1: $expm1 });


/***/ }),
/* 196 */
/***/ (function(module, exports, __webpack_require__) {

// 20.2.2.16 Math.fround(x)
var $export = __webpack_require__(0);

$export($export.S, 'Math', { fround: __webpack_require__(119) });


/***/ }),
/* 197 */
/***/ (function(module, exports, __webpack_require__) {

// 20.2.2.17 Math.hypot([value1[, value2[, … ]]])
var $export = __webpack_require__(0);
var abs = Math.abs;

$export($export.S, 'Math', {
  hypot: function hypot(value1, value2) { // eslint-disable-line no-unused-vars
    var sum = 0;
    var i = 0;
    var aLen = arguments.length;
    var larg = 0;
    var arg, div;
    while (i < aLen) {
      arg = abs(arguments[i++]);
      if (larg < arg) {
        div = larg / arg;
        sum = sum * div * div + 1;
        larg = arg;
      } else if (arg > 0) {
        div = arg / larg;
        sum += div * div;
      } else sum += arg;
    }
    return larg === Infinity ? Infinity : larg * Math.sqrt(sum);
  }
});


/***/ }),
/* 198 */
/***/ (function(module, exports, __webpack_require__) {

// 20.2.2.18 Math.imul(x, y)
var $export = __webpack_require__(0);
var $imul = Math.imul;

// some WebKit versions fails with big numbers, some has wrong arity
$export($export.S + $export.F * __webpack_require__(3)(function () {
  return $imul(0xffffffff, 5) != -5 || $imul.length != 2;
}), 'Math', {
  imul: function imul(x, y) {
    var UINT16 = 0xffff;
    var xn = +x;
    var yn = +y;
    var xl = UINT16 & xn;
    var yl = UINT16 & yn;
    return 0 | xl * yl + ((UINT16 & xn >>> 16) * yl + xl * (UINT16 & yn >>> 16) << 16 >>> 0);
  }
});


/***/ }),
/* 199 */
/***/ (function(module, exports, __webpack_require__) {

// 20.2.2.21 Math.log10(x)
var $export = __webpack_require__(0);

$export($export.S, 'Math', {
  log10: function log10(x) {
    return Math.log(x) * Math.LOG10E;
  }
});


/***/ }),
/* 200 */
/***/ (function(module, exports, __webpack_require__) {

// 20.2.2.20 Math.log1p(x)
var $export = __webpack_require__(0);

$export($export.S, 'Math', { log1p: __webpack_require__(118) });


/***/ }),
/* 201 */
/***/ (function(module, exports, __webpack_require__) {

// 20.2.2.22 Math.log2(x)
var $export = __webpack_require__(0);

$export($export.S, 'Math', {
  log2: function log2(x) {
    return Math.log(x) / Math.LN2;
  }
});


/***/ }),
/* 202 */
/***/ (function(module, exports, __webpack_require__) {

// 20.2.2.28 Math.sign(x)
var $export = __webpack_require__(0);

$export($export.S, 'Math', { sign: __webpack_require__(83) });


/***/ }),
/* 203 */
/***/ (function(module, exports, __webpack_require__) {

// 20.2.2.30 Math.sinh(x)
var $export = __webpack_require__(0);
var expm1 = __webpack_require__(84);
var exp = Math.exp;

// V8 near Chromium 38 has a problem with very small numbers
$export($export.S + $export.F * __webpack_require__(3)(function () {
  return !Math.sinh(-2e-17) != -2e-17;
}), 'Math', {
  sinh: function sinh(x) {
    return Math.abs(x = +x) < 1
      ? (expm1(x) - expm1(-x)) / 2
      : (exp(x - 1) - exp(-x - 1)) * (Math.E / 2);
  }
});


/***/ }),
/* 204 */
/***/ (function(module, exports, __webpack_require__) {

// 20.2.2.33 Math.tanh(x)
var $export = __webpack_require__(0);
var expm1 = __webpack_require__(84);
var exp = Math.exp;

$export($export.S, 'Math', {
  tanh: function tanh(x) {
    var a = expm1(x = +x);
    var b = expm1(-x);
    return a == Infinity ? 1 : b == Infinity ? -1 : (a - b) / (exp(x) + exp(-x));
  }
});


/***/ }),
/* 205 */
/***/ (function(module, exports, __webpack_require__) {

// 20.2.2.34 Math.trunc(x)
var $export = __webpack_require__(0);

$export($export.S, 'Math', {
  trunc: function trunc(it) {
    return (it > 0 ? Math.floor : Math.ceil)(it);
  }
});


/***/ }),
/* 206 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(0);
var toAbsoluteIndex = __webpack_require__(39);
var fromCharCode = String.fromCharCode;
var $fromCodePoint = String.fromCodePoint;

// length should be 1, old FF problem
$export($export.S + $export.F * (!!$fromCodePoint && $fromCodePoint.length != 1), 'String', {
  // 21.1.2.2 String.fromCodePoint(...codePoints)
  fromCodePoint: function fromCodePoint(x) { // eslint-disable-line no-unused-vars
    var res = [];
    var aLen = arguments.length;
    var i = 0;
    var code;
    while (aLen > i) {
      code = +arguments[i++];
      if (toAbsoluteIndex(code, 0x10ffff) !== code) throw RangeError(code + ' is not a valid code point');
      res.push(code < 0x10000
        ? fromCharCode(code)
        : fromCharCode(((code -= 0x10000) >> 10) + 0xd800, code % 0x400 + 0xdc00)
      );
    } return res.join('');
  }
});


/***/ }),
/* 207 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(0);
var toIObject = __webpack_require__(15);
var toLength = __webpack_require__(9);

$export($export.S, 'String', {
  // 21.1.2.4 String.raw(callSite, ...substitutions)
  raw: function raw(callSite) {
    var tpl = toIObject(callSite.raw);
    var len = toLength(tpl.length);
    var aLen = arguments.length;
    var res = [];
    var i = 0;
    while (len > i) {
      res.push(String(tpl[i++]));
      if (i < aLen) res.push(String(arguments[i]));
    } return res.join('');
  }
});


/***/ }),
/* 208 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// 21.1.3.25 String.prototype.trim()
__webpack_require__(49)('trim', function ($trim) {
  return function trim() {
    return $trim(this, 3);
  };
});


/***/ }),
/* 209 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $at = __webpack_require__(85)(true);

// 21.1.3.27 String.prototype[@@iterator]()
__webpack_require__(86)(String, 'String', function (iterated) {
  this._t = String(iterated); // target
  this._i = 0;                // next index
// 21.1.5.2.1 %StringIteratorPrototype%.next()
}, function () {
  var O = this._t;
  var index = this._i;
  var point;
  if (index >= O.length) return { value: undefined, done: true };
  point = $at(O, index);
  this._i += point.length;
  return { value: point, done: false };
});


/***/ }),
/* 210 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(0);
var $at = __webpack_require__(85)(false);
$export($export.P, 'String', {
  // 21.1.3.3 String.prototype.codePointAt(pos)
  codePointAt: function codePointAt(pos) {
    return $at(this, pos);
  }
});


/***/ }),
/* 211 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
// 21.1.3.6 String.prototype.endsWith(searchString [, endPosition])

var $export = __webpack_require__(0);
var toLength = __webpack_require__(9);
var context = __webpack_require__(88);
var ENDS_WITH = 'endsWith';
var $endsWith = ''[ENDS_WITH];

$export($export.P + $export.F * __webpack_require__(89)(ENDS_WITH), 'String', {
  endsWith: function endsWith(searchString /* , endPosition = @length */) {
    var that = context(this, searchString, ENDS_WITH);
    var endPosition = arguments.length > 1 ? arguments[1] : undefined;
    var len = toLength(that.length);
    var end = endPosition === undefined ? len : Math.min(toLength(endPosition), len);
    var search = String(searchString);
    return $endsWith
      ? $endsWith.call(that, search, end)
      : that.slice(end - search.length, end) === search;
  }
});


/***/ }),
/* 212 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
// 21.1.3.7 String.prototype.includes(searchString, position = 0)

var $export = __webpack_require__(0);
var context = __webpack_require__(88);
var INCLUDES = 'includes';

$export($export.P + $export.F * __webpack_require__(89)(INCLUDES), 'String', {
  includes: function includes(searchString /* , position = 0 */) {
    return !!~context(this, searchString, INCLUDES)
      .indexOf(searchString, arguments.length > 1 ? arguments[1] : undefined);
  }
});


/***/ }),
/* 213 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(0);

$export($export.P, 'String', {
  // 21.1.3.13 String.prototype.repeat(count)
  repeat: __webpack_require__(82)
});


/***/ }),
/* 214 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
// 21.1.3.18 String.prototype.startsWith(searchString [, position ])

var $export = __webpack_require__(0);
var toLength = __webpack_require__(9);
var context = __webpack_require__(88);
var STARTS_WITH = 'startsWith';
var $startsWith = ''[STARTS_WITH];

$export($export.P + $export.F * __webpack_require__(89)(STARTS_WITH), 'String', {
  startsWith: function startsWith(searchString /* , position = 0 */) {
    var that = context(this, searchString, STARTS_WITH);
    var index = toLength(Math.min(arguments.length > 1 ? arguments[1] : undefined, that.length));
    var search = String(searchString);
    return $startsWith
      ? $startsWith.call(that, search, index)
      : that.slice(index, index + search.length) === search;
  }
});


/***/ }),
/* 215 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// B.2.3.2 String.prototype.anchor(name)
__webpack_require__(16)('anchor', function (createHTML) {
  return function anchor(name) {
    return createHTML(this, 'a', 'name', name);
  };
});


/***/ }),
/* 216 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// B.2.3.3 String.prototype.big()
__webpack_require__(16)('big', function (createHTML) {
  return function big() {
    return createHTML(this, 'big', '', '');
  };
});


/***/ }),
/* 217 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// B.2.3.4 String.prototype.blink()
__webpack_require__(16)('blink', function (createHTML) {
  return function blink() {
    return createHTML(this, 'blink', '', '');
  };
});


/***/ }),
/* 218 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// B.2.3.5 String.prototype.bold()
__webpack_require__(16)('bold', function (createHTML) {
  return function bold() {
    return createHTML(this, 'b', '', '');
  };
});


/***/ }),
/* 219 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// B.2.3.6 String.prototype.fixed()
__webpack_require__(16)('fixed', function (createHTML) {
  return function fixed() {
    return createHTML(this, 'tt', '', '');
  };
});


/***/ }),
/* 220 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// B.2.3.7 String.prototype.fontcolor(color)
__webpack_require__(16)('fontcolor', function (createHTML) {
  return function fontcolor(color) {
    return createHTML(this, 'font', 'color', color);
  };
});


/***/ }),
/* 221 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// B.2.3.8 String.prototype.fontsize(size)
__webpack_require__(16)('fontsize', function (createHTML) {
  return function fontsize(size) {
    return createHTML(this, 'font', 'size', size);
  };
});


/***/ }),
/* 222 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// B.2.3.9 String.prototype.italics()
__webpack_require__(16)('italics', function (createHTML) {
  return function italics() {
    return createHTML(this, 'i', '', '');
  };
});


/***/ }),
/* 223 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// B.2.3.10 String.prototype.link(url)
__webpack_require__(16)('link', function (createHTML) {
  return function link(url) {
    return createHTML(this, 'a', 'href', url);
  };
});


/***/ }),
/* 224 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// B.2.3.11 String.prototype.small()
__webpack_require__(16)('small', function (createHTML) {
  return function small() {
    return createHTML(this, 'small', '', '');
  };
});


/***/ }),
/* 225 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// B.2.3.12 String.prototype.strike()
__webpack_require__(16)('strike', function (createHTML) {
  return function strike() {
    return createHTML(this, 'strike', '', '');
  };
});


/***/ }),
/* 226 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// B.2.3.13 String.prototype.sub()
__webpack_require__(16)('sub', function (createHTML) {
  return function sub() {
    return createHTML(this, 'sub', '', '');
  };
});


/***/ }),
/* 227 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// B.2.3.14 String.prototype.sup()
__webpack_require__(16)('sup', function (createHTML) {
  return function sup() {
    return createHTML(this, 'sup', '', '');
  };
});


/***/ }),
/* 228 */
/***/ (function(module, exports, __webpack_require__) {

// 20.3.3.1 / 15.9.4.4 Date.now()
var $export = __webpack_require__(0);

$export($export.S, 'Date', { now: function () { return new Date().getTime(); } });


/***/ }),
/* 229 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(0);
var toObject = __webpack_require__(10);
var toPrimitive = __webpack_require__(25);

$export($export.P + $export.F * __webpack_require__(3)(function () {
  return new Date(NaN).toJSON() !== null
    || Date.prototype.toJSON.call({ toISOString: function () { return 1; } }) !== 1;
}), 'Date', {
  // eslint-disable-next-line no-unused-vars
  toJSON: function toJSON(key) {
    var O = toObject(this);
    var pv = toPrimitive(O);
    return typeof pv == 'number' && !isFinite(pv) ? null : O.toISOString();
  }
});


/***/ }),
/* 230 */
/***/ (function(module, exports, __webpack_require__) {

// 20.3.4.36 / 15.9.5.43 Date.prototype.toISOString()
var $export = __webpack_require__(0);
var toISOString = __webpack_require__(231);

// PhantomJS / old WebKit has a broken implementations
$export($export.P + $export.F * (Date.prototype.toISOString !== toISOString), 'Date', {
  toISOString: toISOString
});


/***/ }),
/* 231 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// 20.3.4.36 / 15.9.5.43 Date.prototype.toISOString()
var fails = __webpack_require__(3);
var getTime = Date.prototype.getTime;
var $toISOString = Date.prototype.toISOString;

var lz = function (num) {
  return num > 9 ? num : '0' + num;
};

// PhantomJS / old WebKit has a broken implementations
module.exports = (fails(function () {
  return $toISOString.call(new Date(-5e13 - 1)) != '0385-07-25T07:06:39.999Z';
}) || !fails(function () {
  $toISOString.call(new Date(NaN));
})) ? function toISOString() {
  if (!isFinite(getTime.call(this))) throw RangeError('Invalid time value');
  var d = this;
  var y = d.getUTCFullYear();
  var m = d.getUTCMilliseconds();
  var s = y < 0 ? '-' : y > 9999 ? '+' : '';
  return s + ('00000' + Math.abs(y)).slice(s ? -6 : -4) +
    '-' + lz(d.getUTCMonth() + 1) + '-' + lz(d.getUTCDate()) +
    'T' + lz(d.getUTCHours()) + ':' + lz(d.getUTCMinutes()) +
    ':' + lz(d.getUTCSeconds()) + '.' + (m > 99 ? m : '0' + lz(m)) + 'Z';
} : $toISOString;


/***/ }),
/* 232 */
/***/ (function(module, exports, __webpack_require__) {

var DateProto = Date.prototype;
var INVALID_DATE = 'Invalid Date';
var TO_STRING = 'toString';
var $toString = DateProto[TO_STRING];
var getTime = DateProto.getTime;
if (new Date(NaN) + '' != INVALID_DATE) {
  __webpack_require__(14)(DateProto, TO_STRING, function toString() {
    var value = getTime.call(this);
    // eslint-disable-next-line no-self-compare
    return value === value ? $toString.call(this) : INVALID_DATE;
  });
}


/***/ }),
/* 233 */
/***/ (function(module, exports, __webpack_require__) {

var TO_PRIMITIVE = __webpack_require__(5)('toPrimitive');
var proto = Date.prototype;

if (!(TO_PRIMITIVE in proto)) __webpack_require__(13)(proto, TO_PRIMITIVE, __webpack_require__(234));


/***/ }),
/* 234 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var anObject = __webpack_require__(1);
var toPrimitive = __webpack_require__(25);
var NUMBER = 'number';

module.exports = function (hint) {
  if (hint !== 'string' && hint !== NUMBER && hint !== 'default') throw TypeError('Incorrect hint');
  return toPrimitive(anObject(this), hint != NUMBER);
};


/***/ }),
/* 235 */
/***/ (function(module, exports, __webpack_require__) {

// 22.1.2.2 / 15.4.3.2 Array.isArray(arg)
var $export = __webpack_require__(0);

$export($export.S, 'Array', { isArray: __webpack_require__(58) });


/***/ }),
/* 236 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var ctx = __webpack_require__(19);
var $export = __webpack_require__(0);
var toObject = __webpack_require__(10);
var call = __webpack_require__(120);
var isArrayIter = __webpack_require__(90);
var toLength = __webpack_require__(9);
var createProperty = __webpack_require__(91);
var getIterFn = __webpack_require__(92);

$export($export.S + $export.F * !__webpack_require__(61)(function (iter) { Array.from(iter); }), 'Array', {
  // 22.1.2.1 Array.from(arrayLike, mapfn = undefined, thisArg = undefined)
  from: function from(arrayLike /* , mapfn = undefined, thisArg = undefined */) {
    var O = toObject(arrayLike);
    var C = typeof this == 'function' ? this : Array;
    var aLen = arguments.length;
    var mapfn = aLen > 1 ? arguments[1] : undefined;
    var mapping = mapfn !== undefined;
    var index = 0;
    var iterFn = getIterFn(O);
    var length, result, step, iterator;
    if (mapping) mapfn = ctx(mapfn, aLen > 2 ? arguments[2] : undefined, 2);
    // if object isn't iterable or it's array with default iterator - use simple case
    if (iterFn != undefined && !(C == Array && isArrayIter(iterFn))) {
      for (iterator = iterFn.call(O), result = new C(); !(step = iterator.next()).done; index++) {
        createProperty(result, index, mapping ? call(iterator, mapfn, [step.value, index], true) : step.value);
      }
    } else {
      length = toLength(O.length);
      for (result = new C(length); length > index; index++) {
        createProperty(result, index, mapping ? mapfn(O[index], index) : O[index]);
      }
    }
    result.length = index;
    return result;
  }
});


/***/ }),
/* 237 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(0);
var createProperty = __webpack_require__(91);

// WebKit Array.of isn't generic
$export($export.S + $export.F * __webpack_require__(3)(function () {
  function F() { /* empty */ }
  return !(Array.of.call(F) instanceof F);
}), 'Array', {
  // 22.1.2.3 Array.of( ...items)
  of: function of(/* ...args */) {
    var index = 0;
    var aLen = arguments.length;
    var result = new (typeof this == 'function' ? this : Array)(aLen);
    while (aLen > index) createProperty(result, index, arguments[index++]);
    result.length = aLen;
    return result;
  }
});


/***/ }),
/* 238 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// 22.1.3.13 Array.prototype.join(separator)
var $export = __webpack_require__(0);
var toIObject = __webpack_require__(15);
var arrayJoin = [].join;

// fallback for not array-like strings
$export($export.P + $export.F * (__webpack_require__(52) != Object || !__webpack_require__(21)(arrayJoin)), 'Array', {
  join: function join(separator) {
    return arrayJoin.call(toIObject(this), separator === undefined ? ',' : separator);
  }
});


/***/ }),
/* 239 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(0);
var html = __webpack_require__(78);
var cof = __webpack_require__(20);
var toAbsoluteIndex = __webpack_require__(39);
var toLength = __webpack_require__(9);
var arraySlice = [].slice;

// fallback for not array-like ES3 strings and DOM objects
$export($export.P + $export.F * __webpack_require__(3)(function () {
  if (html) arraySlice.call(html);
}), 'Array', {
  slice: function slice(begin, end) {
    var len = toLength(this.length);
    var klass = cof(this);
    end = end === undefined ? len : end;
    if (klass == 'Array') return arraySlice.call(this, begin, end);
    var start = toAbsoluteIndex(begin, len);
    var upTo = toAbsoluteIndex(end, len);
    var size = toLength(upTo - start);
    var cloned = Array(size);
    var i = 0;
    for (; i < size; i++) cloned[i] = klass == 'String'
      ? this.charAt(start + i)
      : this[start + i];
    return cloned;
  }
});


/***/ }),
/* 240 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(0);
var aFunction = __webpack_require__(11);
var toObject = __webpack_require__(10);
var fails = __webpack_require__(3);
var $sort = [].sort;
var test = [1, 2, 3];

$export($export.P + $export.F * (fails(function () {
  // IE8-
  test.sort(undefined);
}) || !fails(function () {
  // V8 bug
  test.sort(null);
  // Old WebKit
}) || !__webpack_require__(21)($sort)), 'Array', {
  // 22.1.3.25 Array.prototype.sort(comparefn)
  sort: function sort(comparefn) {
    return comparefn === undefined
      ? $sort.call(toObject(this))
      : $sort.call(toObject(this), aFunction(comparefn));
  }
});


/***/ }),
/* 241 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(0);
var $forEach = __webpack_require__(29)(0);
var STRICT = __webpack_require__(21)([].forEach, true);

$export($export.P + $export.F * !STRICT, 'Array', {
  // 22.1.3.10 / 15.4.4.18 Array.prototype.forEach(callbackfn [, thisArg])
  forEach: function forEach(callbackfn /* , thisArg */) {
    return $forEach(this, callbackfn, arguments[1]);
  }
});


/***/ }),
/* 242 */
/***/ (function(module, exports, __webpack_require__) {

var isObject = __webpack_require__(4);
var isArray = __webpack_require__(58);
var SPECIES = __webpack_require__(5)('species');

module.exports = function (original) {
  var C;
  if (isArray(original)) {
    C = original.constructor;
    // cross-realm fallback
    if (typeof C == 'function' && (C === Array || isArray(C.prototype))) C = undefined;
    if (isObject(C)) {
      C = C[SPECIES];
      if (C === null) C = undefined;
    }
  } return C === undefined ? Array : C;
};


/***/ }),
/* 243 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(0);
var $map = __webpack_require__(29)(1);

$export($export.P + $export.F * !__webpack_require__(21)([].map, true), 'Array', {
  // 22.1.3.15 / 15.4.4.19 Array.prototype.map(callbackfn [, thisArg])
  map: function map(callbackfn /* , thisArg */) {
    return $map(this, callbackfn, arguments[1]);
  }
});


/***/ }),
/* 244 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(0);
var $filter = __webpack_require__(29)(2);

$export($export.P + $export.F * !__webpack_require__(21)([].filter, true), 'Array', {
  // 22.1.3.7 / 15.4.4.20 Array.prototype.filter(callbackfn [, thisArg])
  filter: function filter(callbackfn /* , thisArg */) {
    return $filter(this, callbackfn, arguments[1]);
  }
});


/***/ }),
/* 245 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(0);
var $some = __webpack_require__(29)(3);

$export($export.P + $export.F * !__webpack_require__(21)([].some, true), 'Array', {
  // 22.1.3.23 / 15.4.4.17 Array.prototype.some(callbackfn [, thisArg])
  some: function some(callbackfn /* , thisArg */) {
    return $some(this, callbackfn, arguments[1]);
  }
});


/***/ }),
/* 246 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(0);
var $every = __webpack_require__(29)(4);

$export($export.P + $export.F * !__webpack_require__(21)([].every, true), 'Array', {
  // 22.1.3.5 / 15.4.4.16 Array.prototype.every(callbackfn [, thisArg])
  every: function every(callbackfn /* , thisArg */) {
    return $every(this, callbackfn, arguments[1]);
  }
});


/***/ }),
/* 247 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(0);
var $reduce = __webpack_require__(121);

$export($export.P + $export.F * !__webpack_require__(21)([].reduce, true), 'Array', {
  // 22.1.3.18 / 15.4.4.21 Array.prototype.reduce(callbackfn [, initialValue])
  reduce: function reduce(callbackfn /* , initialValue */) {
    return $reduce(this, callbackfn, arguments.length, arguments[1], false);
  }
});


/***/ }),
/* 248 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(0);
var $reduce = __webpack_require__(121);

$export($export.P + $export.F * !__webpack_require__(21)([].reduceRight, true), 'Array', {
  // 22.1.3.19 / 15.4.4.22 Array.prototype.reduceRight(callbackfn [, initialValue])
  reduceRight: function reduceRight(callbackfn /* , initialValue */) {
    return $reduce(this, callbackfn, arguments.length, arguments[1], true);
  }
});


/***/ }),
/* 249 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(0);
var $indexOf = __webpack_require__(56)(false);
var $native = [].indexOf;
var NEGATIVE_ZERO = !!$native && 1 / [1].indexOf(1, -0) < 0;

$export($export.P + $export.F * (NEGATIVE_ZERO || !__webpack_require__(21)($native)), 'Array', {
  // 22.1.3.11 / 15.4.4.14 Array.prototype.indexOf(searchElement [, fromIndex])
  indexOf: function indexOf(searchElement /* , fromIndex = 0 */) {
    return NEGATIVE_ZERO
      // convert -0 to +0
      ? $native.apply(this, arguments) || 0
      : $indexOf(this, searchElement, arguments[1]);
  }
});


/***/ }),
/* 250 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(0);
var toIObject = __webpack_require__(15);
var toInteger = __webpack_require__(27);
var toLength = __webpack_require__(9);
var $native = [].lastIndexOf;
var NEGATIVE_ZERO = !!$native && 1 / [1].lastIndexOf(1, -0) < 0;

$export($export.P + $export.F * (NEGATIVE_ZERO || !__webpack_require__(21)($native)), 'Array', {
  // 22.1.3.14 / 15.4.4.15 Array.prototype.lastIndexOf(searchElement [, fromIndex])
  lastIndexOf: function lastIndexOf(searchElement /* , fromIndex = @[*-1] */) {
    // convert -0 to +0
    if (NEGATIVE_ZERO) return $native.apply(this, arguments) || 0;
    var O = toIObject(this);
    var length = toLength(O.length);
    var index = length - 1;
    if (arguments.length > 1) index = Math.min(index, toInteger(arguments[1]));
    if (index < 0) index = length + index;
    for (;index >= 0; index--) if (index in O) if (O[index] === searchElement) return index || 0;
    return -1;
  }
});


/***/ }),
/* 251 */
/***/ (function(module, exports, __webpack_require__) {

// 22.1.3.3 Array.prototype.copyWithin(target, start, end = this.length)
var $export = __webpack_require__(0);

$export($export.P, 'Array', { copyWithin: __webpack_require__(122) });

__webpack_require__(35)('copyWithin');


/***/ }),
/* 252 */
/***/ (function(module, exports, __webpack_require__) {

// 22.1.3.6 Array.prototype.fill(value, start = 0, end = this.length)
var $export = __webpack_require__(0);

$export($export.P, 'Array', { fill: __webpack_require__(94) });

__webpack_require__(35)('fill');


/***/ }),
/* 253 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// 22.1.3.8 Array.prototype.find(predicate, thisArg = undefined)
var $export = __webpack_require__(0);
var $find = __webpack_require__(29)(5);
var KEY = 'find';
var forced = true;
// Shouldn't skip holes
if (KEY in []) Array(1)[KEY](function () { forced = false; });
$export($export.P + $export.F * forced, 'Array', {
  find: function find(callbackfn /* , that = undefined */) {
    return $find(this, callbackfn, arguments.length > 1 ? arguments[1] : undefined);
  }
});
__webpack_require__(35)(KEY);


/***/ }),
/* 254 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// 22.1.3.9 Array.prototype.findIndex(predicate, thisArg = undefined)
var $export = __webpack_require__(0);
var $find = __webpack_require__(29)(6);
var KEY = 'findIndex';
var forced = true;
// Shouldn't skip holes
if (KEY in []) Array(1)[KEY](function () { forced = false; });
$export($export.P + $export.F * forced, 'Array', {
  findIndex: function findIndex(callbackfn /* , that = undefined */) {
    return $find(this, callbackfn, arguments.length > 1 ? arguments[1] : undefined);
  }
});
__webpack_require__(35)(KEY);


/***/ }),
/* 255 */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(42)('Array');


/***/ }),
/* 256 */
/***/ (function(module, exports, __webpack_require__) {

var global = __webpack_require__(2);
var inheritIfRequired = __webpack_require__(81);
var dP = __webpack_require__(8).f;
var gOPN = __webpack_require__(41).f;
var isRegExp = __webpack_require__(60);
var $flags = __webpack_require__(62);
var $RegExp = global.RegExp;
var Base = $RegExp;
var proto = $RegExp.prototype;
var re1 = /a/g;
var re2 = /a/g;
// "new" creates a new object, old webkit buggy here
var CORRECT_NEW = new $RegExp(re1) !== re1;

if (__webpack_require__(7) && (!CORRECT_NEW || __webpack_require__(3)(function () {
  re2[__webpack_require__(5)('match')] = false;
  // RegExp constructor can alter flags and IsRegExp works correct with @@match
  return $RegExp(re1) != re1 || $RegExp(re2) == re2 || $RegExp(re1, 'i') != '/a/i';
}))) {
  $RegExp = function RegExp(p, f) {
    var tiRE = this instanceof $RegExp;
    var piRE = isRegExp(p);
    var fiU = f === undefined;
    return !tiRE && piRE && p.constructor === $RegExp && fiU ? p
      : inheritIfRequired(CORRECT_NEW
        ? new Base(piRE && !fiU ? p.source : p, f)
        : Base((piRE = p instanceof $RegExp) ? p.source : p, piRE && fiU ? $flags.call(p) : f)
      , tiRE ? this : proto, $RegExp);
  };
  var proxy = function (key) {
    key in $RegExp || dP($RegExp, key, {
      configurable: true,
      get: function () { return Base[key]; },
      set: function (it) { Base[key] = it; }
    });
  };
  for (var keys = gOPN(Base), i = 0; keys.length > i;) proxy(keys[i++]);
  proto.constructor = $RegExp;
  $RegExp.prototype = proto;
  __webpack_require__(14)(global, 'RegExp', $RegExp);
}

__webpack_require__(42)('RegExp');


/***/ }),
/* 257 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

__webpack_require__(124);
var anObject = __webpack_require__(1);
var $flags = __webpack_require__(62);
var DESCRIPTORS = __webpack_require__(7);
var TO_STRING = 'toString';
var $toString = /./[TO_STRING];

var define = function (fn) {
  __webpack_require__(14)(RegExp.prototype, TO_STRING, fn, true);
};

// 21.2.5.14 RegExp.prototype.toString()
if (__webpack_require__(3)(function () { return $toString.call({ source: 'a', flags: 'b' }) != '/a/b'; })) {
  define(function toString() {
    var R = anObject(this);
    return '/'.concat(R.source, '/',
      'flags' in R ? R.flags : !DESCRIPTORS && R instanceof RegExp ? $flags.call(R) : undefined);
  });
// FF44- RegExp#toString has a wrong name
} else if ($toString.name != TO_STRING) {
  define(function toString() {
    return $toString.call(this);
  });
}


/***/ }),
/* 258 */
/***/ (function(module, exports, __webpack_require__) {

// @@match logic
__webpack_require__(63)('match', 1, function (defined, MATCH, $match) {
  // 21.1.3.11 String.prototype.match(regexp)
  return [function match(regexp) {
    'use strict';
    var O = defined(this);
    var fn = regexp == undefined ? undefined : regexp[MATCH];
    return fn !== undefined ? fn.call(regexp, O) : new RegExp(regexp)[MATCH](String(O));
  }, $match];
});


/***/ }),
/* 259 */
/***/ (function(module, exports, __webpack_require__) {

// @@replace logic
__webpack_require__(63)('replace', 2, function (defined, REPLACE, $replace) {
  // 21.1.3.14 String.prototype.replace(searchValue, replaceValue)
  return [function replace(searchValue, replaceValue) {
    'use strict';
    var O = defined(this);
    var fn = searchValue == undefined ? undefined : searchValue[REPLACE];
    return fn !== undefined
      ? fn.call(searchValue, O, replaceValue)
      : $replace.call(String(O), searchValue, replaceValue);
  }, $replace];
});


/***/ }),
/* 260 */
/***/ (function(module, exports, __webpack_require__) {

// @@search logic
__webpack_require__(63)('search', 1, function (defined, SEARCH, $search) {
  // 21.1.3.15 String.prototype.search(regexp)
  return [function search(regexp) {
    'use strict';
    var O = defined(this);
    var fn = regexp == undefined ? undefined : regexp[SEARCH];
    return fn !== undefined ? fn.call(regexp, O) : new RegExp(regexp)[SEARCH](String(O));
  }, $search];
});


/***/ }),
/* 261 */
/***/ (function(module, exports, __webpack_require__) {

// @@split logic
__webpack_require__(63)('split', 2, function (defined, SPLIT, $split) {
  'use strict';
  var isRegExp = __webpack_require__(60);
  var _split = $split;
  var $push = [].push;
  var $SPLIT = 'split';
  var LENGTH = 'length';
  var LAST_INDEX = 'lastIndex';
  if (
    'abbc'[$SPLIT](/(b)*/)[1] == 'c' ||
    'test'[$SPLIT](/(?:)/, -1)[LENGTH] != 4 ||
    'ab'[$SPLIT](/(?:ab)*/)[LENGTH] != 2 ||
    '.'[$SPLIT](/(.?)(.?)/)[LENGTH] != 4 ||
    '.'[$SPLIT](/()()/)[LENGTH] > 1 ||
    ''[$SPLIT](/.?/)[LENGTH]
  ) {
    var NPCG = /()??/.exec('')[1] === undefined; // nonparticipating capturing group
    // based on es5-shim implementation, need to rework it
    $split = function (separator, limit) {
      var string = String(this);
      if (separator === undefined && limit === 0) return [];
      // If `separator` is not a regex, use native split
      if (!isRegExp(separator)) return _split.call(string, separator, limit);
      var output = [];
      var flags = (separator.ignoreCase ? 'i' : '') +
                  (separator.multiline ? 'm' : '') +
                  (separator.unicode ? 'u' : '') +
                  (separator.sticky ? 'y' : '');
      var lastLastIndex = 0;
      var splitLimit = limit === undefined ? 4294967295 : limit >>> 0;
      // Make `global` and avoid `lastIndex` issues by working with a copy
      var separatorCopy = new RegExp(separator.source, flags + 'g');
      var separator2, match, lastIndex, lastLength, i;
      // Doesn't need flags gy, but they don't hurt
      if (!NPCG) separator2 = new RegExp('^' + separatorCopy.source + '$(?!\\s)', flags);
      while (match = separatorCopy.exec(string)) {
        // `separatorCopy.lastIndex` is not reliable cross-browser
        lastIndex = match.index + match[0][LENGTH];
        if (lastIndex > lastLastIndex) {
          output.push(string.slice(lastLastIndex, match.index));
          // Fix browsers whose `exec` methods don't consistently return `undefined` for NPCG
          // eslint-disable-next-line no-loop-func
          if (!NPCG && match[LENGTH] > 1) match[0].replace(separator2, function () {
            for (i = 1; i < arguments[LENGTH] - 2; i++) if (arguments[i] === undefined) match[i] = undefined;
          });
          if (match[LENGTH] > 1 && match.index < string[LENGTH]) $push.apply(output, match.slice(1));
          lastLength = match[0][LENGTH];
          lastLastIndex = lastIndex;
          if (output[LENGTH] >= splitLimit) break;
        }
        if (separatorCopy[LAST_INDEX] === match.index) separatorCopy[LAST_INDEX]++; // Avoid an infinite loop
      }
      if (lastLastIndex === string[LENGTH]) {
        if (lastLength || !separatorCopy.test('')) output.push('');
      } else output.push(string.slice(lastLastIndex));
      return output[LENGTH] > splitLimit ? output.slice(0, splitLimit) : output;
    };
  // Chakra, V8
  } else if ('0'[$SPLIT](undefined, 0)[LENGTH]) {
    $split = function (separator, limit) {
      return separator === undefined && limit === 0 ? [] : _split.call(this, separator, limit);
    };
  }
  // 21.1.3.17 String.prototype.split(separator, limit)
  return [function split(separator, limit) {
    var O = defined(this);
    var fn = separator == undefined ? undefined : separator[SPLIT];
    return fn !== undefined ? fn.call(separator, O, limit) : $split.call(String(O), separator, limit);
  }, $split];
});


/***/ }),
/* 262 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var LIBRARY = __webpack_require__(38);
var global = __webpack_require__(2);
var ctx = __webpack_require__(19);
var classof = __webpack_require__(54);
var $export = __webpack_require__(0);
var isObject = __webpack_require__(4);
var aFunction = __webpack_require__(11);
var anInstance = __webpack_require__(43);
var forOf = __webpack_require__(44);
var speciesConstructor = __webpack_require__(64);
var task = __webpack_require__(96).set;
var microtask = __webpack_require__(97)();
var newPromiseCapabilityModule = __webpack_require__(98);
var perform = __webpack_require__(125);
var promiseResolve = __webpack_require__(126);
var PROMISE = 'Promise';
var TypeError = global.TypeError;
var process = global.process;
var $Promise = global[PROMISE];
var isNode = classof(process) == 'process';
var empty = function () { /* empty */ };
var Internal, newGenericPromiseCapability, OwnPromiseCapability, Wrapper;
var newPromiseCapability = newGenericPromiseCapability = newPromiseCapabilityModule.f;

var USE_NATIVE = !!function () {
  try {
    // correct subclassing with @@species support
    var promise = $Promise.resolve(1);
    var FakePromise = (promise.constructor = {})[__webpack_require__(5)('species')] = function (exec) {
      exec(empty, empty);
    };
    // unhandled rejections tracking support, NodeJS Promise without it fails @@species test
    return (isNode || typeof PromiseRejectionEvent == 'function') && promise.then(empty) instanceof FakePromise;
  } catch (e) { /* empty */ }
}();

// helpers
var sameConstructor = LIBRARY ? function (a, b) {
  // with library wrapper special case
  return a === b || a === $Promise && b === Wrapper;
} : function (a, b) {
  return a === b;
};
var isThenable = function (it) {
  var then;
  return isObject(it) && typeof (then = it.then) == 'function' ? then : false;
};
var notify = function (promise, isReject) {
  if (promise._n) return;
  promise._n = true;
  var chain = promise._c;
  microtask(function () {
    var value = promise._v;
    var ok = promise._s == 1;
    var i = 0;
    var run = function (reaction) {
      var handler = ok ? reaction.ok : reaction.fail;
      var resolve = reaction.resolve;
      var reject = reaction.reject;
      var domain = reaction.domain;
      var result, then;
      try {
        if (handler) {
          if (!ok) {
            if (promise._h == 2) onHandleUnhandled(promise);
            promise._h = 1;
          }
          if (handler === true) result = value;
          else {
            if (domain) domain.enter();
            result = handler(value);
            if (domain) domain.exit();
          }
          if (result === reaction.promise) {
            reject(TypeError('Promise-chain cycle'));
          } else if (then = isThenable(result)) {
            then.call(result, resolve, reject);
          } else resolve(result);
        } else reject(value);
      } catch (e) {
        reject(e);
      }
    };
    while (chain.length > i) run(chain[i++]); // variable length - can't use forEach
    promise._c = [];
    promise._n = false;
    if (isReject && !promise._h) onUnhandled(promise);
  });
};
var onUnhandled = function (promise) {
  task.call(global, function () {
    var value = promise._v;
    var unhandled = isUnhandled(promise);
    var result, handler, console;
    if (unhandled) {
      result = perform(function () {
        if (isNode) {
          process.emit('unhandledRejection', value, promise);
        } else if (handler = global.onunhandledrejection) {
          handler({ promise: promise, reason: value });
        } else if ((console = global.console) && console.error) {
          console.error('Unhandled promise rejection', value);
        }
      });
      // Browsers should not trigger `rejectionHandled` event if it was handled here, NodeJS - should
      promise._h = isNode || isUnhandled(promise) ? 2 : 1;
    } promise._a = undefined;
    if (unhandled && result.e) throw result.v;
  });
};
var isUnhandled = function (promise) {
  if (promise._h == 1) return false;
  var chain = promise._a || promise._c;
  var i = 0;
  var reaction;
  while (chain.length > i) {
    reaction = chain[i++];
    if (reaction.fail || !isUnhandled(reaction.promise)) return false;
  } return true;
};
var onHandleUnhandled = function (promise) {
  task.call(global, function () {
    var handler;
    if (isNode) {
      process.emit('rejectionHandled', promise);
    } else if (handler = global.onrejectionhandled) {
      handler({ promise: promise, reason: promise._v });
    }
  });
};
var $reject = function (value) {
  var promise = this;
  if (promise._d) return;
  promise._d = true;
  promise = promise._w || promise; // unwrap
  promise._v = value;
  promise._s = 2;
  if (!promise._a) promise._a = promise._c.slice();
  notify(promise, true);
};
var $resolve = function (value) {
  var promise = this;
  var then;
  if (promise._d) return;
  promise._d = true;
  promise = promise._w || promise; // unwrap
  try {
    if (promise === value) throw TypeError("Promise can't be resolved itself");
    if (then = isThenable(value)) {
      microtask(function () {
        var wrapper = { _w: promise, _d: false }; // wrap
        try {
          then.call(value, ctx($resolve, wrapper, 1), ctx($reject, wrapper, 1));
        } catch (e) {
          $reject.call(wrapper, e);
        }
      });
    } else {
      promise._v = value;
      promise._s = 1;
      notify(promise, false);
    }
  } catch (e) {
    $reject.call({ _w: promise, _d: false }, e); // wrap
  }
};

// constructor polyfill
if (!USE_NATIVE) {
  // 25.4.3.1 Promise(executor)
  $Promise = function Promise(executor) {
    anInstance(this, $Promise, PROMISE, '_h');
    aFunction(executor);
    Internal.call(this);
    try {
      executor(ctx($resolve, this, 1), ctx($reject, this, 1));
    } catch (err) {
      $reject.call(this, err);
    }
  };
  // eslint-disable-next-line no-unused-vars
  Internal = function Promise(executor) {
    this._c = [];             // <- awaiting reactions
    this._a = undefined;      // <- checked in isUnhandled reactions
    this._s = 0;              // <- state
    this._d = false;          // <- done
    this._v = undefined;      // <- value
    this._h = 0;              // <- rejection state, 0 - default, 1 - handled, 2 - unhandled
    this._n = false;          // <- notify
  };
  Internal.prototype = __webpack_require__(45)($Promise.prototype, {
    // 25.4.5.3 Promise.prototype.then(onFulfilled, onRejected)
    then: function then(onFulfilled, onRejected) {
      var reaction = newPromiseCapability(speciesConstructor(this, $Promise));
      reaction.ok = typeof onFulfilled == 'function' ? onFulfilled : true;
      reaction.fail = typeof onRejected == 'function' && onRejected;
      reaction.domain = isNode ? process.domain : undefined;
      this._c.push(reaction);
      if (this._a) this._a.push(reaction);
      if (this._s) notify(this, false);
      return reaction.promise;
    },
    // 25.4.5.1 Promise.prototype.catch(onRejected)
    'catch': function (onRejected) {
      return this.then(undefined, onRejected);
    }
  });
  OwnPromiseCapability = function () {
    var promise = new Internal();
    this.promise = promise;
    this.resolve = ctx($resolve, promise, 1);
    this.reject = ctx($reject, promise, 1);
  };
  newPromiseCapabilityModule.f = newPromiseCapability = function (C) {
    return sameConstructor($Promise, C)
      ? new OwnPromiseCapability(C)
      : newGenericPromiseCapability(C);
  };
}

$export($export.G + $export.W + $export.F * !USE_NATIVE, { Promise: $Promise });
__webpack_require__(48)($Promise, PROMISE);
__webpack_require__(42)(PROMISE);
Wrapper = __webpack_require__(24)[PROMISE];

// statics
$export($export.S + $export.F * !USE_NATIVE, PROMISE, {
  // 25.4.4.5 Promise.reject(r)
  reject: function reject(r) {
    var capability = newPromiseCapability(this);
    var $$reject = capability.reject;
    $$reject(r);
    return capability.promise;
  }
});
$export($export.S + $export.F * (LIBRARY || !USE_NATIVE), PROMISE, {
  // 25.4.4.6 Promise.resolve(x)
  resolve: function resolve(x) {
    // instanceof instead of internal slot check because we should fix it without replacement native Promise core
    if (x instanceof $Promise && sameConstructor(x.constructor, this)) return x;
    return promiseResolve(this, x);
  }
});
$export($export.S + $export.F * !(USE_NATIVE && __webpack_require__(61)(function (iter) {
  $Promise.all(iter)['catch'](empty);
})), PROMISE, {
  // 25.4.4.1 Promise.all(iterable)
  all: function all(iterable) {
    var C = this;
    var capability = newPromiseCapability(C);
    var resolve = capability.resolve;
    var reject = capability.reject;
    var result = perform(function () {
      var values = [];
      var index = 0;
      var remaining = 1;
      forOf(iterable, false, function (promise) {
        var $index = index++;
        var alreadyCalled = false;
        values.push(undefined);
        remaining++;
        C.resolve(promise).then(function (value) {
          if (alreadyCalled) return;
          alreadyCalled = true;
          values[$index] = value;
          --remaining || resolve(values);
        }, reject);
      });
      --remaining || resolve(values);
    });
    if (result.e) reject(result.v);
    return capability.promise;
  },
  // 25.4.4.4 Promise.race(iterable)
  race: function race(iterable) {
    var C = this;
    var capability = newPromiseCapability(C);
    var reject = capability.reject;
    var result = perform(function () {
      forOf(iterable, false, function (promise) {
        C.resolve(promise).then(capability.resolve, reject);
      });
    });
    if (result.e) reject(result.v);
    return capability.promise;
  }
});


/***/ }),
/* 263 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var weak = __webpack_require__(131);
var validate = __webpack_require__(51);
var WEAK_SET = 'WeakSet';

// 23.4 WeakSet Objects
__webpack_require__(65)(WEAK_SET, function (get) {
  return function WeakSet() { return get(this, arguments.length > 0 ? arguments[0] : undefined); };
}, {
  // 23.4.3.1 WeakSet.prototype.add(value)
  add: function add(value) {
    return weak.def(validate(this, WEAK_SET), value, true);
  }
}, weak, false, true);


/***/ }),
/* 264 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(0);
var $typed = __webpack_require__(66);
var buffer = __webpack_require__(99);
var anObject = __webpack_require__(1);
var toAbsoluteIndex = __webpack_require__(39);
var toLength = __webpack_require__(9);
var isObject = __webpack_require__(4);
var ArrayBuffer = __webpack_require__(2).ArrayBuffer;
var speciesConstructor = __webpack_require__(64);
var $ArrayBuffer = buffer.ArrayBuffer;
var $DataView = buffer.DataView;
var $isView = $typed.ABV && ArrayBuffer.isView;
var $slice = $ArrayBuffer.prototype.slice;
var VIEW = $typed.VIEW;
var ARRAY_BUFFER = 'ArrayBuffer';

$export($export.G + $export.W + $export.F * (ArrayBuffer !== $ArrayBuffer), { ArrayBuffer: $ArrayBuffer });

$export($export.S + $export.F * !$typed.CONSTR, ARRAY_BUFFER, {
  // 24.1.3.1 ArrayBuffer.isView(arg)
  isView: function isView(it) {
    return $isView && $isView(it) || isObject(it) && VIEW in it;
  }
});

$export($export.P + $export.U + $export.F * __webpack_require__(3)(function () {
  return !new $ArrayBuffer(2).slice(1, undefined).byteLength;
}), ARRAY_BUFFER, {
  // 24.1.4.3 ArrayBuffer.prototype.slice(start, end)
  slice: function slice(start, end) {
    if ($slice !== undefined && end === undefined) return $slice.call(anObject(this), start); // FF fix
    var len = anObject(this).byteLength;
    var first = toAbsoluteIndex(start, len);
    var final = toAbsoluteIndex(end === undefined ? len : end, len);
    var result = new (speciesConstructor(this, $ArrayBuffer))(toLength(final - first));
    var viewS = new $DataView(this);
    var viewT = new $DataView(result);
    var index = 0;
    while (first < final) {
      viewT.setUint8(index++, viewS.getUint8(first++));
    } return result;
  }
});

__webpack_require__(42)(ARRAY_BUFFER);


/***/ }),
/* 265 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(0);
$export($export.G + $export.W + $export.F * !__webpack_require__(66).ABV, {
  DataView: __webpack_require__(99).DataView
});


/***/ }),
/* 266 */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(31)('Int8', 1, function (init) {
  return function Int8Array(data, byteOffset, length) {
    return init(this, data, byteOffset, length);
  };
});


/***/ }),
/* 267 */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(31)('Uint8', 1, function (init) {
  return function Uint8Array(data, byteOffset, length) {
    return init(this, data, byteOffset, length);
  };
});


/***/ }),
/* 268 */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(31)('Uint8', 1, function (init) {
  return function Uint8ClampedArray(data, byteOffset, length) {
    return init(this, data, byteOffset, length);
  };
}, true);


/***/ }),
/* 269 */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(31)('Int16', 2, function (init) {
  return function Int16Array(data, byteOffset, length) {
    return init(this, data, byteOffset, length);
  };
});


/***/ }),
/* 270 */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(31)('Uint16', 2, function (init) {
  return function Uint16Array(data, byteOffset, length) {
    return init(this, data, byteOffset, length);
  };
});


/***/ }),
/* 271 */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(31)('Int32', 4, function (init) {
  return function Int32Array(data, byteOffset, length) {
    return init(this, data, byteOffset, length);
  };
});


/***/ }),
/* 272 */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(31)('Uint32', 4, function (init) {
  return function Uint32Array(data, byteOffset, length) {
    return init(this, data, byteOffset, length);
  };
});


/***/ }),
/* 273 */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(31)('Float32', 4, function (init) {
  return function Float32Array(data, byteOffset, length) {
    return init(this, data, byteOffset, length);
  };
});


/***/ }),
/* 274 */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(31)('Float64', 8, function (init) {
  return function Float64Array(data, byteOffset, length) {
    return init(this, data, byteOffset, length);
  };
});


/***/ }),
/* 275 */
/***/ (function(module, exports, __webpack_require__) {

// 26.1.1 Reflect.apply(target, thisArgument, argumentsList)
var $export = __webpack_require__(0);
var aFunction = __webpack_require__(11);
var anObject = __webpack_require__(1);
var rApply = (__webpack_require__(2).Reflect || {}).apply;
var fApply = Function.apply;
// MS Edge argumentsList argument is optional
$export($export.S + $export.F * !__webpack_require__(3)(function () {
  rApply(function () { /* empty */ });
}), 'Reflect', {
  apply: function apply(target, thisArgument, argumentsList) {
    var T = aFunction(target);
    var L = anObject(argumentsList);
    return rApply ? rApply(T, thisArgument, L) : fApply.call(T, thisArgument, L);
  }
});


/***/ }),
/* 276 */
/***/ (function(module, exports, __webpack_require__) {

// 26.1.2 Reflect.construct(target, argumentsList [, newTarget])
var $export = __webpack_require__(0);
var create = __webpack_require__(40);
var aFunction = __webpack_require__(11);
var anObject = __webpack_require__(1);
var isObject = __webpack_require__(4);
var fails = __webpack_require__(3);
var bind = __webpack_require__(113);
var rConstruct = (__webpack_require__(2).Reflect || {}).construct;

// MS Edge supports only 2 arguments and argumentsList argument is optional
// FF Nightly sets third argument as `new.target`, but does not create `this` from it
var NEW_TARGET_BUG = fails(function () {
  function F() { /* empty */ }
  return !(rConstruct(function () { /* empty */ }, [], F) instanceof F);
});
var ARGS_BUG = !fails(function () {
  rConstruct(function () { /* empty */ });
});

$export($export.S + $export.F * (NEW_TARGET_BUG || ARGS_BUG), 'Reflect', {
  construct: function construct(Target, args /* , newTarget */) {
    aFunction(Target);
    anObject(args);
    var newTarget = arguments.length < 3 ? Target : aFunction(arguments[2]);
    if (ARGS_BUG && !NEW_TARGET_BUG) return rConstruct(Target, args, newTarget);
    if (Target == newTarget) {
      // w/o altered newTarget, optimization for 0-4 arguments
      switch (args.length) {
        case 0: return new Target();
        case 1: return new Target(args[0]);
        case 2: return new Target(args[0], args[1]);
        case 3: return new Target(args[0], args[1], args[2]);
        case 4: return new Target(args[0], args[1], args[2], args[3]);
      }
      // w/o altered newTarget, lot of arguments case
      var $args = [null];
      $args.push.apply($args, args);
      return new (bind.apply(Target, $args))();
    }
    // with altered newTarget, not support built-in constructors
    var proto = newTarget.prototype;
    var instance = create(isObject(proto) ? proto : Object.prototype);
    var result = Function.apply.call(Target, instance, args);
    return isObject(result) ? result : instance;
  }
});


/***/ }),
/* 277 */
/***/ (function(module, exports, __webpack_require__) {

// 26.1.3 Reflect.defineProperty(target, propertyKey, attributes)
var dP = __webpack_require__(8);
var $export = __webpack_require__(0);
var anObject = __webpack_require__(1);
var toPrimitive = __webpack_require__(25);

// MS Edge has broken Reflect.defineProperty - throwing instead of returning false
$export($export.S + $export.F * __webpack_require__(3)(function () {
  // eslint-disable-next-line no-undef
  Reflect.defineProperty(dP.f({}, 1, { value: 1 }), 1, { value: 2 });
}), 'Reflect', {
  defineProperty: function defineProperty(target, propertyKey, attributes) {
    anObject(target);
    propertyKey = toPrimitive(propertyKey, true);
    anObject(attributes);
    try {
      dP.f(target, propertyKey, attributes);
      return true;
    } catch (e) {
      return false;
    }
  }
});


/***/ }),
/* 278 */
/***/ (function(module, exports, __webpack_require__) {

// 26.1.4 Reflect.deleteProperty(target, propertyKey)
var $export = __webpack_require__(0);
var gOPD = __webpack_require__(17).f;
var anObject = __webpack_require__(1);

$export($export.S, 'Reflect', {
  deleteProperty: function deleteProperty(target, propertyKey) {
    var desc = gOPD(anObject(target), propertyKey);
    return desc && !desc.configurable ? false : delete target[propertyKey];
  }
});


/***/ }),
/* 279 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// 26.1.5 Reflect.enumerate(target)
var $export = __webpack_require__(0);
var anObject = __webpack_require__(1);
var Enumerate = function (iterated) {
  this._t = anObject(iterated); // target
  this._i = 0;                  // next index
  var keys = this._k = [];      // keys
  var key;
  for (key in iterated) keys.push(key);
};
__webpack_require__(87)(Enumerate, 'Object', function () {
  var that = this;
  var keys = that._k;
  var key;
  do {
    if (that._i >= keys.length) return { value: undefined, done: true };
  } while (!((key = keys[that._i++]) in that._t));
  return { value: key, done: false };
});

$export($export.S, 'Reflect', {
  enumerate: function enumerate(target) {
    return new Enumerate(target);
  }
});


/***/ }),
/* 280 */
/***/ (function(module, exports, __webpack_require__) {

// 26.1.6 Reflect.get(target, propertyKey [, receiver])
var gOPD = __webpack_require__(17);
var getPrototypeOf = __webpack_require__(18);
var has = __webpack_require__(12);
var $export = __webpack_require__(0);
var isObject = __webpack_require__(4);
var anObject = __webpack_require__(1);

function get(target, propertyKey /* , receiver */) {
  var receiver = arguments.length < 3 ? target : arguments[2];
  var desc, proto;
  if (anObject(target) === receiver) return target[propertyKey];
  if (desc = gOPD.f(target, propertyKey)) return has(desc, 'value')
    ? desc.value
    : desc.get !== undefined
      ? desc.get.call(receiver)
      : undefined;
  if (isObject(proto = getPrototypeOf(target))) return get(proto, propertyKey, receiver);
}

$export($export.S, 'Reflect', { get: get });


/***/ }),
/* 281 */
/***/ (function(module, exports, __webpack_require__) {

// 26.1.7 Reflect.getOwnPropertyDescriptor(target, propertyKey)
var gOPD = __webpack_require__(17);
var $export = __webpack_require__(0);
var anObject = __webpack_require__(1);

$export($export.S, 'Reflect', {
  getOwnPropertyDescriptor: function getOwnPropertyDescriptor(target, propertyKey) {
    return gOPD.f(anObject(target), propertyKey);
  }
});


/***/ }),
/* 282 */
/***/ (function(module, exports, __webpack_require__) {

// 26.1.8 Reflect.getPrototypeOf(target)
var $export = __webpack_require__(0);
var getProto = __webpack_require__(18);
var anObject = __webpack_require__(1);

$export($export.S, 'Reflect', {
  getPrototypeOf: function getPrototypeOf(target) {
    return getProto(anObject(target));
  }
});


/***/ }),
/* 283 */
/***/ (function(module, exports, __webpack_require__) {

// 26.1.9 Reflect.has(target, propertyKey)
var $export = __webpack_require__(0);

$export($export.S, 'Reflect', {
  has: function has(target, propertyKey) {
    return propertyKey in target;
  }
});


/***/ }),
/* 284 */
/***/ (function(module, exports, __webpack_require__) {

// 26.1.10 Reflect.isExtensible(target)
var $export = __webpack_require__(0);
var anObject = __webpack_require__(1);
var $isExtensible = Object.isExtensible;

$export($export.S, 'Reflect', {
  isExtensible: function isExtensible(target) {
    anObject(target);
    return $isExtensible ? $isExtensible(target) : true;
  }
});


/***/ }),
/* 285 */
/***/ (function(module, exports, __webpack_require__) {

// 26.1.11 Reflect.ownKeys(target)
var $export = __webpack_require__(0);

$export($export.S, 'Reflect', { ownKeys: __webpack_require__(133) });


/***/ }),
/* 286 */
/***/ (function(module, exports, __webpack_require__) {

// 26.1.12 Reflect.preventExtensions(target)
var $export = __webpack_require__(0);
var anObject = __webpack_require__(1);
var $preventExtensions = Object.preventExtensions;

$export($export.S, 'Reflect', {
  preventExtensions: function preventExtensions(target) {
    anObject(target);
    try {
      if ($preventExtensions) $preventExtensions(target);
      return true;
    } catch (e) {
      return false;
    }
  }
});


/***/ }),
/* 287 */
/***/ (function(module, exports, __webpack_require__) {

// 26.1.13 Reflect.set(target, propertyKey, V [, receiver])
var dP = __webpack_require__(8);
var gOPD = __webpack_require__(17);
var getPrototypeOf = __webpack_require__(18);
var has = __webpack_require__(12);
var $export = __webpack_require__(0);
var createDesc = __webpack_require__(36);
var anObject = __webpack_require__(1);
var isObject = __webpack_require__(4);

function set(target, propertyKey, V /* , receiver */) {
  var receiver = arguments.length < 4 ? target : arguments[3];
  var ownDesc = gOPD.f(anObject(target), propertyKey);
  var existingDescriptor, proto;
  if (!ownDesc) {
    if (isObject(proto = getPrototypeOf(target))) {
      return set(proto, propertyKey, V, receiver);
    }
    ownDesc = createDesc(0);
  }
  if (has(ownDesc, 'value')) {
    if (ownDesc.writable === false || !isObject(receiver)) return false;
    existingDescriptor = gOPD.f(receiver, propertyKey) || createDesc(0);
    existingDescriptor.value = V;
    dP.f(receiver, propertyKey, existingDescriptor);
    return true;
  }
  return ownDesc.set === undefined ? false : (ownDesc.set.call(receiver, V), true);
}

$export($export.S, 'Reflect', { set: set });


/***/ }),
/* 288 */
/***/ (function(module, exports, __webpack_require__) {

// 26.1.14 Reflect.setPrototypeOf(target, proto)
var $export = __webpack_require__(0);
var setProto = __webpack_require__(79);

if (setProto) $export($export.S, 'Reflect', {
  setPrototypeOf: function setPrototypeOf(target, proto) {
    setProto.check(target, proto);
    try {
      setProto.set(target, proto);
      return true;
    } catch (e) {
      return false;
    }
  }
});


/***/ }),
/* 289 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// https://github.com/tc39/Array.prototype.includes
var $export = __webpack_require__(0);
var $includes = __webpack_require__(56)(true);

$export($export.P, 'Array', {
  includes: function includes(el /* , fromIndex = 0 */) {
    return $includes(this, el, arguments.length > 1 ? arguments[1] : undefined);
  }
});

__webpack_require__(35)('includes');


/***/ }),
/* 290 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// https://tc39.github.io/proposal-flatMap/#sec-Array.prototype.flatMap
var $export = __webpack_require__(0);
var flattenIntoArray = __webpack_require__(134);
var toObject = __webpack_require__(10);
var toLength = __webpack_require__(9);
var aFunction = __webpack_require__(11);
var arraySpeciesCreate = __webpack_require__(93);

$export($export.P, 'Array', {
  flatMap: function flatMap(callbackfn /* , thisArg */) {
    var O = toObject(this);
    var sourceLen, A;
    aFunction(callbackfn);
    sourceLen = toLength(O.length);
    A = arraySpeciesCreate(O, 0);
    flattenIntoArray(A, O, O, sourceLen, 0, 1, callbackfn, arguments[1]);
    return A;
  }
});

__webpack_require__(35)('flatMap');


/***/ }),
/* 291 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// https://tc39.github.io/proposal-flatMap/#sec-Array.prototype.flatten
var $export = __webpack_require__(0);
var flattenIntoArray = __webpack_require__(134);
var toObject = __webpack_require__(10);
var toLength = __webpack_require__(9);
var toInteger = __webpack_require__(27);
var arraySpeciesCreate = __webpack_require__(93);

$export($export.P, 'Array', {
  flatten: function flatten(/* depthArg = 1 */) {
    var depthArg = arguments[0];
    var O = toObject(this);
    var sourceLen = toLength(O.length);
    var A = arraySpeciesCreate(O, 0);
    flattenIntoArray(A, O, O, sourceLen, 0, depthArg === undefined ? 1 : toInteger(depthArg));
    return A;
  }
});

__webpack_require__(35)('flatten');


/***/ }),
/* 292 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// https://github.com/mathiasbynens/String.prototype.at
var $export = __webpack_require__(0);
var $at = __webpack_require__(85)(true);

$export($export.P, 'String', {
  at: function at(pos) {
    return $at(this, pos);
  }
});


/***/ }),
/* 293 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// https://github.com/tc39/proposal-string-pad-start-end
var $export = __webpack_require__(0);
var $pad = __webpack_require__(135);

$export($export.P, 'String', {
  padStart: function padStart(maxLength /* , fillString = ' ' */) {
    return $pad(this, maxLength, arguments.length > 1 ? arguments[1] : undefined, true);
  }
});


/***/ }),
/* 294 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// https://github.com/tc39/proposal-string-pad-start-end
var $export = __webpack_require__(0);
var $pad = __webpack_require__(135);

$export($export.P, 'String', {
  padEnd: function padEnd(maxLength /* , fillString = ' ' */) {
    return $pad(this, maxLength, arguments.length > 1 ? arguments[1] : undefined, false);
  }
});


/***/ }),
/* 295 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// https://github.com/sebmarkbage/ecmascript-string-left-right-trim
__webpack_require__(49)('trimLeft', function ($trim) {
  return function trimLeft() {
    return $trim(this, 1);
  };
}, 'trimStart');


/***/ }),
/* 296 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// https://github.com/sebmarkbage/ecmascript-string-left-right-trim
__webpack_require__(49)('trimRight', function ($trim) {
  return function trimRight() {
    return $trim(this, 2);
  };
}, 'trimEnd');


/***/ }),
/* 297 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// https://tc39.github.io/String.prototype.matchAll/
var $export = __webpack_require__(0);
var defined = __webpack_require__(26);
var toLength = __webpack_require__(9);
var isRegExp = __webpack_require__(60);
var getFlags = __webpack_require__(62);
var RegExpProto = RegExp.prototype;

var $RegExpStringIterator = function (regexp, string) {
  this._r = regexp;
  this._s = string;
};

__webpack_require__(87)($RegExpStringIterator, 'RegExp String', function next() {
  var match = this._r.exec(this._s);
  return { value: match, done: match === null };
});

$export($export.P, 'String', {
  matchAll: function matchAll(regexp) {
    defined(this);
    if (!isRegExp(regexp)) throw TypeError(regexp + ' is not a regexp!');
    var S = String(this);
    var flags = 'flags' in RegExpProto ? String(regexp.flags) : getFlags.call(regexp);
    var rx = new RegExp(regexp.source, ~flags.indexOf('g') ? flags : 'g' + flags);
    rx.lastIndex = toLength(regexp.lastIndex);
    return new $RegExpStringIterator(rx, S);
  }
});


/***/ }),
/* 298 */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(75)('asyncIterator');


/***/ }),
/* 299 */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(75)('observable');


/***/ }),
/* 300 */
/***/ (function(module, exports, __webpack_require__) {

// https://github.com/tc39/proposal-object-getownpropertydescriptors
var $export = __webpack_require__(0);
var ownKeys = __webpack_require__(133);
var toIObject = __webpack_require__(15);
var gOPD = __webpack_require__(17);
var createProperty = __webpack_require__(91);

$export($export.S, 'Object', {
  getOwnPropertyDescriptors: function getOwnPropertyDescriptors(object) {
    var O = toIObject(object);
    var getDesc = gOPD.f;
    var keys = ownKeys(O);
    var result = {};
    var i = 0;
    var key, desc;
    while (keys.length > i) {
      desc = getDesc(O, key = keys[i++]);
      if (desc !== undefined) createProperty(result, key, desc);
    }
    return result;
  }
});


/***/ }),
/* 301 */
/***/ (function(module, exports, __webpack_require__) {

// https://github.com/tc39/proposal-object-values-entries
var $export = __webpack_require__(0);
var $values = __webpack_require__(136)(false);

$export($export.S, 'Object', {
  values: function values(it) {
    return $values(it);
  }
});


/***/ }),
/* 302 */
/***/ (function(module, exports, __webpack_require__) {

// https://github.com/tc39/proposal-object-values-entries
var $export = __webpack_require__(0);
var $entries = __webpack_require__(136)(true);

$export($export.S, 'Object', {
  entries: function entries(it) {
    return $entries(it);
  }
});


/***/ }),
/* 303 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(0);
var toObject = __webpack_require__(10);
var aFunction = __webpack_require__(11);
var $defineProperty = __webpack_require__(8);

// B.2.2.2 Object.prototype.__defineGetter__(P, getter)
__webpack_require__(7) && $export($export.P + __webpack_require__(67), 'Object', {
  __defineGetter__: function __defineGetter__(P, getter) {
    $defineProperty.f(toObject(this), P, { get: aFunction(getter), enumerable: true, configurable: true });
  }
});


/***/ }),
/* 304 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(0);
var toObject = __webpack_require__(10);
var aFunction = __webpack_require__(11);
var $defineProperty = __webpack_require__(8);

// B.2.2.3 Object.prototype.__defineSetter__(P, setter)
__webpack_require__(7) && $export($export.P + __webpack_require__(67), 'Object', {
  __defineSetter__: function __defineSetter__(P, setter) {
    $defineProperty.f(toObject(this), P, { set: aFunction(setter), enumerable: true, configurable: true });
  }
});


/***/ }),
/* 305 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(0);
var toObject = __webpack_require__(10);
var toPrimitive = __webpack_require__(25);
var getPrototypeOf = __webpack_require__(18);
var getOwnPropertyDescriptor = __webpack_require__(17).f;

// B.2.2.4 Object.prototype.__lookupGetter__(P)
__webpack_require__(7) && $export($export.P + __webpack_require__(67), 'Object', {
  __lookupGetter__: function __lookupGetter__(P) {
    var O = toObject(this);
    var K = toPrimitive(P, true);
    var D;
    do {
      if (D = getOwnPropertyDescriptor(O, K)) return D.get;
    } while (O = getPrototypeOf(O));
  }
});


/***/ }),
/* 306 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(0);
var toObject = __webpack_require__(10);
var toPrimitive = __webpack_require__(25);
var getPrototypeOf = __webpack_require__(18);
var getOwnPropertyDescriptor = __webpack_require__(17).f;

// B.2.2.5 Object.prototype.__lookupSetter__(P)
__webpack_require__(7) && $export($export.P + __webpack_require__(67), 'Object', {
  __lookupSetter__: function __lookupSetter__(P) {
    var O = toObject(this);
    var K = toPrimitive(P, true);
    var D;
    do {
      if (D = getOwnPropertyDescriptor(O, K)) return D.set;
    } while (O = getPrototypeOf(O));
  }
});


/***/ }),
/* 307 */
/***/ (function(module, exports, __webpack_require__) {

// https://github.com/DavidBruant/Map-Set.prototype.toJSON
var $export = __webpack_require__(0);

$export($export.P + $export.R, 'Map', { toJSON: __webpack_require__(137)('Map') });


/***/ }),
/* 308 */
/***/ (function(module, exports, __webpack_require__) {

// https://github.com/DavidBruant/Map-Set.prototype.toJSON
var $export = __webpack_require__(0);

$export($export.P + $export.R, 'Set', { toJSON: __webpack_require__(137)('Set') });


/***/ }),
/* 309 */
/***/ (function(module, exports, __webpack_require__) {

// https://tc39.github.io/proposal-setmap-offrom/#sec-map.of
__webpack_require__(68)('Map');


/***/ }),
/* 310 */
/***/ (function(module, exports, __webpack_require__) {

// https://tc39.github.io/proposal-setmap-offrom/#sec-set.of
__webpack_require__(68)('Set');


/***/ }),
/* 311 */
/***/ (function(module, exports, __webpack_require__) {

// https://tc39.github.io/proposal-setmap-offrom/#sec-weakmap.of
__webpack_require__(68)('WeakMap');


/***/ }),
/* 312 */
/***/ (function(module, exports, __webpack_require__) {

// https://tc39.github.io/proposal-setmap-offrom/#sec-weakset.of
__webpack_require__(68)('WeakSet');


/***/ }),
/* 313 */
/***/ (function(module, exports, __webpack_require__) {

// https://tc39.github.io/proposal-setmap-offrom/#sec-map.from
__webpack_require__(69)('Map');


/***/ }),
/* 314 */
/***/ (function(module, exports, __webpack_require__) {

// https://tc39.github.io/proposal-setmap-offrom/#sec-set.from
__webpack_require__(69)('Set');


/***/ }),
/* 315 */
/***/ (function(module, exports, __webpack_require__) {

// https://tc39.github.io/proposal-setmap-offrom/#sec-weakmap.from
__webpack_require__(69)('WeakMap');


/***/ }),
/* 316 */
/***/ (function(module, exports, __webpack_require__) {

// https://tc39.github.io/proposal-setmap-offrom/#sec-weakset.from
__webpack_require__(69)('WeakSet');


/***/ }),
/* 317 */
/***/ (function(module, exports, __webpack_require__) {

// https://github.com/tc39/proposal-global
var $export = __webpack_require__(0);

$export($export.G, { global: __webpack_require__(2) });


/***/ }),
/* 318 */
/***/ (function(module, exports, __webpack_require__) {

// https://github.com/tc39/proposal-global
var $export = __webpack_require__(0);

$export($export.S, 'System', { global: __webpack_require__(2) });


/***/ }),
/* 319 */
/***/ (function(module, exports, __webpack_require__) {

// https://github.com/ljharb/proposal-is-error
var $export = __webpack_require__(0);
var cof = __webpack_require__(20);

$export($export.S, 'Error', {
  isError: function isError(it) {
    return cof(it) === 'Error';
  }
});


/***/ }),
/* 320 */
/***/ (function(module, exports, __webpack_require__) {

// https://rwaldron.github.io/proposal-math-extensions/
var $export = __webpack_require__(0);

$export($export.S, 'Math', {
  clamp: function clamp(x, lower, upper) {
    return Math.min(upper, Math.max(lower, x));
  }
});


/***/ }),
/* 321 */
/***/ (function(module, exports, __webpack_require__) {

// https://rwaldron.github.io/proposal-math-extensions/
var $export = __webpack_require__(0);

$export($export.S, 'Math', { DEG_PER_RAD: Math.PI / 180 });


/***/ }),
/* 322 */
/***/ (function(module, exports, __webpack_require__) {

// https://rwaldron.github.io/proposal-math-extensions/
var $export = __webpack_require__(0);
var RAD_PER_DEG = 180 / Math.PI;

$export($export.S, 'Math', {
  degrees: function degrees(radians) {
    return radians * RAD_PER_DEG;
  }
});


/***/ }),
/* 323 */
/***/ (function(module, exports, __webpack_require__) {

// https://rwaldron.github.io/proposal-math-extensions/
var $export = __webpack_require__(0);
var scale = __webpack_require__(139);
var fround = __webpack_require__(119);

$export($export.S, 'Math', {
  fscale: function fscale(x, inLow, inHigh, outLow, outHigh) {
    return fround(scale(x, inLow, inHigh, outLow, outHigh));
  }
});


/***/ }),
/* 324 */
/***/ (function(module, exports, __webpack_require__) {

// https://gist.github.com/BrendanEich/4294d5c212a6d2254703
var $export = __webpack_require__(0);

$export($export.S, 'Math', {
  iaddh: function iaddh(x0, x1, y0, y1) {
    var $x0 = x0 >>> 0;
    var $x1 = x1 >>> 0;
    var $y0 = y0 >>> 0;
    return $x1 + (y1 >>> 0) + (($x0 & $y0 | ($x0 | $y0) & ~($x0 + $y0 >>> 0)) >>> 31) | 0;
  }
});


/***/ }),
/* 325 */
/***/ (function(module, exports, __webpack_require__) {

// https://gist.github.com/BrendanEich/4294d5c212a6d2254703
var $export = __webpack_require__(0);

$export($export.S, 'Math', {
  isubh: function isubh(x0, x1, y0, y1) {
    var $x0 = x0 >>> 0;
    var $x1 = x1 >>> 0;
    var $y0 = y0 >>> 0;
    return $x1 - (y1 >>> 0) - ((~$x0 & $y0 | ~($x0 ^ $y0) & $x0 - $y0 >>> 0) >>> 31) | 0;
  }
});


/***/ }),
/* 326 */
/***/ (function(module, exports, __webpack_require__) {

// https://gist.github.com/BrendanEich/4294d5c212a6d2254703
var $export = __webpack_require__(0);

$export($export.S, 'Math', {
  imulh: function imulh(u, v) {
    var UINT16 = 0xffff;
    var $u = +u;
    var $v = +v;
    var u0 = $u & UINT16;
    var v0 = $v & UINT16;
    var u1 = $u >> 16;
    var v1 = $v >> 16;
    var t = (u1 * v0 >>> 0) + (u0 * v0 >>> 16);
    return u1 * v1 + (t >> 16) + ((u0 * v1 >>> 0) + (t & UINT16) >> 16);
  }
});


/***/ }),
/* 327 */
/***/ (function(module, exports, __webpack_require__) {

// https://rwaldron.github.io/proposal-math-extensions/
var $export = __webpack_require__(0);

$export($export.S, 'Math', { RAD_PER_DEG: 180 / Math.PI });


/***/ }),
/* 328 */
/***/ (function(module, exports, __webpack_require__) {

// https://rwaldron.github.io/proposal-math-extensions/
var $export = __webpack_require__(0);
var DEG_PER_RAD = Math.PI / 180;

$export($export.S, 'Math', {
  radians: function radians(degrees) {
    return degrees * DEG_PER_RAD;
  }
});


/***/ }),
/* 329 */
/***/ (function(module, exports, __webpack_require__) {

// https://rwaldron.github.io/proposal-math-extensions/
var $export = __webpack_require__(0);

$export($export.S, 'Math', { scale: __webpack_require__(139) });


/***/ }),
/* 330 */
/***/ (function(module, exports, __webpack_require__) {

// https://gist.github.com/BrendanEich/4294d5c212a6d2254703
var $export = __webpack_require__(0);

$export($export.S, 'Math', {
  umulh: function umulh(u, v) {
    var UINT16 = 0xffff;
    var $u = +u;
    var $v = +v;
    var u0 = $u & UINT16;
    var v0 = $v & UINT16;
    var u1 = $u >>> 16;
    var v1 = $v >>> 16;
    var t = (u1 * v0 >>> 0) + (u0 * v0 >>> 16);
    return u1 * v1 + (t >>> 16) + ((u0 * v1 >>> 0) + (t & UINT16) >>> 16);
  }
});


/***/ }),
/* 331 */
/***/ (function(module, exports, __webpack_require__) {

// http://jfbastien.github.io/papers/Math.signbit.html
var $export = __webpack_require__(0);

$export($export.S, 'Math', { signbit: function signbit(x) {
  // eslint-disable-next-line no-self-compare
  return (x = +x) != x ? x : x == 0 ? 1 / x == Infinity : x > 0;
} });


/***/ }),
/* 332 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
// https://github.com/tc39/proposal-promise-finally

var $export = __webpack_require__(0);
var core = __webpack_require__(24);
var global = __webpack_require__(2);
var speciesConstructor = __webpack_require__(64);
var promiseResolve = __webpack_require__(126);

$export($export.P + $export.R, 'Promise', { 'finally': function (onFinally) {
  var C = speciesConstructor(this, core.Promise || global.Promise);
  var isFunction = typeof onFinally == 'function';
  return this.then(
    isFunction ? function (x) {
      return promiseResolve(C, onFinally()).then(function () { return x; });
    } : onFinally,
    isFunction ? function (e) {
      return promiseResolve(C, onFinally()).then(function () { throw e; });
    } : onFinally
  );
} });


/***/ }),
/* 333 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// https://github.com/tc39/proposal-promise-try
var $export = __webpack_require__(0);
var newPromiseCapability = __webpack_require__(98);
var perform = __webpack_require__(125);

$export($export.S, 'Promise', { 'try': function (callbackfn) {
  var promiseCapability = newPromiseCapability.f(this);
  var result = perform(callbackfn);
  (result.e ? promiseCapability.reject : promiseCapability.resolve)(result.v);
  return promiseCapability.promise;
} });


/***/ }),
/* 334 */
/***/ (function(module, exports, __webpack_require__) {

var metadata = __webpack_require__(32);
var anObject = __webpack_require__(1);
var toMetaKey = metadata.key;
var ordinaryDefineOwnMetadata = metadata.set;

metadata.exp({ defineMetadata: function defineMetadata(metadataKey, metadataValue, target, targetKey) {
  ordinaryDefineOwnMetadata(metadataKey, metadataValue, anObject(target), toMetaKey(targetKey));
} });


/***/ }),
/* 335 */
/***/ (function(module, exports, __webpack_require__) {

var metadata = __webpack_require__(32);
var anObject = __webpack_require__(1);
var toMetaKey = metadata.key;
var getOrCreateMetadataMap = metadata.map;
var store = metadata.store;

metadata.exp({ deleteMetadata: function deleteMetadata(metadataKey, target /* , targetKey */) {
  var targetKey = arguments.length < 3 ? undefined : toMetaKey(arguments[2]);
  var metadataMap = getOrCreateMetadataMap(anObject(target), targetKey, false);
  if (metadataMap === undefined || !metadataMap['delete'](metadataKey)) return false;
  if (metadataMap.size) return true;
  var targetMetadata = store.get(target);
  targetMetadata['delete'](targetKey);
  return !!targetMetadata.size || store['delete'](target);
} });


/***/ }),
/* 336 */
/***/ (function(module, exports, __webpack_require__) {

var metadata = __webpack_require__(32);
var anObject = __webpack_require__(1);
var getPrototypeOf = __webpack_require__(18);
var ordinaryHasOwnMetadata = metadata.has;
var ordinaryGetOwnMetadata = metadata.get;
var toMetaKey = metadata.key;

var ordinaryGetMetadata = function (MetadataKey, O, P) {
  var hasOwn = ordinaryHasOwnMetadata(MetadataKey, O, P);
  if (hasOwn) return ordinaryGetOwnMetadata(MetadataKey, O, P);
  var parent = getPrototypeOf(O);
  return parent !== null ? ordinaryGetMetadata(MetadataKey, parent, P) : undefined;
};

metadata.exp({ getMetadata: function getMetadata(metadataKey, target /* , targetKey */) {
  return ordinaryGetMetadata(metadataKey, anObject(target), arguments.length < 3 ? undefined : toMetaKey(arguments[2]));
} });


/***/ }),
/* 337 */
/***/ (function(module, exports, __webpack_require__) {

var Set = __webpack_require__(129);
var from = __webpack_require__(138);
var metadata = __webpack_require__(32);
var anObject = __webpack_require__(1);
var getPrototypeOf = __webpack_require__(18);
var ordinaryOwnMetadataKeys = metadata.keys;
var toMetaKey = metadata.key;

var ordinaryMetadataKeys = function (O, P) {
  var oKeys = ordinaryOwnMetadataKeys(O, P);
  var parent = getPrototypeOf(O);
  if (parent === null) return oKeys;
  var pKeys = ordinaryMetadataKeys(parent, P);
  return pKeys.length ? oKeys.length ? from(new Set(oKeys.concat(pKeys))) : pKeys : oKeys;
};

metadata.exp({ getMetadataKeys: function getMetadataKeys(target /* , targetKey */) {
  return ordinaryMetadataKeys(anObject(target), arguments.length < 2 ? undefined : toMetaKey(arguments[1]));
} });


/***/ }),
/* 338 */
/***/ (function(module, exports, __webpack_require__) {

var metadata = __webpack_require__(32);
var anObject = __webpack_require__(1);
var ordinaryGetOwnMetadata = metadata.get;
var toMetaKey = metadata.key;

metadata.exp({ getOwnMetadata: function getOwnMetadata(metadataKey, target /* , targetKey */) {
  return ordinaryGetOwnMetadata(metadataKey, anObject(target)
    , arguments.length < 3 ? undefined : toMetaKey(arguments[2]));
} });


/***/ }),
/* 339 */
/***/ (function(module, exports, __webpack_require__) {

var metadata = __webpack_require__(32);
var anObject = __webpack_require__(1);
var ordinaryOwnMetadataKeys = metadata.keys;
var toMetaKey = metadata.key;

metadata.exp({ getOwnMetadataKeys: function getOwnMetadataKeys(target /* , targetKey */) {
  return ordinaryOwnMetadataKeys(anObject(target), arguments.length < 2 ? undefined : toMetaKey(arguments[1]));
} });


/***/ }),
/* 340 */
/***/ (function(module, exports, __webpack_require__) {

var metadata = __webpack_require__(32);
var anObject = __webpack_require__(1);
var getPrototypeOf = __webpack_require__(18);
var ordinaryHasOwnMetadata = metadata.has;
var toMetaKey = metadata.key;

var ordinaryHasMetadata = function (MetadataKey, O, P) {
  var hasOwn = ordinaryHasOwnMetadata(MetadataKey, O, P);
  if (hasOwn) return true;
  var parent = getPrototypeOf(O);
  return parent !== null ? ordinaryHasMetadata(MetadataKey, parent, P) : false;
};

metadata.exp({ hasMetadata: function hasMetadata(metadataKey, target /* , targetKey */) {
  return ordinaryHasMetadata(metadataKey, anObject(target), arguments.length < 3 ? undefined : toMetaKey(arguments[2]));
} });


/***/ }),
/* 341 */
/***/ (function(module, exports, __webpack_require__) {

var metadata = __webpack_require__(32);
var anObject = __webpack_require__(1);
var ordinaryHasOwnMetadata = metadata.has;
var toMetaKey = metadata.key;

metadata.exp({ hasOwnMetadata: function hasOwnMetadata(metadataKey, target /* , targetKey */) {
  return ordinaryHasOwnMetadata(metadataKey, anObject(target)
    , arguments.length < 3 ? undefined : toMetaKey(arguments[2]));
} });


/***/ }),
/* 342 */
/***/ (function(module, exports, __webpack_require__) {

var $metadata = __webpack_require__(32);
var anObject = __webpack_require__(1);
var aFunction = __webpack_require__(11);
var toMetaKey = $metadata.key;
var ordinaryDefineOwnMetadata = $metadata.set;

$metadata.exp({ metadata: function metadata(metadataKey, metadataValue) {
  return function decorator(target, targetKey) {
    ordinaryDefineOwnMetadata(
      metadataKey, metadataValue,
      (targetKey !== undefined ? anObject : aFunction)(target),
      toMetaKey(targetKey)
    );
  };
} });


/***/ }),
/* 343 */
/***/ (function(module, exports, __webpack_require__) {

// https://github.com/rwaldron/tc39-notes/blob/master/es6/2014-09/sept-25.md#510-globalasap-for-enqueuing-a-microtask
var $export = __webpack_require__(0);
var microtask = __webpack_require__(97)();
var process = __webpack_require__(2).process;
var isNode = __webpack_require__(20)(process) == 'process';

$export($export.G, {
  asap: function asap(fn) {
    var domain = isNode && process.domain;
    microtask(domain ? domain.bind(fn) : fn);
  }
});


/***/ }),
/* 344 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// https://github.com/zenparsing/es-observable
var $export = __webpack_require__(0);
var global = __webpack_require__(2);
var core = __webpack_require__(24);
var microtask = __webpack_require__(97)();
var OBSERVABLE = __webpack_require__(5)('observable');
var aFunction = __webpack_require__(11);
var anObject = __webpack_require__(1);
var anInstance = __webpack_require__(43);
var redefineAll = __webpack_require__(45);
var hide = __webpack_require__(13);
var forOf = __webpack_require__(44);
var RETURN = forOf.RETURN;

var getMethod = function (fn) {
  return fn == null ? undefined : aFunction(fn);
};

var cleanupSubscription = function (subscription) {
  var cleanup = subscription._c;
  if (cleanup) {
    subscription._c = undefined;
    cleanup();
  }
};

var subscriptionClosed = function (subscription) {
  return subscription._o === undefined;
};

var closeSubscription = function (subscription) {
  if (!subscriptionClosed(subscription)) {
    subscription._o = undefined;
    cleanupSubscription(subscription);
  }
};

var Subscription = function (observer, subscriber) {
  anObject(observer);
  this._c = undefined;
  this._o = observer;
  observer = new SubscriptionObserver(this);
  try {
    var cleanup = subscriber(observer);
    var subscription = cleanup;
    if (cleanup != null) {
      if (typeof cleanup.unsubscribe === 'function') cleanup = function () { subscription.unsubscribe(); };
      else aFunction(cleanup);
      this._c = cleanup;
    }
  } catch (e) {
    observer.error(e);
    return;
  } if (subscriptionClosed(this)) cleanupSubscription(this);
};

Subscription.prototype = redefineAll({}, {
  unsubscribe: function unsubscribe() { closeSubscription(this); }
});

var SubscriptionObserver = function (subscription) {
  this._s = subscription;
};

SubscriptionObserver.prototype = redefineAll({}, {
  next: function next(value) {
    var subscription = this._s;
    if (!subscriptionClosed(subscription)) {
      var observer = subscription._o;
      try {
        var m = getMethod(observer.next);
        if (m) return m.call(observer, value);
      } catch (e) {
        try {
          closeSubscription(subscription);
        } finally {
          throw e;
        }
      }
    }
  },
  error: function error(value) {
    var subscription = this._s;
    if (subscriptionClosed(subscription)) throw value;
    var observer = subscription._o;
    subscription._o = undefined;
    try {
      var m = getMethod(observer.error);
      if (!m) throw value;
      value = m.call(observer, value);
    } catch (e) {
      try {
        cleanupSubscription(subscription);
      } finally {
        throw e;
      }
    } cleanupSubscription(subscription);
    return value;
  },
  complete: function complete(value) {
    var subscription = this._s;
    if (!subscriptionClosed(subscription)) {
      var observer = subscription._o;
      subscription._o = undefined;
      try {
        var m = getMethod(observer.complete);
        value = m ? m.call(observer, value) : undefined;
      } catch (e) {
        try {
          cleanupSubscription(subscription);
        } finally {
          throw e;
        }
      } cleanupSubscription(subscription);
      return value;
    }
  }
});

var $Observable = function Observable(subscriber) {
  anInstance(this, $Observable, 'Observable', '_f')._f = aFunction(subscriber);
};

redefineAll($Observable.prototype, {
  subscribe: function subscribe(observer) {
    return new Subscription(observer, this._f);
  },
  forEach: function forEach(fn) {
    var that = this;
    return new (core.Promise || global.Promise)(function (resolve, reject) {
      aFunction(fn);
      var subscription = that.subscribe({
        next: function (value) {
          try {
            return fn(value);
          } catch (e) {
            reject(e);
            subscription.unsubscribe();
          }
        },
        error: reject,
        complete: resolve
      });
    });
  }
});

redefineAll($Observable, {
  from: function from(x) {
    var C = typeof this === 'function' ? this : $Observable;
    var method = getMethod(anObject(x)[OBSERVABLE]);
    if (method) {
      var observable = anObject(method.call(x));
      return observable.constructor === C ? observable : new C(function (observer) {
        return observable.subscribe(observer);
      });
    }
    return new C(function (observer) {
      var done = false;
      microtask(function () {
        if (!done) {
          try {
            if (forOf(x, false, function (it) {
              observer.next(it);
              if (done) return RETURN;
            }) === RETURN) return;
          } catch (e) {
            if (done) throw e;
            observer.error(e);
            return;
          } observer.complete();
        }
      });
      return function () { done = true; };
    });
  },
  of: function of() {
    for (var i = 0, l = arguments.length, items = Array(l); i < l;) items[i] = arguments[i++];
    return new (typeof this === 'function' ? this : $Observable)(function (observer) {
      var done = false;
      microtask(function () {
        if (!done) {
          for (var j = 0; j < items.length; ++j) {
            observer.next(items[j]);
            if (done) return;
          } observer.complete();
        }
      });
      return function () { done = true; };
    });
  }
});

hide($Observable.prototype, OBSERVABLE, function () { return this; });

$export($export.G, { Observable: $Observable });

__webpack_require__(42)('Observable');


/***/ }),
/* 345 */
/***/ (function(module, exports, __webpack_require__) {

// ie9- setTimeout & setInterval additional parameters fix
var global = __webpack_require__(2);
var $export = __webpack_require__(0);
var invoke = __webpack_require__(59);
var partial = __webpack_require__(346);
var navigator = global.navigator;
var MSIE = !!navigator && /MSIE .\./.test(navigator.userAgent); // <- dirty ie9- check
var wrap = function (set) {
  return MSIE ? function (fn, time /* , ...args */) {
    return set(invoke(
      partial,
      [].slice.call(arguments, 2),
      // eslint-disable-next-line no-new-func
      typeof fn == 'function' ? fn : Function(fn)
    ), time);
  } : set;
};
$export($export.G + $export.B + $export.F * MSIE, {
  setTimeout: wrap(global.setTimeout),
  setInterval: wrap(global.setInterval)
});


/***/ }),
/* 346 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var path = __webpack_require__(347);
var invoke = __webpack_require__(59);
var aFunction = __webpack_require__(11);
module.exports = function (/* ...pargs */) {
  var fn = aFunction(this);
  var length = arguments.length;
  var pargs = Array(length);
  var i = 0;
  var _ = path._;
  var holder = false;
  while (length > i) if ((pargs[i] = arguments[i++]) === _) holder = true;
  return function (/* ...args */) {
    var that = this;
    var aLen = arguments.length;
    var j = 0;
    var k = 0;
    var args;
    if (!holder && !aLen) return invoke(fn, pargs, that);
    args = pargs.slice();
    if (holder) for (;length > j; j++) if (args[j] === _) args[j] = arguments[k++];
    while (aLen > k) args.push(arguments[k++]);
    return invoke(fn, args, that);
  };
};


/***/ }),
/* 347 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(2);


/***/ }),
/* 348 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(0);
var $task = __webpack_require__(96);
$export($export.G + $export.B, {
  setImmediate: $task.set,
  clearImmediate: $task.clear
});


/***/ }),
/* 349 */
/***/ (function(module, exports, __webpack_require__) {

var $iterators = __webpack_require__(95);
var getKeys = __webpack_require__(34);
var redefine = __webpack_require__(14);
var global = __webpack_require__(2);
var hide = __webpack_require__(13);
var Iterators = __webpack_require__(50);
var wks = __webpack_require__(5);
var ITERATOR = wks('iterator');
var TO_STRING_TAG = wks('toStringTag');
var ArrayValues = Iterators.Array;

var DOMIterables = {
  CSSRuleList: true, // TODO: Not spec compliant, should be false.
  CSSStyleDeclaration: false,
  CSSValueList: false,
  ClientRectList: false,
  DOMRectList: false,
  DOMStringList: false,
  DOMTokenList: true,
  DataTransferItemList: false,
  FileList: false,
  HTMLAllCollection: false,
  HTMLCollection: false,
  HTMLFormElement: false,
  HTMLSelectElement: false,
  MediaList: true, // TODO: Not spec compliant, should be false.
  MimeTypeArray: false,
  NamedNodeMap: false,
  NodeList: true,
  PaintRequestList: false,
  Plugin: false,
  PluginArray: false,
  SVGLengthList: false,
  SVGNumberList: false,
  SVGPathSegList: false,
  SVGPointList: false,
  SVGStringList: false,
  SVGTransformList: false,
  SourceBufferList: false,
  StyleSheetList: true, // TODO: Not spec compliant, should be false.
  TextTrackCueList: false,
  TextTrackList: false,
  TouchList: false
};

for (var collections = getKeys(DOMIterables), i = 0; i < collections.length; i++) {
  var NAME = collections[i];
  var explicit = DOMIterables[NAME];
  var Collection = global[NAME];
  var proto = Collection && Collection.prototype;
  var key;
  if (proto) {
    if (!proto[ITERATOR]) hide(proto, ITERATOR, ArrayValues);
    if (!proto[TO_STRING_TAG]) hide(proto, TO_STRING_TAG, NAME);
    Iterators[NAME] = ArrayValues;
    if (explicit) for (key in $iterators) if (!proto[key]) redefine(proto, key, $iterators[key], true);
  }
}


/***/ }),
/* 350 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function(global) {/**
 * Copyright (c) 2014, Facebook, Inc.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * https://raw.github.com/facebook/regenerator/master/LICENSE file. An
 * additional grant of patent rights can be found in the PATENTS file in
 * the same directory.
 */

!(function(global) {
  "use strict";

  var Op = Object.prototype;
  var hasOwn = Op.hasOwnProperty;
  var undefined; // More compressible than void 0.
  var $Symbol = typeof Symbol === "function" ? Symbol : {};
  var iteratorSymbol = $Symbol.iterator || "@@iterator";
  var asyncIteratorSymbol = $Symbol.asyncIterator || "@@asyncIterator";
  var toStringTagSymbol = $Symbol.toStringTag || "@@toStringTag";

  var inModule = typeof module === "object";
  var runtime = global.regeneratorRuntime;
  if (runtime) {
    if (inModule) {
      // If regeneratorRuntime is defined globally and we're in a module,
      // make the exports object identical to regeneratorRuntime.
      module.exports = runtime;
    }
    // Don't bother evaluating the rest of this file if the runtime was
    // already defined globally.
    return;
  }

  // Define the runtime globally (as expected by generated code) as either
  // module.exports (if we're in a module) or a new, empty object.
  runtime = global.regeneratorRuntime = inModule ? module.exports : {};

  function wrap(innerFn, outerFn, self, tryLocsList) {
    // If outerFn provided and outerFn.prototype is a Generator, then outerFn.prototype instanceof Generator.
    var protoGenerator = outerFn && outerFn.prototype instanceof Generator ? outerFn : Generator;
    var generator = Object.create(protoGenerator.prototype);
    var context = new Context(tryLocsList || []);

    // The ._invoke method unifies the implementations of the .next,
    // .throw, and .return methods.
    generator._invoke = makeInvokeMethod(innerFn, self, context);

    return generator;
  }
  runtime.wrap = wrap;

  // Try/catch helper to minimize deoptimizations. Returns a completion
  // record like context.tryEntries[i].completion. This interface could
  // have been (and was previously) designed to take a closure to be
  // invoked without arguments, but in all the cases we care about we
  // already have an existing method we want to call, so there's no need
  // to create a new function object. We can even get away with assuming
  // the method takes exactly one argument, since that happens to be true
  // in every case, so we don't have to touch the arguments object. The
  // only additional allocation required is the completion record, which
  // has a stable shape and so hopefully should be cheap to allocate.
  function tryCatch(fn, obj, arg) {
    try {
      return { type: "normal", arg: fn.call(obj, arg) };
    } catch (err) {
      return { type: "throw", arg: err };
    }
  }

  var GenStateSuspendedStart = "suspendedStart";
  var GenStateSuspendedYield = "suspendedYield";
  var GenStateExecuting = "executing";
  var GenStateCompleted = "completed";

  // Returning this object from the innerFn has the same effect as
  // breaking out of the dispatch switch statement.
  var ContinueSentinel = {};

  // Dummy constructor functions that we use as the .constructor and
  // .constructor.prototype properties for functions that return Generator
  // objects. For full spec compliance, you may wish to configure your
  // minifier not to mangle the names of these two functions.
  function Generator() {}
  function GeneratorFunction() {}
  function GeneratorFunctionPrototype() {}

  // This is a polyfill for %IteratorPrototype% for environments that
  // don't natively support it.
  var IteratorPrototype = {};
  IteratorPrototype[iteratorSymbol] = function () {
    return this;
  };

  var getProto = Object.getPrototypeOf;
  var NativeIteratorPrototype = getProto && getProto(getProto(values([])));
  if (NativeIteratorPrototype &&
      NativeIteratorPrototype !== Op &&
      hasOwn.call(NativeIteratorPrototype, iteratorSymbol)) {
    // This environment has a native %IteratorPrototype%; use it instead
    // of the polyfill.
    IteratorPrototype = NativeIteratorPrototype;
  }

  var Gp = GeneratorFunctionPrototype.prototype =
    Generator.prototype = Object.create(IteratorPrototype);
  GeneratorFunction.prototype = Gp.constructor = GeneratorFunctionPrototype;
  GeneratorFunctionPrototype.constructor = GeneratorFunction;
  GeneratorFunctionPrototype[toStringTagSymbol] =
    GeneratorFunction.displayName = "GeneratorFunction";

  // Helper for defining the .next, .throw, and .return methods of the
  // Iterator interface in terms of a single ._invoke method.
  function defineIteratorMethods(prototype) {
    ["next", "throw", "return"].forEach(function(method) {
      prototype[method] = function(arg) {
        return this._invoke(method, arg);
      };
    });
  }

  runtime.isGeneratorFunction = function(genFun) {
    var ctor = typeof genFun === "function" && genFun.constructor;
    return ctor
      ? ctor === GeneratorFunction ||
        // For the native GeneratorFunction constructor, the best we can
        // do is to check its .name property.
        (ctor.displayName || ctor.name) === "GeneratorFunction"
      : false;
  };

  runtime.mark = function(genFun) {
    if (Object.setPrototypeOf) {
      Object.setPrototypeOf(genFun, GeneratorFunctionPrototype);
    } else {
      genFun.__proto__ = GeneratorFunctionPrototype;
      if (!(toStringTagSymbol in genFun)) {
        genFun[toStringTagSymbol] = "GeneratorFunction";
      }
    }
    genFun.prototype = Object.create(Gp);
    return genFun;
  };

  // Within the body of any async function, `await x` is transformed to
  // `yield regeneratorRuntime.awrap(x)`, so that the runtime can test
  // `hasOwn.call(value, "__await")` to determine if the yielded value is
  // meant to be awaited.
  runtime.awrap = function(arg) {
    return { __await: arg };
  };

  function AsyncIterator(generator) {
    function invoke(method, arg, resolve, reject) {
      var record = tryCatch(generator[method], generator, arg);
      if (record.type === "throw") {
        reject(record.arg);
      } else {
        var result = record.arg;
        var value = result.value;
        if (value &&
            typeof value === "object" &&
            hasOwn.call(value, "__await")) {
          return Promise.resolve(value.__await).then(function(value) {
            invoke("next", value, resolve, reject);
          }, function(err) {
            invoke("throw", err, resolve, reject);
          });
        }

        return Promise.resolve(value).then(function(unwrapped) {
          // When a yielded Promise is resolved, its final value becomes
          // the .value of the Promise<{value,done}> result for the
          // current iteration. If the Promise is rejected, however, the
          // result for this iteration will be rejected with the same
          // reason. Note that rejections of yielded Promises are not
          // thrown back into the generator function, as is the case
          // when an awaited Promise is rejected. This difference in
          // behavior between yield and await is important, because it
          // allows the consumer to decide what to do with the yielded
          // rejection (swallow it and continue, manually .throw it back
          // into the generator, abandon iteration, whatever). With
          // await, by contrast, there is no opportunity to examine the
          // rejection reason outside the generator function, so the
          // only option is to throw it from the await expression, and
          // let the generator function handle the exception.
          result.value = unwrapped;
          resolve(result);
        }, reject);
      }
    }

    if (typeof global.process === "object" && global.process.domain) {
      invoke = global.process.domain.bind(invoke);
    }

    var previousPromise;

    function enqueue(method, arg) {
      function callInvokeWithMethodAndArg() {
        return new Promise(function(resolve, reject) {
          invoke(method, arg, resolve, reject);
        });
      }

      return previousPromise =
        // If enqueue has been called before, then we want to wait until
        // all previous Promises have been resolved before calling invoke,
        // so that results are always delivered in the correct order. If
        // enqueue has not been called before, then it is important to
        // call invoke immediately, without waiting on a callback to fire,
        // so that the async generator function has the opportunity to do
        // any necessary setup in a predictable way. This predictability
        // is why the Promise constructor synchronously invokes its
        // executor callback, and why async functions synchronously
        // execute code before the first await. Since we implement simple
        // async functions in terms of async generators, it is especially
        // important to get this right, even though it requires care.
        previousPromise ? previousPromise.then(
          callInvokeWithMethodAndArg,
          // Avoid propagating failures to Promises returned by later
          // invocations of the iterator.
          callInvokeWithMethodAndArg
        ) : callInvokeWithMethodAndArg();
    }

    // Define the unified helper method that is used to implement .next,
    // .throw, and .return (see defineIteratorMethods).
    this._invoke = enqueue;
  }

  defineIteratorMethods(AsyncIterator.prototype);
  AsyncIterator.prototype[asyncIteratorSymbol] = function () {
    return this;
  };
  runtime.AsyncIterator = AsyncIterator;

  // Note that simple async functions are implemented on top of
  // AsyncIterator objects; they just return a Promise for the value of
  // the final result produced by the iterator.
  runtime.async = function(innerFn, outerFn, self, tryLocsList) {
    var iter = new AsyncIterator(
      wrap(innerFn, outerFn, self, tryLocsList)
    );

    return runtime.isGeneratorFunction(outerFn)
      ? iter // If outerFn is a generator, return the full iterator.
      : iter.next().then(function(result) {
          return result.done ? result.value : iter.next();
        });
  };

  function makeInvokeMethod(innerFn, self, context) {
    var state = GenStateSuspendedStart;

    return function invoke(method, arg) {
      if (state === GenStateExecuting) {
        throw new Error("Generator is already running");
      }

      if (state === GenStateCompleted) {
        if (method === "throw") {
          throw arg;
        }

        // Be forgiving, per 25.3.3.3.3 of the spec:
        // https://people.mozilla.org/~jorendorff/es6-draft.html#sec-generatorresume
        return doneResult();
      }

      context.method = method;
      context.arg = arg;

      while (true) {
        var delegate = context.delegate;
        if (delegate) {
          var delegateResult = maybeInvokeDelegate(delegate, context);
          if (delegateResult) {
            if (delegateResult === ContinueSentinel) continue;
            return delegateResult;
          }
        }

        if (context.method === "next") {
          // Setting context._sent for legacy support of Babel's
          // function.sent implementation.
          context.sent = context._sent = context.arg;

        } else if (context.method === "throw") {
          if (state === GenStateSuspendedStart) {
            state = GenStateCompleted;
            throw context.arg;
          }

          context.dispatchException(context.arg);

        } else if (context.method === "return") {
          context.abrupt("return", context.arg);
        }

        state = GenStateExecuting;

        var record = tryCatch(innerFn, self, context);
        if (record.type === "normal") {
          // If an exception is thrown from innerFn, we leave state ===
          // GenStateExecuting and loop back for another invocation.
          state = context.done
            ? GenStateCompleted
            : GenStateSuspendedYield;

          if (record.arg === ContinueSentinel) {
            continue;
          }

          return {
            value: record.arg,
            done: context.done
          };

        } else if (record.type === "throw") {
          state = GenStateCompleted;
          // Dispatch the exception by looping back around to the
          // context.dispatchException(context.arg) call above.
          context.method = "throw";
          context.arg = record.arg;
        }
      }
    };
  }

  // Call delegate.iterator[context.method](context.arg) and handle the
  // result, either by returning a { value, done } result from the
  // delegate iterator, or by modifying context.method and context.arg,
  // setting context.delegate to null, and returning the ContinueSentinel.
  function maybeInvokeDelegate(delegate, context) {
    var method = delegate.iterator[context.method];
    if (method === undefined) {
      // A .throw or .return when the delegate iterator has no .throw
      // method always terminates the yield* loop.
      context.delegate = null;

      if (context.method === "throw") {
        if (delegate.iterator.return) {
          // If the delegate iterator has a return method, give it a
          // chance to clean up.
          context.method = "return";
          context.arg = undefined;
          maybeInvokeDelegate(delegate, context);

          if (context.method === "throw") {
            // If maybeInvokeDelegate(context) changed context.method from
            // "return" to "throw", let that override the TypeError below.
            return ContinueSentinel;
          }
        }

        context.method = "throw";
        context.arg = new TypeError(
          "The iterator does not provide a 'throw' method");
      }

      return ContinueSentinel;
    }

    var record = tryCatch(method, delegate.iterator, context.arg);

    if (record.type === "throw") {
      context.method = "throw";
      context.arg = record.arg;
      context.delegate = null;
      return ContinueSentinel;
    }

    var info = record.arg;

    if (! info) {
      context.method = "throw";
      context.arg = new TypeError("iterator result is not an object");
      context.delegate = null;
      return ContinueSentinel;
    }

    if (info.done) {
      // Assign the result of the finished delegate to the temporary
      // variable specified by delegate.resultName (see delegateYield).
      context[delegate.resultName] = info.value;

      // Resume execution at the desired location (see delegateYield).
      context.next = delegate.nextLoc;

      // If context.method was "throw" but the delegate handled the
      // exception, let the outer generator proceed normally. If
      // context.method was "next", forget context.arg since it has been
      // "consumed" by the delegate iterator. If context.method was
      // "return", allow the original .return call to continue in the
      // outer generator.
      if (context.method !== "return") {
        context.method = "next";
        context.arg = undefined;
      }

    } else {
      // Re-yield the result returned by the delegate method.
      return info;
    }

    // The delegate iterator is finished, so forget it and continue with
    // the outer generator.
    context.delegate = null;
    return ContinueSentinel;
  }

  // Define Generator.prototype.{next,throw,return} in terms of the
  // unified ._invoke helper method.
  defineIteratorMethods(Gp);

  Gp[toStringTagSymbol] = "Generator";

  // A Generator should always return itself as the iterator object when the
  // @@iterator function is called on it. Some browsers' implementations of the
  // iterator prototype chain incorrectly implement this, causing the Generator
  // object to not be returned from this call. This ensures that doesn't happen.
  // See https://github.com/facebook/regenerator/issues/274 for more details.
  Gp[iteratorSymbol] = function() {
    return this;
  };

  Gp.toString = function() {
    return "[object Generator]";
  };

  function pushTryEntry(locs) {
    var entry = { tryLoc: locs[0] };

    if (1 in locs) {
      entry.catchLoc = locs[1];
    }

    if (2 in locs) {
      entry.finallyLoc = locs[2];
      entry.afterLoc = locs[3];
    }

    this.tryEntries.push(entry);
  }

  function resetTryEntry(entry) {
    var record = entry.completion || {};
    record.type = "normal";
    delete record.arg;
    entry.completion = record;
  }

  function Context(tryLocsList) {
    // The root entry object (effectively a try statement without a catch
    // or a finally block) gives us a place to store values thrown from
    // locations where there is no enclosing try statement.
    this.tryEntries = [{ tryLoc: "root" }];
    tryLocsList.forEach(pushTryEntry, this);
    this.reset(true);
  }

  runtime.keys = function(object) {
    var keys = [];
    for (var key in object) {
      keys.push(key);
    }
    keys.reverse();

    // Rather than returning an object with a next method, we keep
    // things simple and return the next function itself.
    return function next() {
      while (keys.length) {
        var key = keys.pop();
        if (key in object) {
          next.value = key;
          next.done = false;
          return next;
        }
      }

      // To avoid creating an additional object, we just hang the .value
      // and .done properties off the next function object itself. This
      // also ensures that the minifier will not anonymize the function.
      next.done = true;
      return next;
    };
  };

  function values(iterable) {
    if (iterable) {
      var iteratorMethod = iterable[iteratorSymbol];
      if (iteratorMethod) {
        return iteratorMethod.call(iterable);
      }

      if (typeof iterable.next === "function") {
        return iterable;
      }

      if (!isNaN(iterable.length)) {
        var i = -1, next = function next() {
          while (++i < iterable.length) {
            if (hasOwn.call(iterable, i)) {
              next.value = iterable[i];
              next.done = false;
              return next;
            }
          }

          next.value = undefined;
          next.done = true;

          return next;
        };

        return next.next = next;
      }
    }

    // Return an iterator with no values.
    return { next: doneResult };
  }
  runtime.values = values;

  function doneResult() {
    return { value: undefined, done: true };
  }

  Context.prototype = {
    constructor: Context,

    reset: function(skipTempReset) {
      this.prev = 0;
      this.next = 0;
      // Resetting context._sent for legacy support of Babel's
      // function.sent implementation.
      this.sent = this._sent = undefined;
      this.done = false;
      this.delegate = null;

      this.method = "next";
      this.arg = undefined;

      this.tryEntries.forEach(resetTryEntry);

      if (!skipTempReset) {
        for (var name in this) {
          // Not sure about the optimal order of these conditions:
          if (name.charAt(0) === "t" &&
              hasOwn.call(this, name) &&
              !isNaN(+name.slice(1))) {
            this[name] = undefined;
          }
        }
      }
    },

    stop: function() {
      this.done = true;

      var rootEntry = this.tryEntries[0];
      var rootRecord = rootEntry.completion;
      if (rootRecord.type === "throw") {
        throw rootRecord.arg;
      }

      return this.rval;
    },

    dispatchException: function(exception) {
      if (this.done) {
        throw exception;
      }

      var context = this;
      function handle(loc, caught) {
        record.type = "throw";
        record.arg = exception;
        context.next = loc;

        if (caught) {
          // If the dispatched exception was caught by a catch block,
          // then let that catch block handle the exception normally.
          context.method = "next";
          context.arg = undefined;
        }

        return !! caught;
      }

      for (var i = this.tryEntries.length - 1; i >= 0; --i) {
        var entry = this.tryEntries[i];
        var record = entry.completion;

        if (entry.tryLoc === "root") {
          // Exception thrown outside of any try block that could handle
          // it, so set the completion value of the entire function to
          // throw the exception.
          return handle("end");
        }

        if (entry.tryLoc <= this.prev) {
          var hasCatch = hasOwn.call(entry, "catchLoc");
          var hasFinally = hasOwn.call(entry, "finallyLoc");

          if (hasCatch && hasFinally) {
            if (this.prev < entry.catchLoc) {
              return handle(entry.catchLoc, true);
            } else if (this.prev < entry.finallyLoc) {
              return handle(entry.finallyLoc);
            }

          } else if (hasCatch) {
            if (this.prev < entry.catchLoc) {
              return handle(entry.catchLoc, true);
            }

          } else if (hasFinally) {
            if (this.prev < entry.finallyLoc) {
              return handle(entry.finallyLoc);
            }

          } else {
            throw new Error("try statement without catch or finally");
          }
        }
      }
    },

    abrupt: function(type, arg) {
      for (var i = this.tryEntries.length - 1; i >= 0; --i) {
        var entry = this.tryEntries[i];
        if (entry.tryLoc <= this.prev &&
            hasOwn.call(entry, "finallyLoc") &&
            this.prev < entry.finallyLoc) {
          var finallyEntry = entry;
          break;
        }
      }

      if (finallyEntry &&
          (type === "break" ||
           type === "continue") &&
          finallyEntry.tryLoc <= arg &&
          arg <= finallyEntry.finallyLoc) {
        // Ignore the finally entry if control is not jumping to a
        // location outside the try/catch block.
        finallyEntry = null;
      }

      var record = finallyEntry ? finallyEntry.completion : {};
      record.type = type;
      record.arg = arg;

      if (finallyEntry) {
        this.method = "next";
        this.next = finallyEntry.finallyLoc;
        return ContinueSentinel;
      }

      return this.complete(record);
    },

    complete: function(record, afterLoc) {
      if (record.type === "throw") {
        throw record.arg;
      }

      if (record.type === "break" ||
          record.type === "continue") {
        this.next = record.arg;
      } else if (record.type === "return") {
        this.rval = this.arg = record.arg;
        this.method = "return";
        this.next = "end";
      } else if (record.type === "normal" && afterLoc) {
        this.next = afterLoc;
      }

      return ContinueSentinel;
    },

    finish: function(finallyLoc) {
      for (var i = this.tryEntries.length - 1; i >= 0; --i) {
        var entry = this.tryEntries[i];
        if (entry.finallyLoc === finallyLoc) {
          this.complete(entry.completion, entry.afterLoc);
          resetTryEntry(entry);
          return ContinueSentinel;
        }
      }
    },

    "catch": function(tryLoc) {
      for (var i = this.tryEntries.length - 1; i >= 0; --i) {
        var entry = this.tryEntries[i];
        if (entry.tryLoc === tryLoc) {
          var record = entry.completion;
          if (record.type === "throw") {
            var thrown = record.arg;
            resetTryEntry(entry);
          }
          return thrown;
        }
      }

      // The context.catch method must only be called with a location
      // argument that corresponds to a known catch block.
      throw new Error("illegal catch attempt");
    },

    delegateYield: function(iterable, resultName, nextLoc) {
      this.delegate = {
        iterator: values(iterable),
        resultName: resultName,
        nextLoc: nextLoc
      };

      if (this.method === "next") {
        // Deliberately forget the last sent value so that we don't
        // accidentally pass it on to the delegate.
        this.arg = undefined;
      }

      return ContinueSentinel;
    }
  };
})(
  // Among the various tricks for obtaining a reference to the global
  // object, this seems to be the most reliable technique that does not
  // use indirect eval (which violates Content Security Policy).
  typeof global === "object" ? global :
  typeof window === "object" ? window :
  typeof self === "object" ? self : this
);

/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(47)))

/***/ }),
/* 351 */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(352);
module.exports = __webpack_require__(24).RegExp.escape;


/***/ }),
/* 352 */
/***/ (function(module, exports, __webpack_require__) {

// https://github.com/benjamingr/RexExp.escape
var $export = __webpack_require__(0);
var $re = __webpack_require__(353)(/[\\^$*+?.()|[\]{}]/g, '\\$&');

$export($export.S, 'RegExp', { escape: function escape(it) { return $re(it); } });


/***/ }),
/* 353 */
/***/ (function(module, exports) {

module.exports = function (regExp, replace) {
  var replacer = replace === Object(replace) ? function (part) {
    return replace[part];
  } : replace;
  return function (it) {
    return String(it).replace(regExp, replacer);
  };
};


/***/ }),
/* 354 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(global) {

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _book = __webpack_require__(355);

var _book2 = _interopRequireDefault(_book);

var _rendition = __webpack_require__(141);

var _rendition2 = _interopRequireDefault(_rendition);

var _epubcfi = __webpack_require__(22);

var _epubcfi2 = _interopRequireDefault(_epubcfi);

var _contents = __webpack_require__(104);

var _contents2 = _interopRequireDefault(_contents);

var _core = __webpack_require__(6);

var utils = _interopRequireWildcard(_core);

var _constants = __webpack_require__(23);

var _urlPolyfill = __webpack_require__(405);

var URLpolyfill = _interopRequireWildcard(_urlPolyfill);

var _iframe = __webpack_require__(143);

var _iframe2 = _interopRequireDefault(_iframe);

var _default = __webpack_require__(105);

var _default2 = _interopRequireDefault(_default);

var _continuous = __webpack_require__(147);

var _continuous2 = _interopRequireDefault(_continuous);

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/**
 * Creates a new Book
 * @param {string|ArrayBuffer} url URL, Path or ArrayBuffer
 * @param {object} options to pass to the book
 * @returns {Book} a new Book object
 * @example ePub("/path/to/book.epub", {})
 */
function ePub(url, options) {
  return new _book2.default(url, options);
}

ePub.VERSION = _constants.EPUBJS_VERSION;

if (typeof global !== "undefined") {
  global.EPUBJS_VERSION = _constants.EPUBJS_VERSION;
}

ePub.Book = _book2.default;
ePub.Rendition = _rendition2.default;
ePub.Contents = _contents2.default;
ePub.CFI = _epubcfi2.default;
ePub.utils = utils;

exports.default = ePub;
module.exports = exports["default"];
/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(47)))

/***/ }),
/* 355 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _eventEmitter = __webpack_require__(30);

var _eventEmitter2 = _interopRequireDefault(_eventEmitter);

var _core = __webpack_require__(6);

var _url = __webpack_require__(70);

var _url2 = _interopRequireDefault(_url);

var _path = __webpack_require__(46);

var _path2 = _interopRequireDefault(_path);

var _spine = __webpack_require__(372);

var _spine2 = _interopRequireDefault(_spine);

var _locations = __webpack_require__(376);

var _locations2 = _interopRequireDefault(_locations);

var _container = __webpack_require__(377);

var _container2 = _interopRequireDefault(_container);

var _packaging = __webpack_require__(378);

var _packaging2 = _interopRequireDefault(_packaging);

var _navigation = __webpack_require__(379);

var _navigation2 = _interopRequireDefault(_navigation);

var _resources = __webpack_require__(380);

var _resources2 = _interopRequireDefault(_resources);

var _pagelist = __webpack_require__(381);

var _pagelist2 = _interopRequireDefault(_pagelist);

var _rendition = __webpack_require__(141);

var _rendition2 = _interopRequireDefault(_rendition);

var _archive = __webpack_require__(400);

var _archive2 = _interopRequireDefault(_archive);

var _request2 = __webpack_require__(73);

var _request3 = _interopRequireDefault(_request2);

var _epubcfi = __webpack_require__(22);

var _epubcfi2 = _interopRequireDefault(_epubcfi);

var _store = __webpack_require__(402);

var _store2 = _interopRequireDefault(_store);

var _displayoptions = __webpack_require__(404);

var _displayoptions2 = _interopRequireDefault(_displayoptions);

var _constants = __webpack_require__(23);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var CONTAINER_PATH = "META-INF/container.xml";
var IBOOKS_DISPLAY_OPTIONS_PATH = "META-INF/com.apple.ibooks.display-options.xml";

var INPUT_TYPE = {
	BINARY: "binary",
	BASE64: "base64",
	EPUB: "epub",
	OPF: "opf",
	MANIFEST: "json",
	DIRECTORY: "directory"
};

/**
 * An Epub representation with methods for the loading, parsing and manipulation
 * of its contents.
 * @class
 * @param {string} [url]
 * @param {object} [options]
 * @param {method} [options.requestMethod] a request function to use instead of the default
 * @param {boolean} [options.requestCredentials=undefined] send the xhr request withCredentials
 * @param {object} [options.requestHeaders=undefined] send the xhr request headers
 * @param {string} [options.encoding=binary] optional to pass 'binary' or base64' for archived Epubs
 * @param {string} [options.replacements=none] use base64, blobUrl, or none for replacing assets in archived Epubs
 * @param {method} [options.canonical] optional function to determine canonical urls for a path
 * @param {string} [options.openAs] optional string to determine the input type
 * @param {string} [options.store=false] cache the contents in local storage, value should be the name of the reader
 * @returns {Book}
 * @example new Book("/path/to/book.epub", {})
 * @example new Book({ replacements: "blobUrl" })
 */

var Book = function () {
	function Book(url, options) {
		var _this = this;

		_classCallCheck(this, Book);

		// Allow passing just options to the Book
		if (typeof options === "undefined" && typeof url !== "string" && url instanceof Blob === false) {
			options = url;
			url = undefined;
		}

		this.settings = (0, _core.extend)(this.settings || {}, {
			requestMethod: undefined,
			requestCredentials: undefined,
			requestHeaders: undefined,
			encoding: undefined,
			replacements: undefined,
			canonical: undefined,
			openAs: undefined,
			store: undefined
		});

		(0, _core.extend)(this.settings, options);

		// Promises
		this.opening = new _core.defer();
		/**
   * @member {promise} opened returns after the book is loaded
   * @memberof Book
   */
		this.opened = this.opening.promise;
		this.isOpen = false;

		this.loading = {
			manifest: new _core.defer(),
			spine: new _core.defer(),
			metadata: new _core.defer(),
			cover: new _core.defer(),
			navigation: new _core.defer(),
			pageList: new _core.defer(),
			resources: new _core.defer(),
			displayOptions: new _core.defer()
		};

		this.loaded = {
			manifest: this.loading.manifest.promise,
			spine: this.loading.spine.promise,
			metadata: this.loading.metadata.promise,
			cover: this.loading.cover.promise,
			navigation: this.loading.navigation.promise,
			pageList: this.loading.pageList.promise,
			resources: this.loading.resources.promise,
			displayOptions: this.loading.displayOptions.promise
		};

		/**
   * @member {promise} ready returns after the book is loaded and parsed
   * @memberof Book
   * @private
   */
		this.ready = Promise.all([this.loaded.manifest, this.loaded.spine, this.loaded.metadata, this.loaded.cover, this.loaded.navigation, this.loaded.resources, this.loaded.displayOptions]);

		// Queue for methods used before opening
		this.isRendered = false;
		// this._q = queue(this);

		/**
   * @member {method} request
   * @memberof Book
   * @private
   */
		this.request = this.settings.requestMethod || _request3.default;

		/**
   * @member {Spine} spine
   * @memberof Book
   */
		this.spine = new _spine2.default();

		/**
   * @member {Locations} locations
   * @memberof Book
   */
		this.locations = new _locations2.default(this.spine, this.load.bind(this));

		/**
   * @member {Navigation} navigation
   * @memberof Book
   */
		this.navigation = undefined;

		/**
   * @member {PageList} pagelist
   * @memberof Book
   */
		this.pageList = undefined;

		/**
   * @member {Url} url
   * @memberof Book
   * @private
   */
		this.url = undefined;

		/**
   * @member {Path} path
   * @memberof Book
   * @private
   */
		this.path = undefined;

		/**
   * @member {boolean} archived
   * @memberof Book
   * @private
   */
		this.archived = false;

		/**
   * @member {Archive} archive
   * @memberof Book
   * @private
   */
		this.archive = undefined;

		/**
   * @member {Store} storage
   * @memberof Book
   * @private
   */
		this.storage = undefined;

		/**
   * @member {Resources} resources
   * @memberof Book
   * @private
   */
		this.resources = undefined;

		/**
   * @member {Rendition} rendition
   * @memberof Book
   * @private
   */
		this.rendition = undefined;

		/**
   * @member {Container} container
   * @memberof Book
   * @private
   */
		this.container = undefined;

		/**
   * @member {Packaging} packaging
   * @memberof Book
   * @private
   */
		this.packaging = undefined;

		/**
   * @member {DisplayOptions} displayOptions
   * @memberof DisplayOptions
   * @private
   */
		this.displayOptions = undefined;

		// this.toc = undefined;
		if (this.settings.store) {
			this.store(this.settings.store);
		}

		if (url) {
			this.open(url, this.settings.openAs).catch(function (error) {
				var err = new Error("Cannot load book at " + url);
				_this.emit(_constants.EVENTS.BOOK.OPEN_FAILED, err);
			});
		}
	}

	/**
  * Open a epub or url
  * @param {string | ArrayBuffer} input Url, Path or ArrayBuffer
  * @param {string} [what="binary", "base64", "epub", "opf", "json", "directory"] force opening as a certain type
  * @returns {Promise} of when the book has been loaded
  * @example book.open("/path/to/book.epub")
  */


	_createClass(Book, [{
		key: "open",
		value: function open(input, what) {
			var opening;
			var type = what || this.determineType(input);

			if (type === INPUT_TYPE.BINARY) {
				this.archived = true;
				this.url = new _url2.default("/", "");
				opening = this.openEpub(input);
			} else if (type === INPUT_TYPE.BASE64) {
				this.archived = true;
				this.url = new _url2.default("/", "");
				opening = this.openEpub(input, type);
			} else if (type === INPUT_TYPE.EPUB) {
				this.archived = true;
				this.url = new _url2.default("/", "");
				opening = this.request(input, "binary", this.settings.requestCredentials).then(this.openEpub.bind(this));
			} else if (type == INPUT_TYPE.OPF) {
				this.url = new _url2.default(input);
				opening = this.openPackaging(this.url.Path.toString());
			} else if (type == INPUT_TYPE.MANIFEST) {
				this.url = new _url2.default(input);
				opening = this.openManifest(this.url.Path.toString());
			} else {
				this.url = new _url2.default(input);
				opening = this.openContainer(CONTAINER_PATH).then(this.openPackaging.bind(this));
			}

			return opening;
		}

		/**
   * Open an archived epub
   * @private
   * @param  {binary} data
   * @param  {string} [encoding]
   * @return {Promise}
   */

	}, {
		key: "openEpub",
		value: function openEpub(data, encoding) {
			var _this2 = this;

			return this.unarchive(data, encoding || this.settings.encoding).then(function () {
				return _this2.openContainer(CONTAINER_PATH);
			}).then(function (packagePath) {
				return _this2.openPackaging(packagePath);
			});
		}

		/**
   * Open the epub container
   * @private
   * @param  {string} url
   * @return {string} packagePath
   */

	}, {
		key: "openContainer",
		value: function openContainer(url) {
			var _this3 = this;

			return this.load(url).then(function (xml) {
				_this3.container = new _container2.default(xml);
				return _this3.resolve(_this3.container.packagePath);
			});
		}

		/**
   * Open the Open Packaging Format Xml
   * @private
   * @param  {string} url
   * @return {Promise}
   */

	}, {
		key: "openPackaging",
		value: function openPackaging(url) {
			var _this4 = this;

			this.path = new _path2.default(url);
			return this.load(url).then(function (xml) {
				_this4.packaging = new _packaging2.default(xml);
				return _this4.unpack(_this4.packaging);
			});
		}

		/**
   * Open the manifest JSON
   * @private
   * @param  {string} url
   * @return {Promise}
   */

	}, {
		key: "openManifest",
		value: function openManifest(url) {
			var _this5 = this;

			this.path = new _path2.default(url);
			return this.load(url).then(function (json) {
				_this5.packaging = new _packaging2.default();
				_this5.packaging.load(json);
				return _this5.unpack(_this5.packaging);
			});
		}

		/**
   * Load a resource from the Book
   * @param  {string} path path to the resource to load
   * @return {Promise}     returns a promise with the requested resource
   */

	}, {
		key: "load",
		value: function load(path) {
			var resolved = this.resolve(path);
			if (this.archived) {
				return this.archive.request(resolved);
			} else {
				return this.request(resolved, null, this.settings.requestCredentials, this.settings.requestHeaders);
			}
		}

		/**
   * Resolve a path to it's absolute position in the Book
   * @param  {string} path
   * @param  {boolean} [absolute] force resolving the full URL
   * @return {string}          the resolved path string
   */

	}, {
		key: "resolve",
		value: function resolve(path, absolute) {
			if (!path) {
				return;
			}
			var resolved = path;
			var isAbsolute = path.indexOf("://") > -1;

			if (isAbsolute) {
				return path;
			}

			if (this.path) {
				resolved = this.path.resolve(path);
			}

			if (absolute != false && this.url) {
				resolved = this.url.resolve(resolved);
			}

			return resolved;
		}

		/**
   * Get a canonical link to a path
   * @param  {string} path
   * @return {string} the canonical path string
   */

	}, {
		key: "canonical",
		value: function canonical(path) {
			var url = path;

			if (!path) {
				return "";
			}

			if (this.settings.canonical) {
				url = this.settings.canonical(path);
			} else {
				url = this.resolve(path, true);
			}

			return url;
		}

		/**
   * Determine the type of they input passed to open
   * @private
   * @param  {string} input
   * @return {string}  binary | directory | epub | opf
   */

	}, {
		key: "determineType",
		value: function determineType(input) {
			var url;
			var path;
			var extension;

			if (this.settings.encoding === "base64") {
				return INPUT_TYPE.BASE64;
			}

			if (typeof input != "string") {
				return INPUT_TYPE.BINARY;
			}

			url = new _url2.default(input);
			path = url.path();
			extension = path.extension;

			if (!extension) {
				return INPUT_TYPE.DIRECTORY;
			}

			if (extension === "epub") {
				return INPUT_TYPE.EPUB;
			}

			if (extension === "opf") {
				return INPUT_TYPE.OPF;
			}

			if (extension === "json") {
				return INPUT_TYPE.MANIFEST;
			}
		}

		/**
   * unpack the contents of the Books packaging
   * @private
   * @param {Packaging} packaging object
   */

	}, {
		key: "unpack",
		value: function unpack(packaging) {
			var _this6 = this;

			this.package = packaging; //TODO: deprecated this

			if (this.packaging.metadata.layout === "") {
				// rendition:layout not set - check display options if book is pre-paginated
				this.load(this.url.resolve(IBOOKS_DISPLAY_OPTIONS_PATH)).then(function (xml) {
					_this6.displayOptions = new _displayoptions2.default(xml);
					_this6.loading.displayOptions.resolve(_this6.displayOptions);
				}).catch(function (err) {
					_this6.displayOptions = new _displayoptions2.default();
					_this6.loading.displayOptions.resolve(_this6.displayOptions);
				});
			} else {
				this.displayOptions = new _displayoptions2.default();
				this.loading.displayOptions.resolve(this.displayOptions);
			}

			this.spine.unpack(this.packaging, this.resolve.bind(this), this.canonical.bind(this));

			this.resources = new _resources2.default(this.packaging.manifest, {
				archive: this.archive,
				resolver: this.resolve.bind(this),
				request: this.request.bind(this),
				replacements: this.settings.replacements || (this.archived ? "blobUrl" : "base64")
			});

			this.loadNavigation(this.packaging).then(function () {
				// this.toc = this.navigation.toc;
				_this6.loading.navigation.resolve(_this6.navigation);
			});

			if (this.packaging.coverPath) {
				this.cover = this.resolve(this.packaging.coverPath);
			}
			// Resolve promises
			this.loading.manifest.resolve(this.packaging.manifest);
			this.loading.metadata.resolve(this.packaging.metadata);
			this.loading.spine.resolve(this.spine);
			this.loading.cover.resolve(this.cover);
			this.loading.resources.resolve(this.resources);
			this.loading.pageList.resolve(this.pageList);

			this.isOpen = true;

			if (this.archived || this.settings.replacements && this.settings.replacements != "none") {
				this.replacements().then(function () {
					_this6.loaded.displayOptions.then(function () {
						_this6.opening.resolve(_this6);
					});
				}).catch(function (err) {
					console.error(err);
				});
			} else {
				// Resolve book opened promise
				this.loaded.displayOptions.then(function () {
					_this6.opening.resolve(_this6);
				});
			}
		}

		/**
   * Load Navigation and PageList from package
   * @private
   * @param {Packaging} packaging
   */

	}, {
		key: "loadNavigation",
		value: function loadNavigation(packaging) {
			var _this7 = this;

			var navPath = packaging.navPath || packaging.ncxPath;
			var toc = packaging.toc;

			// From json manifest
			if (toc) {
				return new Promise(function (resolve, reject) {
					_this7.navigation = new _navigation2.default(toc);

					if (packaging.pageList) {
						_this7.pageList = new _pagelist2.default(packaging.pageList); // TODO: handle page lists from Manifest
					}

					resolve(_this7.navigation);
				});
			}

			if (!navPath) {
				return new Promise(function (resolve, reject) {
					_this7.navigation = new _navigation2.default();
					_this7.pageList = new _pagelist2.default();

					resolve(_this7.navigation);
				});
			}

			return this.load(navPath, "xml").then(function (xml) {
				_this7.navigation = new _navigation2.default(xml);
				_this7.pageList = new _pagelist2.default(xml);
				return _this7.navigation;
			});
		}

		/**
   * Gets a Section of the Book from the Spine
   * Alias for `book.spine.get`
   * @param {string} target
   * @return {Section}
   */

	}, {
		key: "section",
		value: function section(target) {
			return this.spine.get(target);
		}

		/**
   * Sugar to render a book to an element
   * @param  {element | string} element element or string to add a rendition to
   * @param  {object} [options]
   * @return {Rendition}
   */

	}, {
		key: "renderTo",
		value: function renderTo(element, options) {
			this.rendition = new _rendition2.default(this, options);
			this.rendition.attachTo(element);

			return this.rendition;
		}

		/**
   * Set if request should use withCredentials
   * @param {boolean} credentials
   */

	}, {
		key: "setRequestCredentials",
		value: function setRequestCredentials(credentials) {
			this.settings.requestCredentials = credentials;
		}

		/**
   * Set headers request should use
   * @param {object} headers
   */

	}, {
		key: "setRequestHeaders",
		value: function setRequestHeaders(headers) {
			this.settings.requestHeaders = headers;
		}

		/**
   * Unarchive a zipped epub
   * @private
   * @param  {binary} input epub data
   * @param  {string} [encoding]
   * @return {Archive}
   */

	}, {
		key: "unarchive",
		value: function unarchive(input, encoding) {
			this.archive = new _archive2.default();
			return this.archive.open(input, encoding);
		}

		/**
   * Store the epubs contents
   * @private
   * @param  {binary} input epub data
   * @param  {string} [encoding]
   * @return {Store}
   */

	}, {
		key: "store",
		value: function store(name) {
			var _this8 = this;

			// Use "blobUrl" or "base64" for replacements
			var replacementsSetting = this.settings.replacements && this.settings.replacements !== "none";
			// Save original url
			var originalUrl = this.url;
			// Save original request method
			var requester = this.settings.requestMethod || _request3.default.bind(this);
			// Create new Store
			this.storage = new _store2.default(name, requester, this.resolve.bind(this));
			// Replace request method to go through store
			this.request = this.storage.request.bind(this.storage);

			this.opened.then(function () {
				if (_this8.archived) {
					_this8.storage.requester = _this8.archive.request.bind(_this8.archive);
				}
				// Substitute hook
				var substituteResources = function substituteResources(output, section) {
					section.output = _this8.resources.substitute(output, section.url);
				};

				// Set to use replacements
				_this8.resources.settings.replacements = replacementsSetting || "blobUrl";
				// Create replacement urls
				_this8.resources.replacements().then(function () {
					return _this8.resources.replaceCss();
				});

				_this8.storage.on("offline", function () {
					// Remove url to use relative resolving for hrefs
					_this8.url = new _url2.default("/", "");
					// Add hook to replace resources in contents
					_this8.spine.hooks.serialize.register(substituteResources);
				});

				_this8.storage.on("online", function () {
					// Restore original url
					_this8.url = originalUrl;
					// Remove hook
					_this8.spine.hooks.serialize.deregister(substituteResources);
				});
			});

			return this.storage;
		}

		/**
   * Get the cover url
   * @return {string} coverUrl
   */

	}, {
		key: "coverUrl",
		value: function coverUrl() {
			var _this9 = this;

			var retrieved = this.loaded.cover.then(function (url) {
				if (_this9.archived) {
					// return this.archive.createUrl(this.cover);
					return _this9.resources.get(_this9.cover);
				} else {
					return _this9.cover;
				}
			});

			return retrieved;
		}

		/**
   * Load replacement urls
   * @private
   * @return {Promise} completed loading urls
   */

	}, {
		key: "replacements",
		value: function replacements() {
			var _this10 = this;

			this.spine.hooks.serialize.register(function (output, section) {
				section.output = _this10.resources.substitute(output, section.url);
			});

			return this.resources.replacements().then(function () {
				return _this10.resources.replaceCss();
			});
		}

		/**
   * Find a DOM Range for a given CFI Range
   * @param  {EpubCFI} cfiRange a epub cfi range
   * @return {Range}
   */

	}, {
		key: "getRange",
		value: function getRange(cfiRange) {
			var cfi = new _epubcfi2.default(cfiRange);
			var item = this.spine.get(cfi.spinePos);
			var _request = this.load.bind(this);
			if (!item) {
				return new Promise(function (resolve, reject) {
					reject("CFI could not be found");
				});
			}
			return item.load(_request).then(function (contents) {
				var range = cfi.toRange(item.document);
				return range;
			});
		}

		/**
   * Generates the Book Key using the identifer in the manifest or other string provided
   * @param  {string} [identifier] to use instead of metadata identifier
   * @return {string} key
   */

	}, {
		key: "key",
		value: function key(identifier) {
			var ident = identifier || this.packaging.metadata.identifier || this.url.filename;
			return "epubjs:" + _constants.EPUBJS_VERSION + ":" + ident;
		}

		/**
   * Destroy the Book and all associated objects
   */

	}, {
		key: "destroy",
		value: function destroy() {
			this.opened = undefined;
			this.loading = undefined;
			this.loaded = undefined;
			this.ready = undefined;

			this.isOpen = false;
			this.isRendered = false;

			this.spine && this.spine.destroy();
			this.locations && this.locations.destroy();
			this.pageList && this.pageList.destroy();
			this.archive && this.archive.destroy();
			this.resources && this.resources.destroy();
			this.container && this.container.destroy();
			this.packaging && this.packaging.destroy();
			this.rendition && this.rendition.destroy();
			this.displayOptions && this.displayOptions.destroy();

			this.spine = undefined;
			this.locations = undefined;
			this.pageList = undefined;
			this.archive = undefined;
			this.resources = undefined;
			this.container = undefined;
			this.packaging = undefined;
			this.rendition = undefined;

			this.navigation = undefined;
			this.url = undefined;
			this.path = undefined;
			this.archived = false;
		}
	}]);

	return Book;
}();

//-- Enable binding events to book


(0, _eventEmitter2.default)(Book.prototype);

exports.default = Book;
module.exports = exports["default"];

/***/ }),
/* 356 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var assign        = __webpack_require__(357)
  , normalizeOpts = __webpack_require__(365)
  , isCallable    = __webpack_require__(366)
  , contains      = __webpack_require__(367)

  , d;

d = module.exports = function (dscr, value/*, options*/) {
	var c, e, w, options, desc;
	if ((arguments.length < 2) || (typeof dscr !== 'string')) {
		options = value;
		value = dscr;
		dscr = null;
	} else {
		options = arguments[2];
	}
	if (dscr == null) {
		c = w = true;
		e = false;
	} else {
		c = contains.call(dscr, 'c');
		e = contains.call(dscr, 'e');
		w = contains.call(dscr, 'w');
	}

	desc = { value: value, configurable: c, enumerable: e, writable: w };
	return !options ? desc : assign(normalizeOpts(options), desc);
};

d.gs = function (dscr, get, set/*, options*/) {
	var c, e, options, desc;
	if (typeof dscr !== 'string') {
		options = set;
		set = get;
		get = dscr;
		dscr = null;
	} else {
		options = arguments[3];
	}
	if (get == null) {
		get = undefined;
	} else if (!isCallable(get)) {
		options = get;
		get = set = undefined;
	} else if (set == null) {
		set = undefined;
	} else if (!isCallable(set)) {
		options = set;
		set = undefined;
	}
	if (dscr == null) {
		c = true;
		e = false;
	} else {
		c = contains.call(dscr, 'c');
		e = contains.call(dscr, 'e');
	}

	desc = { get: get, set: set, configurable: c, enumerable: e };
	return !options ? desc : assign(normalizeOpts(options), desc);
};


/***/ }),
/* 357 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


module.exports = __webpack_require__(358)()
	? Object.assign
	: __webpack_require__(359);


/***/ }),
/* 358 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


module.exports = function () {
	var assign = Object.assign, obj;
	if (typeof assign !== "function") return false;
	obj = { foo: "raz" };
	assign(obj, { bar: "dwa" }, { trzy: "trzy" });
	return (obj.foo + obj.bar + obj.trzy) === "razdwatrzy";
};


/***/ }),
/* 359 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var keys  = __webpack_require__(360)
  , value = __webpack_require__(364)
  , max   = Math.max;

module.exports = function (dest, src /*, …srcn*/) {
	var error, i, length = max(arguments.length, 2), assign;
	dest = Object(value(dest));
	assign = function (key) {
		try {
			dest[key] = src[key];
		} catch (e) {
			if (!error) error = e;
		}
	};
	for (i = 1; i < length; ++i) {
		src = arguments[i];
		keys(src).forEach(assign);
	}
	if (error !== undefined) throw error;
	return dest;
};


/***/ }),
/* 360 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


module.exports = __webpack_require__(361)()
	? Object.keys
	: __webpack_require__(362);


/***/ }),
/* 361 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


module.exports = function () {
	try {
		Object.keys("primitive");
		return true;
	} catch (e) {
 return false;
}
};


/***/ }),
/* 362 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var isValue = __webpack_require__(100);

var keys = Object.keys;

module.exports = function (object) {
	return keys(isValue(object) ? Object(object) : object);
};


/***/ }),
/* 363 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


// eslint-disable-next-line no-empty-function
module.exports = function () {};


/***/ }),
/* 364 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var isValue = __webpack_require__(100);

module.exports = function (value) {
	if (!isValue(value)) throw new TypeError("Cannot use null or undefined");
	return value;
};


/***/ }),
/* 365 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var isValue = __webpack_require__(100);

var forEach = Array.prototype.forEach, create = Object.create;

var process = function (src, obj) {
	var key;
	for (key in src) obj[key] = src[key];
};

// eslint-disable-next-line no-unused-vars
module.exports = function (opts1 /*, …options*/) {
	var result = create(null);
	forEach.call(arguments, function (options) {
		if (!isValue(options)) return;
		process(Object(options), result);
	});
	return result;
};


/***/ }),
/* 366 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
// Deprecated



module.exports = function (obj) {
 return typeof obj === "function";
};


/***/ }),
/* 367 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


module.exports = __webpack_require__(368)()
	? String.prototype.contains
	: __webpack_require__(369);


/***/ }),
/* 368 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var str = "razdwatrzy";

module.exports = function () {
	if (typeof str.contains !== "function") return false;
	return (str.contains("dwa") === true) && (str.contains("foo") === false);
};


/***/ }),
/* 369 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var indexOf = String.prototype.indexOf;

module.exports = function (searchString/*, position*/) {
	return indexOf.call(this, searchString, arguments[1]) > -1;
};


/***/ }),
/* 370 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


module.exports = function (fn) {
	if (typeof fn !== "function") throw new TypeError(fn + " is not a function");
	return fn;
};


/***/ }),
/* 371 */
/***/ (function(module, exports) {

module.exports = __WEBPACK_EXTERNAL_MODULE_371__;

/***/ }),
/* 372 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _epubcfi = __webpack_require__(22);

var _epubcfi2 = _interopRequireDefault(_epubcfi);

var _hook = __webpack_require__(101);

var _hook2 = _interopRequireDefault(_hook);

var _section = __webpack_require__(373);

var _section2 = _interopRequireDefault(_section);

var _replacements = __webpack_require__(72);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * A collection of Spine Items
 */
var Spine = function () {
	function Spine() {
		_classCallCheck(this, Spine);

		this.spineItems = [];
		this.spineByHref = {};
		this.spineById = {};

		this.hooks = {};
		this.hooks.serialize = new _hook2.default();
		this.hooks.content = new _hook2.default();

		// Register replacements
		this.hooks.content.register(_replacements.replaceBase);
		this.hooks.content.register(_replacements.replaceCanonical);
		this.hooks.content.register(_replacements.replaceMeta);

		this.epubcfi = new _epubcfi2.default();

		this.loaded = false;

		this.items = undefined;
		this.manifest = undefined;
		this.spineNodeIndex = undefined;
		this.baseUrl = undefined;
		this.length = undefined;
	}

	/**
  * Unpack items from a opf into spine items
  * @param  {Packaging} _package
  * @param  {method} resolver URL resolver
  * @param  {method} canonical Resolve canonical url
  */


	_createClass(Spine, [{
		key: "unpack",
		value: function unpack(_package, resolver, canonical) {
			var _this = this;

			this.items = _package.spine;
			this.manifest = _package.manifest;
			this.spineNodeIndex = _package.spineNodeIndex;
			this.baseUrl = _package.baseUrl || _package.basePath || "";
			this.length = this.items.length;

			this.items.forEach(function (item, index) {
				var manifestItem = _this.manifest[item.idref];
				var spineItem;

				item.index = index;
				item.cfiBase = _this.epubcfi.generateChapterComponent(_this.spineNodeIndex, item.index, item.idref);

				if (item.href) {
					item.url = resolver(item.href, true);
					item.canonical = canonical(item.href);
				}

				if (manifestItem) {
					item.href = manifestItem.href;
					item.url = resolver(item.href, true);
					item.canonical = canonical(item.href);

					if (manifestItem.properties.length) {
						item.properties.push.apply(item.properties, manifestItem.properties);
					}
				}

				if (item.linear === "yes") {
					item.prev = function () {
						var prevIndex = item.index;
						while (prevIndex > 0) {
							var prev = this.get(prevIndex - 1);
							if (prev && prev.linear) {
								return prev;
							}
							prevIndex -= 1;
						}
						return;
					}.bind(_this);
					item.next = function () {
						var nextIndex = item.index;
						while (nextIndex < this.spineItems.length - 1) {
							var next = this.get(nextIndex + 1);
							if (next && next.linear) {
								return next;
							}
							nextIndex += 1;
						}
						return;
					}.bind(_this);
				} else {
					item.prev = function () {
						return;
					};
					item.next = function () {
						return;
					};
				}

				spineItem = new _section2.default(item, _this.hooks);

				_this.append(spineItem);
			});

			this.loaded = true;
		}

		/**
   * Get an item from the spine
   * @param  {string|number} [target]
   * @return {Section} section
   * @example spine.get();
   * @example spine.get(1);
   * @example spine.get("chap1.html");
   * @example spine.get("#id1234");
   */

	}, {
		key: "get",
		value: function get(target) {
			var index = 0;

			if (typeof target === "undefined") {
				while (index < this.spineItems.length) {
					var next = this.spineItems[index];
					if (next && next.linear) {
						break;
					}
					index += 1;
				}
			} else if (this.epubcfi.isCfiString(target)) {
				var cfi = new _epubcfi2.default(target);
				index = cfi.spinePos;
			} else if (typeof target === "number" || isNaN(target) === false) {
				index = target;
			} else if (typeof target === "string" && target.indexOf("#") === 0) {
				index = this.spineById[target.substring(1)];
			} else if (typeof target === "string") {
				// Remove fragments
				target = target.split("#")[0];
				index = this.spineByHref[target] || this.spineByHref[encodeURI(target)];
			}

			return this.spineItems[index] || null;
		}

		/**
   * Append a Section to the Spine
   * @private
   * @param  {Section} section
   */

	}, {
		key: "append",
		value: function append(section) {
			var index = this.spineItems.length;
			section.index = index;

			this.spineItems.push(section);

			// Encode and Decode href lookups
			// see pr for details: https://github.com/futurepress/epub.js/pull/358
			this.spineByHref[decodeURI(section.href)] = index;
			this.spineByHref[encodeURI(section.href)] = index;
			this.spineByHref[section.href] = index;

			this.spineById[section.idref] = index;

			return index;
		}

		/**
   * Prepend a Section to the Spine
   * @private
   * @param  {Section} section
   */

	}, {
		key: "prepend",
		value: function prepend(section) {
			// var index = this.spineItems.unshift(section);
			this.spineByHref[section.href] = 0;
			this.spineById[section.idref] = 0;

			// Re-index
			this.spineItems.forEach(function (item, index) {
				item.index = index;
			});

			return 0;
		}

		// insert(section, index) {
		//
		// };

		/**
   * Remove a Section from the Spine
   * @private
   * @param  {Section} section
   */

	}, {
		key: "remove",
		value: function remove(section) {
			var index = this.spineItems.indexOf(section);

			if (index > -1) {
				delete this.spineByHref[section.href];
				delete this.spineById[section.idref];

				return this.spineItems.splice(index, 1);
			}
		}

		/**
   * Loop over the Sections in the Spine
   * @return {method} forEach
   */

	}, {
		key: "each",
		value: function each() {
			return this.spineItems.forEach.apply(this.spineItems, arguments);
		}

		/**
   * Find the first Section in the Spine
   * @return {Section} first section
   */

	}, {
		key: "first",
		value: function first() {
			var index = 0;

			do {
				var next = this.get(index);

				if (next && next.linear) {
					return next;
				}
				index += 1;
			} while (index < this.spineItems.length);
		}

		/**
   * Find the last Section in the Spine
   * @return {Section} last section
   */

	}, {
		key: "last",
		value: function last() {
			var index = this.spineItems.length - 1;

			do {
				var prev = this.get(index);
				if (prev && prev.linear) {
					return prev;
				}
				index -= 1;
			} while (index >= 0);
		}
	}, {
		key: "destroy",
		value: function destroy() {
			this.each(function (section) {
				return section.destroy();
			});

			this.spineItems = undefined;
			this.spineByHref = undefined;
			this.spineById = undefined;

			this.hooks.serialize.clear();
			this.hooks.content.clear();
			this.hooks = undefined;

			this.epubcfi = undefined;

			this.loaded = false;

			this.items = undefined;
			this.manifest = undefined;
			this.spineNodeIndex = undefined;
			this.baseUrl = undefined;
			this.length = undefined;
		}
	}]);

	return Spine;
}();

exports.default = Spine;
module.exports = exports["default"];

/***/ }),
/* 373 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _core = __webpack_require__(6);

var _epubcfi = __webpack_require__(22);

var _epubcfi2 = _interopRequireDefault(_epubcfi);

var _hook = __webpack_require__(101);

var _hook2 = _interopRequireDefault(_hook);

var _replacements = __webpack_require__(72);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Represents a Section of the Book
 *
 * In most books this is equivelent to a Chapter
 * @param {object} item  The spine item representing the section
 * @param {object} hooks hooks for serialize and content
 */
var Section = function () {
	function Section(item, hooks) {
		_classCallCheck(this, Section);

		this.idref = item.idref;
		this.linear = item.linear === "yes";
		this.properties = item.properties;
		this.index = item.index;
		this.href = item.href;
		this.url = item.url;
		this.canonical = item.canonical;
		this.next = item.next;
		this.prev = item.prev;

		this.cfiBase = item.cfiBase;

		if (hooks) {
			this.hooks = hooks;
		} else {
			this.hooks = {};
			this.hooks.serialize = new _hook2.default(this);
			this.hooks.content = new _hook2.default(this);
		}

		this.document = undefined;
		this.contents = undefined;
		this.output = undefined;
	}

	/**
  * Load the section from its url
  * @param  {method} [_request] a request method to use for loading
  * @return {document} a promise with the xml document
  */


	_createClass(Section, [{
		key: "load",
		value: function load(_request) {
			var request = _request || this.request || __webpack_require__(73);
			var loading = new _core.defer();
			var loaded = loading.promise;

			if (this.contents) {
				loading.resolve(this.contents);
			} else {
				request(this.url).then(function (xml) {
					// var directory = new Url(this.url).directory;

					this.document = xml;
					this.contents = xml.documentElement;

					return this.hooks.content.trigger(this.document, this);
				}.bind(this)).then(function () {
					loading.resolve(this.contents);
				}.bind(this)).catch(function (error) {
					loading.reject(error);
				});
			}

			return loaded;
		}

		/**
   * Adds a base tag for resolving urls in the section
   * @private
   */

	}, {
		key: "base",
		value: function base() {
			return (0, _replacements.replaceBase)(this.document, this);
		}

		/**
   * Render the contents of a section
   * @param  {method} [_request] a request method to use for loading
   * @return {string} output a serialized XML Document
   */

	}, {
		key: "render",
		value: function render(_request) {
			var rendering = new _core.defer();
			var rendered = rendering.promise;
			this.output; // TODO: better way to return this from hooks?

			this.load(_request).then(function (contents) {
				var userAgent = typeof navigator !== 'undefined' && navigator.userAgent || '';
				var isIE = userAgent.indexOf('Trident') >= 0;
				var Serializer;
				if (typeof XMLSerializer === "undefined" || isIE) {
					Serializer = __webpack_require__(374).XMLSerializer;
				} else {
					Serializer = XMLSerializer;
				}
				var serializer = new Serializer();
				this.output = serializer.serializeToString(contents);
				return this.output;
			}.bind(this)).then(function () {
				return this.hooks.serialize.trigger(this.output, this);
			}.bind(this)).then(function () {
				rendering.resolve(this.output);
			}.bind(this)).catch(function (error) {
				rendering.reject(error);
			});

			return rendered;
		}

		/**
   * Find a string in a section
   * @param  {string} _query The query string to find
   * @return {object[]} A list of matches, with form {cfi, excerpt}
   */

	}, {
		key: "find",
		value: function find(_query) {
			var section = this;
			var matches = [];
			var query = _query.toLowerCase();
			var find = function find(node) {
				var text = node.textContent.toLowerCase();
				var range = section.document.createRange();
				var cfi;
				var pos;
				var last = -1;
				var excerpt;
				var limit = 150;

				while (pos != -1) {
					// Search for the query
					pos = text.indexOf(query, last + 1);

					if (pos != -1) {
						// We found it! Generate a CFI
						range = section.document.createRange();
						range.setStart(node, pos);
						range.setEnd(node, pos + query.length);

						cfi = section.cfiFromRange(range);

						// Generate the excerpt
						if (node.textContent.length < limit) {
							excerpt = node.textContent;
						} else {
							excerpt = node.textContent.substring(pos - limit / 2, pos + limit / 2);
							excerpt = "..." + excerpt + "...";
						}

						// Add the CFI to the matches list
						matches.push({
							cfi: cfi,
							excerpt: excerpt
						});
					}

					last = pos;
				}
			};

			(0, _core.sprint)(section.document, function (node) {
				find(node);
			});

			return matches;
		}
	}, {
		key: "reconcileLayoutSettings",


		/**
  * Reconciles the current chapters layout properies with
  * the global layout properities.
  * @param {object} globalLayout  The global layout settings object, chapter properties string
  * @return {object} layoutProperties Object with layout properties
  */
		value: function reconcileLayoutSettings(globalLayout) {
			//-- Get the global defaults
			var settings = {
				layout: globalLayout.layout,
				spread: globalLayout.spread,
				orientation: globalLayout.orientation
			};

			//-- Get the chapter's display type
			this.properties.forEach(function (prop) {
				var rendition = prop.replace("rendition:", "");
				var split = rendition.indexOf("-");
				var property, value;

				if (split != -1) {
					property = rendition.slice(0, split);
					value = rendition.slice(split + 1);

					settings[property] = value;
				}
			});
			return settings;
		}

		/**
   * Get a CFI from a Range in the Section
   * @param  {range} _range
   * @return {string} cfi an EpubCFI string
   */

	}, {
		key: "cfiFromRange",
		value: function cfiFromRange(_range) {
			return new _epubcfi2.default(_range, this.cfiBase).toString();
		}

		/**
   * Get a CFI from an Element in the Section
   * @param  {element} el
   * @return {string} cfi an EpubCFI string
   */

	}, {
		key: "cfiFromElement",
		value: function cfiFromElement(el) {
			return new _epubcfi2.default(el, this.cfiBase).toString();
		}

		/**
   * Unload the section document
   */

	}, {
		key: "unload",
		value: function unload() {
			this.document = undefined;
			this.contents = undefined;
			this.output = undefined;
		}
	}, {
		key: "destroy",
		value: function destroy() {
			this.unload();
			this.hooks.serialize.clear();
			this.hooks.content.clear();

			this.hooks = undefined;
			this.idref = undefined;
			this.linear = undefined;
			this.properties = undefined;
			this.index = undefined;
			this.href = undefined;
			this.url = undefined;
			this.next = undefined;
			this.prev = undefined;

			this.cfiBase = undefined;
		}
	}]);

	return Section;
}();

exports.default = Section;
module.exports = exports["default"];

/***/ }),
/* 374 */
/***/ (function(module, exports, __webpack_require__) {

function DOMParser(options){
	this.options = options ||{locator:{}};

}
DOMParser.prototype.parseFromString = function(source,mimeType){
	var options = this.options;
	var sax =  new XMLReader();
	var domBuilder = options.domBuilder || new DOMHandler();//contentHandler and LexicalHandler
	var errorHandler = options.errorHandler;
	var locator = options.locator;
	var defaultNSMap = options.xmlns||{};
	var entityMap = {'lt':'<','gt':'>','amp':'&','quot':'"','apos':"'"}
	if(locator){
		domBuilder.setDocumentLocator(locator)
	}

	sax.errorHandler = buildErrorHandler(errorHandler,domBuilder,locator);
	sax.domBuilder = options.domBuilder || domBuilder;
	if(/\/x?html?$/.test(mimeType)){
		entityMap.nbsp = '\xa0';
		entityMap.copy = '\xa9';
		defaultNSMap['']= 'http://www.w3.org/1999/xhtml';
	}
	defaultNSMap.xml = defaultNSMap.xml || 'http://www.w3.org/XML/1998/namespace';
	if(source){
		sax.parse(source,defaultNSMap,entityMap);
	}else{
		sax.errorHandler.error("invalid doc source");
	}
	return domBuilder.doc;
}
function buildErrorHandler(errorImpl,domBuilder,locator){
	if(!errorImpl){
		if(domBuilder instanceof DOMHandler){
			return domBuilder;
		}
		errorImpl = domBuilder ;
	}
	var errorHandler = {}
	var isCallback = errorImpl instanceof Function;
	locator = locator||{}
	function build(key){
		var fn = errorImpl[key];
		if(!fn && isCallback){
			fn = errorImpl.length == 2?function(msg){errorImpl(key,msg)}:errorImpl;
		}
		errorHandler[key] = fn && function(msg){
			fn('[xmldom '+key+']\t'+msg+_locator(locator));
		}||function(){};
	}
	build('warning');
	build('error');
	build('fatalError');
	return errorHandler;
}

//console.log('#\n\n\n\n\n\n\n####')
/**
 * +ContentHandler+ErrorHandler
 * +LexicalHandler+EntityResolver2
 * -DeclHandler-DTDHandler
 *
 * DefaultHandler:EntityResolver, DTDHandler, ContentHandler, ErrorHandler
 * DefaultHandler2:DefaultHandler,LexicalHandler, DeclHandler, EntityResolver2
 * @link http://www.saxproject.org/apidoc/org/xml/sax/helpers/DefaultHandler.html
 */
function DOMHandler() {
    this.cdata = false;
}
function position(locator,node){
	node.lineNumber = locator.lineNumber;
	node.columnNumber = locator.columnNumber;
}
/**
 * @see org.xml.sax.ContentHandler#startDocument
 * @link http://www.saxproject.org/apidoc/org/xml/sax/ContentHandler.html
 */
DOMHandler.prototype = {
	startDocument : function() {
    	this.doc = new DOMImplementation().createDocument(null, null, null);
    	if (this.locator) {
        	this.doc.documentURI = this.locator.systemId;
    	}
	},
	startElement:function(namespaceURI, localName, qName, attrs) {
		var doc = this.doc;
	    var el = doc.createElementNS(namespaceURI, qName||localName);
	    var len = attrs.length;
	    appendElement(this, el);
	    this.currentElement = el;

		this.locator && position(this.locator,el)
	    for (var i = 0 ; i < len; i++) {
	        var namespaceURI = attrs.getURI(i);
	        var value = attrs.getValue(i);
	        var qName = attrs.getQName(i);
			var attr = doc.createAttributeNS(namespaceURI, qName);
			this.locator &&position(attrs.getLocator(i),attr);
			attr.value = attr.nodeValue = value;
			el.setAttributeNode(attr)
	    }
	},
	endElement:function(namespaceURI, localName, qName) {
		var current = this.currentElement
		var tagName = current.tagName;
		this.currentElement = current.parentNode;
	},
	startPrefixMapping:function(prefix, uri) {
	},
	endPrefixMapping:function(prefix) {
	},
	processingInstruction:function(target, data) {
	    var ins = this.doc.createProcessingInstruction(target, data);
	    this.locator && position(this.locator,ins)
	    appendElement(this, ins);
	},
	ignorableWhitespace:function(ch, start, length) {
	},
	characters:function(chars, start, length) {
		chars = _toString.apply(this,arguments)
		//console.log(chars)
		if(chars){
			if (this.cdata) {
				var charNode = this.doc.createCDATASection(chars);
			} else {
				var charNode = this.doc.createTextNode(chars);
			}
			if(this.currentElement){
				this.currentElement.appendChild(charNode);
			}else if(/^\s*$/.test(chars)){
				this.doc.appendChild(charNode);
				//process xml
			}
			this.locator && position(this.locator,charNode)
		}
	},
	skippedEntity:function(name) {
	},
	endDocument:function() {
		this.doc.normalize();
	},
	setDocumentLocator:function (locator) {
	    if(this.locator = locator){// && !('lineNumber' in locator)){
	    	locator.lineNumber = 0;
	    }
	},
	//LexicalHandler
	comment:function(chars, start, length) {
		chars = _toString.apply(this,arguments)
	    var comm = this.doc.createComment(chars);
	    this.locator && position(this.locator,comm)
	    appendElement(this, comm);
	},

	startCDATA:function() {
	    //used in characters() methods
	    this.cdata = true;
	},
	endCDATA:function() {
	    this.cdata = false;
	},

	startDTD:function(name, publicId, systemId) {
		var impl = this.doc.implementation;
	    if (impl && impl.createDocumentType) {
	        var dt = impl.createDocumentType(name, publicId, systemId);
	        this.locator && position(this.locator,dt)
	        appendElement(this, dt);
	    }
	},
	/**
	 * @see org.xml.sax.ErrorHandler
	 * @link http://www.saxproject.org/apidoc/org/xml/sax/ErrorHandler.html
	 */
	warning:function(error) {
		console.warn('[xmldom warning]\t'+error,_locator(this.locator));
	},
	error:function(error) {
		console.error('[xmldom error]\t'+error,_locator(this.locator));
	},
	fatalError:function(error) {
		console.error('[xmldom fatalError]\t'+error,_locator(this.locator));
	    throw error;
	}
}
function _locator(l){
	if(l){
		return '\n@'+(l.systemId ||'')+'#[line:'+l.lineNumber+',col:'+l.columnNumber+']'
	}
}
function _toString(chars,start,length){
	if(typeof chars == 'string'){
		return chars.substr(start,length)
	}else{//java sax connect width xmldom on rhino(what about: "? && !(chars instanceof String)")
		if(chars.length >= start+length || start){
			return new java.lang.String(chars,start,length)+'';
		}
		return chars;
	}
}

/*
 * @link http://www.saxproject.org/apidoc/org/xml/sax/ext/LexicalHandler.html
 * used method of org.xml.sax.ext.LexicalHandler:
 *  #comment(chars, start, length)
 *  #startCDATA()
 *  #endCDATA()
 *  #startDTD(name, publicId, systemId)
 *
 *
 * IGNORED method of org.xml.sax.ext.LexicalHandler:
 *  #endDTD()
 *  #startEntity(name)
 *  #endEntity(name)
 *
 *
 * @link http://www.saxproject.org/apidoc/org/xml/sax/ext/DeclHandler.html
 * IGNORED method of org.xml.sax.ext.DeclHandler
 * 	#attributeDecl(eName, aName, type, mode, value)
 *  #elementDecl(name, model)
 *  #externalEntityDecl(name, publicId, systemId)
 *  #internalEntityDecl(name, value)
 * @link http://www.saxproject.org/apidoc/org/xml/sax/ext/EntityResolver2.html
 * IGNORED method of org.xml.sax.EntityResolver2
 *  #resolveEntity(String name,String publicId,String baseURI,String systemId)
 *  #resolveEntity(publicId, systemId)
 *  #getExternalSubset(name, baseURI)
 * @link http://www.saxproject.org/apidoc/org/xml/sax/DTDHandler.html
 * IGNORED method of org.xml.sax.DTDHandler
 *  #notationDecl(name, publicId, systemId) {};
 *  #unparsedEntityDecl(name, publicId, systemId, notationName) {};
 */
"endDTD,startEntity,endEntity,attributeDecl,elementDecl,externalEntityDecl,internalEntityDecl,resolveEntity,getExternalSubset,notationDecl,unparsedEntityDecl".replace(/\w+/g,function(key){
	DOMHandler.prototype[key] = function(){return null}
})

/* Private static helpers treated below as private instance methods, so don't need to add these to the public API; we might use a Relator to also get rid of non-standard public properties */
function appendElement (hander,node) {
    if (!hander.currentElement) {
        hander.doc.appendChild(node);
    } else {
        hander.currentElement.appendChild(node);
    }
}//appendChild and setAttributeNS are preformance key

//if(typeof require == 'function'){
	var XMLReader = __webpack_require__(375).XMLReader;
	var DOMImplementation = exports.DOMImplementation = __webpack_require__(140).DOMImplementation;
	exports.XMLSerializer = __webpack_require__(140).XMLSerializer ;
	exports.DOMParser = DOMParser;
//}


/***/ }),
/* 375 */
/***/ (function(module, exports) {

//[4]   	NameStartChar	   ::=   	":" | [A-Z] | "_" | [a-z] | [#xC0-#xD6] | [#xD8-#xF6] | [#xF8-#x2FF] | [#x370-#x37D] | [#x37F-#x1FFF] | [#x200C-#x200D] | [#x2070-#x218F] | [#x2C00-#x2FEF] | [#x3001-#xD7FF] | [#xF900-#xFDCF] | [#xFDF0-#xFFFD] | [#x10000-#xEFFFF]
//[4a]   	NameChar	   ::=   	NameStartChar | "-" | "." | [0-9] | #xB7 | [#x0300-#x036F] | [#x203F-#x2040]
//[5]   	Name	   ::=   	NameStartChar (NameChar)*
var nameStartChar = /[A-Z_a-z\xC0-\xD6\xD8-\xF6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD]///\u10000-\uEFFFF
var nameChar = new RegExp("[\\-\\.0-9"+nameStartChar.source.slice(1,-1)+"\\u00B7\\u0300-\\u036F\\u203F-\\u2040]");
var tagNamePattern = new RegExp('^'+nameStartChar.source+nameChar.source+'*(?:\:'+nameStartChar.source+nameChar.source+'*)?$');
//var tagNamePattern = /^[a-zA-Z_][\w\-\.]*(?:\:[a-zA-Z_][\w\-\.]*)?$/
//var handlers = 'resolveEntity,getExternalSubset,characters,endDocument,endElement,endPrefixMapping,ignorableWhitespace,processingInstruction,setDocumentLocator,skippedEntity,startDocument,startElement,startPrefixMapping,notationDecl,unparsedEntityDecl,error,fatalError,warning,attributeDecl,elementDecl,externalEntityDecl,internalEntityDecl,comment,endCDATA,endDTD,endEntity,startCDATA,startDTD,startEntity'.split(',')

//S_TAG,	S_ATTR,	S_EQ,	S_ATTR_NOQUOT_VALUE
//S_ATTR_SPACE,	S_ATTR_END,	S_TAG_SPACE, S_TAG_CLOSE
var S_TAG = 0;//tag name offerring
var S_ATTR = 1;//attr name offerring
var S_ATTR_SPACE=2;//attr name end and space offer
var S_EQ = 3;//=space?
var S_ATTR_NOQUOT_VALUE = 4;//attr value(no quot value only)
var S_ATTR_END = 5;//attr value end and no space(quot end)
var S_TAG_SPACE = 6;//(attr value end || tag end ) && (space offer)
var S_TAG_CLOSE = 7;//closed el<el />

function XMLReader(){

}

XMLReader.prototype = {
	parse:function(source,defaultNSMap,entityMap){
		var domBuilder = this.domBuilder;
		domBuilder.startDocument();
		_copy(defaultNSMap ,defaultNSMap = {})
		parse(source,defaultNSMap,entityMap,
				domBuilder,this.errorHandler);
		domBuilder.endDocument();
	}
}
function parse(source,defaultNSMapCopy,entityMap,domBuilder,errorHandler){
	function fixedFromCharCode(code) {
		// String.prototype.fromCharCode does not supports
		// > 2 bytes unicode chars directly
		if (code > 0xffff) {
			code -= 0x10000;
			var surrogate1 = 0xd800 + (code >> 10)
				, surrogate2 = 0xdc00 + (code & 0x3ff);

			return String.fromCharCode(surrogate1, surrogate2);
		} else {
			return String.fromCharCode(code);
		}
	}
	function entityReplacer(a){
		var k = a.slice(1,-1);
		if(k in entityMap){
			return entityMap[k];
		}else if(k.charAt(0) === '#'){
			return fixedFromCharCode(parseInt(k.substr(1).replace('x','0x')))
		}else{
			errorHandler.error('entity not found:'+a);
			return a;
		}
	}
	function appendText(end){//has some bugs
		if(end>start){
			var xt = source.substring(start,end).replace(/&#?\w+;/g,entityReplacer);
			locator&&position(start);
			domBuilder.characters(xt,0,end-start);
			start = end
		}
	}
	function position(p,m){
		while(p>=lineEnd && (m = linePattern.exec(source))){
			lineStart = m.index;
			lineEnd = lineStart + m[0].length;
			locator.lineNumber++;
			//console.log('line++:',locator,startPos,endPos)
		}
		locator.columnNumber = p-lineStart+1;
	}
	var lineStart = 0;
	var lineEnd = 0;
	var linePattern = /.*(?:\r\n?|\n)|.*$/g
	var locator = domBuilder.locator;

	var parseStack = [{currentNSMap:defaultNSMapCopy}]
	var closeMap = {};
	var start = 0;
	while(true){
		try{
			var tagStart = source.indexOf('<',start);
			if(tagStart<0){
				if(!source.substr(start).match(/^\s*$/)){
					var doc = domBuilder.doc;
	    			var text = doc.createTextNode(source.substr(start));
	    			doc.appendChild(text);
	    			domBuilder.currentElement = text;
				}
				return;
			}
			if(tagStart>start){
				appendText(tagStart);
			}
			switch(source.charAt(tagStart+1)){
			case '/':
				var end = source.indexOf('>',tagStart+3);
				var tagName = source.substring(tagStart+2,end);
				var config = parseStack.pop();
				if(end<0){

	        		tagName = source.substring(tagStart+2).replace(/[\s<].*/,'');
	        		//console.error('#@@@@@@'+tagName)
	        		errorHandler.error("end tag name: "+tagName+' is not complete:'+config.tagName);
	        		end = tagStart+1+tagName.length;
	        	}else if(tagName.match(/\s</)){
	        		tagName = tagName.replace(/[\s<].*/,'');
	        		errorHandler.error("end tag name: "+tagName+' maybe not complete');
	        		end = tagStart+1+tagName.length;
				}
				//console.error(parseStack.length,parseStack)
				//console.error(config);
				var localNSMap = config.localNSMap;
				var endMatch = config.tagName == tagName;
				var endIgnoreCaseMach = endMatch || config.tagName&&config.tagName.toLowerCase() == tagName.toLowerCase()
		        if(endIgnoreCaseMach){
		        	domBuilder.endElement(config.uri,config.localName,tagName);
					if(localNSMap){
						for(var prefix in localNSMap){
							domBuilder.endPrefixMapping(prefix) ;
						}
					}
					if(!endMatch){
		            	errorHandler.fatalError("end tag name: "+tagName+' is not match the current start tagName:'+config.tagName );
					}
		        }else{
		        	parseStack.push(config)
		        }

				end++;
				break;
				// end elment
			case '?':// <?...?>
				locator&&position(tagStart);
				end = parseInstruction(source,tagStart,domBuilder);
				break;
			case '!':// <!doctype,<![CDATA,<!--
				locator&&position(tagStart);
				end = parseDCC(source,tagStart,domBuilder,errorHandler);
				break;
			default:
				locator&&position(tagStart);
				var el = new ElementAttributes();
				var currentNSMap = parseStack[parseStack.length-1].currentNSMap;
				//elStartEnd
				var end = parseElementStartPart(source,tagStart,el,currentNSMap,entityReplacer,errorHandler);
				var len = el.length;


				if(!el.closed && fixSelfClosed(source,end,el.tagName,closeMap)){
					el.closed = true;
					if(!entityMap.nbsp){
						errorHandler.warning('unclosed xml attribute');
					}
				}
				if(locator && len){
					var locator2 = copyLocator(locator,{});
					//try{//attribute position fixed
					for(var i = 0;i<len;i++){
						var a = el[i];
						position(a.offset);
						a.locator = copyLocator(locator,{});
					}
					//}catch(e){console.error('@@@@@'+e)}
					domBuilder.locator = locator2
					if(appendElement(el,domBuilder,currentNSMap)){
						parseStack.push(el)
					}
					domBuilder.locator = locator;
				}else{
					if(appendElement(el,domBuilder,currentNSMap)){
						parseStack.push(el)
					}
				}



				if(el.uri === 'http://www.w3.org/1999/xhtml' && !el.closed){
					end = parseHtmlSpecialContent(source,end,el.tagName,entityReplacer,domBuilder)
				}else{
					end++;
				}
			}
		}catch(e){
			errorHandler.error('element parse error: '+e)
			//errorHandler.error('element parse error: '+e);
			end = -1;
			//throw e;
		}
		if(end>start){
			start = end;
		}else{
			//TODO: 这里有可能sax回退，有位置错误风险
			appendText(Math.max(tagStart,start)+1);
		}
	}
}
function copyLocator(f,t){
	t.lineNumber = f.lineNumber;
	t.columnNumber = f.columnNumber;
	return t;
}

/**
 * @see #appendElement(source,elStartEnd,el,selfClosed,entityReplacer,domBuilder,parseStack);
 * @return end of the elementStartPart(end of elementEndPart for selfClosed el)
 */
function parseElementStartPart(source,start,el,currentNSMap,entityReplacer,errorHandler){
	var attrName;
	var value;
	var p = ++start;
	var s = S_TAG;//status
	while(true){
		var c = source.charAt(p);
		switch(c){
		case '=':
			if(s === S_ATTR){//attrName
				attrName = source.slice(start,p);
				s = S_EQ;
			}else if(s === S_ATTR_SPACE){
				s = S_EQ;
			}else{
				//fatalError: equal must after attrName or space after attrName
				throw new Error('attribute equal must after attrName');
			}
			break;
		case '\'':
		case '"':
			if(s === S_EQ || s === S_ATTR //|| s == S_ATTR_SPACE
				){//equal
				if(s === S_ATTR){
					errorHandler.warning('attribute value must after "="')
					attrName = source.slice(start,p)
				}
				start = p+1;
				p = source.indexOf(c,start)
				if(p>0){
					value = source.slice(start,p).replace(/&#?\w+;/g,entityReplacer);
					el.add(attrName,value,start-1);
					s = S_ATTR_END;
				}else{
					//fatalError: no end quot match
					throw new Error('attribute value no end \''+c+'\' match');
				}
			}else if(s == S_ATTR_NOQUOT_VALUE){
				value = source.slice(start,p).replace(/&#?\w+;/g,entityReplacer);
				//console.log(attrName,value,start,p)
				el.add(attrName,value,start);
				//console.dir(el)
				errorHandler.warning('attribute "'+attrName+'" missed start quot('+c+')!!');
				start = p+1;
				s = S_ATTR_END
			}else{
				//fatalError: no equal before
				throw new Error('attribute value must after "="');
			}
			break;
		case '/':
			switch(s){
			case S_TAG:
				el.setTagName(source.slice(start,p));
			case S_ATTR_END:
			case S_TAG_SPACE:
			case S_TAG_CLOSE:
				s =S_TAG_CLOSE;
				el.closed = true;
			case S_ATTR_NOQUOT_VALUE:
			case S_ATTR:
			case S_ATTR_SPACE:
				break;
			//case S_EQ:
			default:
				throw new Error("attribute invalid close char('/')")
			}
			break;
		case ''://end document
			//throw new Error('unexpected end of input')
			errorHandler.error('unexpected end of input');
			if(s == S_TAG){
				el.setTagName(source.slice(start,p));
			}
			return p;
		case '>':
			switch(s){
			case S_TAG:
				el.setTagName(source.slice(start,p));
			case S_ATTR_END:
			case S_TAG_SPACE:
			case S_TAG_CLOSE:
				break;//normal
			case S_ATTR_NOQUOT_VALUE://Compatible state
			case S_ATTR:
				value = source.slice(start,p);
				if(value.slice(-1) === '/'){
					el.closed  = true;
					value = value.slice(0,-1)
				}
			case S_ATTR_SPACE:
				if(s === S_ATTR_SPACE){
					value = attrName;
				}
				if(s == S_ATTR_NOQUOT_VALUE){
					errorHandler.warning('attribute "'+value+'" missed quot(")!!');
					el.add(attrName,value.replace(/&#?\w+;/g,entityReplacer),start)
				}else{
					if(currentNSMap[''] !== 'http://www.w3.org/1999/xhtml' || !value.match(/^(?:disabled|checked|selected)$/i)){
						errorHandler.warning('attribute "'+value+'" missed value!! "'+value+'" instead!!')
					}
					el.add(value,value,start)
				}
				break;
			case S_EQ:
				throw new Error('attribute value missed!!');
			}
//			console.log(tagName,tagNamePattern,tagNamePattern.test(tagName))
			return p;
		/*xml space '\x20' | #x9 | #xD | #xA; */
		case '\u0080':
			c = ' ';
		default:
			if(c<= ' '){//space
				switch(s){
				case S_TAG:
					el.setTagName(source.slice(start,p));//tagName
					s = S_TAG_SPACE;
					break;
				case S_ATTR:
					attrName = source.slice(start,p)
					s = S_ATTR_SPACE;
					break;
				case S_ATTR_NOQUOT_VALUE:
					var value = source.slice(start,p).replace(/&#?\w+;/g,entityReplacer);
					errorHandler.warning('attribute "'+value+'" missed quot(")!!');
					el.add(attrName,value,start)
				case S_ATTR_END:
					s = S_TAG_SPACE;
					break;
				//case S_TAG_SPACE:
				//case S_EQ:
				//case S_ATTR_SPACE:
				//	void();break;
				//case S_TAG_CLOSE:
					//ignore warning
				}
			}else{//not space
//S_TAG,	S_ATTR,	S_EQ,	S_ATTR_NOQUOT_VALUE
//S_ATTR_SPACE,	S_ATTR_END,	S_TAG_SPACE, S_TAG_CLOSE
				switch(s){
				//case S_TAG:void();break;
				//case S_ATTR:void();break;
				//case S_ATTR_NOQUOT_VALUE:void();break;
				case S_ATTR_SPACE:
					var tagName =  el.tagName;
					if(currentNSMap[''] !== 'http://www.w3.org/1999/xhtml' || !attrName.match(/^(?:disabled|checked|selected)$/i)){
						errorHandler.warning('attribute "'+attrName+'" missed value!! "'+attrName+'" instead2!!')
					}
					el.add(attrName,attrName,start);
					start = p;
					s = S_ATTR;
					break;
				case S_ATTR_END:
					errorHandler.warning('attribute space is required"'+attrName+'"!!')
				case S_TAG_SPACE:
					s = S_ATTR;
					start = p;
					break;
				case S_EQ:
					s = S_ATTR_NOQUOT_VALUE;
					start = p;
					break;
				case S_TAG_CLOSE:
					throw new Error("elements closed character '/' and '>' must be connected to");
				}
			}
		}//end outer switch
		//console.log('p++',p)
		p++;
	}
}
/**
 * @return true if has new namespace define
 */
function appendElement(el,domBuilder,currentNSMap){
	var tagName = el.tagName;
	var localNSMap = null;
	//var currentNSMap = parseStack[parseStack.length-1].currentNSMap;
	var i = el.length;
	while(i--){
		var a = el[i];
		var qName = a.qName;
		var value = a.value;
		var nsp = qName.indexOf(':');
		if(nsp>0){
			var prefix = a.prefix = qName.slice(0,nsp);
			var localName = qName.slice(nsp+1);
			var nsPrefix = prefix === 'xmlns' && localName
		}else{
			localName = qName;
			prefix = null
			nsPrefix = qName === 'xmlns' && ''
		}
		//can not set prefix,because prefix !== ''
		a.localName = localName ;
		//prefix == null for no ns prefix attribute
		if(nsPrefix !== false){//hack!!
			if(localNSMap == null){
				localNSMap = {}
				//console.log(currentNSMap,0)
				_copy(currentNSMap,currentNSMap={})
				//console.log(currentNSMap,1)
			}
			currentNSMap[nsPrefix] = localNSMap[nsPrefix] = value;
			a.uri = 'http://www.w3.org/2000/xmlns/'
			domBuilder.startPrefixMapping(nsPrefix, value)
		}
	}
	var i = el.length;
	while(i--){
		a = el[i];
		var prefix = a.prefix;
		if(prefix){//no prefix attribute has no namespace
			if(prefix === 'xml'){
				a.uri = 'http://www.w3.org/XML/1998/namespace';
			}if(prefix !== 'xmlns'){
				a.uri = currentNSMap[prefix || '']

				//{console.log('###'+a.qName,domBuilder.locator.systemId+'',currentNSMap,a.uri)}
			}
		}
	}
	var nsp = tagName.indexOf(':');
	if(nsp>0){
		prefix = el.prefix = tagName.slice(0,nsp);
		localName = el.localName = tagName.slice(nsp+1);
	}else{
		prefix = null;//important!!
		localName = el.localName = tagName;
	}
	//no prefix element has default namespace
	var ns = el.uri = currentNSMap[prefix || ''];
	domBuilder.startElement(ns,localName,tagName,el);
	//endPrefixMapping and startPrefixMapping have not any help for dom builder
	//localNSMap = null
	if(el.closed){
		domBuilder.endElement(ns,localName,tagName);
		if(localNSMap){
			for(prefix in localNSMap){
				domBuilder.endPrefixMapping(prefix)
			}
		}
	}else{
		el.currentNSMap = currentNSMap;
		el.localNSMap = localNSMap;
		//parseStack.push(el);
		return true;
	}
}
function parseHtmlSpecialContent(source,elStartEnd,tagName,entityReplacer,domBuilder){
	if(/^(?:script|textarea)$/i.test(tagName)){
		var elEndStart =  source.indexOf('</'+tagName+'>',elStartEnd);
		var text = source.substring(elStartEnd+1,elEndStart);
		if(/[&<]/.test(text)){
			if(/^script$/i.test(tagName)){
				//if(!/\]\]>/.test(text)){
					//lexHandler.startCDATA();
					domBuilder.characters(text,0,text.length);
					//lexHandler.endCDATA();
					return elEndStart;
				//}
			}//}else{//text area
				text = text.replace(/&#?\w+;/g,entityReplacer);
				domBuilder.characters(text,0,text.length);
				return elEndStart;
			//}

		}
	}
	return elStartEnd+1;
}
function fixSelfClosed(source,elStartEnd,tagName,closeMap){
	//if(tagName in closeMap){
	var pos = closeMap[tagName];
	if(pos == null){
		//console.log(tagName)
		pos =  source.lastIndexOf('</'+tagName+'>')
		if(pos<elStartEnd){//忘记闭合
			pos = source.lastIndexOf('</'+tagName)
		}
		closeMap[tagName] =pos
	}
	return pos<elStartEnd;
	//}
}
function _copy(source,target){
	for(var n in source){target[n] = source[n]}
}
function parseDCC(source,start,domBuilder,errorHandler){//sure start with '<!'
	var next= source.charAt(start+2)
	switch(next){
	case '-':
		if(source.charAt(start + 3) === '-'){
			var end = source.indexOf('-->',start+4);
			//append comment source.substring(4,end)//<!--
			if(end>start){
				domBuilder.comment(source,start+4,end-start-4);
				return end+3;
			}else{
				errorHandler.error("Unclosed comment");
				return -1;
			}
		}else{
			//error
			return -1;
		}
	default:
		if(source.substr(start+3,6) == 'CDATA['){
			var end = source.indexOf(']]>',start+9);
			domBuilder.startCDATA();
			domBuilder.characters(source,start+9,end-start-9);
			domBuilder.endCDATA()
			return end+3;
		}
		//<!DOCTYPE
		//startDTD(java.lang.String name, java.lang.String publicId, java.lang.String systemId)
		var matchs = split(source,start);
		var len = matchs.length;
		if(len>1 && /!doctype/i.test(matchs[0][0])){
			var name = matchs[1][0];
			var pubid = len>3 && /^public$/i.test(matchs[2][0]) && matchs[3][0]
			var sysid = len>4 && matchs[4][0];
			var lastMatch = matchs[len-1]
			domBuilder.startDTD(name,pubid && pubid.replace(/^(['"])(.*?)\1$/,'$2'),
					sysid && sysid.replace(/^(['"])(.*?)\1$/,'$2'));
			domBuilder.endDTD();

			return lastMatch.index+lastMatch[0].length
		}
	}
	return -1;
}



function parseInstruction(source,start,domBuilder){
	var end = source.indexOf('?>',start);
	if(end){
		var match = source.substring(start,end).match(/^<\?(\S*)\s*([\s\S]*?)\s*$/);
		if(match){
			var len = match[0].length;
			domBuilder.processingInstruction(match[1], match[2]) ;
			return end+2;
		}else{//error
			return -1;
		}
	}
	return -1;
}

/**
 * @param source
 */
function ElementAttributes(source){

}
ElementAttributes.prototype = {
	setTagName:function(tagName){
		if(!tagNamePattern.test(tagName)){
			throw new Error('invalid tagName:'+tagName)
		}
		this.tagName = tagName
	},
	add:function(qName,value,offset){
		if(!tagNamePattern.test(qName)){
			throw new Error('invalid attribute:'+qName)
		}
		this[this.length++] = {qName:qName,value:value,offset:offset}
	},
	length:0,
	getLocalName:function(i){return this[i].localName},
	getLocator:function(i){return this[i].locator},
	getQName:function(i){return this[i].qName},
	getURI:function(i){return this[i].uri},
	getValue:function(i){return this[i].value}
//	,getIndex:function(uri, localName)){
//		if(localName){
//
//		}else{
//			var qName = uri
//		}
//	},
//	getValue:function(){return this.getValue(this.getIndex.apply(this,arguments))},
//	getType:function(uri,localName){}
//	getType:function(i){},
}




function _set_proto_(thiz,parent){
	thiz.__proto__ = parent;
	return thiz;
}
if(!(_set_proto_({},_set_proto_.prototype) instanceof _set_proto_)){
	_set_proto_ = function(thiz,parent){
		function p(){};
		p.prototype = parent;
		p = new p();
		for(parent in thiz){
			p[parent] = thiz[parent];
		}
		return p;
	}
}

function split(source,start){
	var match;
	var buf = [];
	var reg = /'[^']+'|"[^"]+"|[^\s<>\/=]+=?|(\/?\s*>|<)/g;
	reg.lastIndex = start;
	reg.exec(source);//skip <
	while(match = reg.exec(source)){
		buf.push(match);
		if(match[1])return buf;
	}
}

exports.XMLReader = XMLReader;



/***/ }),
/* 376 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _core = __webpack_require__(6);

var _queue = __webpack_require__(102);

var _queue2 = _interopRequireDefault(_queue);

var _epubcfi = __webpack_require__(22);

var _epubcfi2 = _interopRequireDefault(_epubcfi);

var _constants = __webpack_require__(23);

var _eventEmitter = __webpack_require__(30);

var _eventEmitter2 = _interopRequireDefault(_eventEmitter);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Find Locations for a Book
 * @param {Spine} spine
 * @param {request} request
 * @param {number} [pause=100]
 */
var Locations = function () {
	function Locations(spine, request, pause) {
		_classCallCheck(this, Locations);

		this.spine = spine;
		this.request = request;
		this.pause = pause || 100;

		this.q = new _queue2.default(this);
		this.epubcfi = new _epubcfi2.default();

		this._locations = [];
		this.total = 0;

		this.break = 150;

		this._current = 0;

		this.currentLocation = '';
		this._currentCfi = '';
		this.processingTimeout = undefined;
	}

	/**
  * Load all of sections in the book to generate locations
  * @param  {int} chars how many chars to split on
  * @return {object} locations
  */


	_createClass(Locations, [{
		key: "generate",
		value: function generate(chars) {

			if (chars) {
				this.break = chars;
			}

			this.q.pause();

			this.spine.each(function (section) {
				if (section.linear) {
					this.q.enqueue(this.process.bind(this), section);
				}
			}.bind(this));

			return this.q.run().then(function () {
				this.total = this._locations.length - 1;

				if (this._currentCfi) {
					this.currentLocation = this._currentCfi;
				}

				return this._locations;
				// console.log(this.percentage(this.book.rendition.location.start), this.percentage(this.book.rendition.location.end));
			}.bind(this));
		}
	}, {
		key: "createRange",
		value: function createRange() {
			return {
				startContainer: undefined,
				startOffset: undefined,
				endContainer: undefined,
				endOffset: undefined
			};
		}
	}, {
		key: "process",
		value: function process(section) {

			return section.load(this.request).then(function (contents) {
				var completed = new _core.defer();
				var locations = this.parse(contents, section.cfiBase);
				this._locations = this._locations.concat(locations);

				section.unload();

				this.processingTimeout = setTimeout(function () {
					return completed.resolve(locations);
				}, this.pause);
				return completed.promise;
			}.bind(this));
		}
	}, {
		key: "parse",
		value: function parse(contents, cfiBase, chars) {
			var locations = [];
			var range;
			var doc = contents.ownerDocument;
			var body = (0, _core.qs)(doc, "body");
			var counter = 0;
			var prev;
			var _break = chars || this.break;
			var parser = function parser(node) {
				var len = node.length;
				var dist;
				var pos = 0;

				if (node.textContent.trim().length === 0) {
					return false; // continue
				}

				// Start range
				if (counter == 0) {
					range = this.createRange();
					range.startContainer = node;
					range.startOffset = 0;
				}

				dist = _break - counter;

				// Node is smaller than a break,
				// skip over it
				if (dist > len) {
					counter += len;
					pos = len;
				}

				while (pos < len) {
					dist = _break - counter;

					if (counter === 0) {
						// Start new range
						pos += 1;
						range = this.createRange();
						range.startContainer = node;
						range.startOffset = pos;
					}

					// pos += dist;

					// Gone over
					if (pos + dist >= len) {
						// Continue counter for next node
						counter += len - pos;
						// break
						pos = len;
						// At End
					} else {
						// Advance pos
						pos += dist;

						// End the previous range
						range.endContainer = node;
						range.endOffset = pos;
						// cfi = section.cfiFromRange(range);
						var cfi = new _epubcfi2.default(range, cfiBase).toString();
						locations.push(cfi);
						counter = 0;
					}
				}
				prev = node;
			};

			(0, _core.sprint)(body, parser.bind(this));

			// Close remaining
			if (range && range.startContainer && prev) {
				range.endContainer = prev;
				range.endOffset = prev.length;
				var cfi = new _epubcfi2.default(range, cfiBase).toString();
				locations.push(cfi);
				counter = 0;
			}

			return locations;
		}

		/**
   * Get a location from an EpubCFI
   * @param {EpubCFI} cfi
   * @return {number}
   */

	}, {
		key: "locationFromCfi",
		value: function locationFromCfi(cfi) {
			var loc = void 0;
			if (_epubcfi2.default.prototype.isCfiString(cfi)) {
				cfi = new _epubcfi2.default(cfi);
			}
			// Check if the location has not been set yet
			if (this._locations.length === 0) {
				return -1;
			}

			loc = (0, _core.locationOf)(cfi, this._locations, this.epubcfi.compare);

			if (loc > this.total) {
				return this.total;
			}

			return loc;
		}

		/**
   * Get a percentage position in locations from an EpubCFI
   * @param {EpubCFI} cfi
   * @return {number}
   */

	}, {
		key: "percentageFromCfi",
		value: function percentageFromCfi(cfi) {
			if (this._locations.length === 0) {
				return null;
			}
			// Find closest cfi
			var loc = this.locationFromCfi(cfi);
			// Get percentage in total
			return this.percentageFromLocation(loc);
		}

		/**
   * Get a percentage position from a location index
   * @param {number} location
   * @return {number}
   */

	}, {
		key: "percentageFromLocation",
		value: function percentageFromLocation(loc) {
			if (!loc || !this.total) {
				return 0;
			}

			return loc / this.total;
		}

		/**
   * Get an EpubCFI from location index
   * @param {number} loc
   * @return {EpubCFI} cfi
   */

	}, {
		key: "cfiFromLocation",
		value: function cfiFromLocation(loc) {
			var cfi = -1;
			// check that pg is an int
			if (typeof loc != "number") {
				loc = parseInt(loc);
			}

			if (loc >= 0 && loc < this._locations.length) {
				cfi = this._locations[loc];
			}

			return cfi;
		}

		/**
   * Get an EpubCFI from location percentage
   * @param {number} percentage
   * @return {EpubCFI} cfi
   */

	}, {
		key: "cfiFromPercentage",
		value: function cfiFromPercentage(percentage) {
			var loc = void 0;
			if (percentage > 1) {
				console.warn("Normalize cfiFromPercentage value to between 0 - 1");
			}

			// Make sure 1 goes to very end
			if (percentage >= 1) {
				var cfi = new _epubcfi2.default(this._locations[this.total]);
				cfi.collapse();
				return cfi.toString();
			}

			loc = Math.ceil(this.total * percentage);
			return this.cfiFromLocation(loc);
		}

		/**
   * Load locations from JSON
   * @param {json} locations
   */

	}, {
		key: "load",
		value: function load(locations) {
			if (typeof locations === "string") {
				this._locations = JSON.parse(locations);
			} else {
				this._locations = locations;
			}
			this.total = this._locations.length - 1;
			return this._locations;
		}

		/**
   * Save locations to JSON
   * @return {json}
   */

	}, {
		key: "save",
		value: function save() {
			return JSON.stringify(this._locations);
		}
	}, {
		key: "getCurrent",
		value: function getCurrent() {
			return this._current;
		}
	}, {
		key: "setCurrent",
		value: function setCurrent(curr) {
			var loc;

			if (typeof curr == "string") {
				this._currentCfi = curr;
			} else if (typeof curr == "number") {
				this._current = curr;
			} else {
				return;
			}

			if (this._locations.length === 0) {
				return;
			}

			if (typeof curr == "string") {
				loc = this.locationFromCfi(curr);
				this._current = loc;
			} else {
				loc = curr;
			}

			this.emit(_constants.EVENTS.LOCATIONS.CHANGED, {
				percentage: this.percentageFromLocation(loc)
			});
		}

		/**
   * Get the current location
   */

	}, {
		key: "length",


		/**
   * Locations length
   */
		value: function length() {
			return this._locations.length;
		}
	}, {
		key: "destroy",
		value: function destroy() {
			this.spine = undefined;
			this.request = undefined;
			this.pause = undefined;

			this.q.stop();
			this.q = undefined;
			this.epubcfi = undefined;

			this._locations = undefined;
			this.total = undefined;

			this.break = undefined;
			this._current = undefined;

			this.currentLocation = undefined;
			this._currentCfi = undefined;
			clearTimeout(this.processingTimeout);
		}
	}, {
		key: "currentLocation",
		get: function get() {
			return this._current;
		}

		/**
   * Set the current location
   */
		,
		set: function set(curr) {
			this.setCurrent(curr);
		}
	}]);

	return Locations;
}();

(0, _eventEmitter2.default)(Locations.prototype);

exports.default = Locations;
module.exports = exports["default"];

/***/ }),
/* 377 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _pathWebpack = __webpack_require__(71);

var _pathWebpack2 = _interopRequireDefault(_pathWebpack);

var _core = __webpack_require__(6);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Handles Parsing and Accessing an Epub Container
 * @class
 * @param {document} [containerDocument] xml document
 */
var Container = function () {
	function Container(containerDocument) {
		_classCallCheck(this, Container);

		this.packagePath = '';
		this.directory = '';
		this.encoding = '';

		if (containerDocument) {
			this.parse(containerDocument);
		}
	}

	/**
  * Parse the Container XML
  * @param  {document} containerDocument
  */


	_createClass(Container, [{
		key: "parse",
		value: function parse(containerDocument) {
			//-- <rootfile full-path="OPS/package.opf" media-type="application/oebps-package+xml"/>
			var rootfile;

			if (!containerDocument) {
				throw new Error("Container File Not Found");
			}

			rootfile = (0, _core.qs)(containerDocument, "rootfile");

			if (!rootfile) {
				throw new Error("No RootFile Found");
			}

			this.packagePath = rootfile.getAttribute("full-path");
			this.directory = _pathWebpack2.default.dirname(this.packagePath);
			this.encoding = containerDocument.xmlEncoding;
		}
	}, {
		key: "destroy",
		value: function destroy() {
			this.packagePath = undefined;
			this.directory = undefined;
			this.encoding = undefined;
		}
	}]);

	return Container;
}();

exports.default = Container;
module.exports = exports["default"];

/***/ }),
/* 378 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _core = __webpack_require__(6);

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Open Packaging Format Parser
 * @class
 * @param {document} packageDocument OPF XML
 */
var Packaging = function () {
	function Packaging(packageDocument) {
		_classCallCheck(this, Packaging);

		this.manifest = {};
		this.navPath = '';
		this.ncxPath = '';
		this.coverPath = '';
		this.spineNodeIndex = 0;
		this.spine = [];
		this.metadata = {};

		if (packageDocument) {
			this.parse(packageDocument);
		}
	}

	/**
  * Parse OPF XML
  * @param  {document} packageDocument OPF XML
  * @return {object} parsed package parts
  */


	_createClass(Packaging, [{
		key: 'parse',
		value: function parse(packageDocument) {
			var metadataNode, manifestNode, spineNode;

			if (!packageDocument) {
				throw new Error("Package File Not Found");
			}

			metadataNode = (0, _core.qs)(packageDocument, "metadata");
			if (!metadataNode) {
				throw new Error("No Metadata Found");
			}

			manifestNode = (0, _core.qs)(packageDocument, "manifest");
			if (!manifestNode) {
				throw new Error("No Manifest Found");
			}

			spineNode = (0, _core.qs)(packageDocument, "spine");
			if (!spineNode) {
				throw new Error("No Spine Found");
			}

			this.manifest = this.parseManifest(manifestNode);
			this.navPath = this.findNavPath(manifestNode);
			this.ncxPath = this.findNcxPath(manifestNode, spineNode);
			this.coverPath = this.findCoverPath(packageDocument);

			this.spineNodeIndex = (0, _core.indexOfElementNode)(spineNode);

			this.spine = this.parseSpine(spineNode, this.manifest);

			this.uniqueIdentifier = this.findUniqueIdentifier(packageDocument);
			this.metadata = this.parseMetadata(metadataNode);

			this.metadata.direction = spineNode.getAttribute("page-progression-direction");

			return {
				"metadata": this.metadata,
				"spine": this.spine,
				"manifest": this.manifest,
				"navPath": this.navPath,
				"ncxPath": this.ncxPath,
				"coverPath": this.coverPath,
				"spineNodeIndex": this.spineNodeIndex
			};
		}

		/**
   * Parse Metadata
   * @private
   * @param  {node} xml
   * @return {object} metadata
   */

	}, {
		key: 'parseMetadata',
		value: function parseMetadata(xml) {
			var metadata = {};

			metadata.title = this.getElementText(xml, "title");
			metadata.creator = this.getElementText(xml, "creator");
			metadata.description = this.getElementText(xml, "description");

			metadata.pubdate = this.getElementText(xml, "date");

			metadata.publisher = this.getElementText(xml, "publisher");

			metadata.identifier = this.getElementText(xml, "identifier");
			metadata.language = this.getElementText(xml, "language");
			metadata.rights = this.getElementText(xml, "rights");

			metadata.modified_date = this.getPropertyText(xml, "dcterms:modified");

			metadata.layout = this.getPropertyText(xml, "rendition:layout");
			metadata.orientation = this.getPropertyText(xml, "rendition:orientation");
			metadata.flow = this.getPropertyText(xml, "rendition:flow");
			metadata.viewport = this.getPropertyText(xml, "rendition:viewport");
			metadata.media_active_class = this.getPropertyText(xml, "media:active-class");
			// metadata.page_prog_dir = packageXml.querySelector("spine").getAttribute("page-progression-direction");

			return metadata;
		}

		/**
   * Parse Manifest
   * @private
   * @param  {node} manifestXml
   * @return {object} manifest
   */

	}, {
		key: 'parseManifest',
		value: function parseManifest(manifestXml) {
			var manifest = {};

			//-- Turn items into an array
			// var selected = manifestXml.querySelectorAll("item");
			var selected = (0, _core.qsa)(manifestXml, "item");
			var items = Array.prototype.slice.call(selected);

			//-- Create an object with the id as key
			items.forEach(function (item) {
				var id = item.getAttribute("id"),
				    href = item.getAttribute("href") || "",
				    type = item.getAttribute("media-type") || "",
				    overlay = item.getAttribute("media-overlay") || "",
				    properties = item.getAttribute("properties") || "";

				manifest[id] = {
					"href": href,
					// "url" : href,
					"type": type,
					"overlay": overlay,
					"properties": properties.length ? properties.split(" ") : []
				};
			});

			return manifest;
		}

		/**
   * Parse Spine
   * @private
   * @param  {node} spineXml
   * @param  {Packaging.manifest} manifest
   * @return {object} spine
   */

	}, {
		key: 'parseSpine',
		value: function parseSpine(spineXml, manifest) {
			var spine = [];

			var selected = (0, _core.qsa)(spineXml, "itemref");
			var items = Array.prototype.slice.call(selected);

			// var epubcfi = new EpubCFI();

			//-- Add to array to mantain ordering and cross reference with manifest
			items.forEach(function (item, index) {
				var idref = item.getAttribute("idref");
				// var cfiBase = epubcfi.generateChapterComponent(spineNodeIndex, index, Id);
				var props = item.getAttribute("properties") || "";
				var propArray = props.length ? props.split(" ") : [];
				// var manifestProps = manifest[Id].properties;
				// var manifestPropArray = manifestProps.length ? manifestProps.split(" ") : [];

				var itemref = {
					"idref": idref,
					"linear": item.getAttribute("linear") || "yes",
					"properties": propArray,
					// "href" : manifest[Id].href,
					// "url" :  manifest[Id].url,
					"index": index
					// "cfiBase" : cfiBase
				};
				spine.push(itemref);
			});

			return spine;
		}

		/**
   * Find Unique Identifier
   * @private
   * @param  {node} packageXml
   * @return {string} Unique Identifier text
   */

	}, {
		key: 'findUniqueIdentifier',
		value: function findUniqueIdentifier(packageXml) {
			var uniqueIdentifierId = packageXml.documentElement.getAttribute("unique-identifier");
			if (!uniqueIdentifierId) {
				return "";
			}
			var identifier = packageXml.getElementById(uniqueIdentifierId);
			if (!identifier) {
				return "";
			}

			if (identifier.localName === "identifier" && identifier.namespaceURI === "http://purl.org/dc/elements/1.1/") {
				return identifier.childNodes[0].nodeValue.trim();
			}

			return "";
		}

		/**
   * Find TOC NAV
   * @private
   * @param {element} manifestNode
   * @return {string}
   */

	}, {
		key: 'findNavPath',
		value: function findNavPath(manifestNode) {
			// Find item with property "nav"
			// Should catch nav irregardless of order
			// var node = manifestNode.querySelector("item[properties$='nav'], item[properties^='nav '], item[properties*=' nav ']");
			var node = (0, _core.qsp)(manifestNode, "item", { "properties": "nav" });
			return node ? node.getAttribute("href") : false;
		}

		/**
   * Find TOC NCX
   * media-type="application/x-dtbncx+xml" href="toc.ncx"
   * @private
   * @param {element} manifestNode
   * @param {element} spineNode
   * @return {string}
   */

	}, {
		key: 'findNcxPath',
		value: function findNcxPath(manifestNode, spineNode) {
			// var node = manifestNode.querySelector("item[media-type='application/x-dtbncx+xml']");
			var node = (0, _core.qsp)(manifestNode, "item", { "media-type": "application/x-dtbncx+xml" });
			var tocId;

			// If we can't find the toc by media-type then try to look for id of the item in the spine attributes as
			// according to http://www.idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.4.1.2,
			// "The item that describes the NCX must be referenced by the spine toc attribute."
			if (!node) {
				tocId = spineNode.getAttribute("toc");
				if (tocId) {
					// node = manifestNode.querySelector("item[id='" + tocId + "']");
					node = manifestNode.querySelector('#' + tocId);
				}
			}

			return node ? node.getAttribute("href") : false;
		}

		/**
   * Find the Cover Path
   * <item properties="cover-image" id="ci" href="cover.svg" media-type="image/svg+xml" />
   * Fallback for Epub 2.0
   * @private
   * @param  {node} packageXml
   * @return {string} href
   */

	}, {
		key: 'findCoverPath',
		value: function findCoverPath(packageXml) {
			var pkg = (0, _core.qs)(packageXml, "package");
			var epubVersion = pkg.getAttribute("version");

			if (epubVersion === "2.0") {
				var metaCover = (0, _core.qsp)(packageXml, "meta", { "name": "cover" });
				if (metaCover) {
					var coverId = metaCover.getAttribute("content");
					// var cover = packageXml.querySelector("item[id='" + coverId + "']");
					var cover = packageXml.getElementById(coverId);
					return cover ? cover.getAttribute("href") : "";
				} else {
					return false;
				}
			} else {
				// var node = packageXml.querySelector("item[properties='cover-image']");
				var node = (0, _core.qsp)(packageXml, "item", { "properties": "cover-image" });
				return node ? node.getAttribute("href") : "";
			}
		}

		/**
   * Get text of a namespaced element
   * @private
   * @param  {node} xml
   * @param  {string} tag
   * @return {string} text
   */

	}, {
		key: 'getElementText',
		value: function getElementText(xml, tag) {
			var found = xml.getElementsByTagNameNS("http://purl.org/dc/elements/1.1/", tag);
			var el;

			if (!found || found.length === 0) return "";

			el = found[0];

			if (el.childNodes.length) {
				return el.childNodes[0].nodeValue;
			}

			return "";
		}

		/**
   * Get text by property
   * @private
   * @param  {node} xml
   * @param  {string} property
   * @return {string} text
   */

	}, {
		key: 'getPropertyText',
		value: function getPropertyText(xml, property) {
			var el = (0, _core.qsp)(xml, "meta", { "property": property });

			if (el && el.childNodes.length) {
				return el.childNodes[0].nodeValue;
			}

			return "";
		}

		/**
   * Load JSON Manifest
   * @param  {document} packageDocument OPF XML
   * @return {object} parsed package parts
   */

	}, {
		key: 'load',
		value: function load(json) {
			var _this = this;

			this.metadata = json.metadata;

			var spine = json.readingOrder || json.spine;
			this.spine = spine.map(function (item, index) {
				item.index = index;
				item.linear = item.linear || "yes";
				return item;
			});

			json.resources.forEach(function (item, index) {
				_this.manifest[index] = item;

				if (item.rel && item.rel[0] === "cover") {
					_this.coverPath = item.href;
				}
			});

			this.spineNodeIndex = 0;

			this.toc = json.toc.map(function (item, index) {
				item.label = item.title;
				return item;
			});

			return {
				"metadata": this.metadata,
				"spine": this.spine,
				"manifest": this.manifest,
				"navPath": this.navPath,
				"ncxPath": this.ncxPath,
				"coverPath": this.coverPath,
				"spineNodeIndex": this.spineNodeIndex,
				"toc": this.toc
			};
		}
	}, {
		key: 'destroy',
		value: function destroy() {
			this.manifest = undefined;
			this.navPath = undefined;
			this.ncxPath = undefined;
			this.coverPath = undefined;
			this.spineNodeIndex = undefined;
			this.spine = undefined;
			this.metadata = undefined;
		}
	}]);

	return Packaging;
}();

exports.default = Packaging;
module.exports = exports['default'];

/***/ }),
/* 379 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _core = __webpack_require__(6);

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Navigation Parser
 * @param {document} xml navigation html / xhtml / ncx
 */
var Navigation = function () {
	function Navigation(xml) {
		_classCallCheck(this, Navigation);

		this.toc = [];
		this.tocByHref = {};
		this.tocById = {};

		this.landmarks = [];
		this.landmarksByType = {};

		this.length = 0;
		if (xml) {
			this.parse(xml);
		}
	}

	/**
  * Parse out the navigation items
  * @param {document} xml navigation html / xhtml / ncx
  */


	_createClass(Navigation, [{
		key: "parse",
		value: function parse(xml) {
			var isXml = xml.nodeType;
			var html = void 0;
			var ncx = void 0;

			if (isXml) {
				html = (0, _core.qs)(xml, "html");
				ncx = (0, _core.qs)(xml, "ncx");
			}

			if (!isXml) {
				this.toc = this.load(xml);
			} else if (html) {
				this.toc = this.parseNav(xml);
				this.landmarks = this.parseLandmarks(xml);
			} else if (ncx) {
				this.toc = this.parseNcx(xml);
			}

			this.length = 0;

			this.unpack(this.toc);
		}

		/**
   * Unpack navigation items
   * @private
   * @param  {array} toc
   */

	}, {
		key: "unpack",
		value: function unpack(toc) {
			var item;

			for (var i = 0; i < toc.length; i++) {
				item = toc[i];

				if (item.href) {
					this.tocByHref[item.href] = i;
				}

				if (item.id) {
					this.tocById[item.id] = i;
				}

				this.length++;

				if (item.subitems.length) {
					this.unpack(item.subitems);
				}
			}
		}

		/**
   * Get an item from the navigation
   * @param  {string} target
   * @return {object} navItem
   */

	}, {
		key: "get",
		value: function get(target) {
			var index;

			if (!target) {
				return this.toc;
			}

			if (target.indexOf("#") === 0) {
				index = this.tocById[target.substring(1)];
			} else if (target in this.tocByHref) {
				index = this.tocByHref[target];
			}

			return this.toc[index];
		}

		/**
   * Get a landmark by type
   * List of types: https://idpf.github.io/epub-vocabs/structure/
   * @param  {string} type
   * @return {object} landmarkItem
   */

	}, {
		key: "landmark",
		value: function landmark(type) {
			var index;

			if (!type) {
				return this.landmarks;
			}

			index = this.landmarksByType[type];

			return this.landmarks[index];
		}

		/**
   * Parse toc from a Epub > 3.0 Nav
   * @private
   * @param  {document} navHtml
   * @return {array} navigation list
   */

	}, {
		key: "parseNav",
		value: function parseNav(navHtml) {
			var navElement = (0, _core.querySelectorByType)(navHtml, "nav", "toc");
			var navItems = navElement ? (0, _core.qsa)(navElement, "li") : [];
			var length = navItems.length;
			var i;
			var toc = {};
			var list = [];
			var item, parent;

			if (!navItems || length === 0) return list;

			for (i = 0; i < length; ++i) {
				item = this.navItem(navItems[i]);
				if (item) {
					toc[item.id] = item;
					if (!item.parent) {
						list.push(item);
					} else {
						parent = toc[item.parent];
						parent.subitems.push(item);
					}
				}
			}

			return list;
		}

		/**
   * Create a navItem
   * @private
   * @param  {element} item
   * @return {object} navItem
   */

	}, {
		key: "navItem",
		value: function navItem(item) {
			var id = item.getAttribute("id") || undefined;
			var content = (0, _core.filterChildren)(item, "a", true);

			if (!content) {
				return;
			}

			var src = content.getAttribute("href") || "";

			if (!id) {
				id = src;
			}
			var text = content.textContent || "";
			var subitems = [];
			var parentItem = (0, _core.getParentByTagName)(item, "li");
			var parent = void 0;

			if (parentItem) {
				parent = parentItem.getAttribute("id");
				if (!parent) {
					var parentContent = (0, _core.filterChildren)(parentItem, "a", true);
					parent = parentContent && parentContent.getAttribute("href");
				}
			}

			while (!parent && parentItem) {
				parentItem = (0, _core.getParentByTagName)(parentItem, "li");
				if (parentItem) {
					parent = parentItem.getAttribute("id");
					if (!parent) {
						var _parentContent = (0, _core.filterChildren)(parentItem, "a", true);
						parent = _parentContent && _parentContent.getAttribute("href");
					}
				}
			}

			return {
				"id": id,
				"href": src,
				"label": text,
				"subitems": subitems,
				"parent": parent
			};
		}

		/**
   * Parse landmarks from a Epub > 3.0 Nav
   * @private
   * @param  {document} navHtml
   * @return {array} landmarks list
   */

	}, {
		key: "parseLandmarks",
		value: function parseLandmarks(navHtml) {
			var navElement = (0, _core.querySelectorByType)(navHtml, "nav", "landmarks");
			var navItems = navElement ? (0, _core.qsa)(navElement, "li") : [];
			var length = navItems.length;
			var i;
			var list = [];
			var item;

			if (!navItems || length === 0) return list;

			for (i = 0; i < length; ++i) {
				item = this.landmarkItem(navItems[i]);
				if (item) {
					list.push(item);
					this.landmarksByType[item.type] = i;
				}
			}

			return list;
		}

		/**
   * Create a landmarkItem
   * @private
   * @param  {element} item
   * @return {object} landmarkItem
   */

	}, {
		key: "landmarkItem",
		value: function landmarkItem(item) {
			var content = (0, _core.filterChildren)(item, "a", true);

			if (!content) {
				return;
			}

			var type = content.getAttributeNS("http://www.idpf.org/2007/ops", "type") || undefined;
			var href = content.getAttribute("href") || "";
			var text = content.textContent || "";

			return {
				"href": href,
				"label": text,
				"type": type
			};
		}

		/**
   * Parse from a Epub > 3.0 NC
   * @private
   * @param  {document} navHtml
   * @return {array} navigation list
   */

	}, {
		key: "parseNcx",
		value: function parseNcx(tocXml) {
			var navPoints = (0, _core.qsa)(tocXml, "navPoint");
			var length = navPoints.length;
			var i;
			var toc = {};
			var list = [];
			var item, parent;

			if (!navPoints || length === 0) return list;

			for (i = 0; i < length; ++i) {
				item = this.ncxItem(navPoints[i]);
				toc[item.id] = item;
				if (!item.parent) {
					list.push(item);
				} else {
					parent = toc[item.parent];
					parent.subitems.push(item);
				}
			}

			return list;
		}

		/**
   * Create a ncxItem
   * @private
   * @param  {element} item
   * @return {object} ncxItem
   */

	}, {
		key: "ncxItem",
		value: function ncxItem(item) {
			var id = item.getAttribute("id") || false,
			    content = (0, _core.qs)(item, "content"),
			    src = content.getAttribute("src"),
			    navLabel = (0, _core.qs)(item, "navLabel"),
			    text = navLabel.textContent ? navLabel.textContent : "",
			    subitems = [],
			    parentNode = item.parentNode,
			    parent;

			if (parentNode && (parentNode.nodeName === "navPoint" || parentNode.nodeName.split(':').slice(-1)[0] === "navPoint")) {
				parent = parentNode.getAttribute("id");
			}

			return {
				"id": id,
				"href": src,
				"label": text,
				"subitems": subitems,
				"parent": parent
			};
		}

		/**
   * Load Spine Items
   * @param  {object} json the items to be loaded
   * @return {Array} navItems
   */

	}, {
		key: "load",
		value: function load(json) {
			var _this = this;

			return json.map(function (item) {
				item.label = item.title;
				item.subitems = item.children ? _this.load(item.children) : [];
				return item;
			});
		}

		/**
   * forEach pass through
   * @param  {Function} fn function to run on each item
   * @return {method} forEach loop
   */

	}, {
		key: "forEach",
		value: function forEach(fn) {
			return this.toc.forEach(fn);
		}
	}]);

	return Navigation;
}();

exports.default = Navigation;
module.exports = exports["default"];

/***/ }),
/* 380 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _replacements = __webpack_require__(72);

var _core = __webpack_require__(6);

var _url = __webpack_require__(70);

var _url2 = _interopRequireDefault(_url);

var _mime = __webpack_require__(103);

var _mime2 = _interopRequireDefault(_mime);

var _path = __webpack_require__(46);

var _path2 = _interopRequireDefault(_path);

var _pathWebpack = __webpack_require__(71);

var _pathWebpack2 = _interopRequireDefault(_pathWebpack);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Handle Package Resources
 * @class
 * @param {Manifest} manifest
 * @param {object} [options]
 * @param {string} [options.replacements="base64"]
 * @param {Archive} [options.archive]
 * @param {method} [options.resolver]
 */
var Resources = function () {
	function Resources(manifest, options) {
		_classCallCheck(this, Resources);

		this.settings = {
			replacements: options && options.replacements || "base64",
			archive: options && options.archive,
			resolver: options && options.resolver,
			request: options && options.request
		};

		this.process(manifest);
	}

	/**
  * Process resources
  * @param {Manifest} manifest
  */


	_createClass(Resources, [{
		key: "process",
		value: function process(manifest) {
			this.manifest = manifest;
			this.resources = Object.keys(manifest).map(function (key) {
				return manifest[key];
			});

			this.replacementUrls = [];

			this.html = [];
			this.assets = [];
			this.css = [];

			this.urls = [];
			this.cssUrls = [];

			this.split();
			this.splitUrls();
		}

		/**
   * Split resources by type
   * @private
   */

	}, {
		key: "split",
		value: function split() {

			// HTML
			this.html = this.resources.filter(function (item) {
				if (item.type === "application/xhtml+xml" || item.type === "text/html") {
					return true;
				}
			});

			// Exclude HTML
			this.assets = this.resources.filter(function (item) {
				if (item.type !== "application/xhtml+xml" && item.type !== "text/html") {
					return true;
				}
			});

			// Only CSS
			this.css = this.resources.filter(function (item) {
				if (item.type === "text/css") {
					return true;
				}
			});
		}

		/**
   * Convert split resources into Urls
   * @private
   */

	}, {
		key: "splitUrls",
		value: function splitUrls() {

			// All Assets Urls
			this.urls = this.assets.map(function (item) {
				return item.href;
			}.bind(this));

			// Css Urls
			this.cssUrls = this.css.map(function (item) {
				return item.href;
			});
		}

		/**
   * Create a url to a resource
   * @param {string} url
   * @return {Promise<string>} Promise resolves with url string
   */

	}, {
		key: "createUrl",
		value: function createUrl(url) {
			var parsedUrl = new _url2.default(url);
			var mimeType = _mime2.default.lookup(parsedUrl.filename);

			if (this.settings.archive) {
				return this.settings.archive.createUrl(url, { "base64": this.settings.replacements === "base64" });
			} else {
				if (this.settings.replacements === "base64") {
					return this.settings.request(url, 'blob').then(function (blob) {
						return (0, _core.blob2base64)(blob);
					}).then(function (blob) {
						return (0, _core.createBase64Url)(blob, mimeType);
					});
				} else {
					return this.settings.request(url, 'blob').then(function (blob) {
						return (0, _core.createBlobUrl)(blob, mimeType);
					});
				}
			}
		}

		/**
   * Create blob urls for all the assets
   * @return {Promise}         returns replacement urls
   */

	}, {
		key: "replacements",
		value: function replacements() {
			var _this = this;

			if (this.settings.replacements === "none") {
				return new Promise(function (resolve) {
					resolve(this.urls);
				}.bind(this));
			}

			var replacements = this.urls.map(function (url) {
				var absolute = _this.settings.resolver(url);

				return _this.createUrl(absolute).catch(function (err) {
					console.error(err);
					return null;
				});
			});

			return Promise.all(replacements).then(function (replacementUrls) {
				_this.replacementUrls = replacementUrls.filter(function (url) {
					return typeof url === "string";
				});
				return replacementUrls;
			});
		}

		/**
   * Replace URLs in CSS resources
   * @private
   * @param  {Archive} [archive]
   * @param  {method} [resolver]
   * @return {Promise}
   */

	}, {
		key: "replaceCss",
		value: function replaceCss(archive, resolver) {
			var replaced = [];
			archive = archive || this.settings.archive;
			resolver = resolver || this.settings.resolver;
			this.cssUrls.forEach(function (href) {
				var replacement = this.createCssFile(href, archive, resolver).then(function (replacementUrl) {
					// switch the url in the replacementUrls
					var indexInUrls = this.urls.indexOf(href);
					if (indexInUrls > -1) {
						this.replacementUrls[indexInUrls] = replacementUrl;
					}
				}.bind(this));

				replaced.push(replacement);
			}.bind(this));
			return Promise.all(replaced);
		}

		/**
   * Create a new CSS file with the replaced URLs
   * @private
   * @param  {string} href the original css file
   * @return {Promise}  returns a BlobUrl to the new CSS file or a data url
   */

	}, {
		key: "createCssFile",
		value: function createCssFile(href) {
			var _this2 = this;

			var newUrl;

			if (_pathWebpack2.default.isAbsolute(href)) {
				return new Promise(function (resolve) {
					resolve();
				});
			}

			var absolute = this.settings.resolver(href);

			// Get the text of the css file from the archive
			var textResponse;

			if (this.settings.archive) {
				textResponse = this.settings.archive.getText(absolute);
			} else {
				textResponse = this.settings.request(absolute, "text");
			}

			// Get asset links relative to css file
			var relUrls = this.urls.map(function (assetHref) {
				var resolved = _this2.settings.resolver(assetHref);
				var relative = new _path2.default(absolute).relative(resolved);

				return relative;
			});

			if (!textResponse) {
				// file not found, don't replace
				return new Promise(function (resolve) {
					resolve();
				});
			}

			return textResponse.then(function (text) {
				// Replacements in the css text
				text = (0, _replacements.substitute)(text, relUrls, _this2.replacementUrls);

				// Get the new url
				if (_this2.settings.replacements === "base64") {
					newUrl = (0, _core.createBase64Url)(text, "text/css");
				} else {
					newUrl = (0, _core.createBlobUrl)(text, "text/css");
				}

				return newUrl;
			}, function (err) {
				// handle response errors
				return new Promise(function (resolve) {
					resolve();
				});
			});
		}

		/**
   * Resolve all resources URLs relative to an absolute URL
   * @param  {string} absolute to be resolved to
   * @param  {resolver} [resolver]
   * @return {string[]} array with relative Urls
   */

	}, {
		key: "relativeTo",
		value: function relativeTo(absolute, resolver) {
			resolver = resolver || this.settings.resolver;

			// Get Urls relative to current sections
			return this.urls.map(function (href) {
				var resolved = resolver(href);
				var relative = new _path2.default(absolute).relative(resolved);
				return relative;
			}.bind(this));
		}

		/**
   * Get a URL for a resource
   * @param  {string} path
   * @return {string} url
   */

	}, {
		key: "get",
		value: function get(path) {
			var indexInUrls = this.urls.indexOf(path);
			if (indexInUrls === -1) {
				return;
			}
			if (this.replacementUrls.length) {
				return new Promise(function (resolve, reject) {
					resolve(this.replacementUrls[indexInUrls]);
				}.bind(this));
			} else {
				return this.createUrl(path);
			}
		}

		/**
   * Substitute urls in content, with replacements,
   * relative to a url if provided
   * @param  {string} content
   * @param  {string} [url]   url to resolve to
   * @return {string}         content with urls substituted
   */

	}, {
		key: "substitute",
		value: function substitute(content, url) {
			var relUrls;
			if (url) {
				relUrls = this.relativeTo(url);
			} else {
				relUrls = this.urls;
			}
			return (0, _replacements.substitute)(content, relUrls, this.replacementUrls);
		}
	}, {
		key: "destroy",
		value: function destroy() {
			this.settings = undefined;
			this.manifest = undefined;
			this.resources = undefined;
			this.replacementUrls = undefined;
			this.html = undefined;
			this.assets = undefined;
			this.css = undefined;

			this.urls = undefined;
			this.cssUrls = undefined;
		}
	}]);

	return Resources;
}();

exports.default = Resources;
module.exports = exports["default"];

/***/ }),
/* 381 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _epubcfi = __webpack_require__(22);

var _epubcfi2 = _interopRequireDefault(_epubcfi);

var _core = __webpack_require__(6);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Page List Parser
 * @param {document} [xml]
 */
var PageList = function () {
	function PageList(xml) {
		_classCallCheck(this, PageList);

		this.pages = [];
		this.locations = [];
		this.epubcfi = new _epubcfi2.default();

		this.firstPage = 0;
		this.lastPage = 0;
		this.totalPages = 0;

		this.toc = undefined;
		this.ncx = undefined;

		if (xml) {
			this.pageList = this.parse(xml);
		}

		if (this.pageList && this.pageList.length) {
			this.process(this.pageList);
		}
	}

	/**
  * Parse PageList Xml
  * @param  {document} xml
  */


	_createClass(PageList, [{
		key: "parse",
		value: function parse(xml) {
			var html = (0, _core.qs)(xml, "html");
			var ncx = (0, _core.qs)(xml, "ncx");

			if (html) {
				return this.parseNav(xml);
			} else if (ncx) {
				return this.parseNcx(xml);
			}
		}

		/**
   * Parse a Nav PageList
   * @private
   * @param  {node} navHtml
   * @return {PageList.item[]} list
   */

	}, {
		key: "parseNav",
		value: function parseNav(navHtml) {
			var navElement = (0, _core.querySelectorByType)(navHtml, "nav", "page-list");
			var navItems = navElement ? (0, _core.qsa)(navElement, "li") : [];
			var length = navItems.length;
			var i;
			var list = [];
			var item;

			if (!navItems || length === 0) return list;

			for (i = 0; i < length; ++i) {
				item = this.item(navItems[i]);
				list.push(item);
			}

			return list;
		}
	}, {
		key: "parseNcx",
		value: function parseNcx(navXml) {
			var list = [];
			var i = 0;
			var item;
			var pageList;
			var pageTargets;
			var length = 0;

			pageList = (0, _core.qs)(navXml, "pageList");
			if (!pageList) return list;

			pageTargets = (0, _core.qsa)(pageList, "pageTarget");
			length = pageTargets.length;

			if (!pageTargets || pageTargets.length === 0) {
				return list;
			}

			for (i = 0; i < length; ++i) {
				item = this.ncxItem(pageTargets[i]);
				list.push(item);
			}

			return list;
		}
	}, {
		key: "ncxItem",
		value: function ncxItem(item) {
			var navLabel = (0, _core.qs)(item, "navLabel");
			var navLabelText = (0, _core.qs)(navLabel, "text");
			var pageText = navLabelText.textContent;
			var content = (0, _core.qs)(item, "content");

			var href = content.getAttribute("src");
			var page = parseInt(pageText, 10);

			return {
				"href": href,
				"page": page
			};
		}

		/**
   * Page List Item
   * @private
   * @param  {node} item
   * @return {object} pageListItem
   */

	}, {
		key: "item",
		value: function item(_item) {
			var content = (0, _core.qs)(_item, "a"),
			    href = content.getAttribute("href") || "",
			    text = content.textContent || "",
			    page = parseInt(text),
			    isCfi = href.indexOf("epubcfi"),
			    split,
			    packageUrl,
			    cfi;

			if (isCfi != -1) {
				split = href.split("#");
				packageUrl = split[0];
				cfi = split.length > 1 ? split[1] : false;
				return {
					"cfi": cfi,
					"href": href,
					"packageUrl": packageUrl,
					"page": page
				};
			} else {
				return {
					"href": href,
					"page": page
				};
			}
		}

		/**
   * Process pageList items
   * @private
   * @param  {array} pageList
   */

	}, {
		key: "process",
		value: function process(pageList) {
			pageList.forEach(function (item) {
				this.pages.push(item.page);
				if (item.cfi) {
					this.locations.push(item.cfi);
				}
			}, this);
			this.firstPage = parseInt(this.pages[0]);
			this.lastPage = parseInt(this.pages[this.pages.length - 1]);
			this.totalPages = this.lastPage - this.firstPage;
		}

		/**
   * Get a PageList result from a EpubCFI
   * @param  {string} cfi EpubCFI String
   * @return {number} page
   */

	}, {
		key: "pageFromCfi",
		value: function pageFromCfi(cfi) {
			var pg = -1;

			// Check if the pageList has not been set yet
			if (this.locations.length === 0) {
				return -1;
			}

			// TODO: check if CFI is valid?

			// check if the cfi is in the location list
			// var index = this.locations.indexOf(cfi);
			var index = (0, _core.indexOfSorted)(cfi, this.locations, this.epubcfi.compare);
			if (index != -1) {
				pg = this.pages[index];
			} else {
				// Otherwise add it to the list of locations
				// Insert it in the correct position in the locations page
				//index = EPUBJS.core.insert(cfi, this.locations, this.epubcfi.compare);
				index = (0, _core.locationOf)(cfi, this.locations, this.epubcfi.compare);
				// Get the page at the location just before the new one, or return the first
				pg = index - 1 >= 0 ? this.pages[index - 1] : this.pages[0];
				if (pg !== undefined) {
					// Add the new page in so that the locations and page array match up
					//this.pages.splice(index, 0, pg);
				} else {
					pg = -1;
				}
			}
			return pg;
		}

		/**
   * Get an EpubCFI from a Page List Item
   * @param  {string | number} pg
   * @return {string} cfi
   */

	}, {
		key: "cfiFromPage",
		value: function cfiFromPage(pg) {
			var cfi = -1;
			// check that pg is an int
			if (typeof pg != "number") {
				pg = parseInt(pg);
			}

			// check if the cfi is in the page list
			// Pages could be unsorted.
			var index = this.pages.indexOf(pg);
			if (index != -1) {
				cfi = this.locations[index];
			}
			// TODO: handle pages not in the list
			return cfi;
		}

		/**
   * Get a Page from Book percentage
   * @param  {number} percent
   * @return {number} page
   */

	}, {
		key: "pageFromPercentage",
		value: function pageFromPercentage(percent) {
			var pg = Math.round(this.totalPages * percent);
			return pg;
		}

		/**
   * Returns a value between 0 - 1 corresponding to the location of a page
   * @param  {number} pg the page
   * @return {number} percentage
   */

	}, {
		key: "percentageFromPage",
		value: function percentageFromPage(pg) {
			var percentage = (pg - this.firstPage) / this.totalPages;
			return Math.round(percentage * 1000) / 1000;
		}

		/**
   * Returns a value between 0 - 1 corresponding to the location of a cfi
   * @param  {string} cfi EpubCFI String
   * @return {number} percentage
   */

	}, {
		key: "percentageFromCfi",
		value: function percentageFromCfi(cfi) {
			var pg = this.pageFromCfi(cfi);
			var percentage = this.percentageFromPage(pg);
			return percentage;
		}

		/**
   * Destroy
   */

	}, {
		key: "destroy",
		value: function destroy() {
			this.pages = undefined;
			this.locations = undefined;
			this.epubcfi = undefined;

			this.pageList = undefined;

			this.toc = undefined;
			this.ncx = undefined;
		}
	}]);

	return PageList;
}();

exports.default = PageList;
module.exports = exports["default"];

/***/ }),
/* 382 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _core = __webpack_require__(6);

var _constants = __webpack_require__(23);

var _eventEmitter = __webpack_require__(30);

var _eventEmitter2 = _interopRequireDefault(_eventEmitter);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Figures out the CSS values to apply for a layout
 * @class
 * @param {object} settings
 * @param {string} [settings.layout='reflowable']
 * @param {string} [settings.spread]
 * @param {number} [settings.minSpreadWidth=800]
 * @param {boolean} [settings.evenSpreads=false]
 */
var Layout = function () {
	function Layout(settings) {
		_classCallCheck(this, Layout);

		this.settings = settings;
		this.name = settings.layout || "reflowable";
		this._spread = settings.spread === "none" ? false : true;
		this._minSpreadWidth = settings.minSpreadWidth || 800;
		this._evenSpreads = settings.evenSpreads || false;

		if (settings.flow === "scrolled" || settings.flow === "scrolled-continuous" || settings.flow === "scrolled-doc") {
			this._flow = "scrolled";
		} else {
			this._flow = "paginated";
		}

		this.width = 0;
		this.height = 0;
		this.spreadWidth = 0;
		this.delta = 0;

		this.columnWidth = 0;
		this.gap = 0;
		this.divisor = 1;

		this.props = {
			name: this.name,
			spread: this._spread,
			flow: this._flow,
			width: 0,
			height: 0,
			spreadWidth: 0,
			delta: 0,
			columnWidth: 0,
			gap: 0,
			divisor: 1
		};
	}

	/**
  * Switch the flow between paginated and scrolled
  * @param  {string} flow paginated | scrolled
  * @return {string} simplified flow
  */


	_createClass(Layout, [{
		key: "flow",
		value: function flow(_flow) {
			if (typeof _flow != "undefined") {
				if (_flow === "scrolled" || _flow === "scrolled-continuous" || _flow === "scrolled-doc") {
					this._flow = "scrolled";
				} else {
					this._flow = "paginated";
				}
				// this.props.flow = this._flow;
				this.update({ flow: this._flow });
			}
			return this._flow;
		}

		/**
   * Switch between using spreads or not, and set the
   * width at which they switch to single.
   * @param  {string} spread "none" | "always" | "auto"
   * @param  {number} min integer in pixels
   * @return {boolean} spread true | false
   */

	}, {
		key: "spread",
		value: function spread(_spread, min) {

			if (_spread) {
				this._spread = _spread === "none" ? false : true;
				// this.props.spread = this._spread;
				this.update({ spread: this._spread });
			}

			if (min >= 0) {
				this._minSpreadWidth = min;
			}

			return this._spread;
		}

		/**
   * Calculate the dimensions of the pagination
   * @param  {number} _width  width of the rendering
   * @param  {number} _height height of the rendering
   * @param  {number} _gap    width of the gap between columns
   */

	}, {
		key: "calculate",
		value: function calculate(_width, _height, _gap) {

			var divisor = 1;
			var gap = _gap || 0;

			//-- Check the width and create even width columns
			// var fullWidth = Math.floor(_width);
			var width = _width;
			var height = _height;

			var section = Math.floor(width / 12);

			var columnWidth;
			var spreadWidth;
			var pageWidth;
			var delta;

			if (this._spread && width >= this._minSpreadWidth) {
				divisor = 2;
			} else {
				divisor = 1;
			}

			if (this.name === "reflowable" && this._flow === "paginated" && !(_gap >= 0)) {
				gap = section % 2 === 0 ? section : section - 1;
			}

			if (this.name === "pre-paginated") {
				gap = 0;
			}

			//-- Double Page
			if (divisor > 1) {
				// width = width - gap;
				// columnWidth = (width - gap) / divisor;
				// gap = gap / divisor;
				columnWidth = width / divisor - gap;
				pageWidth = columnWidth + gap;
			} else {
				columnWidth = width;
				pageWidth = width;
			}

			if (this.name === "pre-paginated" && divisor > 1) {
				width = columnWidth;
			}

			spreadWidth = columnWidth * divisor + gap;

			delta = width;

			this.width = width;
			this.height = height;
			this.spreadWidth = spreadWidth;
			this.pageWidth = pageWidth;
			this.delta = delta;

			this.columnWidth = columnWidth;
			this.gap = gap;
			this.divisor = divisor;

			// this.props.width = width;
			// this.props.height = _height;
			// this.props.spreadWidth = spreadWidth;
			// this.props.pageWidth = pageWidth;
			// this.props.delta = delta;
			//
			// this.props.columnWidth = colWidth;
			// this.props.gap = gap;
			// this.props.divisor = divisor;

			this.update({
				width: width,
				height: height,
				spreadWidth: spreadWidth,
				pageWidth: pageWidth,
				delta: delta,
				columnWidth: columnWidth,
				gap: gap,
				divisor: divisor
			});
		}

		/**
   * Apply Css to a Document
   * @param  {Contents} contents
   * @return {Promise}
   */

	}, {
		key: "format",
		value: function format(contents) {
			var formating;

			if (this.name === "pre-paginated") {
				formating = contents.fit(this.columnWidth, this.height);
			} else if (this._flow === "paginated") {
				formating = contents.columns(this.width, this.height, this.columnWidth, this.gap);
			} else {
				// scrolled
				formating = contents.size(this.width, null);
			}

			return formating; // might be a promise in some View Managers
		}

		/**
   * Count number of pages
   * @param  {number} totalLength
   * @param  {number} pageLength
   * @return {{spreads: Number, pages: Number}}
   */

	}, {
		key: "count",
		value: function count(totalLength, pageLength) {

			var spreads = void 0,
			    pages = void 0;

			if (this.name === "pre-paginated") {
				spreads = 1;
				pages = 1;
			} else if (this._flow === "paginated") {
				pageLength = pageLength || this.delta;
				spreads = Math.ceil(totalLength / pageLength);
				pages = spreads * this.divisor;
			} else {
				// scrolled
				pageLength = pageLength || this.height;
				spreads = Math.ceil(totalLength / pageLength);
				pages = spreads;
			}

			return {
				spreads: spreads,
				pages: pages
			};
		}

		/**
   * Update props that have changed
   * @private
   * @param  {object} props
   */

	}, {
		key: "update",
		value: function update(props) {
			var _this = this;

			// Remove props that haven't changed
			Object.keys(props).forEach(function (propName) {
				if (_this.props[propName] === props[propName]) {
					delete props[propName];
				}
			});

			if (Object.keys(props).length > 0) {
				var newProps = (0, _core.extend)(this.props, props);
				this.emit(_constants.EVENTS.LAYOUT.UPDATED, newProps, props);
			}
		}
	}]);

	return Layout;
}();

(0, _eventEmitter2.default)(Layout.prototype);

exports.default = Layout;
module.exports = exports["default"];

/***/ }),
/* 383 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _url = __webpack_require__(70);

var _url2 = _interopRequireDefault(_url);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Themes to apply to displayed content
 * @class
 * @param {Rendition} rendition
 */
var Themes = function () {
	function Themes(rendition) {
		_classCallCheck(this, Themes);

		this.rendition = rendition;
		this._themes = {
			"default": {
				"rules": {},
				"url": "",
				"serialized": ""
			}
		};
		this._overrides = {};
		this._current = "default";
		this._injected = [];
		this.rendition.hooks.content.register(this.inject.bind(this));
		this.rendition.hooks.content.register(this.overrides.bind(this));
	}

	/**
  * Add themes to be used by a rendition
  * @param {object | Array<object> | string}
  * @example themes.register("light", "http://example.com/light.css")
  * @example themes.register("light", { "body": { "color": "purple"}})
  * @example themes.register({ "light" : {...}, "dark" : {...}})
  */


	_createClass(Themes, [{
		key: "register",
		value: function register() {
			if (arguments.length === 0) {
				return;
			}
			if (arguments.length === 1 && _typeof(arguments[0]) === "object") {
				return this.registerThemes(arguments[0]);
			}
			if (arguments.length === 1 && typeof arguments[0] === "string") {
				return this.default(arguments[0]);
			}
			if (arguments.length === 2 && typeof arguments[1] === "string") {
				return this.registerUrl(arguments[0], arguments[1]);
			}
			if (arguments.length === 2 && _typeof(arguments[1]) === "object") {
				return this.registerRules(arguments[0], arguments[1]);
			}
		}

		/**
   * Add a default theme to be used by a rendition
   * @param {object | string} theme
   * @example themes.register("http://example.com/default.css")
   * @example themes.register({ "body": { "color": "purple"}})
   */

	}, {
		key: "default",
		value: function _default(theme) {
			if (!theme) {
				return;
			}
			if (typeof theme === "string") {
				return this.registerUrl("default", theme);
			}
			if ((typeof theme === "undefined" ? "undefined" : _typeof(theme)) === "object") {
				return this.registerRules("default", theme);
			}
		}

		/**
   * Register themes object
   * @param {object} themes
   */

	}, {
		key: "registerThemes",
		value: function registerThemes(themes) {
			for (var theme in themes) {
				if (themes.hasOwnProperty(theme)) {
					if (typeof themes[theme] === "string") {
						this.registerUrl(theme, themes[theme]);
					} else {
						this.registerRules(theme, themes[theme]);
					}
				}
			}
		}

		/**
   * Register a url
   * @param {string} name
   * @param {string} input
   */

	}, {
		key: "registerUrl",
		value: function registerUrl(name, input) {
			var url = new _url2.default(input);
			this._themes[name] = { "url": url.toString() };
			if (this._injected[name]) {
				this.update(name);
			}
		}

		/**
   * Register rule
   * @param {string} name
   * @param {object} rules
   */

	}, {
		key: "registerRules",
		value: function registerRules(name, rules) {
			this._themes[name] = { "rules": rules };
			// TODO: serialize css rules
			if (this._injected[name]) {
				this.update(name);
			}
		}

		/**
   * Select a theme
   * @param {string} name
   */

	}, {
		key: "select",
		value: function select(name) {
			var prev = this._current;
			var contents;

			this._current = name;
			this.update(name);

			contents = this.rendition.getContents();
			contents.forEach(function (content) {
				content.removeClass(prev);
				content.addClass(name);
			});
		}

		/**
   * Update a theme
   * @param {string} name
   */

	}, {
		key: "update",
		value: function update(name) {
			var _this = this;

			var contents = this.rendition.getContents();
			contents.forEach(function (content) {
				_this.add(name, content);
			});
		}

		/**
   * Inject all themes into contents
   * @param {Contents} contents
   */

	}, {
		key: "inject",
		value: function inject(contents) {
			var links = [];
			var themes = this._themes;
			var theme;

			for (var name in themes) {
				if (themes.hasOwnProperty(name) && (name === this._current || name === "default")) {
					theme = themes[name];
					if (theme.rules && Object.keys(theme.rules).length > 0 || theme.url && links.indexOf(theme.url) === -1) {
						this.add(name, contents);
					}
					this._injected.push(name);
				}
			}

			if (this._current != "default") {
				contents.addClass(this._current);
			}
		}

		/**
   * Add Theme to contents
   * @param {string} name
   * @param {Contents} contents
   */

	}, {
		key: "add",
		value: function add(name, contents) {
			var theme = this._themes[name];

			if (!theme || !contents) {
				return;
			}

			if (theme.url) {
				contents.addStylesheet(theme.url);
			} else if (theme.serialized) {
				// TODO: handle serialized
			} else if (theme.rules) {
				contents.addStylesheetRules(theme.rules);
				theme.injected = true;
			}
		}

		/**
   * Add override
   * @param {string} name
   * @param {string} value
   * @param {boolean} priority
   */

	}, {
		key: "override",
		value: function override(name, value, priority) {
			var _this2 = this;

			var contents = this.rendition.getContents();

			this._overrides[name] = {
				value: value,
				priority: priority === true
			};

			contents.forEach(function (content) {
				content.css(name, _this2._overrides[name].value, _this2._overrides[name].priority);
			});
		}

		/**
   * Add all overrides
   * @param {Content} content
   */

	}, {
		key: "overrides",
		value: function overrides(contents) {
			var overrides = this._overrides;

			for (var rule in overrides) {
				if (overrides.hasOwnProperty(rule)) {
					contents.css(rule, overrides[rule].value, overrides[rule].priority);
				}
			}
		}

		/**
   * Adjust the font size of a rendition
   * @param {number} size
   */

	}, {
		key: "fontSize",
		value: function fontSize(size) {
			this.override("font-size", size);
		}

		/**
   * Adjust the font-family of a rendition
   * @param {string} f
   */

	}, {
		key: "font",
		value: function font(f) {
			this.override("font-family", f, true);
		}
	}, {
		key: "destroy",
		value: function destroy() {
			this.rendition = undefined;
			this._themes = undefined;
			this._overrides = undefined;
			this._current = undefined;
			this._injected = undefined;
		}
	}]);

	return Themes;
}();

exports.default = Themes;
module.exports = exports["default"];

/***/ }),
/* 384 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _eventEmitter = __webpack_require__(30);

var _eventEmitter2 = _interopRequireDefault(_eventEmitter);

var _epubcfi = __webpack_require__(22);

var _epubcfi2 = _interopRequireDefault(_epubcfi);

var _constants = __webpack_require__(23);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
	* Handles managing adding & removing Annotations
	* @param {Rendition} rendition
	* @class
	*/
var Annotations = function () {
	function Annotations(rendition) {
		_classCallCheck(this, Annotations);

		this.rendition = rendition;
		this.highlights = [];
		this.underlines = [];
		this.marks = [];
		this._annotations = {};
		this._annotationsBySectionIndex = {};

		this.rendition.hooks.render.register(this.inject.bind(this));
		this.rendition.hooks.unloaded.register(this.clear.bind(this));
	}

	/**
  * Add an annotation to store
  * @param {string} type Type of annotation to add: "highlight", "underline", "mark"
  * @param {EpubCFI} cfiRange EpubCFI range to attach annotation to
  * @param {object} data Data to assign to annotation
  * @param {function} [cb] Callback after annotation is added
  * @param {string} className CSS class to assign to annotation
  * @param {object} styles CSS styles to assign to annotation
  * @returns {Annotation} annotation
  */


	_createClass(Annotations, [{
		key: "add",
		value: function add(type, cfiRange, data, cb, className, styles) {
			var hash = encodeURI(cfiRange + type);
			var cfi = new _epubcfi2.default(cfiRange);
			var sectionIndex = cfi.spinePos;
			var annotation = new Annotation({
				type: type,
				cfiRange: cfiRange,
				data: data,
				sectionIndex: sectionIndex,
				cb: cb,
				className: className,
				styles: styles
			});

			this._annotations[hash] = annotation;

			if (sectionIndex in this._annotationsBySectionIndex) {
				this._annotationsBySectionIndex[sectionIndex].push(hash);
			} else {
				this._annotationsBySectionIndex[sectionIndex] = [hash];
			}

			var views = this.rendition.views();

			views.forEach(function (view) {
				if (annotation.sectionIndex === view.index) {
					annotation.attach(view);
				}
			});

			return annotation;
		}

		/**
   * Remove an annotation from store
   * @param {EpubCFI} cfiRange EpubCFI range the annotation is attached to
   * @param {string} type Type of annotation to add: "highlight", "underline", "mark"
   */

	}, {
		key: "remove",
		value: function remove(cfiRange, type) {
			var _this = this;

			var hash = encodeURI(cfiRange + type);

			if (hash in this._annotations) {
				var annotation = this._annotations[hash];

				if (type && annotation.type !== type) {
					return;
				}

				var views = this.rendition.views();
				views.forEach(function (view) {
					_this._removeFromAnnotationBySectionIndex(annotation.sectionIndex, hash);
					if (annotation.sectionIndex === view.index) {
						annotation.detach(view);
					}
				});

				delete this._annotations[hash];
			}
		}

		/**
   * Remove an annotations by Section Index
   * @private
   */

	}, {
		key: "_removeFromAnnotationBySectionIndex",
		value: function _removeFromAnnotationBySectionIndex(sectionIndex, hash) {
			this._annotationsBySectionIndex[sectionIndex] = this._annotationsAt(sectionIndex).filter(function (h) {
				return h !== hash;
			});
		}

		/**
   * Get annotations by Section Index
   * @private
   */

	}, {
		key: "_annotationsAt",
		value: function _annotationsAt(index) {
			return this._annotationsBySectionIndex[index];
		}

		/**
   * Add a highlight to the store
   * @param {EpubCFI} cfiRange EpubCFI range to attach annotation to
   * @param {object} data Data to assign to annotation
   * @param {function} cb Callback after annotation is clicked
   * @param {string} className CSS class to assign to annotation
   * @param {object} styles CSS styles to assign to annotation
   */

	}, {
		key: "highlight",
		value: function highlight(cfiRange, data, cb, className, styles) {
			return this.add("highlight", cfiRange, data, cb, className, styles);
		}

		/**
   * Add a underline to the store
   * @param {EpubCFI} cfiRange EpubCFI range to attach annotation to
   * @param {object} data Data to assign to annotation
   * @param {function} cb Callback after annotation is clicked
   * @param {string} className CSS class to assign to annotation
   * @param {object} styles CSS styles to assign to annotation
   */

	}, {
		key: "underline",
		value: function underline(cfiRange, data, cb, className, styles) {
			return this.add("underline", cfiRange, data, cb, className, styles);
		}

		/**
   * Add a mark to the store
   * @param {EpubCFI} cfiRange EpubCFI range to attach annotation to
   * @param {object} data Data to assign to annotation
   * @param {function} cb Callback after annotation is clicked
   */

	}, {
		key: "mark",
		value: function mark(cfiRange, data, cb) {
			return this.add("mark", cfiRange, data, cb);
		}

		/**
   * iterate over annotations in the store
   */

	}, {
		key: "each",
		value: function each() {
			return this._annotations.forEach.apply(this._annotations, arguments);
		}

		/**
   * Hook for injecting annotation into a view
   * @param {View} view
   * @private
   */

	}, {
		key: "inject",
		value: function inject(view) {
			var _this2 = this;

			var sectionIndex = view.index;
			if (sectionIndex in this._annotationsBySectionIndex) {
				var annotations = this._annotationsBySectionIndex[sectionIndex];
				annotations.forEach(function (hash) {
					var annotation = _this2._annotations[hash];
					annotation.attach(view);
				});
			}
		}

		/**
   * Hook for removing annotation from a view
   * @param {View} view
   * @private
   */

	}, {
		key: "clear",
		value: function clear(view) {
			var _this3 = this;

			var sectionIndex = view.index;
			if (sectionIndex in this._annotationsBySectionIndex) {
				var annotations = this._annotationsBySectionIndex[sectionIndex];
				annotations.forEach(function (hash) {
					var annotation = _this3._annotations[hash];
					annotation.detach(view);
				});
			}
		}

		/**
   * [Not Implemented] Show annotations
   * @TODO: needs implementation in View
   */

	}, {
		key: "show",
		value: function show() {}

		/**
   * [Not Implemented] Hide annotations
   * @TODO: needs implementation in View
   */

	}, {
		key: "hide",
		value: function hide() {}
	}]);

	return Annotations;
}();

/**
 * Annotation object
 * @class
 * @param {object} options
 * @param {string} options.type Type of annotation to add: "highlight", "underline", "mark"
 * @param {EpubCFI} options.cfiRange EpubCFI range to attach annotation to
 * @param {object} options.data Data to assign to annotation
 * @param {int} options.sectionIndex Index in the Spine of the Section annotation belongs to
 * @param {function} [options.cb] Callback after annotation is clicked
 * @param {string} className CSS class to assign to annotation
 * @param {object} styles CSS styles to assign to annotation
 * @returns {Annotation} annotation
 */


var Annotation = function () {
	function Annotation(_ref) {
		var type = _ref.type,
		    cfiRange = _ref.cfiRange,
		    data = _ref.data,
		    sectionIndex = _ref.sectionIndex,
		    cb = _ref.cb,
		    className = _ref.className,
		    styles = _ref.styles;

		_classCallCheck(this, Annotation);

		this.type = type;
		this.cfiRange = cfiRange;
		this.data = data;
		this.sectionIndex = sectionIndex;
		this.mark = undefined;
		this.cb = cb;
		this.className = className;
		this.styles = styles;
	}

	/**
  * Update stored data
  * @param {object} data
  */


	_createClass(Annotation, [{
		key: "update",
		value: function update(data) {
			this.data = data;
		}

		/**
   * Add to a view
   * @param {View} view
   */

	}, {
		key: "attach",
		value: function attach(view) {
			var cfiRange = this.cfiRange,
			    data = this.data,
			    type = this.type,
			    mark = this.mark,
			    cb = this.cb,
			    className = this.className,
			    styles = this.styles;

			var result = void 0;

			if (type === "highlight") {
				result = view.highlight(cfiRange, data, cb, className, styles);
			} else if (type === "underline") {
				result = view.underline(cfiRange, data, cb, className, styles);
			} else if (type === "mark") {
				result = view.mark(cfiRange, data, cb);
			}

			this.mark = result;
			this.emit(_constants.EVENTS.ANNOTATION.ATTACH, result);
			return result;
		}

		/**
   * Remove from a view
   * @param {View} view
   */

	}, {
		key: "detach",
		value: function detach(view) {
			var cfiRange = this.cfiRange,
			    type = this.type;

			var result = void 0;

			if (view) {
				if (type === "highlight") {
					result = view.unhighlight(cfiRange);
				} else if (type === "underline") {
					result = view.ununderline(cfiRange);
				} else if (type === "mark") {
					result = view.unmark(cfiRange);
				}
			}

			this.mark = undefined;
			this.emit(_constants.EVENTS.ANNOTATION.DETACH, result);
			return result;
		}

		/**
   * [Not Implemented] Get text of an annotation
   * @TODO: needs implementation in contents
   */

	}, {
		key: "text",
		value: function text() {}
	}]);

	return Annotation;
}();

(0, _eventEmitter2.default)(Annotation.prototype);

exports.default = Annotations;
module.exports = exports["default"];

/***/ }),
/* 385 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.Underline = exports.Highlight = exports.Mark = exports.Pane = undefined;

var _get = function get(object, property, receiver) {
    if (object === null) object = Function.prototype;var desc = Object.getOwnPropertyDescriptor(object, property);if (desc === undefined) {
        var parent = Object.getPrototypeOf(object);if (parent === null) {
            return undefined;
        } else {
            return get(parent, property, receiver);
        }
    } else if ("value" in desc) {
        return desc.value;
    } else {
        var getter = desc.get;if (getter === undefined) {
            return undefined;
        }return getter.call(receiver);
    }
};

var _createClass = function () {
    function defineProperties(target, props) {
        for (var i = 0; i < props.length; i++) {
            var descriptor = props[i];descriptor.enumerable = descriptor.enumerable || false;descriptor.configurable = true;if ("value" in descriptor) descriptor.writable = true;Object.defineProperty(target, descriptor.key, descriptor);
        }
    }return function (Constructor, protoProps, staticProps) {
        if (protoProps) defineProperties(Constructor.prototype, protoProps);if (staticProps) defineProperties(Constructor, staticProps);return Constructor;
    };
}();

var _svg = __webpack_require__(386);

var _svg2 = _interopRequireDefault(_svg);

var _events = __webpack_require__(387);

var _events2 = _interopRequireDefault(_events);

function _interopRequireDefault(obj) {
    return obj && obj.__esModule ? obj : { default: obj };
}

function _possibleConstructorReturn(self, call) {
    if (!self) {
        throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
    }return call && ((typeof call === "undefined" ? "undefined" : _typeof(call)) === "object" || typeof call === "function") ? call : self;
}

function _inherits(subClass, superClass) {
    if (typeof superClass !== "function" && superClass !== null) {
        throw new TypeError("Super expression must either be null or a function, not " + (typeof superClass === "undefined" ? "undefined" : _typeof(superClass)));
    }subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } });if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
}

function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) {
        throw new TypeError("Cannot call a class as a function");
    }
}

var Pane = exports.Pane = function () {
    function Pane(target) {
        var container = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : document.body;

        _classCallCheck(this, Pane);

        this.target = target;
        this.element = _svg2.default.createElement('svg');
        this.marks = [];

        // Match the coordinates of the target element
        this.element.style.position = 'absolute';
        // Disable pointer events
        this.element.setAttribute('pointer-events', 'none');

        // Set up mouse event proxying between the target element and the marks
        _events2.default.proxyMouse(this.target, this.marks);

        this.container = container;
        this.container.appendChild(this.element);

        this.render();
    }

    _createClass(Pane, [{
        key: 'addMark',
        value: function addMark(mark) {
            var g = _svg2.default.createElement('g');
            this.element.appendChild(g);
            mark.bind(g, this.container);

            this.marks.push(mark);

            mark.render();
            return mark;
        }
    }, {
        key: 'removeMark',
        value: function removeMark(mark) {
            var idx = this.marks.indexOf(mark);
            if (idx === -1) {
                return;
            }
            var el = mark.unbind();
            this.element.removeChild(el);
            this.marks.splice(idx, 1);
        }
    }, {
        key: 'render',
        value: function render() {
            setCoords(this.element, coords(this.target, this.container));
            var _iteratorNormalCompletion = true;
            var _didIteratorError = false;
            var _iteratorError = undefined;

            try {
                for (var _iterator = this.marks[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                    var m = _step.value;

                    m.render();
                }
            } catch (err) {
                _didIteratorError = true;
                _iteratorError = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion && _iterator.return) {
                        _iterator.return();
                    }
                } finally {
                    if (_didIteratorError) {
                        throw _iteratorError;
                    }
                }
            }
        }
    }]);

    return Pane;
}();

var Mark = exports.Mark = function () {
    function Mark() {
        _classCallCheck(this, Mark);

        this.element = null;
    }

    _createClass(Mark, [{
        key: 'bind',
        value: function bind(element, container) {
            this.element = element;
            this.container = container;
        }
    }, {
        key: 'unbind',
        value: function unbind() {
            var el = this.element;
            this.element = null;
            return el;
        }
    }, {
        key: 'render',
        value: function render() {}
    }, {
        key: 'dispatchEvent',
        value: function dispatchEvent(e) {
            if (!this.element) return;
            this.element.dispatchEvent(e);
        }
    }, {
        key: 'getBoundingClientRect',
        value: function getBoundingClientRect() {
            return this.element.getBoundingClientRect();
        }
    }, {
        key: 'getClientRects',
        value: function getClientRects() {
            var rects = [];
            var el = this.element.firstChild;
            while (el) {
                rects.push(el.getBoundingClientRect());
                el = el.nextSibling;
            }
            return rects;
        }
    }, {
        key: 'filteredRanges',
        value: function filteredRanges() {
            var rects = Array.from(this.range.getClientRects());

            // De-duplicate the boxes
            return rects.filter(function (box) {
                for (var i = 0; i < rects.length; i++) {
                    if (rects[i] === box) {
                        return true;
                    }
                    var contained = contains(rects[i], box);
                    if (contained) {
                        return false;
                    }
                }
                return true;
            });
        }
    }]);

    return Mark;
}();

var Highlight = exports.Highlight = function (_Mark) {
    _inherits(Highlight, _Mark);

    function Highlight(range, className, data, attributes) {
        _classCallCheck(this, Highlight);

        var _this = _possibleConstructorReturn(this, (Highlight.__proto__ || Object.getPrototypeOf(Highlight)).call(this));

        _this.range = range;
        _this.className = className;
        _this.data = data || {};
        _this.attributes = attributes || {};
        return _this;
    }

    _createClass(Highlight, [{
        key: 'bind',
        value: function bind(element, container) {
            _get(Highlight.prototype.__proto__ || Object.getPrototypeOf(Highlight.prototype), 'bind', this).call(this, element, container);

            for (var attr in this.data) {
                if (this.data.hasOwnProperty(attr)) {
                    this.element.dataset[attr] = this.data[attr];
                }
            }

            for (var attr in this.attributes) {
                if (this.attributes.hasOwnProperty(attr)) {
                    this.element.setAttribute(attr, this.attributes[attr]);
                }
            }

            if (this.className) {
                this.element.classList.add(this.className);
            }
        }
    }, {
        key: 'render',
        value: function render() {
            // Empty element
            while (this.element.firstChild) {
                this.element.removeChild(this.element.firstChild);
            }

            var docFrag = this.element.ownerDocument.createDocumentFragment();
            var filtered = this.filteredRanges();
            var offset = this.element.getBoundingClientRect();
            var container = this.container.getBoundingClientRect();

            for (var i = 0, len = filtered.length; i < len; i++) {
                var r = filtered[i];
                var el = _svg2.default.createElement('rect');
                el.setAttribute('x', r.left - offset.left + container.left);
                el.setAttribute('y', r.top - offset.top + container.top);
                el.setAttribute('height', r.height);
                el.setAttribute('width', r.width);
                docFrag.appendChild(el);
            }

            this.element.appendChild(docFrag);
        }
    }]);

    return Highlight;
}(Mark);

var Underline = exports.Underline = function (_Highlight) {
    _inherits(Underline, _Highlight);

    function Underline(range, className, data, attributes) {
        _classCallCheck(this, Underline);

        return _possibleConstructorReturn(this, (Underline.__proto__ || Object.getPrototypeOf(Underline)).call(this, range, className, data, attributes));
    }

    _createClass(Underline, [{
        key: 'render',
        value: function render() {
            // Empty element
            while (this.element.firstChild) {
                this.element.removeChild(this.element.firstChild);
            }

            var docFrag = this.element.ownerDocument.createDocumentFragment();
            var filtered = this.filteredRanges();
            var offset = this.element.getBoundingClientRect();
            var container = this.container.getBoundingClientRect();

            for (var i = 0, len = filtered.length; i < len; i++) {
                var r = filtered[i];

                var rect = _svg2.default.createElement('rect');
                rect.setAttribute('x', r.left - offset.left + container.left);
                rect.setAttribute('y', r.top - offset.top + container.top);
                rect.setAttribute('height', r.height);
                rect.setAttribute('width', r.width);
                rect.setAttribute('fill', 'none');

                var line = _svg2.default.createElement('line');
                line.setAttribute('x1', r.left - offset.left + container.left);
                line.setAttribute('x2', r.left - offset.left + container.left + r.width);
                line.setAttribute('y1', r.top - offset.top + container.top + r.height - 1);
                line.setAttribute('y2', r.top - offset.top + container.top + r.height - 1);

                line.setAttribute('stroke-width', 1);
                line.setAttribute('stroke', 'black'); //TODO: match text color?
                line.setAttribute('stroke-linecap', 'square');

                docFrag.appendChild(rect);

                docFrag.appendChild(line);
            }

            this.element.appendChild(docFrag);
        }
    }]);

    return Underline;
}(Highlight);

function coords(el, container) {
    var offset = container.getBoundingClientRect();
    var rect = el.getBoundingClientRect();

    return {
        top: rect.top - offset.top,
        left: rect.left - offset.left,
        height: el.scrollHeight,
        width: el.scrollWidth
    };
}

function setCoords(el, coords) {
    el.style.setProperty('top', coords.top + 'px', 'important');
    el.style.setProperty('left', coords.left + 'px', 'important');
    el.style.setProperty('height', coords.height + 'px', 'important');
    el.style.setProperty('width', coords.width + 'px', 'important');
}

function contains(rect1, rect2) {
    return rect2.right <= rect1.right && rect2.left >= rect1.left && rect2.top >= rect1.top && rect2.bottom <= rect1.bottom;
}

/***/ }),
/* 386 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.createElement = createElement;
function createElement(name) {
    return document.createElementNS('http://www.w3.org/2000/svg', name);
}

exports.default = {
    createElement: createElement
};

/***/ }),
/* 387 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.proxyMouse = proxyMouse;
exports.clone = clone;
// import 'babelify/polyfill'; // needed for Object.assign

exports.default = {
    proxyMouse: proxyMouse
};

/**
 * Start proxying all mouse events that occur on the target node to each node in
 * a set of tracked nodes.
 *
 * The items in tracked do not strictly have to be DOM Nodes, but they do have
 * to have dispatchEvent, getBoundingClientRect, and getClientRects methods.
 *
 * @param target {Node} The node on which to listen for mouse events.
 * @param tracked {Node[]} A (possibly mutable) array of nodes to which to proxy
 *                         events.
 */

function proxyMouse(target, tracked) {
    function dispatch(e) {
        // We walk through the set of tracked elements in reverse order so that
        // events are sent to those most recently added first.
        //
        // This is the least surprising behaviour as it simulates the way the
        // browser would work if items added later were drawn "on top of"
        // earlier ones.
        for (var i = tracked.length - 1; i >= 0; i--) {
            var t = tracked[i];
            var x = e.clientX;
            var y = e.clientY;

            if (e.touches && e.touches.length) {
                x = e.touches[0].clientX;
                y = e.touches[0].clientY;
            }

            if (!contains(t, target, x, y)) {
                continue;
            }

            // The event targets this mark, so dispatch a cloned event:
            t.dispatchEvent(clone(e));
            // We only dispatch the cloned event to the first matching mark.
            break;
        }
    }

    if (target.nodeName === "iframe" || target.nodeName === "IFRAME") {

        try {
            // Try to get the contents if same domain
            this.target = target.contentDocument;
        } catch (err) {
            this.target = target;
        }
    } else {
        this.target = target;
    }

    var _arr = ['mouseup', 'mousedown', 'click', 'touchstart'];
    for (var _i = 0; _i < _arr.length; _i++) {
        var ev = _arr[_i];
        this.target.addEventListener(ev, function (e) {
            return dispatch(e);
        }, false);
    }
}

/**
 * Clone a mouse event object.
 *
 * @param e {MouseEvent} A mouse event object to clone.
 * @returns {MouseEvent}
 */
function clone(e) {
    var opts = Object.assign({}, e, { bubbles: false });
    try {
        return new MouseEvent(e.type, opts);
    } catch (err) {
        // compat: webkit
        var copy = document.createEvent('MouseEvents');
        copy.initMouseEvent(e.type, false, opts.cancelable, opts.view, opts.detail, opts.screenX, opts.screenY, opts.clientX, opts.clientY, opts.ctrlKey, opts.altKey, opts.shiftKey, opts.metaKey, opts.button, opts.relatedTarget);
        return copy;
    }
}

/**
 * Check if the item contains the point denoted by the passed coordinates
 * @param item {Object} An object with getBoundingClientRect and getClientRects
 *                      methods.
 * @param x {Number}
 * @param y {Number}
 * @returns {Boolean}
 */
function contains(item, target, x, y) {
    // offset
    var offset = target.getBoundingClientRect();

    function rectContains(r, x, y) {
        var top = r.top - offset.top;
        var left = r.left - offset.left;
        var bottom = top + r.height;
        var right = left + r.width;
        return top <= y && left <= x && bottom > y && right > x;
    }

    // Check overall bounding box first
    var rect = item.getBoundingClientRect();
    if (!rectContains(rect, x, y)) {
        return false;
    }

    // Then continue to check each child rect
    var rects = item.getClientRects();
    for (var i = 0, len = rects.length; i < len; i++) {
        if (rectContains(rects[i], x, y)) {
            return true;
        }
    }
    return false;
}

/***/ }),
/* 388 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _core = __webpack_require__(6);

var _throttle = __webpack_require__(389);

var _throttle2 = _interopRequireDefault(_throttle);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Stage = function () {
	function Stage(_options) {
		_classCallCheck(this, Stage);

		this.settings = _options || {};
		this.id = "epubjs-container-" + (0, _core.uuid)();

		this.container = this.create(this.settings);

		if (this.settings.hidden) {
			this.wrapper = this.wrap(this.container);
		}
	}

	/*
 * Creates an element to render to.
 * Resizes to passed width and height or to the elements size
 */


	_createClass(Stage, [{
		key: "create",
		value: function create(options) {
			var height = options.height; // !== false ? options.height : "100%";
			var width = options.width; // !== false ? options.width : "100%";
			var overflow = options.overflow || false;
			var axis = options.axis || "vertical";
			var direction = options.direction;

			(0, _core.extend)(this.settings, options);

			if (options.height && (0, _core.isNumber)(options.height)) {
				height = options.height + "px";
			}

			if (options.width && (0, _core.isNumber)(options.width)) {
				width = options.width + "px";
			}

			// Create new container element
			var container = document.createElement("div");

			container.id = this.id;
			container.classList.add("epub-container");

			// Style Element
			// container.style.fontSize = "0";
			container.style.wordSpacing = "0";
			container.style.lineHeight = "0";
			container.style.verticalAlign = "top";
			container.style.position = "relative";

			if (axis === "horizontal") {
				// container.style.whiteSpace = "nowrap";
				container.style.display = "flex";
				container.style.flexDirection = "row";
				container.style.flexWrap = "nowrap";
			}

			if (width) {
				container.style.width = width;
			}

			if (height) {
				container.style.height = height;
			}

			if (overflow) {
				if (overflow === "scroll" && axis === "vertical") {
					container.style["overflow-y"] = overflow;
					container.style["overflow-x"] = "hidden";
				} else if (overflow === "scroll" && axis === "horizontal") {
					container.style["overflow-y"] = "hidden";
					container.style["overflow-x"] = overflow;
				} else {
					container.style["overflow"] = overflow;
				}
			}

			if (direction) {
				container.dir = direction;
				container.style["direction"] = direction;
			}

			if (direction && this.settings.fullsize) {
				document.body.style["direction"] = direction;
			}

			return container;
		}
	}, {
		key: "wrap",
		value: function wrap(container) {
			var wrapper = document.createElement("div");

			wrapper.style.visibility = "hidden";
			wrapper.style.overflow = "hidden";
			wrapper.style.width = "0";
			wrapper.style.height = "0";

			wrapper.appendChild(container);
			return wrapper;
		}
	}, {
		key: "getElement",
		value: function getElement(_element) {
			var element;

			if ((0, _core.isElement)(_element)) {
				element = _element;
			} else if (typeof _element === "string") {
				element = document.getElementById(_element);
			}

			if (!element) {
				throw new Error("Not an Element");
			}

			return element;
		}
	}, {
		key: "attachTo",
		value: function attachTo(what) {

			var element = this.getElement(what);
			var base;

			if (!element) {
				return;
			}

			if (this.settings.hidden) {
				base = this.wrapper;
			} else {
				base = this.container;
			}

			element.appendChild(base);

			this.element = element;

			return element;
		}
	}, {
		key: "getContainer",
		value: function getContainer() {
			return this.container;
		}
	}, {
		key: "onResize",
		value: function onResize(func) {
			// Only listen to window for resize event if width and height are not fixed.
			// This applies if it is set to a percent or auto.
			if (!(0, _core.isNumber)(this.settings.width) || !(0, _core.isNumber)(this.settings.height)) {
				this.resizeFunc = (0, _throttle2.default)(func, 50);
				window.addEventListener("resize", this.resizeFunc, false);
			}
		}
	}, {
		key: "onOrientationChange",
		value: function onOrientationChange(func) {
			this.orientationChangeFunc = func;
			window.addEventListener("orientationchange", this.orientationChangeFunc, false);
		}
	}, {
		key: "size",
		value: function size(width, height) {
			var bounds;
			var _width = width || this.settings.width;
			var _height = height || this.settings.height;

			// If width or height are set to false, inherit them from containing element
			if (width === null) {
				bounds = this.element.getBoundingClientRect();

				if (bounds.width) {
					width = Math.floor(bounds.width);
					this.container.style.width = width + "px";
				}
			} else {
				if ((0, _core.isNumber)(width)) {
					this.container.style.width = width + "px";
				} else {
					this.container.style.width = width;
				}
			}

			if (height === null) {
				bounds = bounds || this.element.getBoundingClientRect();

				if (bounds.height) {
					height = bounds.height;
					this.container.style.height = height + "px";
				}
			} else {
				if ((0, _core.isNumber)(height)) {
					this.container.style.height = height + "px";
				} else {
					this.container.style.height = height;
				}
			}

			if (!(0, _core.isNumber)(width)) {
				width = this.container.clientWidth;
			}

			if (!(0, _core.isNumber)(height)) {
				height = this.container.clientHeight;
			}

			this.containerStyles = window.getComputedStyle(this.container);

			this.containerPadding = {
				left: parseFloat(this.containerStyles["padding-left"]) || 0,
				right: parseFloat(this.containerStyles["padding-right"]) || 0,
				top: parseFloat(this.containerStyles["padding-top"]) || 0,
				bottom: parseFloat(this.containerStyles["padding-bottom"]) || 0
			};

			// Bounds not set, get them from window
			var _windowBounds = (0, _core.windowBounds)();
			var bodyStyles = window.getComputedStyle(document.body);
			var bodyPadding = {
				left: parseFloat(bodyStyles["padding-left"]) || 0,
				right: parseFloat(bodyStyles["padding-right"]) || 0,
				top: parseFloat(bodyStyles["padding-top"]) || 0,
				bottom: parseFloat(bodyStyles["padding-bottom"]) || 0
			};

			if (!_width) {
				width = _windowBounds.width - bodyPadding.left - bodyPadding.right;
			}

			if (this.settings.fullsize && !_height || !_height) {
				height = _windowBounds.height - bodyPadding.top - bodyPadding.bottom;
			}

			return {
				width: width - this.containerPadding.left - this.containerPadding.right,
				height: height - this.containerPadding.top - this.containerPadding.bottom
			};
		}
	}, {
		key: "bounds",
		value: function bounds() {
			var box = void 0;
			if (this.container.style.overflow !== "visible") {
				box = this.container && this.container.getBoundingClientRect();
			}

			if (!box || !box.width || !box.height) {
				return (0, _core.windowBounds)();
			} else {
				return box;
			}
		}
	}, {
		key: "getSheet",
		value: function getSheet() {
			var style = document.createElement("style");

			// WebKit hack --> https://davidwalsh.name/add-rules-stylesheets
			style.appendChild(document.createTextNode(""));

			document.head.appendChild(style);

			return style.sheet;
		}
	}, {
		key: "addStyleRules",
		value: function addStyleRules(selector, rulesArray) {
			var scope = "#" + this.id + " ";
			var rules = "";

			if (!this.sheet) {
				this.sheet = this.getSheet();
			}

			rulesArray.forEach(function (set) {
				for (var prop in set) {
					if (set.hasOwnProperty(prop)) {
						rules += prop + ":" + set[prop] + ";";
					}
				}
			});

			this.sheet.insertRule(scope + selector + " {" + rules + "}", 0);
		}
	}, {
		key: "axis",
		value: function axis(_axis) {
			if (_axis === "horizontal") {
				this.container.style.display = "flex";
				this.container.style.flexDirection = "row";
				this.container.style.flexWrap = "nowrap";
			} else {
				this.container.style.display = "block";
			}
			this.settings.axis = _axis;
		}

		// orientation(orientation) {
		// 	if (orientation === "landscape") {
		//
		// 	} else {
		//
		// 	}
		//
		// 	this.orientation = orientation;
		// }

	}, {
		key: "direction",
		value: function direction(dir) {
			if (this.container) {
				this.container.dir = dir;
				this.container.style["direction"] = dir;
			}

			if (this.settings.fullsize) {
				document.body.style["direction"] = dir;
			}
			this.settings.dir = dir;
		}
	}, {
		key: "overflow",
		value: function overflow(_overflow) {
			if (this.container) {
				if (_overflow === "scroll" && this.settings.axis === "vertical") {
					this.container.style["overflow-y"] = _overflow;
					this.container.style["overflow-x"] = "hidden";
				} else if (_overflow === "scroll" && this.settings.axis === "horizontal") {
					this.container.style["overflow-y"] = "hidden";
					this.container.style["overflow-x"] = _overflow;
				} else {
					this.container.style["overflow"] = _overflow;
				}
			}
			this.settings.overflow = _overflow;
		}
	}, {
		key: "destroy",
		value: function destroy() {
			var base;

			if (this.element) {

				if (this.settings.hidden) {
					base = this.wrapper;
				} else {
					base = this.container;
				}

				if (this.element.contains(this.container)) {
					this.element.removeChild(this.container);
				}

				window.removeEventListener("resize", this.resizeFunc);
				window.removeEventListener("orientationChange", this.orientationChangeFunc);
			}
		}
	}]);

	return Stage;
}();

exports.default = Stage;
module.exports = exports["default"];

/***/ }),
/* 389 */
/***/ (function(module, exports, __webpack_require__) {

var debounce = __webpack_require__(144),
    isObject = __webpack_require__(106);

/** Error message constants. */
var FUNC_ERROR_TEXT = 'Expected a function';

/**
 * Creates a throttled function that only invokes `func` at most once per
 * every `wait` milliseconds. The throttled function comes with a `cancel`
 * method to cancel delayed `func` invocations and a `flush` method to
 * immediately invoke them. Provide `options` to indicate whether `func`
 * should be invoked on the leading and/or trailing edge of the `wait`
 * timeout. The `func` is invoked with the last arguments provided to the
 * throttled function. Subsequent calls to the throttled function return the
 * result of the last `func` invocation.
 *
 * **Note:** If `leading` and `trailing` options are `true`, `func` is
 * invoked on the trailing edge of the timeout only if the throttled function
 * is invoked more than once during the `wait` timeout.
 *
 * If `wait` is `0` and `leading` is `false`, `func` invocation is deferred
 * until to the next tick, similar to `setTimeout` with a timeout of `0`.
 *
 * See [David Corbacho's article](https://css-tricks.com/debouncing-throttling-explained-examples/)
 * for details over the differences between `_.throttle` and `_.debounce`.
 *
 * @static
 * @memberOf _
 * @since 0.1.0
 * @category Function
 * @param {Function} func The function to throttle.
 * @param {number} [wait=0] The number of milliseconds to throttle invocations to.
 * @param {Object} [options={}] The options object.
 * @param {boolean} [options.leading=true]
 *  Specify invoking on the leading edge of the timeout.
 * @param {boolean} [options.trailing=true]
 *  Specify invoking on the trailing edge of the timeout.
 * @returns {Function} Returns the new throttled function.
 * @example
 *
 * // Avoid excessively updating the position while scrolling.
 * jQuery(window).on('scroll', _.throttle(updatePosition, 100));
 *
 * // Invoke `renewToken` when the click event is fired, but not more than once every 5 minutes.
 * var throttled = _.throttle(renewToken, 300000, { 'trailing': false });
 * jQuery(element).on('click', throttled);
 *
 * // Cancel the trailing throttled invocation.
 * jQuery(window).on('popstate', throttled.cancel);
 */
function throttle(func, wait, options) {
  var leading = true,
      trailing = true;

  if (typeof func != 'function') {
    throw new TypeError(FUNC_ERROR_TEXT);
  }
  if (isObject(options)) {
    leading = 'leading' in options ? !!options.leading : leading;
    trailing = 'trailing' in options ? !!options.trailing : trailing;
  }
  return debounce(func, wait, {
    'leading': leading,
    'maxWait': wait,
    'trailing': trailing
  });
}

module.exports = throttle;


/***/ }),
/* 390 */
/***/ (function(module, exports, __webpack_require__) {

var root = __webpack_require__(145);

/**
 * Gets the timestamp of the number of milliseconds that have elapsed since
 * the Unix epoch (1 January 1970 00:00:00 UTC).
 *
 * @static
 * @memberOf _
 * @since 2.4.0
 * @category Date
 * @returns {number} Returns the timestamp.
 * @example
 *
 * _.defer(function(stamp) {
 *   console.log(_.now() - stamp);
 * }, _.now());
 * // => Logs the number of milliseconds it took for the deferred invocation.
 */
var now = function() {
  return root.Date.now();
};

module.exports = now;


/***/ }),
/* 391 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function(global) {/** Detect free variable `global` from Node.js. */
var freeGlobal = typeof global == 'object' && global && global.Object === Object && global;

module.exports = freeGlobal;

/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(47)))

/***/ }),
/* 392 */
/***/ (function(module, exports, __webpack_require__) {

var isObject = __webpack_require__(106),
    isSymbol = __webpack_require__(393);

/** Used as references for various `Number` constants. */
var NAN = 0 / 0;

/** Used to match leading and trailing whitespace. */
var reTrim = /^\s+|\s+$/g;

/** Used to detect bad signed hexadecimal string values. */
var reIsBadHex = /^[-+]0x[0-9a-f]+$/i;

/** Used to detect binary string values. */
var reIsBinary = /^0b[01]+$/i;

/** Used to detect octal string values. */
var reIsOctal = /^0o[0-7]+$/i;

/** Built-in method references without a dependency on `root`. */
var freeParseInt = parseInt;

/**
 * Converts `value` to a number.
 *
 * @static
 * @memberOf _
 * @since 4.0.0
 * @category Lang
 * @param {*} value The value to process.
 * @returns {number} Returns the number.
 * @example
 *
 * _.toNumber(3.2);
 * // => 3.2
 *
 * _.toNumber(Number.MIN_VALUE);
 * // => 5e-324
 *
 * _.toNumber(Infinity);
 * // => Infinity
 *
 * _.toNumber('3.2');
 * // => 3.2
 */
function toNumber(value) {
  if (typeof value == 'number') {
    return value;
  }
  if (isSymbol(value)) {
    return NAN;
  }
  if (isObject(value)) {
    var other = typeof value.valueOf == 'function' ? value.valueOf() : value;
    value = isObject(other) ? (other + '') : other;
  }
  if (typeof value != 'string') {
    return value === 0 ? value : +value;
  }
  value = value.replace(reTrim, '');
  var isBinary = reIsBinary.test(value);
  return (isBinary || reIsOctal.test(value))
    ? freeParseInt(value.slice(2), isBinary ? 2 : 8)
    : (reIsBadHex.test(value) ? NAN : +value);
}

module.exports = toNumber;


/***/ }),
/* 393 */
/***/ (function(module, exports, __webpack_require__) {

var baseGetTag = __webpack_require__(394),
    isObjectLike = __webpack_require__(397);

/** `Object#toString` result references. */
var symbolTag = '[object Symbol]';

/**
 * Checks if `value` is classified as a `Symbol` primitive or object.
 *
 * @static
 * @memberOf _
 * @since 4.0.0
 * @category Lang
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is a symbol, else `false`.
 * @example
 *
 * _.isSymbol(Symbol.iterator);
 * // => true
 *
 * _.isSymbol('abc');
 * // => false
 */
function isSymbol(value) {
  return typeof value == 'symbol' ||
    (isObjectLike(value) && baseGetTag(value) == symbolTag);
}

module.exports = isSymbol;


/***/ }),
/* 394 */
/***/ (function(module, exports, __webpack_require__) {

var Symbol = __webpack_require__(146),
    getRawTag = __webpack_require__(395),
    objectToString = __webpack_require__(396);

/** `Object#toString` result references. */
var nullTag = '[object Null]',
    undefinedTag = '[object Undefined]';

/** Built-in value references. */
var symToStringTag = Symbol ? Symbol.toStringTag : undefined;

/**
 * The base implementation of `getTag` without fallbacks for buggy environments.
 *
 * @private
 * @param {*} value The value to query.
 * @returns {string} Returns the `toStringTag`.
 */
function baseGetTag(value) {
  if (value == null) {
    return value === undefined ? undefinedTag : nullTag;
  }
  return (symToStringTag && symToStringTag in Object(value))
    ? getRawTag(value)
    : objectToString(value);
}

module.exports = baseGetTag;


/***/ }),
/* 395 */
/***/ (function(module, exports, __webpack_require__) {

var Symbol = __webpack_require__(146);

/** Used for built-in method references. */
var objectProto = Object.prototype;

/** Used to check objects for own properties. */
var hasOwnProperty = objectProto.hasOwnProperty;

/**
 * Used to resolve the
 * [`toStringTag`](http://ecma-international.org/ecma-262/7.0/#sec-object.prototype.tostring)
 * of values.
 */
var nativeObjectToString = objectProto.toString;

/** Built-in value references. */
var symToStringTag = Symbol ? Symbol.toStringTag : undefined;

/**
 * A specialized version of `baseGetTag` which ignores `Symbol.toStringTag` values.
 *
 * @private
 * @param {*} value The value to query.
 * @returns {string} Returns the raw `toStringTag`.
 */
function getRawTag(value) {
  var isOwn = hasOwnProperty.call(value, symToStringTag),
      tag = value[symToStringTag];

  try {
    value[symToStringTag] = undefined;
    var unmasked = true;
  } catch (e) {}

  var result = nativeObjectToString.call(value);
  if (unmasked) {
    if (isOwn) {
      value[symToStringTag] = tag;
    } else {
      delete value[symToStringTag];
    }
  }
  return result;
}

module.exports = getRawTag;


/***/ }),
/* 396 */
/***/ (function(module, exports) {

/** Used for built-in method references. */
var objectProto = Object.prototype;

/**
 * Used to resolve the
 * [`toStringTag`](http://ecma-international.org/ecma-262/7.0/#sec-object.prototype.tostring)
 * of values.
 */
var nativeObjectToString = objectProto.toString;

/**
 * Converts `value` to a string using `Object.prototype.toString`.
 *
 * @private
 * @param {*} value The value to convert.
 * @returns {string} Returns the converted string.
 */
function objectToString(value) {
  return nativeObjectToString.call(value);
}

module.exports = objectToString;


/***/ }),
/* 397 */
/***/ (function(module, exports) {

/**
 * Checks if `value` is object-like. A value is object-like if it's not `null`
 * and has a `typeof` result of "object".
 *
 * @static
 * @memberOf _
 * @since 4.0.0
 * @category Lang
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is object-like, else `false`.
 * @example
 *
 * _.isObjectLike({});
 * // => true
 *
 * _.isObjectLike([1, 2, 3]);
 * // => true
 *
 * _.isObjectLike(_.noop);
 * // => false
 *
 * _.isObjectLike(null);
 * // => false
 */
function isObjectLike(value) {
  return value != null && typeof value == 'object';
}

module.exports = isObjectLike;


/***/ }),
/* 398 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Views = function () {
	function Views(container) {
		_classCallCheck(this, Views);

		this.container = container;
		this._views = [];
		this.length = 0;
		this.hidden = false;
	}

	_createClass(Views, [{
		key: "all",
		value: function all() {
			return this._views;
		}
	}, {
		key: "first",
		value: function first() {
			return this._views[0];
		}
	}, {
		key: "last",
		value: function last() {
			return this._views[this._views.length - 1];
		}
	}, {
		key: "indexOf",
		value: function indexOf(view) {
			return this._views.indexOf(view);
		}
	}, {
		key: "slice",
		value: function slice() {
			return this._views.slice.apply(this._views, arguments);
		}
	}, {
		key: "get",
		value: function get(i) {
			return this._views[i];
		}
	}, {
		key: "append",
		value: function append(view) {
			this._views.push(view);
			if (this.container) {
				this.container.appendChild(view.element);
			}
			this.length++;
			return view;
		}
	}, {
		key: "prepend",
		value: function prepend(view) {
			this._views.unshift(view);
			if (this.container) {
				this.container.insertBefore(view.element, this.container.firstChild);
			}
			this.length++;
			return view;
		}
	}, {
		key: "insert",
		value: function insert(view, index) {
			this._views.splice(index, 0, view);

			if (this.container) {
				if (index < this.container.children.length) {
					this.container.insertBefore(view.element, this.container.children[index]);
				} else {
					this.container.appendChild(view.element);
				}
			}

			this.length++;
			return view;
		}
	}, {
		key: "remove",
		value: function remove(view) {
			var index = this._views.indexOf(view);

			if (index > -1) {
				this._views.splice(index, 1);
			}

			this.destroy(view);

			this.length--;
		}
	}, {
		key: "destroy",
		value: function destroy(view) {
			if (view.displayed) {
				view.destroy();
			}

			if (this.container) {
				this.container.removeChild(view.element);
			}
			view = null;
		}

		// Iterators

	}, {
		key: "forEach",
		value: function forEach() {
			return this._views.forEach.apply(this._views, arguments);
		}
	}, {
		key: "clear",
		value: function clear() {
			// Remove all views
			var view;
			var len = this.length;

			if (!this.length) return;

			for (var i = 0; i < len; i++) {
				view = this._views[i];
				this.destroy(view);
			}

			this._views = [];
			this.length = 0;
		}
	}, {
		key: "find",
		value: function find(section) {

			var view;
			var len = this.length;

			for (var i = 0; i < len; i++) {
				view = this._views[i];
				if (view.displayed && view.section.index == section.index) {
					return view;
				}
			}
		}
	}, {
		key: "displayed",
		value: function displayed() {
			var displayed = [];
			var view;
			var len = this.length;

			for (var i = 0; i < len; i++) {
				view = this._views[i];
				if (view.displayed) {
					displayed.push(view);
				}
			}
			return displayed;
		}
	}, {
		key: "show",
		value: function show() {
			var view;
			var len = this.length;

			for (var i = 0; i < len; i++) {
				view = this._views[i];
				if (view.displayed) {
					view.show();
				}
			}
			this.hidden = false;
		}
	}, {
		key: "hide",
		value: function hide() {
			var view;
			var len = this.length;

			for (var i = 0; i < len; i++) {
				view = this._views[i];
				if (view.displayed) {
					view.hide();
				}
			}
			this.hidden = true;
		}
	}]);

	return Views;
}();

exports.default = Views;
module.exports = exports["default"];

/***/ }),
/* 399 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _core = __webpack_require__(6);

var _constants = __webpack_require__(23);

var _eventEmitter = __webpack_require__(30);

var _eventEmitter2 = _interopRequireDefault(_eventEmitter);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

// easing equations from https://github.com/danro/easing-js/blob/master/easing.js
var PI_D2 = Math.PI / 2;
var EASING_EQUATIONS = {
	easeOutSine: function easeOutSine(pos) {
		return Math.sin(pos * PI_D2);
	},
	easeInOutSine: function easeInOutSine(pos) {
		return -0.5 * (Math.cos(Math.PI * pos) - 1);
	},
	easeInOutQuint: function easeInOutQuint(pos) {
		if ((pos /= 0.5) < 1) {
			return 0.5 * Math.pow(pos, 5);
		}
		return 0.5 * (Math.pow(pos - 2, 5) + 2);
	},
	easeInCubic: function easeInCubic(pos) {
		return Math.pow(pos, 3);
	}
};

var Snap = function () {
	function Snap(manager, options) {
		_classCallCheck(this, Snap);

		this.settings = (0, _core.extend)({
			duration: 80,
			minVelocity: 0.2,
			minDistance: 10,
			easing: EASING_EQUATIONS['easeInCubic']
		}, options || {});

		this.supportsTouch = this.supportsTouch();

		if (this.supportsTouch) {
			this.setup(manager);
		}
	}

	_createClass(Snap, [{
		key: "setup",
		value: function setup(manager) {
			this.manager = manager;

			this.layout = this.manager.layout;

			this.fullsize = this.manager.settings.fullsize;
			if (this.fullsize) {
				this.element = this.manager.stage.element;
				this.scroller = window;
				this.disableScroll();
			} else {
				this.element = this.manager.stage.container;
				this.scroller = this.element;
				this.element.style["WebkitOverflowScrolling"] = "touch";
			}

			// this.overflow = this.manager.overflow;

			// set lookahead offset to page width
			this.manager.settings.offset = this.layout.width;
			this.manager.settings.afterScrolledTimeout = this.settings.duration * 2;

			this.isVertical = this.manager.settings.axis === "vertical";

			// disable snapping if not paginated or axis in not horizontal
			if (!this.manager.isPaginated || this.isVertical) {
				return;
			}

			this.touchCanceler = false;
			this.resizeCanceler = false;
			this.snapping = false;

			this.scrollLeft;
			this.scrollTop;

			this.startTouchX = undefined;
			this.startTouchY = undefined;
			this.startTime = undefined;
			this.endTouchX = undefined;
			this.endTouchY = undefined;
			this.endTime = undefined;

			this.addListeners();
		}
	}, {
		key: "supportsTouch",
		value: function supportsTouch() {
			if ('ontouchstart' in window || window.DocumentTouch && document instanceof DocumentTouch) {
				return true;
			}

			return false;
		}
	}, {
		key: "disableScroll",
		value: function disableScroll() {
			this.element.style.overflow = "hidden";
		}
	}, {
		key: "enableScroll",
		value: function enableScroll() {
			this.element.style.overflow = "";
		}
	}, {
		key: "addListeners",
		value: function addListeners() {
			this._onResize = this.onResize.bind(this);
			window.addEventListener('resize', this._onResize);

			this._onScroll = this.onScroll.bind(this);
			this.scroller.addEventListener('scroll', this._onScroll);

			this._onTouchStart = this.onTouchStart.bind(this);
			this.scroller.addEventListener('touchstart', this._onTouchStart, { passive: true });
			this.on('touchstart', this._onTouchStart);

			this._onTouchMove = this.onTouchMove.bind(this);
			this.scroller.addEventListener('touchmove', this._onTouchMove, { passive: true });
			this.on('touchmove', this._onTouchMove);

			this._onTouchEnd = this.onTouchEnd.bind(this);
			this.scroller.addEventListener('touchend', this._onTouchEnd, { passive: true });
			this.on('touchend', this._onTouchEnd);

			this._afterDisplayed = this.afterDisplayed.bind(this);
			this.manager.on(_constants.EVENTS.MANAGERS.ADDED, this._afterDisplayed);
		}
	}, {
		key: "removeListeners",
		value: function removeListeners() {
			window.removeEventListener('resize', this._onResize);
			this._onResize = undefined;

			this.scroller.removeEventListener('scroll', this._onScroll);
			this._onScroll = undefined;

			this.scroller.removeEventListener('touchstart', this._onTouchStart, { passive: true });
			this.off('touchstart', this._onTouchStart);
			this._onTouchStart = undefined;

			this.scroller.removeEventListener('touchmove', this._onTouchMove, { passive: true });
			this.off('touchmove', this._onTouchMove);
			this._onTouchMove = undefined;

			this.scroller.removeEventListener('touchend', this._onTouchEnd, { passive: true });
			this.off('touchend', this._onTouchEnd);
			this._onTouchEnd = undefined;

			this.manager.off(_constants.EVENTS.MANAGERS.ADDED, this._afterDisplayed);
			this._afterDisplayed = undefined;
		}
	}, {
		key: "afterDisplayed",
		value: function afterDisplayed(view) {
			var _this = this;

			var contents = view.contents;
			["touchstart", "touchmove", "touchend"].forEach(function (e) {
				contents.on(e, function (ev) {
					return _this.triggerViewEvent(ev, contents);
				});
			});
		}
	}, {
		key: "triggerViewEvent",
		value: function triggerViewEvent(e, contents) {
			this.emit(e.type, e, contents);
		}
	}, {
		key: "onScroll",
		value: function onScroll(e) {
			this.scrollLeft = this.fullsize ? window.scrollX : this.scroller.scrollLeft;
			this.scrollTop = this.fullsize ? window.scrollY : this.scroller.scrollTop;
		}
	}, {
		key: "onResize",
		value: function onResize(e) {
			this.resizeCanceler = true;
		}
	}, {
		key: "onTouchStart",
		value: function onTouchStart(e) {
			var _e$touches$ = e.touches[0],
			    screenX = _e$touches$.screenX,
			    screenY = _e$touches$.screenY;


			if (this.fullsize) {
				this.enableScroll();
			}

			this.touchCanceler = true;

			if (!this.startTouchX) {
				this.startTouchX = screenX;
				this.startTouchY = screenY;
				this.startTime = this.now();
			}

			this.endTouchX = screenX;
			this.endTouchY = screenY;
			this.endTime = this.now();
		}
	}, {
		key: "onTouchMove",
		value: function onTouchMove(e) {
			var _e$touches$2 = e.touches[0],
			    screenX = _e$touches$2.screenX,
			    screenY = _e$touches$2.screenY;

			var deltaY = Math.abs(screenY - this.endTouchY);

			this.touchCanceler = true;

			if (!this.fullsize && deltaY < 10) {
				this.element.scrollLeft -= screenX - this.endTouchX;
			}

			this.endTouchX = screenX;
			this.endTouchY = screenY;
			this.endTime = this.now();
		}
	}, {
		key: "onTouchEnd",
		value: function onTouchEnd(e) {
			if (this.fullsize) {
				this.disableScroll();
			}

			this.touchCanceler = false;

			var swipped = this.wasSwiped();

			if (swipped !== 0) {
				this.snap(swipped);
			} else {
				this.snap();
			}

			this.startTouchX = undefined;
			this.startTouchY = undefined;
			this.startTime = undefined;
			this.endTouchX = undefined;
			this.endTouchY = undefined;
			this.endTime = undefined;
		}
	}, {
		key: "wasSwiped",
		value: function wasSwiped() {
			var snapWidth = this.layout.pageWidth * this.layout.divisor;
			var distance = this.endTouchX - this.startTouchX;
			var absolute = Math.abs(distance);
			var time = this.endTime - this.startTime;
			var velocity = distance / time;
			var minVelocity = this.settings.minVelocity;

			if (absolute <= this.settings.minDistance || absolute >= snapWidth) {
				return 0;
			}

			if (velocity > minVelocity) {
				// previous
				return -1;
			} else if (velocity < -minVelocity) {
				// next
				return 1;
			}
		}
	}, {
		key: "needsSnap",
		value: function needsSnap() {
			var left = this.scrollLeft;
			var snapWidth = this.layout.pageWidth * this.layout.divisor;
			return left % snapWidth !== 0;
		}
	}, {
		key: "snap",
		value: function snap() {
			var howMany = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 0;

			var left = this.scrollLeft;
			var snapWidth = this.layout.pageWidth * this.layout.divisor;
			var snapTo = Math.round(left / snapWidth) * snapWidth;

			if (howMany) {
				snapTo += howMany * snapWidth;
			}

			return this.smoothScrollTo(snapTo);
		}
	}, {
		key: "smoothScrollTo",
		value: function smoothScrollTo(destination) {
			var deferred = new _core.defer();
			var start = this.scrollLeft;
			var startTime = this.now();

			var duration = this.settings.duration;
			var easing = this.settings.easing;

			this.snapping = true;

			// add animation loop
			function tick() {
				var now = this.now();
				var time = Math.min(1, (now - startTime) / duration);
				var timeFunction = easing(time);

				if (this.touchCanceler || this.resizeCanceler) {
					this.resizeCanceler = false;
					this.snapping = false;
					deferred.resolve();
					return;
				}

				if (time < 1) {
					window.requestAnimationFrame(tick.bind(this));
					this.scrollTo(start + (destination - start) * time, 0);
				} else {
					this.scrollTo(destination, 0);
					this.snapping = false;
					deferred.resolve();
				}
			}

			tick.call(this);

			return deferred.promise;
		}
	}, {
		key: "scrollTo",
		value: function scrollTo() {
			var left = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 0;
			var top = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 0;

			if (this.fullsize) {
				window.scroll(left, top);
			} else {
				this.scroller.scrollLeft = left;
				this.scroller.scrollTop = top;
			}
		}
	}, {
		key: "now",
		value: function now() {
			return 'now' in window.performance ? performance.now() : new Date().getTime();
		}
	}, {
		key: "destroy",
		value: function destroy() {
			if (!this.scroller) {
				return;
			}

			if (this.fullsize) {
				this.enableScroll();
			}

			this.removeListeners();

			this.scroller = undefined;
		}
	}]);

	return Snap;
}();

(0, _eventEmitter2.default)(Snap.prototype);

exports.default = Snap;
module.exports = exports["default"];

/***/ }),
/* 400 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _core = __webpack_require__(6);

var _request = __webpack_require__(73);

var _request2 = _interopRequireDefault(_request);

var _mime = __webpack_require__(103);

var _mime2 = _interopRequireDefault(_mime);

var _path = __webpack_require__(46);

var _path2 = _interopRequireDefault(_path);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Handles Unzipping a requesting files from an Epub Archive
 * @class
 */
var Archive = function () {
	function Archive() {
		_classCallCheck(this, Archive);

		this.zip = undefined;
		this.urlCache = {};

		this.checkRequirements();
	}

	/**
  * Checks to see if JSZip exists in global namspace,
  * Requires JSZip if it isn't there
  * @private
  */


	_createClass(Archive, [{
		key: "checkRequirements",
		value: function checkRequirements() {
			try {
				if (typeof JSZip === "undefined") {
					var _JSZip = __webpack_require__(401);
					this.zip = new _JSZip();
				} else {
					this.zip = new JSZip();
				}
			} catch (e) {
				throw new Error("JSZip lib not loaded");
			}
		}

		/**
   * Open an archive
   * @param  {binary} input
   * @param  {boolean} [isBase64] tells JSZip if the input data is base64 encoded
   * @return {Promise} zipfile
   */

	}, {
		key: "open",
		value: function open(input, isBase64) {
			return this.zip.loadAsync(input, { "base64": isBase64 });
		}

		/**
   * Load and Open an archive
   * @param  {string} zipUrl
   * @param  {boolean} [isBase64] tells JSZip if the input data is base64 encoded
   * @return {Promise} zipfile
   */

	}, {
		key: "openUrl",
		value: function openUrl(zipUrl, isBase64) {
			return (0, _request2.default)(zipUrl, "binary").then(function (data) {
				return this.zip.loadAsync(data, { "base64": isBase64 });
			}.bind(this));
		}

		/**
   * Request a url from the archive
   * @param  {string} url  a url to request from the archive
   * @param  {string} [type] specify the type of the returned result
   * @return {Promise<Blob | string | JSON | Document | XMLDocument>}
   */

	}, {
		key: "request",
		value: function request(url, type) {
			var deferred = new _core.defer();
			var response;
			var path = new _path2.default(url);

			// If type isn't set, determine it from the file extension
			if (!type) {
				type = path.extension;
			}

			if (type == "blob") {
				response = this.getBlob(url);
			} else {
				response = this.getText(url);
			}

			if (response) {
				response.then(function (r) {
					var result = this.handleResponse(r, type);
					deferred.resolve(result);
				}.bind(this));
			} else {
				deferred.reject({
					message: "File not found in the epub: " + url,
					stack: new Error().stack
				});
			}
			return deferred.promise;
		}

		/**
   * Handle the response from request
   * @private
   * @param  {any} response
   * @param  {string} [type]
   * @return {any} the parsed result
   */

	}, {
		key: "handleResponse",
		value: function handleResponse(response, type) {
			var r;

			if (type == "json") {
				r = JSON.parse(response);
			} else if ((0, _core.isXml)(type)) {
				r = (0, _core.parse)(response, "text/xml");
			} else if (type == "xhtml") {
				r = (0, _core.parse)(response, "application/xhtml+xml");
			} else if (type == "html" || type == "htm") {
				r = (0, _core.parse)(response, "text/html");
			} else {
				r = response;
			}

			return r;
		}

		/**
   * Get a Blob from Archive by Url
   * @param  {string} url
   * @param  {string} [mimeType]
   * @return {Blob}
   */

	}, {
		key: "getBlob",
		value: function getBlob(url, mimeType) {
			var decodededUrl = window.decodeURIComponent(url.substr(1)); // Remove first slash
			var entry = this.zip.file(decodededUrl);

			if (entry) {
				mimeType = mimeType || _mime2.default.lookup(entry.name);
				return entry.async("uint8array").then(function (uint8array) {
					return new Blob([uint8array], { type: mimeType });
				});
			}
		}

		/**
   * Get Text from Archive by Url
   * @param  {string} url
   * @param  {string} [encoding]
   * @return {string}
   */

	}, {
		key: "getText",
		value: function getText(url, encoding) {
			var decodededUrl = window.decodeURIComponent(url.substr(1)); // Remove first slash
			var entry = this.zip.file(decodededUrl);

			if (entry) {
				return entry.async("string").then(function (text) {
					return text;
				});
			}
		}

		/**
   * Get a base64 encoded result from Archive by Url
   * @param  {string} url
   * @param  {string} [mimeType]
   * @return {string} base64 encoded
   */

	}, {
		key: "getBase64",
		value: function getBase64(url, mimeType) {
			var decodededUrl = window.decodeURIComponent(url.substr(1)); // Remove first slash
			var entry = this.zip.file(decodededUrl);

			if (entry) {
				mimeType = mimeType || _mime2.default.lookup(entry.name);
				return entry.async("base64").then(function (data) {
					return "data:" + mimeType + ";base64," + data;
				});
			}
		}

		/**
   * Create a Url from an unarchived item
   * @param  {string} url
   * @param  {object} [options.base64] use base64 encoding or blob url
   * @return {Promise} url promise with Url string
   */

	}, {
		key: "createUrl",
		value: function createUrl(url, options) {
			var deferred = new _core.defer();
			var _URL = window.URL || window.webkitURL || window.mozURL;
			var tempUrl;
			var response;
			var useBase64 = options && options.base64;

			if (url in this.urlCache) {
				deferred.resolve(this.urlCache[url]);
				return deferred.promise;
			}

			if (useBase64) {
				response = this.getBase64(url);

				if (response) {
					response.then(function (tempUrl) {

						this.urlCache[url] = tempUrl;
						deferred.resolve(tempUrl);
					}.bind(this));
				}
			} else {

				response = this.getBlob(url);

				if (response) {
					response.then(function (blob) {

						tempUrl = _URL.createObjectURL(blob);
						this.urlCache[url] = tempUrl;
						deferred.resolve(tempUrl);
					}.bind(this));
				}
			}

			if (!response) {
				deferred.reject({
					message: "File not found in the epub: " + url,
					stack: new Error().stack
				});
			}

			return deferred.promise;
		}

		/**
   * Revoke Temp Url for a achive item
   * @param  {string} url url of the item in the archive
   */

	}, {
		key: "revokeUrl",
		value: function revokeUrl(url) {
			var _URL = window.URL || window.webkitURL || window.mozURL;
			var fromCache = this.urlCache[url];
			if (fromCache) _URL.revokeObjectURL(fromCache);
		}
	}, {
		key: "destroy",
		value: function destroy() {
			var _URL = window.URL || window.webkitURL || window.mozURL;
			for (var fromCache in this.urlCache) {
				_URL.revokeObjectURL(fromCache);
			}
			this.zip = undefined;
			this.urlCache = {};
		}
	}]);

	return Archive;
}();

exports.default = Archive;
module.exports = exports["default"];

/***/ }),
/* 401 */
/***/ (function(module, exports) {

if(typeof __WEBPACK_EXTERNAL_MODULE_401__ === 'undefined') {var e = new Error("Cannot find module \"jszip\""); e.code = 'MODULE_NOT_FOUND'; throw e;}
module.exports = __WEBPACK_EXTERNAL_MODULE_401__;

/***/ }),
/* 402 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _core = __webpack_require__(6);

var _request = __webpack_require__(73);

var _request2 = _interopRequireDefault(_request);

var _mime = __webpack_require__(103);

var _mime2 = _interopRequireDefault(_mime);

var _path = __webpack_require__(46);

var _path2 = _interopRequireDefault(_path);

var _eventEmitter = __webpack_require__(30);

var _eventEmitter2 = _interopRequireDefault(_eventEmitter);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Handles saving and requesting files from local storage
 * @class
 * @param {string} name This should be the name of the application for modals
 * @param {function} [requester]
 * @param {function} [resolver]
 */
var Store = function () {
	function Store(name, requester, resolver) {
		_classCallCheck(this, Store);

		this.urlCache = {};

		this.storage = undefined;

		this.name = name;
		this.requester = requester || _request2.default;
		this.resolver = resolver;

		this.online = true;

		this.checkRequirements();

		this.addListeners();
	}

	/**
  * Checks to see if localForage exists in global namspace,
  * Requires localForage if it isn't there
  * @private
  */


	_createClass(Store, [{
		key: "checkRequirements",
		value: function checkRequirements() {
			try {
				var store = void 0;
				if (typeof localforage === "undefined") {
					store = __webpack_require__(403);
				} else {
					store = localforage;
				}
				this.storage = store.createInstance({
					name: this.name
				});
			} catch (e) {
				throw new Error("localForage lib not loaded");
			}
		}

		/**
   * Add online and offline event listeners
   * @private
   */

	}, {
		key: "addListeners",
		value: function addListeners() {
			this._status = this.status.bind(this);
			window.addEventListener('online', this._status);
			window.addEventListener('offline', this._status);
		}

		/**
   * Remove online and offline event listeners
   * @private
   */

	}, {
		key: "removeListeners",
		value: function removeListeners() {
			window.removeEventListener('online', this._status);
			window.removeEventListener('offline', this._status);
			this._status = undefined;
		}

		/**
   * Update the online / offline status
   * @private
   */

	}, {
		key: "status",
		value: function status(event) {
			var online = navigator.onLine;
			this.online = online;
			if (online) {
				this.emit("online", this);
			} else {
				this.emit("offline", this);
			}
		}

		/**
   * Add all of a book resources to the store
   * @param  {Resources} resources  book resources
   * @param  {boolean} [force] force resaving resources
   * @return {Promise<object>} store objects
   */

	}, {
		key: "add",
		value: function add(resources, force) {
			var _this = this;

			var mapped = resources.resources.map(function (item) {
				var href = item.href;

				var url = _this.resolver(href);
				var encodedUrl = window.encodeURIComponent(url);

				return _this.storage.getItem(encodedUrl).then(function (item) {
					if (!item || force) {
						return _this.requester(url, "binary").then(function (data) {
							return _this.storage.setItem(encodedUrl, data);
						});
					} else {
						return item;
					}
				});
			});
			return Promise.all(mapped);
		}

		/**
   * Put binary data from a url to storage
   * @param  {string} url  a url to request from storage
   * @param  {boolean} [withCredentials]
   * @param  {object} [headers]
   * @return {Promise<Blob>}
   */

	}, {
		key: "put",
		value: function put(url, withCredentials, headers) {
			var _this2 = this;

			var encodedUrl = window.encodeURIComponent(url);

			return this.storage.getItem(encodedUrl).then(function (result) {
				if (!result) {
					return _this2.requester(url, "binary", withCredentials, headers).then(function (data) {
						return _this2.storage.setItem(encodedUrl, data);
					});
				}
				return result;
			});
		}

		/**
   * Request a url
   * @param  {string} url  a url to request from storage
   * @param  {string} [type] specify the type of the returned result
   * @param  {boolean} [withCredentials]
   * @param  {object} [headers]
   * @return {Promise<Blob | string | JSON | Document | XMLDocument>}
   */

	}, {
		key: "request",
		value: function request(url, type, withCredentials, headers) {
			var _this3 = this;

			if (this.online) {
				// From network
				return this.requester(url, type, withCredentials, headers).then(function (data) {
					// save to store if not present
					_this3.put(url);
					return data;
				});
			} else {
				// From store
				return this.retrieve(url, type);
			}
		}

		/**
   * Request a url from storage
   * @param  {string} url  a url to request from storage
   * @param  {string} [type] specify the type of the returned result
   * @return {Promise<Blob | string | JSON | Document | XMLDocument>}
   */

	}, {
		key: "retrieve",
		value: function retrieve(url, type) {
			var _this4 = this;

			var deferred = new _core.defer();
			var response;
			var path = new _path2.default(url);

			// If type isn't set, determine it from the file extension
			if (!type) {
				type = path.extension;
			}

			if (type == "blob") {
				response = this.getBlob(url);
			} else {
				response = this.getText(url);
			}

			return response.then(function (r) {
				var deferred = new _core.defer();
				var result;
				if (r) {
					result = _this4.handleResponse(r, type);
					deferred.resolve(result);
				} else {
					deferred.reject({
						message: "File not found in storage: " + url,
						stack: new Error().stack
					});
				}
				return deferred.promise;
			});
		}

		/**
   * Handle the response from request
   * @private
   * @param  {any} response
   * @param  {string} [type]
   * @return {any} the parsed result
   */

	}, {
		key: "handleResponse",
		value: function handleResponse(response, type) {
			var r;

			if (type == "json") {
				r = JSON.parse(response);
			} else if ((0, _core.isXml)(type)) {
				r = (0, _core.parse)(response, "text/xml");
			} else if (type == "xhtml") {
				r = (0, _core.parse)(response, "application/xhtml+xml");
			} else if (type == "html" || type == "htm") {
				r = (0, _core.parse)(response, "text/html");
			} else {
				r = response;
			}

			return r;
		}

		/**
   * Get a Blob from Storage by Url
   * @param  {string} url
   * @param  {string} [mimeType]
   * @return {Blob}
   */

	}, {
		key: "getBlob",
		value: function getBlob(url, mimeType) {
			var encodedUrl = window.encodeURIComponent(url);

			return this.storage.getItem(encodedUrl).then(function (uint8array) {
				if (!uint8array) return;

				mimeType = mimeType || _mime2.default.lookup(url);

				return new Blob([uint8array], { type: mimeType });
			});
		}

		/**
   * Get Text from Storage by Url
   * @param  {string} url
   * @param  {string} [mimeType]
   * @return {string}
   */

	}, {
		key: "getText",
		value: function getText(url, mimeType) {
			var encodedUrl = window.encodeURIComponent(url);

			mimeType = mimeType || _mime2.default.lookup(url);

			return this.storage.getItem(encodedUrl).then(function (uint8array) {
				var deferred = new _core.defer();
				var reader = new FileReader();
				var blob;

				if (!uint8array) return;

				blob = new Blob([uint8array], { type: mimeType });

				reader.addEventListener("loadend", function () {
					deferred.resolve(reader.result);
				});

				reader.readAsText(blob, mimeType);

				return deferred.promise;
			});
		}

		/**
   * Get a base64 encoded result from Storage by Url
   * @param  {string} url
   * @param  {string} [mimeType]
   * @return {string} base64 encoded
   */

	}, {
		key: "getBase64",
		value: function getBase64(url, mimeType) {
			var encodedUrl = window.encodeURIComponent(url);

			mimeType = mimeType || _mime2.default.lookup(url);

			return this.storage.getItem(encodedUrl).then(function (uint8array) {
				var deferred = new _core.defer();
				var reader = new FileReader();
				var blob;

				if (!uint8array) return;

				blob = new Blob([uint8array], { type: mimeType });

				reader.addEventListener("loadend", function () {
					deferred.resolve(reader.result);
				});
				reader.readAsDataURL(blob, mimeType);

				return deferred.promise;
			});
		}

		/**
   * Create a Url from a stored item
   * @param  {string} url
   * @param  {object} [options.base64] use base64 encoding or blob url
   * @return {Promise} url promise with Url string
   */

	}, {
		key: "createUrl",
		value: function createUrl(url, options) {
			var deferred = new _core.defer();
			var _URL = window.URL || window.webkitURL || window.mozURL;
			var tempUrl;
			var response;
			var useBase64 = options && options.base64;

			if (url in this.urlCache) {
				deferred.resolve(this.urlCache[url]);
				return deferred.promise;
			}

			if (useBase64) {
				response = this.getBase64(url);

				if (response) {
					response.then(function (tempUrl) {

						this.urlCache[url] = tempUrl;
						deferred.resolve(tempUrl);
					}.bind(this));
				}
			} else {

				response = this.getBlob(url);

				if (response) {
					response.then(function (blob) {

						tempUrl = _URL.createObjectURL(blob);
						this.urlCache[url] = tempUrl;
						deferred.resolve(tempUrl);
					}.bind(this));
				}
			}

			if (!response) {
				deferred.reject({
					message: "File not found in storage: " + url,
					stack: new Error().stack
				});
			}

			return deferred.promise;
		}

		/**
   * Revoke Temp Url for a achive item
   * @param  {string} url url of the item in the store
   */

	}, {
		key: "revokeUrl",
		value: function revokeUrl(url) {
			var _URL = window.URL || window.webkitURL || window.mozURL;
			var fromCache = this.urlCache[url];
			if (fromCache) _URL.revokeObjectURL(fromCache);
		}
	}, {
		key: "destroy",
		value: function destroy() {
			var _URL = window.URL || window.webkitURL || window.mozURL;
			for (var fromCache in this.urlCache) {
				_URL.revokeObjectURL(fromCache);
			}
			this.urlCache = {};
			this.removeListeners();
		}
	}]);

	return Store;
}();

(0, _eventEmitter2.default)(Store.prototype);

exports.default = Store;
module.exports = exports["default"];

/***/ }),
/* 403 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function(global) {var require;var require;/*!
    localForage -- Offline Storage, Improved
    Version 1.7.2
    https://localforage.github.io/localForage
    (c) 2013-2017 Mozilla, Apache License 2.0
*/
(function(f){if(true){module.exports=f()}else if(typeof define==="function"&&define.amd){define([],f)}else{var g;if(typeof window!=="undefined"){g=window}else if(typeof global!=="undefined"){g=global}else if(typeof self!=="undefined"){g=self}else{g=this}g.localforage = f()}})(function(){var define,module,exports;return (function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return require(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw (f.code="MODULE_NOT_FOUND", f)}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(_dereq_,module,exports){
(function (global){
'use strict';
var Mutation = global.MutationObserver || global.WebKitMutationObserver;

var scheduleDrain;

{
  if (Mutation) {
    var called = 0;
    var observer = new Mutation(nextTick);
    var element = global.document.createTextNode('');
    observer.observe(element, {
      characterData: true
    });
    scheduleDrain = function () {
      element.data = (called = ++called % 2);
    };
  } else if (!global.setImmediate && typeof global.MessageChannel !== 'undefined') {
    var channel = new global.MessageChannel();
    channel.port1.onmessage = nextTick;
    scheduleDrain = function () {
      channel.port2.postMessage(0);
    };
  } else if ('document' in global && 'onreadystatechange' in global.document.createElement('script')) {
    scheduleDrain = function () {

      // Create a <script> element; its readystatechange event will be fired asynchronously once it is inserted
      // into the document. Do so, thus queuing up the task. Remember to clean up once it's been called.
      var scriptEl = global.document.createElement('script');
      scriptEl.onreadystatechange = function () {
        nextTick();

        scriptEl.onreadystatechange = null;
        scriptEl.parentNode.removeChild(scriptEl);
        scriptEl = null;
      };
      global.document.documentElement.appendChild(scriptEl);
    };
  } else {
    scheduleDrain = function () {
      setTimeout(nextTick, 0);
    };
  }
}

var draining;
var queue = [];
//named nextTick for less confusing stack traces
function nextTick() {
  draining = true;
  var i, oldQueue;
  var len = queue.length;
  while (len) {
    oldQueue = queue;
    queue = [];
    i = -1;
    while (++i < len) {
      oldQueue[i]();
    }
    len = queue.length;
  }
  draining = false;
}

module.exports = immediate;
function immediate(task) {
  if (queue.push(task) === 1 && !draining) {
    scheduleDrain();
  }
}

}).call(this,typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
},{}],2:[function(_dereq_,module,exports){
'use strict';
var immediate = _dereq_(1);

/* istanbul ignore next */
function INTERNAL() {}

var handlers = {};

var REJECTED = ['REJECTED'];
var FULFILLED = ['FULFILLED'];
var PENDING = ['PENDING'];

module.exports = Promise;

function Promise(resolver) {
  if (typeof resolver !== 'function') {
    throw new TypeError('resolver must be a function');
  }
  this.state = PENDING;
  this.queue = [];
  this.outcome = void 0;
  if (resolver !== INTERNAL) {
    safelyResolveThenable(this, resolver);
  }
}

Promise.prototype["catch"] = function (onRejected) {
  return this.then(null, onRejected);
};
Promise.prototype.then = function (onFulfilled, onRejected) {
  if (typeof onFulfilled !== 'function' && this.state === FULFILLED ||
    typeof onRejected !== 'function' && this.state === REJECTED) {
    return this;
  }
  var promise = new this.constructor(INTERNAL);
  if (this.state !== PENDING) {
    var resolver = this.state === FULFILLED ? onFulfilled : onRejected;
    unwrap(promise, resolver, this.outcome);
  } else {
    this.queue.push(new QueueItem(promise, onFulfilled, onRejected));
  }

  return promise;
};
function QueueItem(promise, onFulfilled, onRejected) {
  this.promise = promise;
  if (typeof onFulfilled === 'function') {
    this.onFulfilled = onFulfilled;
    this.callFulfilled = this.otherCallFulfilled;
  }
  if (typeof onRejected === 'function') {
    this.onRejected = onRejected;
    this.callRejected = this.otherCallRejected;
  }
}
QueueItem.prototype.callFulfilled = function (value) {
  handlers.resolve(this.promise, value);
};
QueueItem.prototype.otherCallFulfilled = function (value) {
  unwrap(this.promise, this.onFulfilled, value);
};
QueueItem.prototype.callRejected = function (value) {
  handlers.reject(this.promise, value);
};
QueueItem.prototype.otherCallRejected = function (value) {
  unwrap(this.promise, this.onRejected, value);
};

function unwrap(promise, func, value) {
  immediate(function () {
    var returnValue;
    try {
      returnValue = func(value);
    } catch (e) {
      return handlers.reject(promise, e);
    }
    if (returnValue === promise) {
      handlers.reject(promise, new TypeError('Cannot resolve promise with itself'));
    } else {
      handlers.resolve(promise, returnValue);
    }
  });
}

handlers.resolve = function (self, value) {
  var result = tryCatch(getThen, value);
  if (result.status === 'error') {
    return handlers.reject(self, result.value);
  }
  var thenable = result.value;

  if (thenable) {
    safelyResolveThenable(self, thenable);
  } else {
    self.state = FULFILLED;
    self.outcome = value;
    var i = -1;
    var len = self.queue.length;
    while (++i < len) {
      self.queue[i].callFulfilled(value);
    }
  }
  return self;
};
handlers.reject = function (self, error) {
  self.state = REJECTED;
  self.outcome = error;
  var i = -1;
  var len = self.queue.length;
  while (++i < len) {
    self.queue[i].callRejected(error);
  }
  return self;
};

function getThen(obj) {
  // Make sure we only access the accessor once as required by the spec
  var then = obj && obj.then;
  if (obj && (typeof obj === 'object' || typeof obj === 'function') && typeof then === 'function') {
    return function appyThen() {
      then.apply(obj, arguments);
    };
  }
}

function safelyResolveThenable(self, thenable) {
  // Either fulfill, reject or reject with error
  var called = false;
  function onError(value) {
    if (called) {
      return;
    }
    called = true;
    handlers.reject(self, value);
  }

  function onSuccess(value) {
    if (called) {
      return;
    }
    called = true;
    handlers.resolve(self, value);
  }

  function tryToUnwrap() {
    thenable(onSuccess, onError);
  }

  var result = tryCatch(tryToUnwrap);
  if (result.status === 'error') {
    onError(result.value);
  }
}

function tryCatch(func, value) {
  var out = {};
  try {
    out.value = func(value);
    out.status = 'success';
  } catch (e) {
    out.status = 'error';
    out.value = e;
  }
  return out;
}

Promise.resolve = resolve;
function resolve(value) {
  if (value instanceof this) {
    return value;
  }
  return handlers.resolve(new this(INTERNAL), value);
}

Promise.reject = reject;
function reject(reason) {
  var promise = new this(INTERNAL);
  return handlers.reject(promise, reason);
}

Promise.all = all;
function all(iterable) {
  var self = this;
  if (Object.prototype.toString.call(iterable) !== '[object Array]') {
    return this.reject(new TypeError('must be an array'));
  }

  var len = iterable.length;
  var called = false;
  if (!len) {
    return this.resolve([]);
  }

  var values = new Array(len);
  var resolved = 0;
  var i = -1;
  var promise = new this(INTERNAL);

  while (++i < len) {
    allResolver(iterable[i], i);
  }
  return promise;
  function allResolver(value, i) {
    self.resolve(value).then(resolveFromAll, function (error) {
      if (!called) {
        called = true;
        handlers.reject(promise, error);
      }
    });
    function resolveFromAll(outValue) {
      values[i] = outValue;
      if (++resolved === len && !called) {
        called = true;
        handlers.resolve(promise, values);
      }
    }
  }
}

Promise.race = race;
function race(iterable) {
  var self = this;
  if (Object.prototype.toString.call(iterable) !== '[object Array]') {
    return this.reject(new TypeError('must be an array'));
  }

  var len = iterable.length;
  var called = false;
  if (!len) {
    return this.resolve([]);
  }

  var i = -1;
  var promise = new this(INTERNAL);

  while (++i < len) {
    resolver(iterable[i]);
  }
  return promise;
  function resolver(value) {
    self.resolve(value).then(function (response) {
      if (!called) {
        called = true;
        handlers.resolve(promise, response);
      }
    }, function (error) {
      if (!called) {
        called = true;
        handlers.reject(promise, error);
      }
    });
  }
}

},{"1":1}],3:[function(_dereq_,module,exports){
(function (global){
'use strict';
if (typeof global.Promise !== 'function') {
  global.Promise = _dereq_(2);
}

}).call(this,typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
},{"2":2}],4:[function(_dereq_,module,exports){
'use strict';

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function getIDB() {
    /* global indexedDB,webkitIndexedDB,mozIndexedDB,OIndexedDB,msIndexedDB */
    try {
        if (typeof indexedDB !== 'undefined') {
            return indexedDB;
        }
        if (typeof webkitIndexedDB !== 'undefined') {
            return webkitIndexedDB;
        }
        if (typeof mozIndexedDB !== 'undefined') {
            return mozIndexedDB;
        }
        if (typeof OIndexedDB !== 'undefined') {
            return OIndexedDB;
        }
        if (typeof msIndexedDB !== 'undefined') {
            return msIndexedDB;
        }
    } catch (e) {
        return;
    }
}

var idb = getIDB();

function isIndexedDBValid() {
    try {
        // Initialize IndexedDB; fall back to vendor-prefixed versions
        // if needed.
        if (!idb) {
            return false;
        }
        // We mimic PouchDB here;
        //
        // We test for openDatabase because IE Mobile identifies itself
        // as Safari. Oh the lulz...
        var isSafari = typeof openDatabase !== 'undefined' && /(Safari|iPhone|iPad|iPod)/.test(navigator.userAgent) && !/Chrome/.test(navigator.userAgent) && !/BlackBerry/.test(navigator.platform);

        var hasFetch = typeof fetch === 'function' && fetch.toString().indexOf('[native code') !== -1;

        // Safari <10.1 does not meet our requirements for IDB support (#5572)
        // since Safari 10.1 shipped with fetch, we can use that to detect it
        return (!isSafari || hasFetch) && typeof indexedDB !== 'undefined' &&
        // some outdated implementations of IDB that appear on Samsung
        // and HTC Android devices <4.4 are missing IDBKeyRange
        // See: https://github.com/mozilla/localForage/issues/128
        // See: https://github.com/mozilla/localForage/issues/272
        typeof IDBKeyRange !== 'undefined';
    } catch (e) {
        return false;
    }
}

// Abstracts constructing a Blob object, so it also works in older
// browsers that don't support the native Blob constructor. (i.e.
// old QtWebKit versions, at least).
// Abstracts constructing a Blob object, so it also works in older
// browsers that don't support the native Blob constructor. (i.e.
// old QtWebKit versions, at least).
function createBlob(parts, properties) {
    /* global BlobBuilder,MSBlobBuilder,MozBlobBuilder,WebKitBlobBuilder */
    parts = parts || [];
    properties = properties || {};
    try {
        return new Blob(parts, properties);
    } catch (e) {
        if (e.name !== 'TypeError') {
            throw e;
        }
        var Builder = typeof BlobBuilder !== 'undefined' ? BlobBuilder : typeof MSBlobBuilder !== 'undefined' ? MSBlobBuilder : typeof MozBlobBuilder !== 'undefined' ? MozBlobBuilder : WebKitBlobBuilder;
        var builder = new Builder();
        for (var i = 0; i < parts.length; i += 1) {
            builder.append(parts[i]);
        }
        return builder.getBlob(properties.type);
    }
}

// This is CommonJS because lie is an external dependency, so Rollup
// can just ignore it.
if (typeof Promise === 'undefined') {
    // In the "nopromises" build this will just throw if you don't have
    // a global promise object, but it would throw anyway later.
    _dereq_(3);
}
var Promise$1 = Promise;

function executeCallback(promise, callback) {
    if (callback) {
        promise.then(function (result) {
            callback(null, result);
        }, function (error) {
            callback(error);
        });
    }
}

function executeTwoCallbacks(promise, callback, errorCallback) {
    if (typeof callback === 'function') {
        promise.then(callback);
    }

    if (typeof errorCallback === 'function') {
        promise["catch"](errorCallback);
    }
}

function normalizeKey(key) {
    // Cast the key to a string, as that's all we can set as a key.
    if (typeof key !== 'string') {
        console.warn(key + ' used as a key, but it is not a string.');
        key = String(key);
    }

    return key;
}

function getCallback() {
    if (arguments.length && typeof arguments[arguments.length - 1] === 'function') {
        return arguments[arguments.length - 1];
    }
}

// Some code originally from async_storage.js in
// [Gaia](https://github.com/mozilla-b2g/gaia).

var DETECT_BLOB_SUPPORT_STORE = 'local-forage-detect-blob-support';
var supportsBlobs = void 0;
var dbContexts = {};
var toString = Object.prototype.toString;

// Transaction Modes
var READ_ONLY = 'readonly';
var READ_WRITE = 'readwrite';

// Transform a binary string to an array buffer, because otherwise
// weird stuff happens when you try to work with the binary string directly.
// It is known.
// From http://stackoverflow.com/questions/14967647/ (continues on next line)
// encode-decode-image-with-base64-breaks-image (2013-04-21)
function _binStringToArrayBuffer(bin) {
    var length = bin.length;
    var buf = new ArrayBuffer(length);
    var arr = new Uint8Array(buf);
    for (var i = 0; i < length; i++) {
        arr[i] = bin.charCodeAt(i);
    }
    return buf;
}

//
// Blobs are not supported in all versions of IndexedDB, notably
// Chrome <37 and Android <5. In those versions, storing a blob will throw.
//
// Various other blob bugs exist in Chrome v37-42 (inclusive).
// Detecting them is expensive and confusing to users, and Chrome 37-42
// is at very low usage worldwide, so we do a hacky userAgent check instead.
//
// content-type bug: https://code.google.com/p/chromium/issues/detail?id=408120
// 404 bug: https://code.google.com/p/chromium/issues/detail?id=447916
// FileReader bug: https://code.google.com/p/chromium/issues/detail?id=447836
//
// Code borrowed from PouchDB. See:
// https://github.com/pouchdb/pouchdb/blob/master/packages/node_modules/pouchdb-adapter-idb/src/blobSupport.js
//
function _checkBlobSupportWithoutCaching(idb) {
    return new Promise$1(function (resolve) {
        var txn = idb.transaction(DETECT_BLOB_SUPPORT_STORE, READ_WRITE);
        var blob = createBlob(['']);
        txn.objectStore(DETECT_BLOB_SUPPORT_STORE).put(blob, 'key');

        txn.onabort = function (e) {
            // If the transaction aborts now its due to not being able to
            // write to the database, likely due to the disk being full
            e.preventDefault();
            e.stopPropagation();
            resolve(false);
        };

        txn.oncomplete = function () {
            var matchedChrome = navigator.userAgent.match(/Chrome\/(\d+)/);
            var matchedEdge = navigator.userAgent.match(/Edge\//);
            // MS Edge pretends to be Chrome 42:
            // https://msdn.microsoft.com/en-us/library/hh869301%28v=vs.85%29.aspx
            resolve(matchedEdge || !matchedChrome || parseInt(matchedChrome[1], 10) >= 43);
        };
    })["catch"](function () {
        return false; // error, so assume unsupported
    });
}

function _checkBlobSupport(idb) {
    if (typeof supportsBlobs === 'boolean') {
        return Promise$1.resolve(supportsBlobs);
    }
    return _checkBlobSupportWithoutCaching(idb).then(function (value) {
        supportsBlobs = value;
        return supportsBlobs;
    });
}

function _deferReadiness(dbInfo) {
    var dbContext = dbContexts[dbInfo.name];

    // Create a deferred object representing the current database operation.
    var deferredOperation = {};

    deferredOperation.promise = new Promise$1(function (resolve, reject) {
        deferredOperation.resolve = resolve;
        deferredOperation.reject = reject;
    });

    // Enqueue the deferred operation.
    dbContext.deferredOperations.push(deferredOperation);

    // Chain its promise to the database readiness.
    if (!dbContext.dbReady) {
        dbContext.dbReady = deferredOperation.promise;
    } else {
        dbContext.dbReady = dbContext.dbReady.then(function () {
            return deferredOperation.promise;
        });
    }
}

function _advanceReadiness(dbInfo) {
    var dbContext = dbContexts[dbInfo.name];

    // Dequeue a deferred operation.
    var deferredOperation = dbContext.deferredOperations.pop();

    // Resolve its promise (which is part of the database readiness
    // chain of promises).
    if (deferredOperation) {
        deferredOperation.resolve();
        return deferredOperation.promise;
    }
}

function _rejectReadiness(dbInfo, err) {
    var dbContext = dbContexts[dbInfo.name];

    // Dequeue a deferred operation.
    var deferredOperation = dbContext.deferredOperations.pop();

    // Reject its promise (which is part of the database readiness
    // chain of promises).
    if (deferredOperation) {
        deferredOperation.reject(err);
        return deferredOperation.promise;
    }
}

function _getConnection(dbInfo, upgradeNeeded) {
    return new Promise$1(function (resolve, reject) {
        dbContexts[dbInfo.name] = dbContexts[dbInfo.name] || createDbContext();

        if (dbInfo.db) {
            if (upgradeNeeded) {
                _deferReadiness(dbInfo);
                dbInfo.db.close();
            } else {
                return resolve(dbInfo.db);
            }
        }

        var dbArgs = [dbInfo.name];

        if (upgradeNeeded) {
            dbArgs.push(dbInfo.version);
        }

        var openreq = idb.open.apply(idb, dbArgs);

        if (upgradeNeeded) {
            openreq.onupgradeneeded = function (e) {
                var db = openreq.result;
                try {
                    db.createObjectStore(dbInfo.storeName);
                    if (e.oldVersion <= 1) {
                        // Added when support for blob shims was added
                        db.createObjectStore(DETECT_BLOB_SUPPORT_STORE);
                    }
                } catch (ex) {
                    if (ex.name === 'ConstraintError') {
                        console.warn('The database "' + dbInfo.name + '"' + ' has been upgraded from version ' + e.oldVersion + ' to version ' + e.newVersion + ', but the storage "' + dbInfo.storeName + '" already exists.');
                    } else {
                        throw ex;
                    }
                }
            };
        }

        openreq.onerror = function (e) {
            e.preventDefault();
            reject(openreq.error);
        };

        openreq.onsuccess = function () {
            resolve(openreq.result);
            _advanceReadiness(dbInfo);
        };
    });
}

function _getOriginalConnection(dbInfo) {
    return _getConnection(dbInfo, false);
}

function _getUpgradedConnection(dbInfo) {
    return _getConnection(dbInfo, true);
}

function _isUpgradeNeeded(dbInfo, defaultVersion) {
    if (!dbInfo.db) {
        return true;
    }

    var isNewStore = !dbInfo.db.objectStoreNames.contains(dbInfo.storeName);
    var isDowngrade = dbInfo.version < dbInfo.db.version;
    var isUpgrade = dbInfo.version > dbInfo.db.version;

    if (isDowngrade) {
        // If the version is not the default one
        // then warn for impossible downgrade.
        if (dbInfo.version !== defaultVersion) {
            console.warn('The database "' + dbInfo.name + '"' + " can't be downgraded from version " + dbInfo.db.version + ' to version ' + dbInfo.version + '.');
        }
        // Align the versions to prevent errors.
        dbInfo.version = dbInfo.db.version;
    }

    if (isUpgrade || isNewStore) {
        // If the store is new then increment the version (if needed).
        // This will trigger an "upgradeneeded" event which is required
        // for creating a store.
        if (isNewStore) {
            var incVersion = dbInfo.db.version + 1;
            if (incVersion > dbInfo.version) {
                dbInfo.version = incVersion;
            }
        }

        return true;
    }

    return false;
}

// encode a blob for indexeddb engines that don't support blobs
function _encodeBlob(blob) {
    return new Promise$1(function (resolve, reject) {
        var reader = new FileReader();
        reader.onerror = reject;
        reader.onloadend = function (e) {
            var base64 = btoa(e.target.result || '');
            resolve({
                __local_forage_encoded_blob: true,
                data: base64,
                type: blob.type
            });
        };
        reader.readAsBinaryString(blob);
    });
}

// decode an encoded blob
function _decodeBlob(encodedBlob) {
    var arrayBuff = _binStringToArrayBuffer(atob(encodedBlob.data));
    return createBlob([arrayBuff], { type: encodedBlob.type });
}

// is this one of our fancy encoded blobs?
function _isEncodedBlob(value) {
    return value && value.__local_forage_encoded_blob;
}

// Specialize the default `ready()` function by making it dependent
// on the current database operations. Thus, the driver will be actually
// ready when it's been initialized (default) *and* there are no pending
// operations on the database (initiated by some other instances).
function _fullyReady(callback) {
    var self = this;

    var promise = self._initReady().then(function () {
        var dbContext = dbContexts[self._dbInfo.name];

        if (dbContext && dbContext.dbReady) {
            return dbContext.dbReady;
        }
    });

    executeTwoCallbacks(promise, callback, callback);
    return promise;
}

// Try to establish a new db connection to replace the
// current one which is broken (i.e. experiencing
// InvalidStateError while creating a transaction).
function _tryReconnect(dbInfo) {
    _deferReadiness(dbInfo);

    var dbContext = dbContexts[dbInfo.name];
    var forages = dbContext.forages;

    for (var i = 0; i < forages.length; i++) {
        var forage = forages[i];
        if (forage._dbInfo.db) {
            forage._dbInfo.db.close();
            forage._dbInfo.db = null;
        }
    }
    dbInfo.db = null;

    return _getOriginalConnection(dbInfo).then(function (db) {
        dbInfo.db = db;
        if (_isUpgradeNeeded(dbInfo)) {
            // Reopen the database for upgrading.
            return _getUpgradedConnection(dbInfo);
        }
        return db;
    }).then(function (db) {
        // store the latest db reference
        // in case the db was upgraded
        dbInfo.db = dbContext.db = db;
        for (var i = 0; i < forages.length; i++) {
            forages[i]._dbInfo.db = db;
        }
    })["catch"](function (err) {
        _rejectReadiness(dbInfo, err);
        throw err;
    });
}

// FF doesn't like Promises (micro-tasks) and IDDB store operations,
// so we have to do it with callbacks
function createTransaction(dbInfo, mode, callback, retries) {
    if (retries === undefined) {
        retries = 1;
    }

    try {
        var tx = dbInfo.db.transaction(dbInfo.storeName, mode);
        callback(null, tx);
    } catch (err) {
        if (retries > 0 && (!dbInfo.db || err.name === 'InvalidStateError' || err.name === 'NotFoundError')) {
            return Promise$1.resolve().then(function () {
                if (!dbInfo.db || err.name === 'NotFoundError' && !dbInfo.db.objectStoreNames.contains(dbInfo.storeName) && dbInfo.version <= dbInfo.db.version) {
                    // increase the db version, to create the new ObjectStore
                    if (dbInfo.db) {
                        dbInfo.version = dbInfo.db.version + 1;
                    }
                    // Reopen the database for upgrading.
                    return _getUpgradedConnection(dbInfo);
                }
            }).then(function () {
                return _tryReconnect(dbInfo).then(function () {
                    createTransaction(dbInfo, mode, callback, retries - 1);
                });
            })["catch"](callback);
        }

        callback(err);
    }
}

function createDbContext() {
    return {
        // Running localForages sharing a database.
        forages: [],
        // Shared database.
        db: null,
        // Database readiness (promise).
        dbReady: null,
        // Deferred operations on the database.
        deferredOperations: []
    };
}

// Open the IndexedDB database (automatically creates one if one didn't
// previously exist), using any options set in the config.
function _initStorage(options) {
    var self = this;
    var dbInfo = {
        db: null
    };

    if (options) {
        for (var i in options) {
            dbInfo[i] = options[i];
        }
    }

    // Get the current context of the database;
    var dbContext = dbContexts[dbInfo.name];

    // ...or create a new context.
    if (!dbContext) {
        dbContext = createDbContext();
        // Register the new context in the global container.
        dbContexts[dbInfo.name] = dbContext;
    }

    // Register itself as a running localForage in the current context.
    dbContext.forages.push(self);

    // Replace the default `ready()` function with the specialized one.
    if (!self._initReady) {
        self._initReady = self.ready;
        self.ready = _fullyReady;
    }

    // Create an array of initialization states of the related localForages.
    var initPromises = [];

    function ignoreErrors() {
        // Don't handle errors here,
        // just makes sure related localForages aren't pending.
        return Promise$1.resolve();
    }

    for (var j = 0; j < dbContext.forages.length; j++) {
        var forage = dbContext.forages[j];
        if (forage !== self) {
            // Don't wait for itself...
            initPromises.push(forage._initReady()["catch"](ignoreErrors));
        }
    }

    // Take a snapshot of the related localForages.
    var forages = dbContext.forages.slice(0);

    // Initialize the connection process only when
    // all the related localForages aren't pending.
    return Promise$1.all(initPromises).then(function () {
        dbInfo.db = dbContext.db;
        // Get the connection or open a new one without upgrade.
        return _getOriginalConnection(dbInfo);
    }).then(function (db) {
        dbInfo.db = db;
        if (_isUpgradeNeeded(dbInfo, self._defaultConfig.version)) {
            // Reopen the database for upgrading.
            return _getUpgradedConnection(dbInfo);
        }
        return db;
    }).then(function (db) {
        dbInfo.db = dbContext.db = db;
        self._dbInfo = dbInfo;
        // Share the final connection amongst related localForages.
        for (var k = 0; k < forages.length; k++) {
            var forage = forages[k];
            if (forage !== self) {
                // Self is already up-to-date.
                forage._dbInfo.db = dbInfo.db;
                forage._dbInfo.version = dbInfo.version;
            }
        }
    });
}

function getItem(key, callback) {
    var self = this;

    key = normalizeKey(key);

    var promise = new Promise$1(function (resolve, reject) {
        self.ready().then(function () {
            createTransaction(self._dbInfo, READ_ONLY, function (err, transaction) {
                if (err) {
                    return reject(err);
                }

                try {
                    var store = transaction.objectStore(self._dbInfo.storeName);
                    var req = store.get(key);

                    req.onsuccess = function () {
                        var value = req.result;
                        if (value === undefined) {
                            value = null;
                        }
                        if (_isEncodedBlob(value)) {
                            value = _decodeBlob(value);
                        }
                        resolve(value);
                    };

                    req.onerror = function () {
                        reject(req.error);
                    };
                } catch (e) {
                    reject(e);
                }
            });
        })["catch"](reject);
    });

    executeCallback(promise, callback);
    return promise;
}

// Iterate over all items stored in database.
function iterate(iterator, callback) {
    var self = this;

    var promise = new Promise$1(function (resolve, reject) {
        self.ready().then(function () {
            createTransaction(self._dbInfo, READ_ONLY, function (err, transaction) {
                if (err) {
                    return reject(err);
                }

                try {
                    var store = transaction.objectStore(self._dbInfo.storeName);
                    var req = store.openCursor();
                    var iterationNumber = 1;

                    req.onsuccess = function () {
                        var cursor = req.result;

                        if (cursor) {
                            var value = cursor.value;
                            if (_isEncodedBlob(value)) {
                                value = _decodeBlob(value);
                            }
                            var result = iterator(value, cursor.key, iterationNumber++);

                            // when the iterator callback retuns any
                            // (non-`undefined`) value, then we stop
                            // the iteration immediately
                            if (result !== void 0) {
                                resolve(result);
                            } else {
                                cursor["continue"]();
                            }
                        } else {
                            resolve();
                        }
                    };

                    req.onerror = function () {
                        reject(req.error);
                    };
                } catch (e) {
                    reject(e);
                }
            });
        })["catch"](reject);
    });

    executeCallback(promise, callback);

    return promise;
}

function setItem(key, value, callback) {
    var self = this;

    key = normalizeKey(key);

    var promise = new Promise$1(function (resolve, reject) {
        var dbInfo;
        self.ready().then(function () {
            dbInfo = self._dbInfo;
            if (toString.call(value) === '[object Blob]') {
                return _checkBlobSupport(dbInfo.db).then(function (blobSupport) {
                    if (blobSupport) {
                        return value;
                    }
                    return _encodeBlob(value);
                });
            }
            return value;
        }).then(function (value) {
            createTransaction(self._dbInfo, READ_WRITE, function (err, transaction) {
                if (err) {
                    return reject(err);
                }

                try {
                    var store = transaction.objectStore(self._dbInfo.storeName);

                    // The reason we don't _save_ null is because IE 10 does
                    // not support saving the `null` type in IndexedDB. How
                    // ironic, given the bug below!
                    // See: https://github.com/mozilla/localForage/issues/161
                    if (value === null) {
                        value = undefined;
                    }

                    var req = store.put(value, key);

                    transaction.oncomplete = function () {
                        // Cast to undefined so the value passed to
                        // callback/promise is the same as what one would get out
                        // of `getItem()` later. This leads to some weirdness
                        // (setItem('foo', undefined) will return `null`), but
                        // it's not my fault localStorage is our baseline and that
                        // it's weird.
                        if (value === undefined) {
                            value = null;
                        }

                        resolve(value);
                    };
                    transaction.onabort = transaction.onerror = function () {
                        var err = req.error ? req.error : req.transaction.error;
                        reject(err);
                    };
                } catch (e) {
                    reject(e);
                }
            });
        })["catch"](reject);
    });

    executeCallback(promise, callback);
    return promise;
}

function removeItem(key, callback) {
    var self = this;

    key = normalizeKey(key);

    var promise = new Promise$1(function (resolve, reject) {
        self.ready().then(function () {
            createTransaction(self._dbInfo, READ_WRITE, function (err, transaction) {
                if (err) {
                    return reject(err);
                }

                try {
                    var store = transaction.objectStore(self._dbInfo.storeName);
                    // We use a Grunt task to make this safe for IE and some
                    // versions of Android (including those used by Cordova).
                    // Normally IE won't like `.delete()` and will insist on
                    // using `['delete']()`, but we have a build step that
                    // fixes this for us now.
                    var req = store["delete"](key);
                    transaction.oncomplete = function () {
                        resolve();
                    };

                    transaction.onerror = function () {
                        reject(req.error);
                    };

                    // The request will be also be aborted if we've exceeded our storage
                    // space.
                    transaction.onabort = function () {
                        var err = req.error ? req.error : req.transaction.error;
                        reject(err);
                    };
                } catch (e) {
                    reject(e);
                }
            });
        })["catch"](reject);
    });

    executeCallback(promise, callback);
    return promise;
}

function clear(callback) {
    var self = this;

    var promise = new Promise$1(function (resolve, reject) {
        self.ready().then(function () {
            createTransaction(self._dbInfo, READ_WRITE, function (err, transaction) {
                if (err) {
                    return reject(err);
                }

                try {
                    var store = transaction.objectStore(self._dbInfo.storeName);
                    var req = store.clear();

                    transaction.oncomplete = function () {
                        resolve();
                    };

                    transaction.onabort = transaction.onerror = function () {
                        var err = req.error ? req.error : req.transaction.error;
                        reject(err);
                    };
                } catch (e) {
                    reject(e);
                }
            });
        })["catch"](reject);
    });

    executeCallback(promise, callback);
    return promise;
}

function length(callback) {
    var self = this;

    var promise = new Promise$1(function (resolve, reject) {
        self.ready().then(function () {
            createTransaction(self._dbInfo, READ_ONLY, function (err, transaction) {
                if (err) {
                    return reject(err);
                }

                try {
                    var store = transaction.objectStore(self._dbInfo.storeName);
                    var req = store.count();

                    req.onsuccess = function () {
                        resolve(req.result);
                    };

                    req.onerror = function () {
                        reject(req.error);
                    };
                } catch (e) {
                    reject(e);
                }
            });
        })["catch"](reject);
    });

    executeCallback(promise, callback);
    return promise;
}

function key(n, callback) {
    var self = this;

    var promise = new Promise$1(function (resolve, reject) {
        if (n < 0) {
            resolve(null);

            return;
        }

        self.ready().then(function () {
            createTransaction(self._dbInfo, READ_ONLY, function (err, transaction) {
                if (err) {
                    return reject(err);
                }

                try {
                    var store = transaction.objectStore(self._dbInfo.storeName);
                    var advanced = false;
                    var req = store.openCursor();

                    req.onsuccess = function () {
                        var cursor = req.result;
                        if (!cursor) {
                            // this means there weren't enough keys
                            resolve(null);

                            return;
                        }

                        if (n === 0) {
                            // We have the first key, return it if that's what they
                            // wanted.
                            resolve(cursor.key);
                        } else {
                            if (!advanced) {
                                // Otherwise, ask the cursor to skip ahead n
                                // records.
                                advanced = true;
                                cursor.advance(n);
                            } else {
                                // When we get here, we've got the nth key.
                                resolve(cursor.key);
                            }
                        }
                    };

                    req.onerror = function () {
                        reject(req.error);
                    };
                } catch (e) {
                    reject(e);
                }
            });
        })["catch"](reject);
    });

    executeCallback(promise, callback);
    return promise;
}

function keys(callback) {
    var self = this;

    var promise = new Promise$1(function (resolve, reject) {
        self.ready().then(function () {
            createTransaction(self._dbInfo, READ_ONLY, function (err, transaction) {
                if (err) {
                    return reject(err);
                }

                try {
                    var store = transaction.objectStore(self._dbInfo.storeName);
                    var req = store.openCursor();
                    var keys = [];

                    req.onsuccess = function () {
                        var cursor = req.result;

                        if (!cursor) {
                            resolve(keys);
                            return;
                        }

                        keys.push(cursor.key);
                        cursor["continue"]();
                    };

                    req.onerror = function () {
                        reject(req.error);
                    };
                } catch (e) {
                    reject(e);
                }
            });
        })["catch"](reject);
    });

    executeCallback(promise, callback);
    return promise;
}

function dropInstance(options, callback) {
    callback = getCallback.apply(this, arguments);

    var currentConfig = this.config();
    options = typeof options !== 'function' && options || {};
    if (!options.name) {
        options.name = options.name || currentConfig.name;
        options.storeName = options.storeName || currentConfig.storeName;
    }

    var self = this;
    var promise;
    if (!options.name) {
        promise = Promise$1.reject('Invalid arguments');
    } else {
        var isCurrentDb = options.name === currentConfig.name && self._dbInfo.db;

        var dbPromise = isCurrentDb ? Promise$1.resolve(self._dbInfo.db) : _getOriginalConnection(options).then(function (db) {
            var dbContext = dbContexts[options.name];
            var forages = dbContext.forages;
            dbContext.db = db;
            for (var i = 0; i < forages.length; i++) {
                forages[i]._dbInfo.db = db;
            }
            return db;
        });

        if (!options.storeName) {
            promise = dbPromise.then(function (db) {
                _deferReadiness(options);

                var dbContext = dbContexts[options.name];
                var forages = dbContext.forages;

                db.close();
                for (var i = 0; i < forages.length; i++) {
                    var forage = forages[i];
                    forage._dbInfo.db = null;
                }

                var dropDBPromise = new Promise$1(function (resolve, reject) {
                    var req = idb.deleteDatabase(options.name);

                    req.onerror = req.onblocked = function (err) {
                        var db = req.result;
                        if (db) {
                            db.close();
                        }
                        reject(err);
                    };

                    req.onsuccess = function () {
                        var db = req.result;
                        if (db) {
                            db.close();
                        }
                        resolve(db);
                    };
                });

                return dropDBPromise.then(function (db) {
                    dbContext.db = db;
                    for (var i = 0; i < forages.length; i++) {
                        var _forage = forages[i];
                        _advanceReadiness(_forage._dbInfo);
                    }
                })["catch"](function (err) {
                    (_rejectReadiness(options, err) || Promise$1.resolve())["catch"](function () {});
                    throw err;
                });
            });
        } else {
            promise = dbPromise.then(function (db) {
                if (!db.objectStoreNames.contains(options.storeName)) {
                    return;
                }

                var newVersion = db.version + 1;

                _deferReadiness(options);

                var dbContext = dbContexts[options.name];
                var forages = dbContext.forages;

                db.close();
                for (var i = 0; i < forages.length; i++) {
                    var forage = forages[i];
                    forage._dbInfo.db = null;
                    forage._dbInfo.version = newVersion;
                }

                var dropObjectPromise = new Promise$1(function (resolve, reject) {
                    var req = idb.open(options.name, newVersion);

                    req.onerror = function (err) {
                        var db = req.result;
                        db.close();
                        reject(err);
                    };

                    req.onupgradeneeded = function () {
                        var db = req.result;
                        db.deleteObjectStore(options.storeName);
                    };

                    req.onsuccess = function () {
                        var db = req.result;
                        db.close();
                        resolve(db);
                    };
                });

                return dropObjectPromise.then(function (db) {
                    dbContext.db = db;
                    for (var j = 0; j < forages.length; j++) {
                        var _forage2 = forages[j];
                        _forage2._dbInfo.db = db;
                        _advanceReadiness(_forage2._dbInfo);
                    }
                })["catch"](function (err) {
                    (_rejectReadiness(options, err) || Promise$1.resolve())["catch"](function () {});
                    throw err;
                });
            });
        }
    }

    executeCallback(promise, callback);
    return promise;
}

var asyncStorage = {
    _driver: 'asyncStorage',
    _initStorage: _initStorage,
    _support: isIndexedDBValid(),
    iterate: iterate,
    getItem: getItem,
    setItem: setItem,
    removeItem: removeItem,
    clear: clear,
    length: length,
    key: key,
    keys: keys,
    dropInstance: dropInstance
};

function isWebSQLValid() {
    return typeof openDatabase === 'function';
}

// Sadly, the best way to save binary data in WebSQL/localStorage is serializing
// it to Base64, so this is how we store it to prevent very strange errors with less
// verbose ways of binary <-> string data storage.
var BASE_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';

var BLOB_TYPE_PREFIX = '~~local_forage_type~';
var BLOB_TYPE_PREFIX_REGEX = /^~~local_forage_type~([^~]+)~/;

var SERIALIZED_MARKER = '__lfsc__:';
var SERIALIZED_MARKER_LENGTH = SERIALIZED_MARKER.length;

// OMG the serializations!
var TYPE_ARRAYBUFFER = 'arbf';
var TYPE_BLOB = 'blob';
var TYPE_INT8ARRAY = 'si08';
var TYPE_UINT8ARRAY = 'ui08';
var TYPE_UINT8CLAMPEDARRAY = 'uic8';
var TYPE_INT16ARRAY = 'si16';
var TYPE_INT32ARRAY = 'si32';
var TYPE_UINT16ARRAY = 'ur16';
var TYPE_UINT32ARRAY = 'ui32';
var TYPE_FLOAT32ARRAY = 'fl32';
var TYPE_FLOAT64ARRAY = 'fl64';
var TYPE_SERIALIZED_MARKER_LENGTH = SERIALIZED_MARKER_LENGTH + TYPE_ARRAYBUFFER.length;

var toString$1 = Object.prototype.toString;

function stringToBuffer(serializedString) {
    // Fill the string into a ArrayBuffer.
    var bufferLength = serializedString.length * 0.75;
    var len = serializedString.length;
    var i;
    var p = 0;
    var encoded1, encoded2, encoded3, encoded4;

    if (serializedString[serializedString.length - 1] === '=') {
        bufferLength--;
        if (serializedString[serializedString.length - 2] === '=') {
            bufferLength--;
        }
    }

    var buffer = new ArrayBuffer(bufferLength);
    var bytes = new Uint8Array(buffer);

    for (i = 0; i < len; i += 4) {
        encoded1 = BASE_CHARS.indexOf(serializedString[i]);
        encoded2 = BASE_CHARS.indexOf(serializedString[i + 1]);
        encoded3 = BASE_CHARS.indexOf(serializedString[i + 2]);
        encoded4 = BASE_CHARS.indexOf(serializedString[i + 3]);

        /*jslint bitwise: true */
        bytes[p++] = encoded1 << 2 | encoded2 >> 4;
        bytes[p++] = (encoded2 & 15) << 4 | encoded3 >> 2;
        bytes[p++] = (encoded3 & 3) << 6 | encoded4 & 63;
    }
    return buffer;
}

// Converts a buffer to a string to store, serialized, in the backend
// storage library.
function bufferToString(buffer) {
    // base64-arraybuffer
    var bytes = new Uint8Array(buffer);
    var base64String = '';
    var i;

    for (i = 0; i < bytes.length; i += 3) {
        /*jslint bitwise: true */
        base64String += BASE_CHARS[bytes[i] >> 2];
        base64String += BASE_CHARS[(bytes[i] & 3) << 4 | bytes[i + 1] >> 4];
        base64String += BASE_CHARS[(bytes[i + 1] & 15) << 2 | bytes[i + 2] >> 6];
        base64String += BASE_CHARS[bytes[i + 2] & 63];
    }

    if (bytes.length % 3 === 2) {
        base64String = base64String.substring(0, base64String.length - 1) + '=';
    } else if (bytes.length % 3 === 1) {
        base64String = base64String.substring(0, base64String.length - 2) + '==';
    }

    return base64String;
}

// Serialize a value, afterwards executing a callback (which usually
// instructs the `setItem()` callback/promise to be executed). This is how
// we store binary data with localStorage.
function serialize(value, callback) {
    var valueType = '';
    if (value) {
        valueType = toString$1.call(value);
    }

    // Cannot use `value instanceof ArrayBuffer` or such here, as these
    // checks fail when running the tests using casper.js...
    //
    // TODO: See why those tests fail and use a better solution.
    if (value && (valueType === '[object ArrayBuffer]' || value.buffer && toString$1.call(value.buffer) === '[object ArrayBuffer]')) {
        // Convert binary arrays to a string and prefix the string with
        // a special marker.
        var buffer;
        var marker = SERIALIZED_MARKER;

        if (value instanceof ArrayBuffer) {
            buffer = value;
            marker += TYPE_ARRAYBUFFER;
        } else {
            buffer = value.buffer;

            if (valueType === '[object Int8Array]') {
                marker += TYPE_INT8ARRAY;
            } else if (valueType === '[object Uint8Array]') {
                marker += TYPE_UINT8ARRAY;
            } else if (valueType === '[object Uint8ClampedArray]') {
                marker += TYPE_UINT8CLAMPEDARRAY;
            } else if (valueType === '[object Int16Array]') {
                marker += TYPE_INT16ARRAY;
            } else if (valueType === '[object Uint16Array]') {
                marker += TYPE_UINT16ARRAY;
            } else if (valueType === '[object Int32Array]') {
                marker += TYPE_INT32ARRAY;
            } else if (valueType === '[object Uint32Array]') {
                marker += TYPE_UINT32ARRAY;
            } else if (valueType === '[object Float32Array]') {
                marker += TYPE_FLOAT32ARRAY;
            } else if (valueType === '[object Float64Array]') {
                marker += TYPE_FLOAT64ARRAY;
            } else {
                callback(new Error('Failed to get type for BinaryArray'));
            }
        }

        callback(marker + bufferToString(buffer));
    } else if (valueType === '[object Blob]') {
        // Conver the blob to a binaryArray and then to a string.
        var fileReader = new FileReader();

        fileReader.onload = function () {
            // Backwards-compatible prefix for the blob type.
            var str = BLOB_TYPE_PREFIX + value.type + '~' + bufferToString(this.result);

            callback(SERIALIZED_MARKER + TYPE_BLOB + str);
        };

        fileReader.readAsArrayBuffer(value);
    } else {
        try {
            callback(JSON.stringify(value));
        } catch (e) {
            console.error("Couldn't convert value into a JSON string: ", value);

            callback(null, e);
        }
    }
}

// Deserialize data we've inserted into a value column/field. We place
// special markers into our strings to mark them as encoded; this isn't
// as nice as a meta field, but it's the only sane thing we can do whilst
// keeping localStorage support intact.
//
// Oftentimes this will just deserialize JSON content, but if we have a
// special marker (SERIALIZED_MARKER, defined above), we will extract
// some kind of arraybuffer/binary data/typed array out of the string.
function deserialize(value) {
    // If we haven't marked this string as being specially serialized (i.e.
    // something other than serialized JSON), we can just return it and be
    // done with it.
    if (value.substring(0, SERIALIZED_MARKER_LENGTH) !== SERIALIZED_MARKER) {
        return JSON.parse(value);
    }

    // The following code deals with deserializing some kind of Blob or
    // TypedArray. First we separate out the type of data we're dealing
    // with from the data itself.
    var serializedString = value.substring(TYPE_SERIALIZED_MARKER_LENGTH);
    var type = value.substring(SERIALIZED_MARKER_LENGTH, TYPE_SERIALIZED_MARKER_LENGTH);

    var blobType;
    // Backwards-compatible blob type serialization strategy.
    // DBs created with older versions of localForage will simply not have the blob type.
    if (type === TYPE_BLOB && BLOB_TYPE_PREFIX_REGEX.test(serializedString)) {
        var matcher = serializedString.match(BLOB_TYPE_PREFIX_REGEX);
        blobType = matcher[1];
        serializedString = serializedString.substring(matcher[0].length);
    }
    var buffer = stringToBuffer(serializedString);

    // Return the right type based on the code/type set during
    // serialization.
    switch (type) {
        case TYPE_ARRAYBUFFER:
            return buffer;
        case TYPE_BLOB:
            return createBlob([buffer], { type: blobType });
        case TYPE_INT8ARRAY:
            return new Int8Array(buffer);
        case TYPE_UINT8ARRAY:
            return new Uint8Array(buffer);
        case TYPE_UINT8CLAMPEDARRAY:
            return new Uint8ClampedArray(buffer);
        case TYPE_INT16ARRAY:
            return new Int16Array(buffer);
        case TYPE_UINT16ARRAY:
            return new Uint16Array(buffer);
        case TYPE_INT32ARRAY:
            return new Int32Array(buffer);
        case TYPE_UINT32ARRAY:
            return new Uint32Array(buffer);
        case TYPE_FLOAT32ARRAY:
            return new Float32Array(buffer);
        case TYPE_FLOAT64ARRAY:
            return new Float64Array(buffer);
        default:
            throw new Error('Unkown type: ' + type);
    }
}

var localforageSerializer = {
    serialize: serialize,
    deserialize: deserialize,
    stringToBuffer: stringToBuffer,
    bufferToString: bufferToString
};

/*
 * Includes code from:
 *
 * base64-arraybuffer
 * https://github.com/niklasvh/base64-arraybuffer
 *
 * Copyright (c) 2012 Niklas von Hertzen
 * Licensed under the MIT license.
 */

function createDbTable(t, dbInfo, callback, errorCallback) {
    t.executeSql('CREATE TABLE IF NOT EXISTS ' + dbInfo.storeName + ' ' + '(id INTEGER PRIMARY KEY, key unique, value)', [], callback, errorCallback);
}

// Open the WebSQL database (automatically creates one if one didn't
// previously exist), using any options set in the config.
function _initStorage$1(options) {
    var self = this;
    var dbInfo = {
        db: null
    };

    if (options) {
        for (var i in options) {
            dbInfo[i] = typeof options[i] !== 'string' ? options[i].toString() : options[i];
        }
    }

    var dbInfoPromise = new Promise$1(function (resolve, reject) {
        // Open the database; the openDatabase API will automatically
        // create it for us if it doesn't exist.
        try {
            dbInfo.db = openDatabase(dbInfo.name, String(dbInfo.version), dbInfo.description, dbInfo.size);
        } catch (e) {
            return reject(e);
        }

        // Create our key/value table if it doesn't exist.
        dbInfo.db.transaction(function (t) {
            createDbTable(t, dbInfo, function () {
                self._dbInfo = dbInfo;
                resolve();
            }, function (t, error) {
                reject(error);
            });
        }, reject);
    });

    dbInfo.serializer = localforageSerializer;
    return dbInfoPromise;
}

function tryExecuteSql(t, dbInfo, sqlStatement, args, callback, errorCallback) {
    t.executeSql(sqlStatement, args, callback, function (t, error) {
        if (error.code === error.SYNTAX_ERR) {
            t.executeSql('SELECT name FROM sqlite_master ' + "WHERE type='table' AND name = ?", [dbInfo.storeName], function (t, results) {
                if (!results.rows.length) {
                    // if the table is missing (was deleted)
                    // re-create it table and retry
                    createDbTable(t, dbInfo, function () {
                        t.executeSql(sqlStatement, args, callback, errorCallback);
                    }, errorCallback);
                } else {
                    errorCallback(t, error);
                }
            }, errorCallback);
        } else {
            errorCallback(t, error);
        }
    }, errorCallback);
}

function getItem$1(key, callback) {
    var self = this;

    key = normalizeKey(key);

    var promise = new Promise$1(function (resolve, reject) {
        self.ready().then(function () {
            var dbInfo = self._dbInfo;
            dbInfo.db.transaction(function (t) {
                tryExecuteSql(t, dbInfo, 'SELECT * FROM ' + dbInfo.storeName + ' WHERE key = ? LIMIT 1', [key], function (t, results) {
                    var result = results.rows.length ? results.rows.item(0).value : null;

                    // Check to see if this is serialized content we need to
                    // unpack.
                    if (result) {
                        result = dbInfo.serializer.deserialize(result);
                    }

                    resolve(result);
                }, function (t, error) {
                    reject(error);
                });
            });
        })["catch"](reject);
    });

    executeCallback(promise, callback);
    return promise;
}

function iterate$1(iterator, callback) {
    var self = this;

    var promise = new Promise$1(function (resolve, reject) {
        self.ready().then(function () {
            var dbInfo = self._dbInfo;

            dbInfo.db.transaction(function (t) {
                tryExecuteSql(t, dbInfo, 'SELECT * FROM ' + dbInfo.storeName, [], function (t, results) {
                    var rows = results.rows;
                    var length = rows.length;

                    for (var i = 0; i < length; i++) {
                        var item = rows.item(i);
                        var result = item.value;

                        // Check to see if this is serialized content
                        // we need to unpack.
                        if (result) {
                            result = dbInfo.serializer.deserialize(result);
                        }

                        result = iterator(result, item.key, i + 1);

                        // void(0) prevents problems with redefinition
                        // of `undefined`.
                        if (result !== void 0) {
                            resolve(result);
                            return;
                        }
                    }

                    resolve();
                }, function (t, error) {
                    reject(error);
                });
            });
        })["catch"](reject);
    });

    executeCallback(promise, callback);
    return promise;
}

function _setItem(key, value, callback, retriesLeft) {
    var self = this;

    key = normalizeKey(key);

    var promise = new Promise$1(function (resolve, reject) {
        self.ready().then(function () {
            // The localStorage API doesn't return undefined values in an
            // "expected" way, so undefined is always cast to null in all
            // drivers. See: https://github.com/mozilla/localForage/pull/42
            if (value === undefined) {
                value = null;
            }

            // Save the original value to pass to the callback.
            var originalValue = value;

            var dbInfo = self._dbInfo;
            dbInfo.serializer.serialize(value, function (value, error) {
                if (error) {
                    reject(error);
                } else {
                    dbInfo.db.transaction(function (t) {
                        tryExecuteSql(t, dbInfo, 'INSERT OR REPLACE INTO ' + dbInfo.storeName + ' ' + '(key, value) VALUES (?, ?)', [key, value], function () {
                            resolve(originalValue);
                        }, function (t, error) {
                            reject(error);
                        });
                    }, function (sqlError) {
                        // The transaction failed; check
                        // to see if it's a quota error.
                        if (sqlError.code === sqlError.QUOTA_ERR) {
                            // We reject the callback outright for now, but
                            // it's worth trying to re-run the transaction.
                            // Even if the user accepts the prompt to use
                            // more storage on Safari, this error will
                            // be called.
                            //
                            // Try to re-run the transaction.
                            if (retriesLeft > 0) {
                                resolve(_setItem.apply(self, [key, originalValue, callback, retriesLeft - 1]));
                                return;
                            }
                            reject(sqlError);
                        }
                    });
                }
            });
        })["catch"](reject);
    });

    executeCallback(promise, callback);
    return promise;
}

function setItem$1(key, value, callback) {
    return _setItem.apply(this, [key, value, callback, 1]);
}

function removeItem$1(key, callback) {
    var self = this;

    key = normalizeKey(key);

    var promise = new Promise$1(function (resolve, reject) {
        self.ready().then(function () {
            var dbInfo = self._dbInfo;
            dbInfo.db.transaction(function (t) {
                tryExecuteSql(t, dbInfo, 'DELETE FROM ' + dbInfo.storeName + ' WHERE key = ?', [key], function () {
                    resolve();
                }, function (t, error) {
                    reject(error);
                });
            });
        })["catch"](reject);
    });

    executeCallback(promise, callback);
    return promise;
}

// Deletes every item in the table.
// TODO: Find out if this resets the AUTO_INCREMENT number.
function clear$1(callback) {
    var self = this;

    var promise = new Promise$1(function (resolve, reject) {
        self.ready().then(function () {
            var dbInfo = self._dbInfo;
            dbInfo.db.transaction(function (t) {
                tryExecuteSql(t, dbInfo, 'DELETE FROM ' + dbInfo.storeName, [], function () {
                    resolve();
                }, function (t, error) {
                    reject(error);
                });
            });
        })["catch"](reject);
    });

    executeCallback(promise, callback);
    return promise;
}

// Does a simple `COUNT(key)` to get the number of items stored in
// localForage.
function length$1(callback) {
    var self = this;

    var promise = new Promise$1(function (resolve, reject) {
        self.ready().then(function () {
            var dbInfo = self._dbInfo;
            dbInfo.db.transaction(function (t) {
                // Ahhh, SQL makes this one soooooo easy.
                tryExecuteSql(t, dbInfo, 'SELECT COUNT(key) as c FROM ' + dbInfo.storeName, [], function (t, results) {
                    var result = results.rows.item(0).c;
                    resolve(result);
                }, function (t, error) {
                    reject(error);
                });
            });
        })["catch"](reject);
    });

    executeCallback(promise, callback);
    return promise;
}

// Return the key located at key index X; essentially gets the key from a
// `WHERE id = ?`. This is the most efficient way I can think to implement
// this rarely-used (in my experience) part of the API, but it can seem
// inconsistent, because we do `INSERT OR REPLACE INTO` on `setItem()`, so
// the ID of each key will change every time it's updated. Perhaps a stored
// procedure for the `setItem()` SQL would solve this problem?
// TODO: Don't change ID on `setItem()`.
function key$1(n, callback) {
    var self = this;

    var promise = new Promise$1(function (resolve, reject) {
        self.ready().then(function () {
            var dbInfo = self._dbInfo;
            dbInfo.db.transaction(function (t) {
                tryExecuteSql(t, dbInfo, 'SELECT key FROM ' + dbInfo.storeName + ' WHERE id = ? LIMIT 1', [n + 1], function (t, results) {
                    var result = results.rows.length ? results.rows.item(0).key : null;
                    resolve(result);
                }, function (t, error) {
                    reject(error);
                });
            });
        })["catch"](reject);
    });

    executeCallback(promise, callback);
    return promise;
}

function keys$1(callback) {
    var self = this;

    var promise = new Promise$1(function (resolve, reject) {
        self.ready().then(function () {
            var dbInfo = self._dbInfo;
            dbInfo.db.transaction(function (t) {
                tryExecuteSql(t, dbInfo, 'SELECT key FROM ' + dbInfo.storeName, [], function (t, results) {
                    var keys = [];

                    for (var i = 0; i < results.rows.length; i++) {
                        keys.push(results.rows.item(i).key);
                    }

                    resolve(keys);
                }, function (t, error) {
                    reject(error);
                });
            });
        })["catch"](reject);
    });

    executeCallback(promise, callback);
    return promise;
}

// https://www.w3.org/TR/webdatabase/#databases
// > There is no way to enumerate or delete the databases available for an origin from this API.
function getAllStoreNames(db) {
    return new Promise$1(function (resolve, reject) {
        db.transaction(function (t) {
            t.executeSql('SELECT name FROM sqlite_master ' + "WHERE type='table' AND name <> '__WebKitDatabaseInfoTable__'", [], function (t, results) {
                var storeNames = [];

                for (var i = 0; i < results.rows.length; i++) {
                    storeNames.push(results.rows.item(i).name);
                }

                resolve({
                    db: db,
                    storeNames: storeNames
                });
            }, function (t, error) {
                reject(error);
            });
        }, function (sqlError) {
            reject(sqlError);
        });
    });
}

function dropInstance$1(options, callback) {
    callback = getCallback.apply(this, arguments);

    var currentConfig = this.config();
    options = typeof options !== 'function' && options || {};
    if (!options.name) {
        options.name = options.name || currentConfig.name;
        options.storeName = options.storeName || currentConfig.storeName;
    }

    var self = this;
    var promise;
    if (!options.name) {
        promise = Promise$1.reject('Invalid arguments');
    } else {
        promise = new Promise$1(function (resolve) {
            var db;
            if (options.name === currentConfig.name) {
                // use the db reference of the current instance
                db = self._dbInfo.db;
            } else {
                db = openDatabase(options.name, '', '', 0);
            }

            if (!options.storeName) {
                // drop all database tables
                resolve(getAllStoreNames(db));
            } else {
                resolve({
                    db: db,
                    storeNames: [options.storeName]
                });
            }
        }).then(function (operationInfo) {
            return new Promise$1(function (resolve, reject) {
                operationInfo.db.transaction(function (t) {
                    function dropTable(storeName) {
                        return new Promise$1(function (resolve, reject) {
                            t.executeSql('DROP TABLE IF EXISTS ' + storeName, [], function () {
                                resolve();
                            }, function (t, error) {
                                reject(error);
                            });
                        });
                    }

                    var operations = [];
                    for (var i = 0, len = operationInfo.storeNames.length; i < len; i++) {
                        operations.push(dropTable(operationInfo.storeNames[i]));
                    }

                    Promise$1.all(operations).then(function () {
                        resolve();
                    })["catch"](function (e) {
                        reject(e);
                    });
                }, function (sqlError) {
                    reject(sqlError);
                });
            });
        });
    }

    executeCallback(promise, callback);
    return promise;
}

var webSQLStorage = {
    _driver: 'webSQLStorage',
    _initStorage: _initStorage$1,
    _support: isWebSQLValid(),
    iterate: iterate$1,
    getItem: getItem$1,
    setItem: setItem$1,
    removeItem: removeItem$1,
    clear: clear$1,
    length: length$1,
    key: key$1,
    keys: keys$1,
    dropInstance: dropInstance$1
};

function isLocalStorageValid() {
    try {
        return typeof localStorage !== 'undefined' && 'setItem' in localStorage &&
        // in IE8 typeof localStorage.setItem === 'object'
        !!localStorage.setItem;
    } catch (e) {
        return false;
    }
}

function _getKeyPrefix(options, defaultConfig) {
    var keyPrefix = options.name + '/';

    if (options.storeName !== defaultConfig.storeName) {
        keyPrefix += options.storeName + '/';
    }
    return keyPrefix;
}

// Check if localStorage throws when saving an item
function checkIfLocalStorageThrows() {
    var localStorageTestKey = '_localforage_support_test';

    try {
        localStorage.setItem(localStorageTestKey, true);
        localStorage.removeItem(localStorageTestKey);

        return false;
    } catch (e) {
        return true;
    }
}

// Check if localStorage is usable and allows to save an item
// This method checks if localStorage is usable in Safari Private Browsing
// mode, or in any other case where the available quota for localStorage
// is 0 and there wasn't any saved items yet.
function _isLocalStorageUsable() {
    return !checkIfLocalStorageThrows() || localStorage.length > 0;
}

// Config the localStorage backend, using options set in the config.
function _initStorage$2(options) {
    var self = this;
    var dbInfo = {};
    if (options) {
        for (var i in options) {
            dbInfo[i] = options[i];
        }
    }

    dbInfo.keyPrefix = _getKeyPrefix(options, self._defaultConfig);

    if (!_isLocalStorageUsable()) {
        return Promise$1.reject();
    }

    self._dbInfo = dbInfo;
    dbInfo.serializer = localforageSerializer;

    return Promise$1.resolve();
}

// Remove all keys from the datastore, effectively destroying all data in
// the app's key/value store!
function clear$2(callback) {
    var self = this;
    var promise = self.ready().then(function () {
        var keyPrefix = self._dbInfo.keyPrefix;

        for (var i = localStorage.length - 1; i >= 0; i--) {
            var key = localStorage.key(i);

            if (key.indexOf(keyPrefix) === 0) {
                localStorage.removeItem(key);
            }
        }
    });

    executeCallback(promise, callback);
    return promise;
}

// Retrieve an item from the store. Unlike the original async_storage
// library in Gaia, we don't modify return values at all. If a key's value
// is `undefined`, we pass that value to the callback function.
function getItem$2(key, callback) {
    var self = this;

    key = normalizeKey(key);

    var promise = self.ready().then(function () {
        var dbInfo = self._dbInfo;
        var result = localStorage.getItem(dbInfo.keyPrefix + key);

        // If a result was found, parse it from the serialized
        // string into a JS object. If result isn't truthy, the key
        // is likely undefined and we'll pass it straight to the
        // callback.
        if (result) {
            result = dbInfo.serializer.deserialize(result);
        }

        return result;
    });

    executeCallback(promise, callback);
    return promise;
}

// Iterate over all items in the store.
function iterate$2(iterator, callback) {
    var self = this;

    var promise = self.ready().then(function () {
        var dbInfo = self._dbInfo;
        var keyPrefix = dbInfo.keyPrefix;
        var keyPrefixLength = keyPrefix.length;
        var length = localStorage.length;

        // We use a dedicated iterator instead of the `i` variable below
        // so other keys we fetch in localStorage aren't counted in
        // the `iterationNumber` argument passed to the `iterate()`
        // callback.
        //
        // See: github.com/mozilla/localForage/pull/435#discussion_r38061530
        var iterationNumber = 1;

        for (var i = 0; i < length; i++) {
            var key = localStorage.key(i);
            if (key.indexOf(keyPrefix) !== 0) {
                continue;
            }
            var value = localStorage.getItem(key);

            // If a result was found, parse it from the serialized
            // string into a JS object. If result isn't truthy, the
            // key is likely undefined and we'll pass it straight
            // to the iterator.
            if (value) {
                value = dbInfo.serializer.deserialize(value);
            }

            value = iterator(value, key.substring(keyPrefixLength), iterationNumber++);

            if (value !== void 0) {
                return value;
            }
        }
    });

    executeCallback(promise, callback);
    return promise;
}

// Same as localStorage's key() method, except takes a callback.
function key$2(n, callback) {
    var self = this;
    var promise = self.ready().then(function () {
        var dbInfo = self._dbInfo;
        var result;
        try {
            result = localStorage.key(n);
        } catch (error) {
            result = null;
        }

        // Remove the prefix from the key, if a key is found.
        if (result) {
            result = result.substring(dbInfo.keyPrefix.length);
        }

        return result;
    });

    executeCallback(promise, callback);
    return promise;
}

function keys$2(callback) {
    var self = this;
    var promise = self.ready().then(function () {
        var dbInfo = self._dbInfo;
        var length = localStorage.length;
        var keys = [];

        for (var i = 0; i < length; i++) {
            var itemKey = localStorage.key(i);
            if (itemKey.indexOf(dbInfo.keyPrefix) === 0) {
                keys.push(itemKey.substring(dbInfo.keyPrefix.length));
            }
        }

        return keys;
    });

    executeCallback(promise, callback);
    return promise;
}

// Supply the number of keys in the datastore to the callback function.
function length$2(callback) {
    var self = this;
    var promise = self.keys().then(function (keys) {
        return keys.length;
    });

    executeCallback(promise, callback);
    return promise;
}

// Remove an item from the store, nice and simple.
function removeItem$2(key, callback) {
    var self = this;

    key = normalizeKey(key);

    var promise = self.ready().then(function () {
        var dbInfo = self._dbInfo;
        localStorage.removeItem(dbInfo.keyPrefix + key);
    });

    executeCallback(promise, callback);
    return promise;
}

// Set a key's value and run an optional callback once the value is set.
// Unlike Gaia's implementation, the callback function is passed the value,
// in case you want to operate on that value only after you're sure it
// saved, or something like that.
function setItem$2(key, value, callback) {
    var self = this;

    key = normalizeKey(key);

    var promise = self.ready().then(function () {
        // Convert undefined values to null.
        // https://github.com/mozilla/localForage/pull/42
        if (value === undefined) {
            value = null;
        }

        // Save the original value to pass to the callback.
        var originalValue = value;

        return new Promise$1(function (resolve, reject) {
            var dbInfo = self._dbInfo;
            dbInfo.serializer.serialize(value, function (value, error) {
                if (error) {
                    reject(error);
                } else {
                    try {
                        localStorage.setItem(dbInfo.keyPrefix + key, value);
                        resolve(originalValue);
                    } catch (e) {
                        // localStorage capacity exceeded.
                        // TODO: Make this a specific error/event.
                        if (e.name === 'QuotaExceededError' || e.name === 'NS_ERROR_DOM_QUOTA_REACHED') {
                            reject(e);
                        }
                        reject(e);
                    }
                }
            });
        });
    });

    executeCallback(promise, callback);
    return promise;
}

function dropInstance$2(options, callback) {
    callback = getCallback.apply(this, arguments);

    options = typeof options !== 'function' && options || {};
    if (!options.name) {
        var currentConfig = this.config();
        options.name = options.name || currentConfig.name;
        options.storeName = options.storeName || currentConfig.storeName;
    }

    var self = this;
    var promise;
    if (!options.name) {
        promise = Promise$1.reject('Invalid arguments');
    } else {
        promise = new Promise$1(function (resolve) {
            if (!options.storeName) {
                resolve(options.name + '/');
            } else {
                resolve(_getKeyPrefix(options, self._defaultConfig));
            }
        }).then(function (keyPrefix) {
            for (var i = localStorage.length - 1; i >= 0; i--) {
                var key = localStorage.key(i);

                if (key.indexOf(keyPrefix) === 0) {
                    localStorage.removeItem(key);
                }
            }
        });
    }

    executeCallback(promise, callback);
    return promise;
}

var localStorageWrapper = {
    _driver: 'localStorageWrapper',
    _initStorage: _initStorage$2,
    _support: isLocalStorageValid(),
    iterate: iterate$2,
    getItem: getItem$2,
    setItem: setItem$2,
    removeItem: removeItem$2,
    clear: clear$2,
    length: length$2,
    key: key$2,
    keys: keys$2,
    dropInstance: dropInstance$2
};

var sameValue = function sameValue(x, y) {
    return x === y || typeof x === 'number' && typeof y === 'number' && isNaN(x) && isNaN(y);
};

var includes = function includes(array, searchElement) {
    var len = array.length;
    var i = 0;
    while (i < len) {
        if (sameValue(array[i], searchElement)) {
            return true;
        }
        i++;
    }

    return false;
};

var isArray = Array.isArray || function (arg) {
    return Object.prototype.toString.call(arg) === '[object Array]';
};

// Drivers are stored here when `defineDriver()` is called.
// They are shared across all instances of localForage.
var DefinedDrivers = {};

var DriverSupport = {};

var DefaultDrivers = {
    INDEXEDDB: asyncStorage,
    WEBSQL: webSQLStorage,
    LOCALSTORAGE: localStorageWrapper
};

var DefaultDriverOrder = [DefaultDrivers.INDEXEDDB._driver, DefaultDrivers.WEBSQL._driver, DefaultDrivers.LOCALSTORAGE._driver];

var OptionalDriverMethods = ['dropInstance'];

var LibraryMethods = ['clear', 'getItem', 'iterate', 'key', 'keys', 'length', 'removeItem', 'setItem'].concat(OptionalDriverMethods);

var DefaultConfig = {
    description: '',
    driver: DefaultDriverOrder.slice(),
    name: 'localforage',
    // Default DB size is _JUST UNDER_ 5MB, as it's the highest size
    // we can use without a prompt.
    size: 4980736,
    storeName: 'keyvaluepairs',
    version: 1.0
};

function callWhenReady(localForageInstance, libraryMethod) {
    localForageInstance[libraryMethod] = function () {
        var _args = arguments;
        return localForageInstance.ready().then(function () {
            return localForageInstance[libraryMethod].apply(localForageInstance, _args);
        });
    };
}

function extend() {
    for (var i = 1; i < arguments.length; i++) {
        var arg = arguments[i];

        if (arg) {
            for (var _key in arg) {
                if (arg.hasOwnProperty(_key)) {
                    if (isArray(arg[_key])) {
                        arguments[0][_key] = arg[_key].slice();
                    } else {
                        arguments[0][_key] = arg[_key];
                    }
                }
            }
        }
    }

    return arguments[0];
}

var LocalForage = function () {
    function LocalForage(options) {
        _classCallCheck(this, LocalForage);

        for (var driverTypeKey in DefaultDrivers) {
            if (DefaultDrivers.hasOwnProperty(driverTypeKey)) {
                var driver = DefaultDrivers[driverTypeKey];
                var driverName = driver._driver;
                this[driverTypeKey] = driverName;

                if (!DefinedDrivers[driverName]) {
                    // we don't need to wait for the promise,
                    // since the default drivers can be defined
                    // in a blocking manner
                    this.defineDriver(driver);
                }
            }
        }

        this._defaultConfig = extend({}, DefaultConfig);
        this._config = extend({}, this._defaultConfig, options);
        this._driverSet = null;
        this._initDriver = null;
        this._ready = false;
        this._dbInfo = null;

        this._wrapLibraryMethodsWithReady();
        this.setDriver(this._config.driver)["catch"](function () {});
    }

    // Set any config values for localForage; can be called anytime before
    // the first API call (e.g. `getItem`, `setItem`).
    // We loop through options so we don't overwrite existing config
    // values.


    LocalForage.prototype.config = function config(options) {
        // If the options argument is an object, we use it to set values.
        // Otherwise, we return either a specified config value or all
        // config values.
        if ((typeof options === 'undefined' ? 'undefined' : _typeof(options)) === 'object') {
            // If localforage is ready and fully initialized, we can't set
            // any new configuration values. Instead, we return an error.
            if (this._ready) {
                return new Error("Can't call config() after localforage " + 'has been used.');
            }

            for (var i in options) {
                if (i === 'storeName') {
                    options[i] = options[i].replace(/\W/g, '_');
                }

                if (i === 'version' && typeof options[i] !== 'number') {
                    return new Error('Database version must be a number.');
                }

                this._config[i] = options[i];
            }

            // after all config options are set and
            // the driver option is used, try setting it
            if ('driver' in options && options.driver) {
                return this.setDriver(this._config.driver);
            }

            return true;
        } else if (typeof options === 'string') {
            return this._config[options];
        } else {
            return this._config;
        }
    };

    // Used to define a custom driver, shared across all instances of
    // localForage.


    LocalForage.prototype.defineDriver = function defineDriver(driverObject, callback, errorCallback) {
        var promise = new Promise$1(function (resolve, reject) {
            try {
                var driverName = driverObject._driver;
                var complianceError = new Error('Custom driver not compliant; see ' + 'https://mozilla.github.io/localForage/#definedriver');

                // A driver name should be defined and not overlap with the
                // library-defined, default drivers.
                if (!driverObject._driver) {
                    reject(complianceError);
                    return;
                }

                var driverMethods = LibraryMethods.concat('_initStorage');
                for (var i = 0, len = driverMethods.length; i < len; i++) {
                    var driverMethodName = driverMethods[i];

                    // when the property is there,
                    // it should be a method even when optional
                    var isRequired = !includes(OptionalDriverMethods, driverMethodName);
                    if ((isRequired || driverObject[driverMethodName]) && typeof driverObject[driverMethodName] !== 'function') {
                        reject(complianceError);
                        return;
                    }
                }

                var configureMissingMethods = function configureMissingMethods() {
                    var methodNotImplementedFactory = function methodNotImplementedFactory(methodName) {
                        return function () {
                            var error = new Error('Method ' + methodName + ' is not implemented by the current driver');
                            var promise = Promise$1.reject(error);
                            executeCallback(promise, arguments[arguments.length - 1]);
                            return promise;
                        };
                    };

                    for (var _i = 0, _len = OptionalDriverMethods.length; _i < _len; _i++) {
                        var optionalDriverMethod = OptionalDriverMethods[_i];
                        if (!driverObject[optionalDriverMethod]) {
                            driverObject[optionalDriverMethod] = methodNotImplementedFactory(optionalDriverMethod);
                        }
                    }
                };

                configureMissingMethods();

                var setDriverSupport = function setDriverSupport(support) {
                    if (DefinedDrivers[driverName]) {
                        console.info('Redefining LocalForage driver: ' + driverName);
                    }
                    DefinedDrivers[driverName] = driverObject;
                    DriverSupport[driverName] = support;
                    // don't use a then, so that we can define
                    // drivers that have simple _support methods
                    // in a blocking manner
                    resolve();
                };

                if ('_support' in driverObject) {
                    if (driverObject._support && typeof driverObject._support === 'function') {
                        driverObject._support().then(setDriverSupport, reject);
                    } else {
                        setDriverSupport(!!driverObject._support);
                    }
                } else {
                    setDriverSupport(true);
                }
            } catch (e) {
                reject(e);
            }
        });

        executeTwoCallbacks(promise, callback, errorCallback);
        return promise;
    };

    LocalForage.prototype.driver = function driver() {
        return this._driver || null;
    };

    LocalForage.prototype.getDriver = function getDriver(driverName, callback, errorCallback) {
        var getDriverPromise = DefinedDrivers[driverName] ? Promise$1.resolve(DefinedDrivers[driverName]) : Promise$1.reject(new Error('Driver not found.'));

        executeTwoCallbacks(getDriverPromise, callback, errorCallback);
        return getDriverPromise;
    };

    LocalForage.prototype.getSerializer = function getSerializer(callback) {
        var serializerPromise = Promise$1.resolve(localforageSerializer);
        executeTwoCallbacks(serializerPromise, callback);
        return serializerPromise;
    };

    LocalForage.prototype.ready = function ready(callback) {
        var self = this;

        var promise = self._driverSet.then(function () {
            if (self._ready === null) {
                self._ready = self._initDriver();
            }

            return self._ready;
        });

        executeTwoCallbacks(promise, callback, callback);
        return promise;
    };

    LocalForage.prototype.setDriver = function setDriver(drivers, callback, errorCallback) {
        var self = this;

        if (!isArray(drivers)) {
            drivers = [drivers];
        }

        var supportedDrivers = this._getSupportedDrivers(drivers);

        function setDriverToConfig() {
            self._config.driver = self.driver();
        }

        function extendSelfWithDriver(driver) {
            self._extend(driver);
            setDriverToConfig();

            self._ready = self._initStorage(self._config);
            return self._ready;
        }

        function initDriver(supportedDrivers) {
            return function () {
                var currentDriverIndex = 0;

                function driverPromiseLoop() {
                    while (currentDriverIndex < supportedDrivers.length) {
                        var driverName = supportedDrivers[currentDriverIndex];
                        currentDriverIndex++;

                        self._dbInfo = null;
                        self._ready = null;

                        return self.getDriver(driverName).then(extendSelfWithDriver)["catch"](driverPromiseLoop);
                    }

                    setDriverToConfig();
                    var error = new Error('No available storage method found.');
                    self._driverSet = Promise$1.reject(error);
                    return self._driverSet;
                }

                return driverPromiseLoop();
            };
        }

        // There might be a driver initialization in progress
        // so wait for it to finish in order to avoid a possible
        // race condition to set _dbInfo
        var oldDriverSetDone = this._driverSet !== null ? this._driverSet["catch"](function () {
            return Promise$1.resolve();
        }) : Promise$1.resolve();

        this._driverSet = oldDriverSetDone.then(function () {
            var driverName = supportedDrivers[0];
            self._dbInfo = null;
            self._ready = null;

            return self.getDriver(driverName).then(function (driver) {
                self._driver = driver._driver;
                setDriverToConfig();
                self._wrapLibraryMethodsWithReady();
                self._initDriver = initDriver(supportedDrivers);
            });
        })["catch"](function () {
            setDriverToConfig();
            var error = new Error('No available storage method found.');
            self._driverSet = Promise$1.reject(error);
            return self._driverSet;
        });

        executeTwoCallbacks(this._driverSet, callback, errorCallback);
        return this._driverSet;
    };

    LocalForage.prototype.supports = function supports(driverName) {
        return !!DriverSupport[driverName];
    };

    LocalForage.prototype._extend = function _extend(libraryMethodsAndProperties) {
        extend(this, libraryMethodsAndProperties);
    };

    LocalForage.prototype._getSupportedDrivers = function _getSupportedDrivers(drivers) {
        var supportedDrivers = [];
        for (var i = 0, len = drivers.length; i < len; i++) {
            var driverName = drivers[i];
            if (this.supports(driverName)) {
                supportedDrivers.push(driverName);
            }
        }
        return supportedDrivers;
    };

    LocalForage.prototype._wrapLibraryMethodsWithReady = function _wrapLibraryMethodsWithReady() {
        // Add a stub for each driver API method that delays the call to the
        // corresponding driver method until localForage is ready. These stubs
        // will be replaced by the driver methods as soon as the driver is
        // loaded, so there is no performance impact.
        for (var i = 0, len = LibraryMethods.length; i < len; i++) {
            callWhenReady(this, LibraryMethods[i]);
        }
    };

    LocalForage.prototype.createInstance = function createInstance(options) {
        return new LocalForage(options);
    };

    return LocalForage;
}();

// The actual localForage object that we expose as a module or via a
// global. It's extended by pulling in one of our other libraries.


var localforage_js = new LocalForage();

module.exports = localforage_js;

},{"3":3}]},{},[4])(4)
});

/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(47)))

/***/ }),
/* 404 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _core = __webpack_require__(6);

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Open DisplayOptions Format Parser
 * @class
 * @param {document} displayOptionsDocument XML
 */
var DisplayOptions = function () {
	function DisplayOptions(displayOptionsDocument) {
		_classCallCheck(this, DisplayOptions);

		this.interactive = "";
		this.fixedLayout = "";
		this.openToSpread = "";
		this.orientationLock = "";

		if (displayOptionsDocument) {
			this.parse(displayOptionsDocument);
		}
	}

	/**
  * Parse XML
  * @param  {document} displayOptionsDocument XML
  * @return {DisplayOptions} self
  */


	_createClass(DisplayOptions, [{
		key: "parse",
		value: function parse(displayOptionsDocument) {
			var _this = this;

			if (!displayOptionsDocument) {
				return this;
			}

			var displayOptionsNode = (0, _core.qs)(displayOptionsDocument, "display_options");
			if (!displayOptionsNode) {
				return this;
			}

			var options = (0, _core.qsa)(displayOptionsNode, "option");
			options.forEach(function (el) {
				var value = "";

				if (el.childNodes.length) {
					value = el.childNodes[0].nodeValue;
				}

				switch (el.attributes.name.value) {
					case "interactive":
						_this.interactive = value;
						break;
					case "fixed-layout":
						_this.fixedLayout = value;
						break;
					case "open-to-spread":
						_this.openToSpread = value;
						break;
					case "orientation-lock":
						_this.orientationLock = value;
						break;
				}
			});

			return this;
		}
	}, {
		key: "destroy",
		value: function destroy() {
			this.interactive = undefined;
			this.fixedLayout = undefined;
			this.openToSpread = undefined;
			this.orientationLock = undefined;
		}
	}]);

	return DisplayOptions;
}();

exports.default = DisplayOptions;
module.exports = exports["default"];

/***/ }),
/* 405 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function(global) {(function(global) {
  /**
   * Polyfill URLSearchParams
   *
   * Inspired from : https://github.com/WebReflection/url-search-params/blob/master/src/url-search-params.js
   */

  var checkIfIteratorIsSupported = function() {
    try {
      return !!Symbol.iterator;
    } catch (error) {
      return false;
    }
  };


  var iteratorSupported = checkIfIteratorIsSupported();

  var createIterator = function(items) {
    var iterator = {
      next: function() {
        var value = items.shift();
        return { done: value === void 0, value: value };
      }
    };

    if (iteratorSupported) {
      iterator[Symbol.iterator] = function() {
        return iterator;
      };
    }

    return iterator;
  };

  /**
   * Search param name and values should be encoded according to https://url.spec.whatwg.org/#urlencoded-serializing
   * encodeURIComponent() produces the same result except encoding spaces as `%20` instead of `+`.
   */
  var serializeParam = function(value) {
    return encodeURIComponent(value).replace(/%20/g, '+');
  };

  var deserializeParam = function(value) {
    return decodeURIComponent(value).replace(/\+/g, ' ');
  };

  var polyfillURLSearchParams = function() {

    var URLSearchParams = function(searchString) {
      Object.defineProperty(this, '_entries', { writable: true, value: {} });
      var typeofSearchString = typeof searchString;

      if (typeofSearchString === 'undefined') {
        // do nothing
      } else if (typeofSearchString === 'string') {
        if (searchString !== '') {
          this._fromString(searchString);
        }
      } else if (searchString instanceof URLSearchParams) {
        var _this = this;
        searchString.forEach(function(value, name) {
          _this.append(name, value);
        });
      } else if ((searchString !== null) && (typeofSearchString === 'object')) {
        if (Object.prototype.toString.call(searchString) === '[object Array]') {
          for (var i = 0; i < searchString.length; i++) {
            var entry = searchString[i];
            if ((Object.prototype.toString.call(entry) === '[object Array]') || (entry.length !== 2)) {
              this.append(entry[0], entry[1]);
            } else {
              throw new TypeError('Expected [string, any] as entry at index ' + i + ' of URLSearchParams\'s input');
            }
          }
        } else {
          for (var key in searchString) {
            if (searchString.hasOwnProperty(key)) {
              this.append(key, searchString[key]);
            }
          }
        }
      } else {
        throw new TypeError('Unsupported input\'s type for URLSearchParams');
      }
    };

    var proto = URLSearchParams.prototype;

    proto.append = function(name, value) {
      if (name in this._entries) {
        this._entries[name].push(String(value));
      } else {
        this._entries[name] = [String(value)];
      }
    };

    proto.delete = function(name) {
      delete this._entries[name];
    };

    proto.get = function(name) {
      return (name in this._entries) ? this._entries[name][0] : null;
    };

    proto.getAll = function(name) {
      return (name in this._entries) ? this._entries[name].slice(0) : [];
    };

    proto.has = function(name) {
      return (name in this._entries);
    };

    proto.set = function(name, value) {
      this._entries[name] = [String(value)];
    };

    proto.forEach = function(callback, thisArg) {
      var entries;
      for (var name in this._entries) {
        if (this._entries.hasOwnProperty(name)) {
          entries = this._entries[name];
          for (var i = 0; i < entries.length; i++) {
            callback.call(thisArg, entries[i], name, this);
          }
        }
      }
    };

    proto.keys = function() {
      var items = [];
      this.forEach(function(value, name) {
        items.push(name);
      });
      return createIterator(items);
    };

    proto.values = function() {
      var items = [];
      this.forEach(function(value) {
        items.push(value);
      });
      return createIterator(items);
    };

    proto.entries = function() {
      var items = [];
      this.forEach(function(value, name) {
        items.push([name, value]);
      });
      return createIterator(items);
    };

    if (iteratorSupported) {
      proto[Symbol.iterator] = proto.entries;
    }

    proto.toString = function() {
      var searchArray = [];
      this.forEach(function(value, name) {
        searchArray.push(serializeParam(name) + '=' + serializeParam(value));
      });
      return searchArray.join('&');
    };


    global.URLSearchParams = URLSearchParams;
  };

  if (!('URLSearchParams' in global) || (new URLSearchParams('?a=1').toString() !== 'a=1')) {
    polyfillURLSearchParams();
  }

  var proto = URLSearchParams.prototype;

  if (typeof proto.sort !== 'function') {
    proto.sort = function() {
      var _this = this;
      var items = [];
      this.forEach(function(value, name) {
        items.push([name, value]);
        if (!_this._entries) {
          _this.delete(name);
        }
      });
      items.sort(function(a, b) {
        if (a[0] < b[0]) {
          return -1;
        } else if (a[0] > b[0]) {
          return +1;
        } else {
          return 0;
        }
      });
      if (_this._entries) { // force reset because IE keeps keys index
        _this._entries = {};
      }
      for (var i = 0; i < items.length; i++) {
        this.append(items[i][0], items[i][1]);
      }
    };
  }

  if (typeof proto._fromString !== 'function') {
    Object.defineProperty(proto, '_fromString', {
      enumerable: false,
      configurable: false,
      writable: false,
      value: function(searchString) {
        if (this._entries) {
          this._entries = {};
        } else {
          var keys = [];
          this.forEach(function(value, name) {
            keys.push(name);
          });
          for (var i = 0; i < keys.length; i++) {
            this.delete(keys[i]);
          }
        }

        searchString = searchString.replace(/^\?/, '');
        var attributes = searchString.split('&');
        var attribute;
        for (var i = 0; i < attributes.length; i++) {
          attribute = attributes[i].split('=');
          this.append(
            deserializeParam(attribute[0]),
            (attribute.length > 1) ? deserializeParam(attribute[1]) : ''
          );
        }
      }
    });
  }

  // HTMLAnchorElement

})(
  (typeof global !== 'undefined') ? global
    : ((typeof window !== 'undefined') ? window
    : ((typeof self !== 'undefined') ? self : this))
);

(function(global) {
  /**
   * Polyfill URL
   *
   * Inspired from : https://github.com/arv/DOM-URL-Polyfill/blob/master/src/url.js
   */

  var checkIfURLIsSupported = function() {
    try {
      var u = new URL('b', 'http://a');
      u.pathname = 'c%20d';
      return (u.href === 'http://a/c%20d') && u.searchParams;
    } catch (e) {
      return false;
    }
  };


  var polyfillURL = function() {
    var _URL = global.URL;

    var URL = function(url, base) {
      if (typeof url !== 'string') url = String(url);

      // Only create another document if the base is different from current location.
      var doc = document, baseElement;
      if (base && (global.location === void 0 || base !== global.location.href)) {
        doc = document.implementation.createHTMLDocument('');
        baseElement = doc.createElement('base');
        baseElement.href = base;
        doc.head.appendChild(baseElement);
        try {
          if (baseElement.href.indexOf(base) !== 0) throw new Error(baseElement.href);
        } catch (err) {
          throw new Error('URL unable to set base ' + base + ' due to ' + err);
        }
      }

      var anchorElement = doc.createElement('a');
      anchorElement.href = url;
      if (baseElement) {
        doc.body.appendChild(anchorElement);
        anchorElement.href = anchorElement.href; // force href to refresh
      }

      if (anchorElement.protocol === ':' || !/:/.test(anchorElement.href)) {
        throw new TypeError('Invalid URL');
      }

      Object.defineProperty(this, '_anchorElement', {
        value: anchorElement
      });


      // create a linked searchParams which reflect its changes on URL
      var searchParams = new URLSearchParams(this.search);
      var enableSearchUpdate = true;
      var enableSearchParamsUpdate = true;
      var _this = this;
      ['append', 'delete', 'set'].forEach(function(methodName) {
        var method = searchParams[methodName];
        searchParams[methodName] = function() {
          method.apply(searchParams, arguments);
          if (enableSearchUpdate) {
            enableSearchParamsUpdate = false;
            _this.search = searchParams.toString();
            enableSearchParamsUpdate = true;
          }
        };
      });

      Object.defineProperty(this, 'searchParams', {
        value: searchParams,
        enumerable: true
      });

      var search = void 0;
      Object.defineProperty(this, '_updateSearchParams', {
        enumerable: false,
        configurable: false,
        writable: false,
        value: function() {
          if (this.search !== search) {
            search = this.search;
            if (enableSearchParamsUpdate) {
              enableSearchUpdate = false;
              this.searchParams._fromString(this.search);
              enableSearchUpdate = true;
            }
          }
        }
      });
    };

    var proto = URL.prototype;

    var linkURLWithAnchorAttribute = function(attributeName) {
      Object.defineProperty(proto, attributeName, {
        get: function() {
          return this._anchorElement[attributeName];
        },
        set: function(value) {
          this._anchorElement[attributeName] = value;
        },
        enumerable: true
      });
    };

    ['hash', 'host', 'hostname', 'port', 'protocol']
      .forEach(function(attributeName) {
        linkURLWithAnchorAttribute(attributeName);
      });

    Object.defineProperty(proto, 'search', {
      get: function() {
        return this._anchorElement['search'];
      },
      set: function(value) {
        this._anchorElement['search'] = value;
        this._updateSearchParams();
      },
      enumerable: true
    });

    Object.defineProperties(proto, {

      'toString': {
        get: function() {
          var _this = this;
          return function() {
            return _this.href;
          };
        }
      },

      'href': {
        get: function() {
          return this._anchorElement.href.replace(/\?$/, '');
        },
        set: function(value) {
          this._anchorElement.href = value;
          this._updateSearchParams();
        },
        enumerable: true
      },

      'pathname': {
        get: function() {
          return this._anchorElement.pathname.replace(/(^\/?)/, '/');
        },
        set: function(value) {
          this._anchorElement.pathname = value;
        },
        enumerable: true
      },

      'origin': {
        get: function() {
          // get expected port from protocol
          var expectedPort = { 'http:': 80, 'https:': 443, 'ftp:': 21 }[this._anchorElement.protocol];
          // add port to origin if, expected port is different than actual port
          // and it is not empty f.e http://foo:8080
          // 8080 != 80 && 8080 != ''
          var addPortToOrigin = this._anchorElement.port != expectedPort &&
            this._anchorElement.port !== '';

          return this._anchorElement.protocol +
            '//' +
            this._anchorElement.hostname +
            (addPortToOrigin ? (':' + this._anchorElement.port) : '');
        },
        enumerable: true
      },

      'password': { // TODO
        get: function() {
          return '';
        },
        set: function(value) {
        },
        enumerable: true
      },

      'username': { // TODO
        get: function() {
          return '';
        },
        set: function(value) {
        },
        enumerable: true
      },
    });

    URL.createObjectURL = function(blob) {
      return _URL.createObjectURL.apply(_URL, arguments);
    };

    URL.revokeObjectURL = function(url) {
      return _URL.revokeObjectURL.apply(_URL, arguments);
    };

    global.URL = URL;

  };

  if (!checkIfURLIsSupported()) {
    polyfillURL();
  }

  if ((global.location !== void 0) && !('origin' in global.location)) {
    var getOrigin = function() {
      return global.location.protocol + '//' + global.location.hostname + (global.location.port ? (':' + global.location.port) : '');
    };

    try {
      Object.defineProperty(global.location, 'origin', {
        get: getOrigin,
        enumerable: true
      });
    } catch (e) {
      setInterval(function() {
        global.location.origin = getOrigin();
      }, 100);
    }
  }

})(
  (typeof global !== 'undefined') ? global
    : ((typeof window !== 'undefined') ? window
    : ((typeof self !== 'undefined') ? self : this))
);

/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(47)))

/***/ })
/******/ ]);
});
//# sourceMappingURL=epub.legacy.js.map