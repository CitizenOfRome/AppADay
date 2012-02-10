XHR-Proxy: Feb 9th & 10th 2012
-----------------------------------------------------------
Here is a PHP-based proxy mechanism to bypass the Cross-Domain-Restrictions placed by browsers by using your server to fetch the data for you.
The get_page_data function in the JS file takes the Target_URL and a callback function as parameters; The callback function will be called with a single string argument containing the data returned by the server.
The PHP script simply gets and prints the data from a (valid) URL passed to it as a request.
A special thanks to @Gokhan Arik for his contribution :)

Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
-----------------------------------------------------------
