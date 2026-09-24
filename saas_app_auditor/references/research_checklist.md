# SaaS Application Research Checklist

Work through this checklist when researching a target SaaS application, before writing
any questionnaire rows. The goal is to ground every question in something real about
this specific app — its actual admin settings, known abuse patterns, and past
incidents — not generic cloud-security boilerplate.

## 1. Identity & Access
- SSO support (SAML/OIDC) and whether it can be enforced tenant-wide
- MFA support: which factors, whether it can be required for all users, whether it can
  be required for admins specifically, phishing-resistant options (passkeys/FIDO2)
- Password policy controls (if local auth is still allowed alongside SSO)
- Admin role model: is there granular RBAC, or only a blunt "admin vs. everyone" split
- Break-glass/emergency access accounts and how they're protected
- Session lifetime, idle timeout, and concurrent session controls
- Session/token revocation: can an admin kill active sessions on demand

## 2. OAuth Apps & Third-Party Integrations
- Does the platform have an app marketplace / OAuth app ecosystem
- Can users install third-party OAuth apps without admin approval (self-service consent)
- What scopes/permissions are available to OAuth apps (read-only vs. full data access)
- Is there an admin review/allowlist process for connected apps
- Historical incidents involving malicious or over-permissioned OAuth apps on this
  platform or its ecosystem (search for "<app name> OAuth app abuse", "<app name>
  malicious integration", "<app name> supply chain")

## 3. API & Service Accounts
- API key/token issuance model: personal tokens, service accounts, scoped keys
- Default token expiry and rotation support
- Rate limiting / anomaly detection on API usage
- Where tokens are commonly leaked in practice (CI/CD configs, public repos, chat)

## 4. Logging & Monitoring
- What admin/audit events are logged (login, permission changes, data export, config
  changes, OAuth app installs)
- Can logs be exported to a SIEM (API, webhook, syslog)
- Log retention period, and whether retention/export requires a premium tier
- Can audit logging itself be disabled or gapped by an admin (or attacker with admin
  rights) — this is the T1562.008 angle

## 5. Data Sharing & External Collaboration
- Default sharing posture for new content (private by default vs. org-wide vs. public
  link)
- External sharing / guest access controls, and whether they can be restricted by
  domain
- Bulk export/download controls (can any user export the full dataset)
- DLP or content-inspection features, if any

## 6. Network & Tenant Hardening
- IP allowlisting / conditional access by network location
- Domain verification and email domain capture (can anyone claim a workspace on your
  domain)
- Subdomain/tenant takeover history for this platform
- Support for customer-managed encryption keys, if relevant to the app's risk profile

## 7. Vendor Security Posture (background, not questionnaire fodder by itself)
- Vendor's trust/security center, SOC 2 / ISO 27001 status
- Published hardening guide or security best-practices doc
- CIS Benchmark, if one exists for this platform
- Public incident history: search "<app name> breach", "<app name> security incident",
  "<app name> CVE", and check recent SaaS-security vendor writeups (vendors like
  AppOmni, Obsidian Security, Adaptive Shield, Push Security regularly publish
  platform-specific abuse research)

## Research Output

For each area above where you found something concrete and specific to this app,
capture:
- The specific setting/control name (as the vendor names it, so the question sounds
  informed rather than generic)
- Why it matters (the abuse scenario)
- The MITRE tactic/technique it maps to (see `mitre_attack_categories.md`)
- A rough severity if left misconfigured

Skip areas where you can't find anything specific — a generic question not grounded in
this app's actual settings undermines the "credible conversation with admins" goal.
