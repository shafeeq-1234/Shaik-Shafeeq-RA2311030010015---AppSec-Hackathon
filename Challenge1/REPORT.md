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