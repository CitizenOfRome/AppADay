//Engage.js: Gives the number of active users for a perticular page
engage_counter = 0;
function setCookie(c_name,value,exdays) {
    var exdate=new Date();
    exdate.setDate(exdate.getDate() + exdays);
    var c_value=escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString());
    document.cookie=c_name + "=" + c_value;
}
function getCookie(c_name) {
    var i,x,y,ARRcookies=document.cookie.split(";");
    for (i=0;i<ARRcookies.length;i++) {
      x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
      y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
      x=x.replace(/^\s+|\s+$/g,"");
      if(x===c_name)    return unescape(y);
    }
    return false;
}
engage_counter = 0;
function engaged(active) {
    cookie = getCookie("engaged");
    if((cookie==="active" && active) || (cookie!=="active" && !active))    return;
    if(cookie!=="active" && active)    setCookie("engaged", "active", 300);
    if(cookie==="active" && !active)    setCookie("engaged", "", -1);
    ajax = window.XMLHttpRequest?(new XMLHttpRequest()):(new ActiveXObject("Microsoft.XMLHttp"));
    ajax.onreadystatechange=function() {
        if(ajax.readyState===4) {
            engage_counter = ajax.responseText;
            if(document.getElementById("engage_counter"))   document.getElementById("engage_counter").innerHTML=ajax.responseText;
        }
    };
    //alert(active);
    ajax.open("GET", "/?on="+(active?1:0)+"&url="+encodeURIComponent(window.location.pathname), true);
    ajax.send(null);
}
window.onload=function(e){engaged(true); /*if(e)e.returnValue="1"; return "1"*/};
window.onbeforeunload=function(e){engaged(false); /*if(e)e.returnValue="0"; return "0"*/};
//else if(window.onunload)   window.onunload=function(e){engaged(false); /*if(e)e.returnValue="0"; return "0"*/};