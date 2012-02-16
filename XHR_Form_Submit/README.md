XHR-Form-Submit: Feb 16th 2012
-----------------------------------------------------------
This script allows you to easily submit forms via XHR(ajax).

To use it, simply include the JavaScript and add an onsubmit to your form-element, like:

    <form method="POST" action="post.php" onsubmit="JavaScript:post_form(this, my_callback); return false;">
    
Where, my_callback is called with the XHR_responseText as its parameter, like: 

    my_callback = function(xhr_response){...}

Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
-----------------------------------------------------------
