/*!
 *                                                                                                                          (℠)
 * # BiB/i Extension: Unaccessibilizer
 *
 * - "What a..."
 * - Reluctantly coded by Satoru MATSUSHIMA. - http://bibi.epub.link or https://github.com/satorumurmur/bibi
 * - Public Domain. - http://unlicense.org/UNLICENSE
 *
 */
Bibi.x({name:"Unaccessibilizer",description:"What a...",author:"Satoru MATSUSHIMA (@satorumurmur)",version:"0.3.0",build:201706181736})(function(){var e=function(e){X.Presets.Unaccessibilizer["select-elements"]&&["-webkit-","-moz-","-ms-",""].forEach(function(t){["user-select","user-drag"].forEach(function(n){e.Body.style[t+n]="none"})}),X.Presets.Unaccessibilizer["save-images"]&&Array.prototype.forEach.call(e.Body.querySelectorAll("img, svg, image"),function(e){["-webkit-","-moz-","-ms-",""].forEach(function(t){["user-select","user-drag"].forEach(function(n){e.style[t+n]="none"}),O.Mobile&&(e.style[t+"pointer-events"]="none")}),e.draggable=!1,e.addEventListener("contextmenu",O.preventDefault)}),X.Presets.Unaccessibilizer["use-contextmenu"]&&e.contentDocument.addEventListener("contextmenu",O.preventDefault)};E.bind("bibi:postprocessed-item-content",function(t){e(t)}),e(O)});