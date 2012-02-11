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
// key = window.location.search.substring(window.location.search.indexOf("=")+1, window.location.search.indexOf("&"));
//alert(key==="1");
liked=(document.getElementsByTagName("a")[0].classList[2]==="like_button_like");
if(liked) {
  eventFire(document.getElementsByTagName("a")[2], "click"); //XLike
  setTimeout('eventFire(document.getElementsByTagName("a")[2], "click")', 100);
}
else{
  eventFire(document.getElementsByTagName("a")[0], "click"); //Like
  setTimeout('eventFire(document.getElementsByTagName("a")[0], "click")', 100);
}
// if(key==="1" && !liked)  eventFire(document.getElementsByTagName("a")[0], "click");
// else if(key==="0" && liked)  eventFire(document.getElementsByTagName("a")[2], "click");
var port = chrome.extension.connect({name: "FBLike"});
liked=(document.getElementsByTagName("a")[0].classList[2]==="like_button_like");
port.postMessage({liked:liked});
port.onMessage.addListener(function(msg) {
  liked=(document.getElementsByTagName("a")[0].classList[2]==="like_button_like");
  if(msg.like && !liked)    eventFire(document.getElementsByTagName("a")[0], "click");
  if(!msg.like && liked)    eventFire(document.getElementsByTagName("a")[2], "click");
  //alert(msg);
});
