//chrome.extension.onRequest.addListener( function(request, sender, sendResponse) {   alert("r:"+request.url);if(request.url===window.location.href) {sendResponse({});}});
function eventFire(el, etype){
    /*http://stackoverflow.com/a/5440986/937891*/
    if (el.fireEvent) {
      el.fireEvent('on' + etype);
    } else {
      var evObj = document.createEvent('Events');
      evObj.initEvent(etype, true, false);
      el.dispatchEvent(evObj);
    }
}
var port = chrome.extension.connect({name: "FBLike"});
port.onMessage.addListener(function(msg) {
    //alert(msg.url+"\n"+window.location.href);
if(msg.url!==window.location.href)   return;
key = (window.location.search.substring(window.location.search.indexOf("=")+1, window.location.search.indexOf("&")));
//alert(key==="1");
liked=(document.getElementsByTagName("a")[0].classList[2]==="like_button_like");
if(key.indexOf(".")===0) {
    key = key.substring(1);
    //alert(key+"/like.png");
    if(liked) {
        //chrome.browserAction.setIcon({path:key+"/ylike.png"});
        chrome.browserAction.setBadgeText({text:"Done"});
        chrome.browserAction.setTitle({title:"Click to UnLike this page"});
    }
    else {
        //chrome.browserAction.setIcon({path:key+"/like.png"});
        chrome.browserAction.setBadgeText({text:"Like"});
        chrome.browserAction.setTitle({title:"Click to Like this page"});
    }
}
else {
    if(liked) {
      eventFire(document.getElementsByTagName("a")[2], "click"); //XLike
      setTimeout('eventFire(document.getElementsByTagName("a")[2], "click")', 100);
      //chrome.browserAction.setIcon({path:key+"/like.png"});
      chrome.browserAction.setBadgeText({text:"Like"});
      chrome.browserAction.setTitle({title:"Click to Like this page"});
    }
    else{
      eventFire(document.getElementsByTagName("a")[0], "click"); //Like
      setTimeout('eventFire(document.getElementsByTagName("a")[0], "click")', 100);
      //chrome.browserAction.setIcon({path:key+"/ylike.png"});
      chrome.browserAction.setBadgeText({text:"Done"});
      chrome.browserAction.setTitle({title:"Click to UnLike this page"});
    }
}
});
// if(key==="1" && !liked)  eventFire(document.getElementsByTagName("a")[0], "click");
// else if(key==="0" && liked)  eventFire(document.getElementsByTagName("a")[2], "click");
// var port = chrome.extension.connect({name: "FBLike"});
// liked=(document.getElementsByTagName("a")[0].classList[2]==="like_button_like");
// port.postMessage({liked:liked});
// port.onMessage.addListener(function(msg) {
  // liked=(document.getElementsByTagName("a")[0].classList[2]==="like_button_like");
  // if(msg.like && !liked)    eventFire(document.getElementsByTagName("a")[0], "click");
  // if(!msg.like && liked)    eventFire(document.getElementsByTagName("a")[2], "click");
  // alert(msg);
// });

