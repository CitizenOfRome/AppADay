bound: function (event){
    event=q(event);
    var y=event.type;
    if(!g.get(this,s))  throw new Error("Bad listenHandler context.");
    var z=g.get(this,s)[y];
    if(!z)  throw new Error("No registered handlers for `"+y+"'.");
    if(y=='click'){
        var aa=j.byTag(event.getTarget(),'a'), ba=o('click',aa,event).set_namespace('evt_ext');
        if(window.ArbiterMonitor)   ArbiterMonitor.initUA(ba,[aa]);
    }
    var ca=Event.getPriorities();
    for(var da=0;da<ca.length;da++){
        var ea=ca[da];
        if(ea in z){
            var fa=z[ea];
            for(var ga=0;ga<fa.length;ga++){
                if(!fa[ga])continue;
                var ha=fa[ga].fire(this,event);
                if(ha===false){return event.kill();}
                else if(event.cancelBubble)event.stop();
            }
        }
    }
    return event.returnValue;
}
function (d){
    d=d||window.event;
    a=d.target||d.srcElement;
    var e=Parent.byTag(a,'A');
    if(!e)  return;
    var f=e.getAttribute('ajaxify'), g=e.href, h=f||g;
    if(h){
        var i=user_action('a',e,d).set_namespace('primer');
        if(window.ArbiterMonitor) ArbiterMonitor.initUA(i,[e]);
    }
    if(f&&g&&!(/#$/).test(g)){
        var j=d.which&&d.which!=1, k=d.altKey||d.ctrlKey||d.metaKey||d.shiftKey;
        if(j||k)return;
    }
    trackReferrer(e,h);
    var l=['dialog'],m=e.rel&&e.rel.match(b);
    m=m&&m[0];
    switch(m){
        case 'dialog-pipe': l.push('ajaxpipe');
        case 'dialog':case 'dialog-post': Bootloader.loadComponents(l, function(){
            Dialog.bootstrap(h,null,m=='dialog',null,null,e);
            });
            break;
        case 'async':case 'async-post': Bootloader.loadComponents('async', function(){AsyncRequest.bootstrap(h,e);});break;
        case 'theater':
            if(window.Env&&Env.snowlift){
                Bootloader.loadComponents('PhotoSnowlift',function(){PhotoSnowlift.bootstrap(h,e);});
            }
            else Bootloader.loadComponents('PhotoSnowbox',function(){PhotoSnowbox.bootstrap(h,e);});
            break;
        case 'toggle':
            CSS.toggleClass(e.parentNode,'openToggler');
            Bootloader.loadComponents('Toggler',function(){Toggler.bootstrap(e);});
            break;
        default:return;
    }
    return false;
}

  function getPageData(target_url, callback) {
    ajax = window.XMLHttpRequest?(new XMLHttpRequest()):(new ActiveXObject("Microsoft.XMLHttp"));
    ajax.onreadystatechange=function() {
      if(ajax.readyState===4) {
        html_data = ajax.responseText;
        callback(html_data);
      }
    };
    ajax.open("GET", "https://www.facebook.com/plugins/like.php?href="+encodeURIComponent(target_url), true);
    ajax.send(null);
  }
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
  doClick = function(st) {
    document.getElementById("gustamos").innerHTML = st;
    eventFire(document.getElementsByTagName("a")[0], "click");
  }
var QueryString = function () {
  /*http://stackoverflow.com/a/979995*/
  // This function is anonymous, is executed immediately and 
  // the return value is assigned to QueryString!
  var query_string = {};
  var query = window.location.search.substring(1);
  var vars = query.split("&");
  for (var i=0;i<vars.length;i++) {
    var pair = vars[i].split("=");
        // If first entry with this name
    if (typeof query_string[pair[0]] === "undefined") {
      query_string[pair[0]] = pair[1];
        // If second entry with this name
    } else if (typeof query_string[pair[0]] === "string") {
      var arr = [ query_string[pair[0]], pair[1] ];
      query_string[pair[0]] = arr;
        // If third or later entry with this name
    } else {
      query_string[pair[0]].push(pair[1]);
    }
  } 
    return query_string;
} ();