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