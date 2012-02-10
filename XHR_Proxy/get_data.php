<?php
    if(filter_var($_REQUEST["url"], FILTER_VALIDATE_URL, FILTER_FLAG_SCHEME_REQUIRED))   echo file_get_contents($_REQUEST["url"]);
    #else die("BAD_URL");
?>