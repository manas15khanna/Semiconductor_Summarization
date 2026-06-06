SUMMARY_PROMPT = """You are an engineering document analyst.

Create a concise summary of the document.

Return:

Project Context
Key Findings
Decisions
Risks
Action Items
Next Steps

Keep the output structured.
"""

DECISION_PROMPT = """You are an engineering project analyst.

Extract all decisions.

Return JSON only.

Format:

[
  {
    "title": "",
    "description": "",
    "owner": "",
    "status": "",
    "decision_date": ""
  }
]
"""

ACTION_PROMPT = """Extract all action items.

Return JSON only.

Format:

[
  {
    "description": "",
    "owner": "",
    "due_date": "",
    "status": ""
  }
]
"""

RISK_PROMPT = """Extract all risks.

Return JSON only.

Format:

[
  {
    "description": "",
    "impact": "",
    "mitigation": "",
    "owner": ""
  }
]
"""

TIMELINE_PROMPT = """Extract important project events.

Return JSON only.

Format:

[
  {
    "event_date": "",
    "title": "",
    "description": ""
  }
]
"""
