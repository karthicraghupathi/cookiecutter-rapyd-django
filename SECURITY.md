# Security Policy

## Supported versions

Only the latest commit on `main` is actively maintained. There are no versioned
release branches with backported security fixes.

## Reporting a vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Email **karthicr@gmail.com** with:

- A description of the vulnerability and its potential impact.
- Steps to reproduce or a proof-of-concept (if applicable).
- Any suggested mitigations you have in mind.

You should receive a response within 7 days. If the report is accepted, a fix will
be prepared and released as soon as practical, and you will be credited in the
changelog unless you prefer otherwise.

## Scope

This repo is a code-generation template. Security issues in the *generated* project
(e.g., insecure Django settings defaults, weak `SECRET_KEY` generation) are in scope.
Vulnerabilities in upstream dependencies (Django, environs, etc.) should be reported
to those projects directly.
