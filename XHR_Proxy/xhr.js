function get_page_data(target_url, callback) {
    ajax = window.XMLHttpRequest?(new XMLHttpRequest()):(new ActiveXObject("Microsoft.XMLHttp"));
    ajax.onreadystatechange=function() {
      if(ajax.readyState===4) {
        html_data = ajax.responseText;
        callback(html_data);
      }
    };
    ajax.open("GET", "./get_data.php?url="+encodeURIComponent(target_url), true);
    ajax.send(null);
}