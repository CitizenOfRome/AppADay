function submit(url, callback, method, params) {
    method = method||"GET";
    params = params||null;
    ajax = window.XMLHttpRequest?(new XMLHttpRequest()):(new ActiveXObject("Microsoft.XMLHttp"));
    ajax.onreadystatechange=function() {
        if(ajax.readyState===4) {
            //if(ajax.responseText!=="1" || ajax.status>=400) return submit(url, method, params);
            if(callback)    callback(ajax.responseText);
        }
    };
    if(method==="GET" && params!==null) {
        if(url.indexOf("?")>=0)    url=url+"&"+params;
        else    url = url+"?"+params;
        params=null;
    }
    ajax.open(method, url, true);
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
function post_form(form, callback) {
    var params="", add="", names=[];
    url = form.action;
    method = form.method;
    for(i=0;i<form.length;i++) {
        if(names.indexOf(form[i].name)>=0)   continue;
        names.push(form[i].name);
        value = get_value(form[i], form);
        if(value===false)   continue;
        params = params+add+form[i].name+"="+value;
        add = "&";
    }
    form.reset();
    return submit(url, callback, method, params);
}