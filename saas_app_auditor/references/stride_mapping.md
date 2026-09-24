# STRIDE Reference for Threat Modeling

Grounding reference for the `STRIDE Category` column when building a threat model from
a filled-out questionnaire. STRIDE has exactly six categories — every threat row must
use one of them, no invented variants.

| Category | Definition |
|---|---|
| **Spoofing** | An attacker assumes an identity that isn't theirs — stolen credentials, session hijacking, impersonating a trusted service or account |
| **Tampering** | Unauthorized modification of data, configuration, or system state |
| **Repudiation** | An action can't be reliably attributed or proven — missing/disableable logs, no audit trail |
| **Information Disclosure** | Sensitive data exposed to someone who shouldn't see it |
| **Denial of Service** | Legitimate use of the system is disrupted or blocked |
| **Elevation of Privilege** | An actor gains capabilities/access beyond what they should have |

## Deriving STRIDE from the questionnaire's MITRE Category

The questionnaire's `MITRE Category` column and its `Answer`/`Description/Abuse
Context` text are the input for this judgment call — there's no rigid 1:1 table,
because the same MITRE technique can threaten different STRIDE properties depending on
the specific scenario. Use this as a starting point, then adjust to the actual threat
described:

- **Initial Access** (Valid Accounts, Phishing, Trusted Relationship) → usually
  **Spoofing** (attacker impersonates a legitimate identity to get in)
- **Persistence** (Account Manipulation, Additional Cloud Roles/Credentials) → usually
  **Elevation of Privilege**, sometimes **Tampering** if the account/role change is
  the tampering act itself
- **Privilege Escalation** (Account Manipulation, Domain/Tenant Policy Modification) →
  **Elevation of Privilege**
- **Defense Evasion — Impair/Disable Logs** (T1562.008) → **Repudiation** (this is the
  clearest, most direct mapping in the whole list)
- **Defense Evasion — Modify Authentication Process** (T1556) → **Tampering** (of the
  auth process itself) or **Spoofing** (if the result is impersonation, e.g. MFA
  bypass)
- **Credential Access** (Brute Force, Unsecured Credentials, Steal Application Access
  Token) → **Spoofing** (the stolen/guessed credential is used to impersonate) or
  **Information Disclosure** (if the finding is about credentials being exposed,
  before any impersonation happens)
- **Discovery** → **Information Disclosure**
- **Collection**, **Exfiltration** → **Information Disclosure**
- **Impact — Data Destruction/Encrypted for Impact** → **Tampering** (the data is
  altered/destroyed) with a **Denial of Service** angle if availability is the harm
- **Impact — Service Stop** → **Denial of Service**
- **Command and Control** → context-dependent; often **Tampering** or **Information
  Disclosure** depending on what the C2 channel is being used for

## Not every questionnaire row becomes a threat row

Most rows map to exactly one threat. A few need judgment:
- **Split** a row into more than one threat-model row if the answer reveals distinct
  threats across different STRIDE categories (e.g. "no session timeout" can be both a
  Spoofing threat — hijacked session reused — and, if sessions grant broad access, an
  Elevation of Privilege consideration).
- **Fold into other rows rather than standing alone** the baseline questions that
  describe detection/response maturity in general rather than a specific threat —
  "crown jewels / SOC alerting priorities" and "admin's sense of anomalous activity."
  Their answers should inform the `Current Mitigation` and `Mitigation Status` text of
  the *other* rows they relate to (e.g. if the admin says bulk exports would trigger an
  alert, that strengthens the mitigation status of the Information Disclosure threat
  tied to bulk export). Only give them their own row if the answer surfaces a genuinely
  distinct, specific gap that isn't already covered elsewhere.
- **Data classification** ("what kind of data lives here") isn't a threat itself — it's
  context that should raise or lower the stakes described in other rows' `Threat` text
  (e.g. "...exposing regulated PHI" vs. "...exposing internal-only data"). Don't give
  it a standalone row.
