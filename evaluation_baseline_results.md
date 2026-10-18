# Baseline evaluation before tool-first graph guard

Model: `gemini-3.1-flash-lite`. The same 24 questions were run before the graph enforced a tool observation.

Factual keyword checks: **24/24**. Tool use: **23/24**. The careful expert answered one price question without a tool, prompting the graph fix.

| Persona | Variant | Factual checks | Tool use |
|---|---|---:|---:|
| friendly_advisor | few_shot_system | 3/3 | 3/3 |
| friendly_advisor | zero_shot_system | 3/3 | 3/3 |
| friendly_advisor | brief_plan_system | 3/3 | 3/3 |
| friendly_advisor | in_message | 3/3 | 3/3 |
| careful_expert | few_shot_system | 3/3 | 2/3 |
| careful_expert | zero_shot_system | 3/3 | 3/3 |
| careful_expert | brief_plan_system | 3/3 | 3/3 |
| careful_expert | in_message | 3/3 | 3/3 |

## Skipped-tool case

Question: What is the exact hourly price?

Answer: Harborlight Learning Studio does not publish fixed hourly rates. Pricing and tutor availability are confirmed following a discovery call, as they are tailored to individual requirements.

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "answer": "Harborlight Learning Studio does not publish fixed hourly rates. Pricing and tutor availability are confirmed following a discovery call, as they are tailored to individual requirements."
    }
  }
]
```