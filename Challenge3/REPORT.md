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