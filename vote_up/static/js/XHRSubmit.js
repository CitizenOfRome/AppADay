function submit(url, callback, method, params, img_id, callOnRepeat) {
    method = method||"GET";
    method = method.toUpperCase();
    params = params||null;
    var ajax = window.XMLHttpRequest?(new XMLHttpRequest()):(new ActiveXObject("Microsoft.XMLHttp"));
    ajax.onreadystatechange=function() {
        if(ajax.readyState===4) {
            //if(ajax.responseText!=="1" || ajax.status>=400) return submit(url, callback, method, params);
            if(window.mySubmits)    window.mySubmits.splice(thisIndex, 1);
            if(document.getElementById(img_id)) document.getElementById(img_id).style.visibility = "hidden";
            if(callback)    callback(ajax.responseText);
        }
    };
    if(method==="GET" && params!==null) {
        if(url.indexOf("?")>=0)    url=url+"&"+params;
        else    url = url+"?"+params;
        params=null;
    }
    //Prevent repetetion when waiting on the same request
    var thisString = String([url, callback, method, params, img_id, callOnRepeat])+"";
    if(!window.mySubmits)   window.mySubmits = [];
    else {
        var thisIndex = window.mySubmits.indexOf(thisString);
        if(thisIndex>-1)    return callOnRepeat?callOnRepeat(thisString):false;
        else    window.mySubmits.push(thisString);
    }
    if(document.getElementById(img_id)) document.getElementById(img_id).style.visibility = "visible";
    ajax.open(method, url, true);
    if(!ajax)   window.mySubmits.splice(thisIndex, 1);
    if(method==="POST")   ajax.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    ajax.send(params);
}
function get_selected(chk) {
    result="";
    sp = "";
    for(var i=0;i<chk.length;i++) {
        if(chk[i].checked) {
            result+=sp+chk[i].value;
            sp="+";
        }
    }
    return result;
}
function get_value(element, form) {
    switch((element.localName.toLowerCase())) {
        case "input":
            if(element.type==="checkbox" || element.type==="radio") return get_selected(form[element.name]);
            if(element.type!=="text" && element.type!=="password" && element.type!=="hidden")   return false;
        case "textarea":
            return element.value;
        case "select":
            return element.options[element.selectedIndex].value;
        default:
            return false;
    }
}
function post_form(form, callback, callbefore, img_id) {
    var params="", add="", names=[], par={};
    url = form.action;
    method = form.method;
    for(i=0;i<form.length;i++) {
        if(names.indexOf(form[i].name)>=0)   continue;
        names.push(form[i].name);
        value = get_value(form[i], form);
        if(value===false)   continue;
        value = encodeURIComponent(value);
        params = params+add+form[i].name+"="+value;
        par[form[i].name] = value;
        add = "&";
    }
    if(callbefore)  callbefore(par, form);
    /*else    form.reset();*/
    callback_n = function (s) { return callback(s, par, form); };
    return submit(url, callback_n, method, params, img_id);
}