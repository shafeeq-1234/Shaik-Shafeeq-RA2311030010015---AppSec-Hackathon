# SQL Injection Demonstration and Prevention

## Task A – Exploit

### Payload 1 (Login as Alice without Password)

**Username:**
```text
alice' --
```

**Password:**
```text
anything
```

**Result:** Successful Login

**Explanation:**
Everything after `--` is treated as a comment and ignored by SQL. The password check is bypassed.

---

### Payload 2 (Login Using Only Password Field)

**Username:**
```text
anything
```

**Password:**
```text
' OR '1'='1
```

**Result:** Successful Login

**Explanation:**
The condition `'1'='1'` is always true, causing the authentication query to return a valid result and bypass the login check.

---

## Task B – Fix

### Vulnerable Code

```python
query = f"SELECT * FROM users WHERE username='{u}' AND password='{p}'"
row = conn.execute(query).fetchone()
```

### Secure Code (Parameterized Query)

```python
row = conn.execute(
    "SELECT * FROM users WHERE username=? AND password=?",
    (u, p)
).fetchone()
```

**Explanation:**
Parameterized queries ensure that user input is treated as data rather than executable SQL code, preventing SQL injection attacks.

---

## Task C – Explanation

SQL injection occurs when user input is directly concatenated into a SQL query. An attacker can insert SQL syntax that changes the intended query logic. This can allow bypassing authentication, reading sensitive data, or modifying records in the database.

Parameterized queries separate SQL code from user data. The database treats user input strictly as values and not as executable SQL commands. This prevents attackers from injecting malicious SQL statements and helps secure the application against SQL injection vulnerabilities.

---

## Conclusion

SQL injection is a critical security vulnerability caused by improper handling of user input. Using parameterized queries is one of the most effective ways to prevent SQL injection and protect database-driven applications from unauthorized access and data manipulation.

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

# Insecure Direct Object Reference (IDOR) Demonstration and Prevention

## Challenge 3 — The Invoice Peek

## Task A – Exploit

### Scenario

The application allows users to view invoices through a URL containing an invoice identifier.

Example:

```text
/invoice/1
```

A user can modify the invoice ID in the URL:

```text
/invoice/2
```

### Observation

By changing the invoice ID, a user can access invoices belonging to other users.

The application returns different responses depending on whether the invoice exists, revealing information about valid invoice records.

### Result

A logged-in user (Alice) can view another user's (Bob's) invoice simply by changing the invoice identifier in the URL.

**Impact:**

- Unauthorized access to sensitive data
- Exposure of customer information
- Violation of access control policies
- Information disclosure through predictable object identifiers

---

## Task B – Fix

### Secure Authorization Check

Replace the vulnerable logic with proper ownership verification:

```python
if not inv:
    return 'Not found', 404

if inv['owner'] != session['user']:
    return 'Access denied', 403
```

### Explanation

The first check verifies that the invoice exists.

The second check ensures that the currently authenticated user owns the requested invoice before granting access.

If the user is not the owner, the application returns:

```text
Access denied
```

with HTTP status code:

```text
403 Forbidden
```

This prevents users from accessing resources that belong to others.

---

## Task C – Explanation

### Authentication vs Authorization

#### Authentication

Authentication verifies **who a user is**.

Examples:

- Username and password login
- Multi-factor authentication
- Single Sign-On (SSO)

Authentication answers the question:

> "Who are you?"

#### Authorization

Authorization determines **what resources a user is allowed to access**.

Examples:

- Viewing personal invoices
- Accessing administrative pages
- Modifying account settings

Authorization answers the question:

> "What are you allowed to do?"

---

### Challenge Analysis

In this challenge, Alice was successfully authenticated because the application recognized that she was logged in.

However, the application failed to verify whether Alice owned the requested invoice.

As a result, Alice could access Bob's invoice by modifying the invoice identifier in the URL.

This vulnerability is known as an **Insecure Direct Object Reference (IDOR)**.

### Why IDOR Occurs

IDOR vulnerabilities occur when:

- Object identifiers are exposed to users
- The application trusts user-supplied identifiers
- Authorization checks are missing or incomplete

Example:

```text
/invoice/1
/invoice/2
/invoice/3
```

If the application only checks whether the user is logged in and does not verify ownership, users can access resources belonging to others.

---

## Security Impact

An IDOR vulnerability may allow attackers to:

- View confidential information
- Access private documents
- Modify or delete other users' data
- Escalate privileges
- Bypass business rules

---

## Conclusion

This challenge demonstrated an Insecure Direct Object Reference (IDOR) vulnerability caused by missing authorization checks. While authentication confirmed the user's identity, authorization was not enforced to verify resource ownership. Implementing proper ownership validation ensures that users can only access resources they are permitted to view, preventing unauthorized data exposure.

# Broken Authentication and Session Management Demonstration

## Challenge 4 — Three Locks, All Broken

## Task A – Identify the Vulnerabilities

### Flaw 1: Weak Secret Key

#### Vulnerable Code

```python
app.secret_key = 'abc'
```

#### Issue

The application uses a weak and predictable secret key.

#### Attack

An attacker may be able to guess or brute-force the secret key and forge Flask session cookies. This could allow unauthorized access, privilege escalation, or session hijacking.

---

### Flaw 2: Insecure Password Hashing (MD5)

#### Vulnerable Code

```python
hashlib.md5(...)
```

#### Issue

Passwords are hashed using MD5, which is considered cryptographically insecure.

#### Attack

Attackers can rapidly crack MD5 hashes using:

- Rainbow tables
- Dictionary attacks
- Brute-force attacks
- GPU-accelerated cracking tools

This may lead to the recovery of user passwords.

---

### Flaw 3: Incomplete Session Logout

#### Vulnerable Code

```python
session.pop('user', None)
```

#### Issue

Only the `user` session variable is removed.

#### Attack

Other session data may remain active after logout, potentially allowing unauthorized reuse of session information.

---

## Task B – Fix

### Fix 1: Secure Secret Key

#### Secure Code

```python
import secrets

app.secret_key = secrets.token_hex(32)
```

#### Explanation

A randomly generated 256-bit secret key is significantly harder to guess and helps protect session integrity.

---

### Fix 2: Secure Password Hashing

#### Add Imports

```python
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
```

#### Store Passwords Securely

```python
USERS = {
    'admin': generate_password_hash('admin123'),
    'alice': generate_password_hash('alicepass')
}
```

#### Verify Passwords Securely

```python
if u in USERS and check_password_hash(USERS[u], p):
    session['user'] = u
    return redirect('/dashboard')
```

#### Explanation

Passwords are stored as secure hashes rather than plaintext or weak MD5 hashes. Verification is performed using a secure password-checking function.

---

### Fix 3: Proper Session Logout

#### Vulnerable Code

```python
session.pop('user', None)
```

#### Secure Code

```python
session.clear()
```

#### Explanation

`session.clear()` removes all session data, ensuring that no residual information remains after logout.

---

## Task C – Explanation

### Why MD5 Is Insecure

MD5 is considered insecure for password storage because:

- It is extremely fast to compute.
- It is vulnerable to brute-force attacks.
- It is vulnerable to rainbow-table attacks.
- It does not provide built-in salting.
- Identical passwords produce identical hashes.

Example:

```text
password123 → same MD5 hash every time
```

This makes password databases easier to crack if they are compromised.

---

### Why Bcrypt and Argon2 Are Better

Modern password hashing algorithms such as **Bcrypt** and **Argon2** are specifically designed for password protection.

#### Advantages

##### 1. Slow Computation

They intentionally require more processing time, making brute-force attacks significantly slower.

##### 2. Automatic Salting

A unique random salt is added to every password.

Example:

```text
password123 → Hash A
password123 → Hash B
```

Even identical passwords produce different hashes.

##### 3. Configurable Cost Factors

Administrators can increase the computational difficulty as hardware becomes faster.

##### 4. Resistance to Large-Scale Cracking

These algorithms are designed to make password guessing expensive in terms of time and computing resources.

---

## Security Impact

If the identified vulnerabilities remain unpatched, attackers may be able to:

- Forge authentication cookies
- Hijack user sessions
- Recover user passwords
- Gain unauthorized access
- Escalate privileges
- Maintain access after logout

---

## Conclusion

This challenge demonstrated multiple authentication and session management weaknesses, including a weak secret key, insecure MD5 password hashing, and incomplete session invalidation. Replacing MD5 with modern password hashing algorithms such as Bcrypt or Argon2, using strong randomly generated secret keys, and properly clearing sessions during logout significantly improves application security and protects user accounts from compromise.

# Security Headers and Information Disclosure Demonstration

## Challenge 5 – Security Headers

## Task A – Identify the Vulnerabilities

### 1. Debug Mode Information Disclosure

#### Visit

```text
http://127.0.0.1:5000/error
```

#### Information Exposed

When Flask debug mode is enabled, error pages may reveal:

- Stack traces
- Source code snippets
- Environment variables
- Application configuration details
- File paths
- Internal server information

#### Danger

Attackers can use this information to:

- Discover application structure
- Identify vulnerable components
- Locate sensitive files
- Gather intelligence for further attacks

---

### 2. Missing Security Headers

The application does not include important HTTP security headers.

#### Missing Headers

```text
X-Frame-Options
X-Content-Type-Options
Content-Security-Policy
Referrer-Policy
```

#### Risk

Without these headers, the application becomes more vulnerable to:

- Clickjacking attacks
- Content sniffing attacks
- Cross-Site Scripting (XSS)
- Information leakage through referrers

---

### 3. HTML Security Issue

#### Vulnerable Code

```html
<iframe src="https://evil.com"></iframe>
```

#### Issue

The page loads content from an untrusted external source.

#### Risk

Embedding untrusted content may:

- Expose users to malicious websites
- Allow phishing attempts
- Deliver malicious scripts
- Create trust and privacy issues

---

### Verify Headers Using Curl

Run the following command:

```bash
curl -I http://localhost:5000/
```

This displays the HTTP response headers and can be used to verify whether security headers are present.

---

## Task B – Fix

### Fix 1: Disable Debug Mode

#### Secure Configuration

```python
app.config['DEBUG'] = False
```

#### Explanation

Disabling debug mode prevents sensitive diagnostic information from being exposed to users.

---

### Fix 2: Add Security Headers

#### Secure Code

```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response
```

#### Explanation

These headers strengthen browser-side security protections and reduce the attack surface of the application.

---

### Fix 3: Remove Untrusted Iframe

#### Vulnerable Code

```html
<body>
<h1>Hello, world!</h1>
<iframe src="https://evil.com"></iframe>
</body>
```

#### Secure Code

```html
<body>
<h1>Hello, world!</h1>
</body>
```

#### Explanation

Removing the external iframe eliminates the risk of loading potentially malicious third-party content.

---

## Task C – Explanation

### X-Frame-Options

#### Purpose

`X-Frame-Options` protects against clickjacking attacks by controlling whether a webpage can be embedded inside a frame or iframe.

#### Recommended Value

```http
X-Frame-Options: DENY
```

#### Attack Scenario Without Protection

An attacker creates a malicious website that loads the legitimate application inside an invisible iframe.

Example:

```html
<iframe src="https://target-site.com"></iframe>
```

The attacker overlays deceptive content and tricks users into clicking hidden buttons.

#### Potential Consequences

- Unauthorized account actions
- Accidental purchases
- Permission changes
- Account compromise

---

### Content-Security-Policy (CSP)

#### Purpose

`Content-Security-Policy` restricts the sources from which scripts, styles, images, and other resources may be loaded.

#### Recommended Policy

```http
Content-Security-Policy: default-src 'self'
```

#### Benefits

- Prevents execution of unauthorized scripts
- Reduces the impact of XSS vulnerabilities
- Controls resource loading behavior
- Helps protect sensitive user data

#### Attack Scenario Without CSP

If an attacker successfully injects JavaScript through an XSS vulnerability, the browser may execute the malicious script.

Example:

```html
<script>
stealCookies();
</script>
```

#### Potential Consequences

- Session theft
- Account takeover
- Data exfiltration
- Credential theft
- Malware delivery

---

### X-Content-Type-Options

#### Purpose

Prevents browsers from MIME-sniffing content types.

#### Recommended Value

```http
X-Content-Type-Options: nosniff
```

#### Benefit

Reduces the risk of browsers incorrectly interpreting files as executable content.

---

### Referrer-Policy

#### Purpose

Controls how much referral information is shared with external websites.

#### Recommended Value

```http
Referrer-Policy: strict-origin-when-cross-origin
```

#### Benefit

Protects user privacy and prevents sensitive URL information from being leaked to third parties.

---

## Security Impact

If these issues remain unresolved, attackers may be able to:

- Gather sensitive server information
- Launch clickjacking attacks
- Exploit XSS vulnerabilities more effectively
- Steal session data
- Leak private information
- Deliver malicious content through embedded resources

---

## Conclusion

This challenge demonstrated the importance of secure application configuration and HTTP security headers. Disabling debug mode prevents information disclosure, while headers such as `X-Frame-Options`, `Content-Security-Policy`, `X-Content-Type-Options`, and `Referrer-Policy` provide additional layers of defense against common web attacks. Removing untrusted external content further reduces security risks and helps protect users from malicious activity.