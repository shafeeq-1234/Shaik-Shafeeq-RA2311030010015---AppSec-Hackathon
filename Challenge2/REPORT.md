# Cross-Site Scripting (XSS) Demonstration and Prevention

## Challenge 2 — The Comment Box That Bites Back

## Task A – Exploit

### Payload 1 (Alert)

**Post Comment:**
```html
<script>alert('XSS')</script>
```

**Result:**
An alert box appears displaying the message:

```text
XSS
```

**Explanation:**
The application renders user input without sanitization, allowing JavaScript code to execute in the browser.

---

### Payload 2 (Steal Cookie)

**Post Comment:**
```html
<script>alert(document.cookie)</script>
```

**Result:**
An alert box appears displaying the user's cookies.

**Explanation:**
The injected script accesses `document.cookie` and executes in the victim's browser, demonstrating how attackers can access sensitive session information.

---

## Task B – Fix

### Fix 1: Remove Unsafe Rendering

#### Vulnerable Code

```html
<div>{{ c | safe }}</div>
```

#### Secure Code

```html
<div>{{ c }}</div>
```

**Result:**
Scripts are displayed as plain text instead of being executed.

**Explanation:**
Removing the `safe` filter enables automatic HTML escaping, preventing browsers from interpreting user input as executable code.

---

### Fix 2: Protect Session Cookies

#### Vulnerable Code

```python
resp.set_cookie('session', 'SUPERSECRET42')
```

#### Secure Code

```python
resp.set_cookie(
    'session',
    'SUPERSECRET42',
    httponly=True
)
```

**Explanation:**
The `HttpOnly` attribute prevents JavaScript from accessing cookies through `document.cookie`, reducing the impact of XSS attacks.

---

## Task C – Explanation

Cross-Site Scripting (XSS) is a web security vulnerability that allows attackers to inject malicious scripts into web pages viewed by other users.

### Reflected XSS

Reflected XSS occurs when malicious input is immediately returned in the server response and executed in the victim's browser. The payload is typically delivered through a crafted URL or form submission.

### Stored XSS

Stored XSS occurs when malicious code is permanently stored on the server, such as in comments, forum posts, or user profiles. The script is executed whenever users view the affected content.

### Challenge Analysis

This challenge demonstrated **Stored XSS** because the malicious script was saved as a comment and executed each time the page loaded.

### Why Stored XSS Is Dangerous

Stored XSS is generally more dangerous than Reflected XSS because it affects every user who views the compromised content. Attackers can:

- Steal session cookies
- Hijack user accounts
- Perform actions on behalf of users
- Redirect users to malicious websites
- Distribute malware
- Capture sensitive information

---

## Conclusion

This challenge demonstrated how improperly handled user input can lead to Stored XSS vulnerabilities. By escaping user-generated content and protecting cookies with the `HttpOnly` attribute, applications can significantly reduce the risk of XSS attacks and protect user sessions from compromise.