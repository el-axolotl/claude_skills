# MITRE ATT&CK Reference for SaaS Audits

This is the grounding reference for the "MITRE Category" column. Use it instead of
inventing tactic/technique names from memory — pick from this list, and only cite a
technique ID here if it's actually applicable to the risk area you're documenting.

Format used in the questionnaire's `MITRE Category` column:

```
<Tactic> (<Technique ID>: <Technique Name>)
```

Example: `Credential Access (T1110.003: Password Spraying)`

If a risk area maps to a tactic but no single technique fits cleanly, the tactic name
alone is acceptable: `Defense Evasion`.

## The 14 Enterprise Tactics (MITRE ATT&CK)

1. **Reconnaissance** (TA0043)
2. **Resource Development** (TA0042)
3. **Initial Access** (TA0001)
4. **Execution** (TA0002)
5. **Persistence** (TA0003)
6. **Privilege Escalation** (TA0004)
7. **Defense Evasion** (TA0005)
8. **Credential Access** (TA0006)
9. **Discovery** (TA0007)
10. **Lateral Movement** (TA0008)
11. **Collection** (TA0009)
12. **Command and Control** (TA0011)
13. **Exfiltration** (TA0010)
14. **Impact** (TA0040)

## Techniques Most Frequently Seen in SaaS / Identity Attacks

These are the techniques that show up repeatedly in real-world SaaS breach reports
(Okta, Microsoft 365/Entra, Salesforce, Snowflake, Slack, GitHub, Drift/Salesloft,
Scattered Spider campaigns, etc.). Prioritize questionnaire rows that map to these —
they represent where attackers actually spend their effort against SaaS platforms.

### Initial Access (TA0001)
- **T1078.004** — Valid Accounts: Cloud Accounts (reused/stolen credentials, no MFA)
- **T1566.002** — Phishing: Spearphishing Link (credential harvesting pages)
- **T1199** — Trusted Relationship (compromise via a connected third-party vendor/app)
- **T1190** — Exploit Public-Facing Application (exposed admin panels, APIs)

### Persistence (TA0003)
- **T1098.001** — Account Manipulation: Additional Cloud Credentials (API keys, secondary auth added to an account)
- **T1098.003** — Account Manipulation: Additional Cloud Roles (privilege grants)
- **T1136.003** — Create Account: Cloud Account (rogue admin/service accounts)
- **T1556.006** — Modify Authentication Process: Multi-Factor Authentication (MFA downgrade/disable)
- **T1556.009** — Modify Authentication Process: Conditional Access Policies
- **T1550.001** — Use Alternate Authentication Material: Application Access Token (malicious OAuth app grants — a top SaaS attack vector)
- **T1550.004** — Use Alternate Authentication Material: Web Session Cookie (session/token theft, replay)

### Privilege Escalation (TA0004)
- **T1098** — Account Manipulation (role/permission escalation)
- **T1484** — Domain or Tenant Policy Modification (identity provider policy tampering)

### Defense Evasion (TA0005)
- **T1562.008** — Impair Defenses: Disable or Modify Cloud Logs (turning off audit logging)
- **T1556** — Modify Authentication Process (see above, also fits here)
- **T1070** — Indicator Removal (clearing activity/audit trails where permitted)

### Credential Access (TA0006)
- **T1110** — Brute Force (T1110.003 Password Spraying against SSO)
- **T1111** — Multi-Factor Authentication Interception
- **T1621** — Multi-Factor Authentication Request Generation (MFA fatigue/push bombing)
- **T1528** — Steal Application Access Token (OAuth token theft)
- **T1552** — Unsecured Credentials (API keys/secrets in code, config, chat, tickets)
- **T1589** — Gather Victim Identity Information (precursor recon, often via the SaaS app itself)

### Discovery (TA0007)
- **T1526** — Cloud Service Discovery (enumerating connected SaaS/integrations)
- **T1087.004** — Account Discovery: Cloud Account
- **T1069.003** — Permission Groups Discovery: Cloud Groups

### Collection (TA0009)
- **T1114.002** — Email Collection: Remote Email Collection (mailbox export/forwarding rules)
- **T1213.002** — Data from Information Repositories: Sharepoint
- **T1213.003** — Data from Information Repositories: Code Repositories
- **T1530** — Data from Cloud Storage (over-shared drives/buckets)

### Command and Control (TA0011)
- **T1102** — Web Service (abusing a trusted SaaS platform as a C2 channel)

### Exfiltration (TA0010)
- **T1567.002** — Exfiltration Over Web Service: Exfiltration to Cloud Storage
- **T1048** — Exfiltration Over Alternative Protocol

### Impact (TA0040)
- **T1485** — Data Destruction (mass delete via API/bulk tools)
- **T1486** — Data Encrypted for Impact (SaaS-native ransomware, e.g. mass file encryption via connected storage)
- **T1489** — Service Stop (deactivating tenant/security features)

## How to Use This When Building a Questionnaire

1. During research, tie every misconfiguration or hardening gap you find to one of the
   techniques above (or the closest tactic if no technique fits).
2. Favor risk areas that map to techniques in this list over obscure ones — the goal is
   to focus the conversation on what's actually being exploited in the wild.
3. It's fine for multiple questionnaire rows to map to the same tactic/technique — e.g.
   several Persistence questions (OAuth app consent, MFA enforcement, admin role
   creation) are expected and valuable.
4. Don't force-fit a technique ID that doesn't really apply. A correct tactic-only
   category beats a wrong technique ID.
