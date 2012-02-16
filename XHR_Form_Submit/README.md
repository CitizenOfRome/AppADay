XHR-Form-Submit: Feb 16th 2012
-----------------------------------------------------------
This is a way to easily submit forms via XHR(ajax).

To use it, simply include the JavaScript and add an onsubmit to your form-element, like:

    onsubmit="JavaScript:post_form(this, 'post.php', 'POST', my_callback); return false;"
    
Where, my_callback = function(xhr_response){...}

Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
-----------------------------------------------------------
