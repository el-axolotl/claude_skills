# Baseline Questions (Always Include)

These 16 topics must appear in every questionnaire this skill produces, regardless of
which SaaS app is being audited. They're the questions that matter for almost any
SaaS platform's identity and data-governance posture, and they anchor the interview
even when app-specific research turns up little else.

Treat this as a floor, not a ceiling: app-specific rows from research (per
`research_checklist.md`) get added on top, and where research turned up the app's
actual setting/feature name, swap it into the question below so it reads as specific
to that app rather than generic. If nothing app-specific was found for a baseline
topic, ship the generic phrasing as-is — these should never be dropped for lack of
research.

Severity shown is a sensible default; adjust up or down based on what research reveals
about this specific app (e.g. bump "IP Allowlisting" to Low if the app is inherently
accessed from unmanaged devices everywhere and allowlisting isn't a realistic control).

| # | Topic | MITRE Category | Default Severity |
|---|-------|-----------------|-------------------|
| 1 | SSO vs. local auth | Initial Access (T1078.004: Valid Accounts - Cloud Accounts) | High |
| 2 | MFA enforcement | Credential Access (T1110: Brute Force) | Critical |
| 3 | Break-glass admin accounts | Initial Access (T1078.004: Valid Accounts - Cloud Accounts) | High |
| 4 | Shared user accounts | Initial Access (T1078.004: Valid Accounts - Cloud Accounts) | Medium |
| 5 | Session timeout / idle expiry | Persistence (T1550.004: Use Alternate Authentication Material - Web Session Cookie) | Medium |
| 6 | IP allowlisting | Initial Access (T1078.004: Valid Accounts - Cloud Accounts) | Medium |
| 7 | Least-privilege role design | Privilege Escalation (T1098: Account Manipulation) | High |
| 8 | Approval workflow for permission/role changes | Persistence (T1098.003: Account Manipulation - Additional Cloud Roles) | Medium |
| 9 | Offboarding automation | Initial Access (T1078.004: Valid Accounts - Cloud Accounts) | High |
| 10 | Quarterly user access reviews | Persistence (T1098.003: Account Manipulation - Additional Cloud Roles) | Medium |
| 11 | Active contractor accounts | Initial Access (T1199: Trusted Relationship) | Medium |
| 12 | API key rotation | Credential Access (T1552: Unsecured Credentials) | Medium |
| 13 | Audit logs to SIEM | Defense Evasion (T1562.008: Impair Defenses - Disable or Modify Cloud Logs) | High |
| 14 | Data classification in the app | Collection (T1530: Data from Cloud Storage) | Medium |
| 15 | Crown-jewels / SOC alerting priorities | Impact | High |
| 16 | Admin's sense of anomalous activity | Discovery | Medium |

## Canonical phrasing

Use these as the default question + abuse-context text. Customize the bracketed
portions with app-specific terms found during research (e.g. the app's actual name
for its SSO integration, admin console, or roles feature).

**1. SSO vs. local auth**
Q: "Is authentication handled entirely through SSO, or can users still sign in with a
local [app] username and password alongside it?"
D: Local/direct-login paths sit outside your SSO provider's conditional access, MFA
enforcement, and centralized deprovisioning — they're the accounts attackers target
first because they're invisible to identity-team controls.

**2. MFA enforcement**
Q: "Is MFA required for every account in [app], with no exceptions for admins,
service accounts, or accounts that predate the SSO rollout?"
D: Any account excluded from MFA enforcement is a standing gap; attackers actively
search for exactly these leftover accounts before attempting credential stuffing or
password spraying.

**3. Break-glass admin accounts**
Q: "Are there break-glass or emergency-access admin accounts for [app], and if so,
where are those credentials stored and who currently has access to them?"
D: Break-glass accounts are usually the highest-privileged, least-monitored accounts
in the tenant. If credentials are stored insecurely or access isn't tightly scoped,
they become a standing Valid Accounts vector with no MFA to stop it.

**4. Shared user accounts**
Q: "Are there any shared or generic user accounts in [app] — logins used by more than
one person or team?"
D: Shared accounts blur accountability (no way to attribute an action to a person),
multiply credential-leak exposure, and usually can't be cleanly offboarded when one of
the people sharing it leaves.

**5. Session timeout / idle expiry**
Q: "What are the session timeout and idle-expiry settings for [app], and do they apply
consistently across web, mobile, and API sessions?"
D: A stolen session token or cookie is only as dangerous as it is long-lived. Long or
unset session lifetimes turn a one-time token theft into extended, silent access.

**6. IP allowlisting**
Q: "Does [app] support restricting access by IP range or network location, and is that
enabled today?"
D: IP allowlisting doesn't stop a determined attacker, but it closes off the large
volume of opportunistic credential-stuffing and password-spraying traffic that never
originates from a trusted network.

**7. Least-privilege role design**
Q: "Walk me through how roles are structured in [app] — are they scoped to what each
job actually needs, or are people commonly given broader access than they use?"
D: Overly broad default roles mean a single compromised account (or one rogue insider)
already has the access an attacker would otherwise have to work to escalate into.

**8. Approval workflow for permission/role changes**
Q: "Is there a formal approval process before someone's permissions change or a new
role is created in [app], or can an admin make that change unilaterally?"
D: Without a second set of eyes, a compromised admin account — or a malicious insider
— can grant itself or others standing access that blends into normal admin activity
and goes unnoticed.

**9. Offboarding automation**
Q: "When someone leaves the company or changes teams, is their [app] access revoked
automatically, or does it depend on someone remembering to do it manually?"
D: Manual offboarding is where orphaned, still-active accounts come from — exactly the
kind of forgotten Valid Account an attacker (or a disgruntled former employee) can use
without triggering any alarms.

**10. Quarterly user access reviews**
Q: "Are user access levels in [app] formally reviewed on a recurring basis — quarterly
or otherwise — to catch permissions that should have been revoked?"
D: Access reviews are the backstop that catches everything the offboarding process and
approval workflow missed. Without them, privilege creep accumulates silently for
years.

**11. Active contractor accounts**
Q: "Are there any active contractor or third-party vendor accounts in [app] right now,
and how is their access scoped and time-limited?"
D: Contractor and third-party accounts are a classic Trusted Relationship vector —
often over-provisioned, rarely offboarded promptly, and a favorite target because
compromising one contractor can open a door into multiple client tenants.

**12. API key rotation**
Q: "How often are API keys or service-account credentials for [app] rotated, and is
that enforced automatically or left to whoever created the key?"
D: Long-lived, unrotated API keys are exactly what turns up leaked in a public repo,
CI/CD log, or old chat message years after anyone remembers they exist — and they
keep working until someone actively kills them.

**13. Audit logs to SIEM**
Q: "Are [app]'s audit logs being exported to your SIEM, and who would actually notice
if that export silently stopped working?"
D: If logging isn't centralized and monitored, an attacker with admin access can
disable or gap logging as one of their first moves, and every other control in this
questionnaire becomes unverifiable after the fact.

**14. Data classification in the app**
Q: "What kind of data actually lives in [app] — is there PII, PHI/HIPAA-regulated
data, financial data, or other regulated or sensitive information stored here?"
D: This sets the blast radius for everything else in the questionnaire. The same
misconfiguration is a minor finding in a tool with no sensitive data and a
reportable incident in one that holds regulated PII or PHI.

**15. Crown-jewels / SOC alerting priorities**
Q: "If you had to name the two or three operations in [app] that would be most
damaging if abused — mass export, bulk delete, a permission change, an integration
being added — what would they be, and does the SOC currently get alerted on any of
them?"
D: This directly identifies what should be instrumented for detection. It's common for
the single most damaging possible action in an app to have zero alerting on it simply
because no one framed it that way before.

**16. Admin's sense of anomalous activity**
Q: "As the person who knows this app best, what would activity in [app] have to look
like for it to feel wrong or suspicious to you?"
D: Admins often have an intuitive sense of "normal" that isn't written down anywhere or
reflected in any alert rule. This surfaces informal detection knowledge that should be
formalized — and reveals gaps where even the admin wouldn't notice an attack.
