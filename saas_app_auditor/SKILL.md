---
name: saas-app-auditor
description: Use this skill when the user wants to audit a SaaS application's security posture or build an interview questionnaire for it — e.g. "audit our Salesforce instance," "build a security questionnaire for Slack," "help me prep for a security conversation with the Workday admins." Researches the specific SaaS app for real misconfigurations and admin-console controls, maps each risk to a MITRE ATT&CK tactic/technique, and outputs an interview-ready .xlsx questionnaire.
---

# SaaS App Auditor

Builds a security questionnaire for a specific SaaS application, meant to be used
live in a conversation with that app's technical admins/stakeholders to surface real
risk — not a generic compliance checklist. Every question should sound like it comes
from someone who has actually read this app's admin console documentation, and should
invite the admin to explain rather than answer yes/no.

Output is a single `.xlsx` file with columns, in this exact order:

`MITRE Category | Severity | Question | Answer | Description/Abuse Context`

`Answer` is always left blank — it's filled in live during the interview.

## Workflow

### 1. Confirm the target
Identify the specific SaaS application (e.g. "Salesforce," "Slack," "Workday," not
"our CRM"). If the user hasn't said which app, ask. If they've mentioned a specific
concern or scope (e.g. "focus on data exfiltration," "we just rolled out SSO"), note
it — it should bias which tactics get the most questions, not replace the general
audit.

### 2. Research the app
Read `references/research_checklist.md` and work through it using WebSearch/WebFetch.
Prioritize, in order:
1. The vendor's own security/trust center and admin/hardening documentation
2. CIS Benchmark for the app, if one exists
3. SaaS-security vendor research on this specific platform (AppOmni, Obsidian
   Security, Adaptive Shield, Push Security, and similar publish platform-specific
   abuse writeups — these are gold for realistic abuse context)
4. Public incident/breach history involving this app or its ecosystem (e.g. OAuth app
   supply-chain incidents, credential-stuffing campaigns)

Ground every questionnaire row in something concrete you found — an actual setting
name, an actual documented control, an actual real-world abuse pattern. Skip areas
where research turns up nothing specific; a generic, ungrounded question undermines
the "credible conversation with admins" goal and is worse than one fewer row.

### 3. Map each risk to MITRE ATT&CK
Read `references/mitre_attack_categories.md`. For each risk area from research, assign
a category formatted as `<Tactic> (<Technique ID>: <Technique Name>)`, e.g.
`Credential Access (T1110.003: Password Spraying)`. Use the tactic alone only if no
listed technique genuinely fits — don't force a technique ID onto something it doesn't
describe.

Weight coverage toward the techniques flagged in that reference as frequently seen in
real SaaS attacks. It's fine — expected, even — for several rows to land in the same
tactic (e.g. multiple Persistence questions on OAuth apps, MFA enforcement, and rogue
account creation) since that's where SaaS attackers concentrate.

Aim for breadth across tactics rather than a pile of questions in just one or two
categories, unless the user asked to focus narrowly.

### 4. Write the questions
Start from `references/baseline_questions.md` — its 16 topics are mandatory and must
appear in every questionnaire this skill produces, regardless of app or research
findings. Use its canonical phrasing, substituting in the app's actual feature/setting
names wherever research turned them up (e.g. "local username and password" becomes
"local email/password login" if that's literally what the app calls it). Its default
severities are a starting point — adjust based on what research reveals about this
specific app.

On top of those 16, add rows for whatever app-specific risks research surfaced. For
each additional risk area, write:
- **Question** — open-ended and conversational, phrased to invite an explanation
  ("Walk me through...", "Who can...", "What happens when...", "How would your team
  know if...") rather than a yes/no. Reference the app's actual setting/feature name
  so it's clear this is specific to their environment.
- **Severity** — `Critical`, `High`, `Medium`, or `Low`:
  - **Critical**: a gap here alone enables account takeover or mass data
    exfiltration, likely undetected (e.g. MFA not enforced tenant-wide, audit logging
    disabled/exportable-only-on-paid-tier-and-unused)
  - **High**: significant exposure, but needs one more condition or step to be
    catastrophic (e.g. unreviewed OAuth app scopes, no IP restrictions on admin
    console)
  - **Medium**: real but bounded exposure — needs an already-authenticated or
    insider position, or blast radius is limited (e.g. missing session timeout,
    overly broad default sharing for a low-sensitivity content type)
  - **Low**: hygiene/best-practice gap with low likelihood or low impact on its own
- **Description/Abuse Context** — 1-3 sentences: why this matters and, concretely, how
  an attacker would abuse the gap. Write for the person facilitating the interview,
  not the admin being interviewed — this is your talk-track.

The 16 baseline rows plus app-specific findings typically land around 25-40 rows total
for a full audit. Don't pad beyond what's grounded in research just to hit a number —
but don't drop below the 16 baseline rows either.

### 5. Assemble the input JSON
Write a JSON file matching `assets/questionnaire_schema_example.json`:
```json
{
  "app_name": "Example SaaS App",
  "rows": [
    {
      "mitre_category": "...",
      "severity": "High",
      "question": "...",
      "description": "..."
    }
  ]
}
```
Save it to a temp/scratch location (not the repo).

### 6. Generate the workbook
Run the script (installs `openpyxl` first if missing):
```
python -c "import openpyxl" 2>nul || pip install openpyxl
python scripts/generate_questionnaire.py --input <path-to-rows.json> --output "<AppName>_Security_Questionnaire.xlsx"
```
The script handles all formatting: bold header row, frozen header, autofilter,
per-severity color coding, wrapped text, and a dropdown data-validation list on the
Severity column. It does not invent or alter question content — if a row looks wrong,
fix the JSON and rerun rather than hand-editing the workbook's formatting logic.

### 7. Hand off
Tell the user where the file was written and give a one-line summary of coverage
(tactic spread, severity counts, anything you skipped due to lack of research
grounding). Offer to adjust scope, depth, or focus areas.

## Reference files
- `references/baseline_questions.md` — the 16 mandatory questions every questionnaire
  must include, with canonical phrasing, MITRE mapping, and default severity
- `references/mitre_attack_categories.md` — MITRE tactic/technique list to categorize
  against, with notes on which techniques are most frequently seen in SaaS attacks
- `references/research_checklist.md` — what to look for when researching a target app
- `assets/questionnaire_schema_example.json` — exact JSON shape the script expects
- `scripts/generate_questionnaire.py` — formats the researched rows into the final
  `.xlsx`

---

# Threat Model (from a filled-out questionnaire)

Builds a STRIDE-based threat model from a questionnaire produced by this skill and
subsequently filled out (the `Answer` column populated from the admin interview).
Output is a single `.xlsx` file with columns, in this exact order:

`STRIDE Category | System Component | Threat | Current Mitigation | Mitigation Status | Linked Tickets`

Unlike the questionnaire, every column here is filled in by Claude — there's no column
left blank for the user. `Linked Tickets` is left empty unless a ticket is explicitly
referenced in an answer; the user adds ticket references later as remediation work
gets tracked.

## Workflow

### 1. Read the filled-out questionnaire
```
python -c "import openpyxl" 2>nul || pip install openpyxl
python scripts/read_questionnaire.py --input "<path-to-filled-questionnaire.xlsx>"
```
This prints each row (MITRE Category, Severity, Question, Answer, Description/Abuse
Context) as JSON. It does no analysis — read the output yourself. If the `Answer`
column is empty for a row, that row can't produce a reliable threat yet; skip it and
note it to the user rather than guessing at an answer that wasn't given.

### 2. Derive STRIDE threats
Read `references/stride_mapping.md`. For each answered row:
- Assign one of the six STRIDE categories based on the actual threat described in the
  answer, not a mechanical lookup — the reference gives starting guidance from the
  row's MITRE Category, but the answer's specifics can shift which STRIDE property is
  really at risk.
- Most rows produce exactly one threat row. Split into multiple rows when an answer
  reveals genuinely distinct threats; fold detection-maturity rows (crown jewels, sense
  of anomalous activity) and the data-classification row into other threats' context
  rather than giving them their own row — see the reference for why.
- Write **System Component** as a short label for the affected part of the app (e.g.
  "Authentication / SSO," "OAuth App Marketplace," "Audit Logging," "API / Service
  Accounts," "Role & Permission Management") — use the app's actual terminology where
  the questionnaire's Description/Abuse Context or the original research named it.
- Write **Threat** as a concrete STRIDE-style statement: who/what could do what, and
  why the current setup allows it. Ground it in the specific answer, not a generic
  restatement of the question.
- Write **Current Mitigation** as a factual summary of what the answer said actually
  exists today — quote or closely paraphrase the admin's answer.
- Set **Mitigation Status** to one of: `Not Mitigated`, `Partially Mitigated`,
  `Mitigated`, `Risk Accepted`, `Unknown`. Use `Risk Accepted` only if the answer
  explicitly says the org has decided not to fix it; use `Unknown` only if the answer
  was too vague to judge, not as a default.
- Leave **Linked Tickets** empty unless the answer explicitly names a ticket ID.

### 3. Assemble the input JSON
Write a JSON file matching `assets/threat_model_schema_example.json`:
```json
{
  "app_name": "Example SaaS App",
  "rows": [
    {
      "stride_category": "Spoofing",
      "system_component": "...",
      "threat": "...",
      "current_mitigation": "...",
      "mitigation_status": "Partially Mitigated",
      "linked_tickets": ""
    }
  ]
}
```
Save it to a temp/scratch location (not the repo).

### 4. Generate the workbook
```
python scripts/generate_threat_model.py --input <path-to-threats.json> --output "<AppName>_Threat_Model.xlsx"
```
The script formats the workbook (bold frozen header, autofilter, wrapped text,
color-coded Mitigation Status, dropdown validation on STRIDE Category and Mitigation
Status) and validates STRIDE/status values — it doesn't invent or alter threat
content.

### 5. Hand off
Report the output path, a quick STRIDE-category and mitigation-status breakdown, and
call out any questionnaire rows you skipped because they had no answer yet.

## Reference files (threat model)
- `references/stride_mapping.md` — STRIDE definitions and guidance for deriving a
  category from a questionnaire row's MITRE Category and answer
- `assets/threat_model_schema_example.json` — exact JSON shape the script expects
- `scripts/read_questionnaire.py` — dumps a filled-out questionnaire `.xlsx` to JSON
- `scripts/generate_threat_model.py` — formats the derived threats into the final
  `.xlsx`
