# REPORT.md

# Challenge 1 – SQL Injection

## Task C – Explanation

SQL injection occurs when user input is directly concatenated into a SQL query. An attacker can insert SQL syntax that changes the intended query logic. This can allow bypassing authentication, reading data, or modifying records. Parameterized queries separate SQL code from user data. The database treats user input only as values and not executable SQL commands. This prevents attackers from injecting malicious SQL statements.

---

# Challenge 2 – The Comment Box That Bites Back (Stored XSS)

## Task C – Explanation

Reflected XSS occurs when malicious input is immediately returned in the server response and executed in the victim's browser. Stored XSS occurs when malicious code is permanently stored on the server and later executed when users view the content. This challenge demonstrated Stored XSS because the script was saved as a comment and executed whenever the page loaded. Stored XSS is generally more dangerous because it affects every user who views the page. Attackers can steal sessions, perform actions on behalf of users, or distribute malware.

---

# Challenge 3 – The Invoice Peek (IDOR)

## Task C – Explanation

Authentication verifies who a user is, while authorization determines what resources that user can access. In this challenge, Alice was successfully authenticated because the application knew she was logged in. However, the application did not verify whether Alice owned the requested invoice. As a result, Alice could access Bob's invoice by changing the URL. This is an Insecure Direct Object Reference (IDOR) vulnerability caused by missing authorization checks.

---

# Challenge 4 – Three Locks, All Broken

## Task C – Explanation

MD5 is considered insecure because it is extremely fast and vulnerable to brute-force and rainbow-table attacks. It also lacks built-in salting, making identical passwords produce identical hashes. Bcrypt and Argon2 are intentionally slow password hashing algorithms designed to resist large-scale cracking attempts. They automatically use salts and allow configurable cost factors that increase the computational effort required for each password guess. This makes password cracking significantly more difficult.

---

# Challenge 5 – Security Headers

## Task C – Explanation

### X-Frame-Options

X-Frame-Options prevents clickjacking attacks by stopping a page from being embedded inside a frame. Without this header, an attacker can place the application inside an invisible iframe and trick users into clicking hidden buttons. This could result in unauthorized actions being performed on behalf of the victim.

### Content-Security-Policy

Content-Security-Policy restricts the sources from which scripts, styles, and other resources can be loaded. Without CSP, attackers may inject malicious JavaScript through XSS vulnerabilities. This can lead to session theft, account compromise, or data exfiltration.
