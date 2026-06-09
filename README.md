## Overview

This repository contains solutions, exploit demonstrations, and remediation techniques for common web application vulnerabilities. Each challenge demonstrates a real-world security issue, its impact, and the appropriate mitigation strategy.

## Challenges Covered

| Challenge   | Vulnerability                              |
| ----------- | ------------------------------------------ |
| Challenge 1 | SQL Injection (SQLi)                       |
| Challenge 2 | Cross-Site Scripting (XSS)                 |
| Challenge 3 | Insecure Direct Object Reference (IDOR)    |
| Challenge 4 | Broken Authentication & Session Management |
| Challenge 5 | Security Headers & Information Disclosure  |

---

# Challenge 1 – SQL Injection

## Vulnerability

User input was directly concatenated into SQL queries, allowing attackers to manipulate query logic and bypass authentication.

### Example Payload

```sql
alice' --
```

### Impact

* Authentication bypass
* Unauthorized data access
* Database manipulation

## Mitigation

Use parameterized queries:

```python
row = conn.execute(
    "SELECT * FROM users WHERE username=? AND password=?",
    (u, p)
).fetchone()
```

---

# Challenge 2 – Stored Cross-Site Scripting (XSS)

## Vulnerability

User comments were rendered without sanitization, allowing arbitrary JavaScript execution.

### Example Payload

```html
<script>alert('XSS')</script>
```

### Impact

* Session theft
* Account takeover
* Malicious script execution

## Mitigation

Escape user input:

```html
<div>{{ c }}</div>
```

Protect session cookies:

```python
resp.set_cookie(
    'session',
    'SUPERSECRET42',
    httponly=True
)
```

---

# Challenge 3 – Insecure Direct Object Reference (IDOR)

## Vulnerability

Users could access resources belonging to other users by modifying object identifiers in URLs.

### Example

```text
/invoice/1
/invoice/2
```

### Impact

* Unauthorized access to sensitive data
* Information disclosure

## Mitigation

Implement authorization checks:

```python
if inv['owner'] != session['user']:
    return 'Access denied', 403
```

---

# Challenge 4 – Broken Authentication

## Vulnerabilities Identified

### Weak Secret Key

```python
app.secret_key = 'abc'
```

### Insecure Password Hashing

```python
hashlib.md5(...)
```

### Improper Session Logout

```python
session.pop('user', None)
```

## Mitigations

### Strong Secret Key

```python
import secrets
app.secret_key = secrets.token_hex(32)
```

### Secure Password Hashing

```python
generate_password_hash()
check_password_hash()
```

### Secure Logout

```python
session.clear()
```

---

# Challenge 5 – Security Headers

## Issues Identified

* Debug mode enabled
* Missing security headers
* Untrusted iframe content

### Missing Headers

* X-Frame-Options
* X-Content-Type-Options
* Content-Security-Policy
* Referrer-Policy

## Mitigation

```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response
```

---

# Key Security Concepts Learned

* SQL Injection Prevention
* Input Validation and Output Encoding
* Secure Session Management
* Authentication vs Authorization
* Principle of Least Privilege
* Secure Password Storage
* HTTP Security Headers
* Defense in Depth

---

# Technologies Used

* Python
* Flask
* SQLite
* HTML
* HTTP Security Headers

---

# Author

**Shaik Shafeeq**

Cyber Security Student | SRM Institute of Science and Technology

