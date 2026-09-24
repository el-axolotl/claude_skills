# SaaS App Auditor

A Claude skill that helps you uncover security risk in a SaaS application you choose,
by researching that app and crafting a technical questionnaire and a follow-on threat
model — both meant to drive a real conversation with the app's technical admins or
stakeholders, not to serve as a generic compliance checklist. Point it at an app (e.g.
Snowflake, Okta, Salesforce, Slack) and it researches real misconfigurations and
admin-console controls for that specific platform, maps each risk to MITRE ATT&CK,
and produces an interview-ready `.xlsx` questionnaire. Once that questionnaire comes
back filled out from the interview, the skill can turn the answers into a STRIDE-based
threat model tracking what's mitigated and what isn't.

## Folder structure

```
saas_app_auditor/
├── SKILL.md                                 # Skill instructions Claude follows
├── README.md                                # This file
├── assets/
│   ├── questionnaire_schema_example.json    # Input shape for the questionnaire generator
│   └── threat_model_schema_example.json     # Input shape for the threat model generator
├── references/
│   ├── baseline_questions.md                # 16 questions every questionnaire must include
│   ├── mitre_attack_categories.md           # MITRE ATT&CK tactics/techniques reference
│   ├── research_checklist.md                # What to research about a target SaaS app
│   └── stride_mapping.md                    # STRIDE reference for building threat models
└── scripts/
    ├── generate_questionnaire.py            # Formats researched rows into the .xlsx questionnaire
    ├── read_questionnaire.py                # Dumps a filled-out questionnaire .xlsx to JSON
    └── generate_threat_model.py             # Formats derived threats into the .xlsx threat model
```

## Installation

These steps assume you're setting this up in Claude for the first time.

1. **Clone this repo:**
   ```
   git clone https://github.com/el-axolotl/claude_skills.git
   ```
2. **Locate the skill folder** — it's `claude_skills/saas_app_auditor`. This is the
   folder you'll upload; the rest of the repo is not needed by Claude.
3. **Zip the skill folder** so `SKILL.md` sits at the top level of the archive (not
   nested inside another folder). On Windows/PowerShell:
   ```powershell
   Compress-Archive -Path "claude_skills\saas_app_auditor" -DestinationPath "saas_app_auditor.zip"
   ```
4. **Enable code execution in Claude** (one-time prerequisite):
   - Free/Pro/Max: go to **Settings > Capabilities** and turn on **Code execution and
     file creation**.
   - Team/Enterprise: an org owner must enable this in **Organization settings >
     Plugins & skills** under the Policy tab.
5. **Upload the skill:**
   - Go to **Customize > Skills**.
   - Click the **+** button, then **+ Create skill**.
   - Choose **Upload a skill** and select `saas_app_auditor.zip`.
6. **Toggle it on** — the skill appears in your skills list after upload; flip the
   switch next to it to enable it.

## How to use it

Once enabled, just describe what you want in plain language — Claude will follow
`SKILL.md` to research the app, build the questionnaire, and/or generate the threat
model.

**Build a questionnaire for a specific app:**
> Build a SaaS security questionnaire for Snowflake.

> I need a security audit questionnaire for Okta so I can run through it with their
> admin team next week — we just rolled out SSO and I want to make sure it's actually
> enforced everywhere.

Either prompt produces a `.xlsx` with columns `MITRE Category | Severity | Question |
Answer | Description/Abuse Context`, with `Answer` left blank for you to fill in live
during the interview.

**Build a threat model from a filled-out questionnaire:**
> I filled out the Snowflake questionnaire during our call with their admins —
> here's `Snowflake_Security_Questionnaire.xlsx`. Build a threat model from it.

This produces a `.xlsx` with columns `STRIDE Category | System Component | Threat |
Current Mitigation | Mitigation Status | Linked Tickets`, derived entirely from the
answers you captured.
