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