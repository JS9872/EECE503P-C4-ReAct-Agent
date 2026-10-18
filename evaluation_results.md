# C4 live evaluation results

Joey Saade - 202305993

Model: `gemini-3.1-flash-lite` on the free tier. Cases: programming fit, study coaching fit, and unpublished hourly price. Each persona ran all four prompt variants on all three cases.

Final graph: **24/24** factual keyword checks and **24/24** tool-use checks. Baseline graph: **23/24** tool-use checks; one careful-expert answer skipped its tool. The final graph enforces a tool observation before an answer.

The keyword check initially missed valid variations of ?no fixed rate.? I reviewed all price answers and broadened the check to recognize those phrasings while still rejecting a stated dollar amount. These are small, task-specific checks, not a general quality benchmark.

| Persona | Prompt variant | Factual checks | Tool use | Mean answer words |
|---|---|---:|---:|---:|
| friendly_advisor | few_shot_system | 3/3 | 3/3 | 29.7 |
| friendly_advisor | zero_shot_system | 3/3 | 3/3 | 54.0 |
| friendly_advisor | brief_plan_system | 3/3 | 3/3 | 27.7 |
| friendly_advisor | in_message | 3/3 | 3/3 | 42.7 |
| careful_expert | few_shot_system | 3/3 | 3/3 | 32.7 |
| careful_expert | zero_shot_system | 3/3 | 3/3 | 37.3 |
| careful_expert | brief_plan_system | 3/3 | 3/3 | 35.0 |
| careful_expert | in_message | 3/3 | 3/3 | 28.3 |

## Interpretation

All setups handled the three test questions correctly after the tool-first guard was added. The friendly advisor used 38.5 words per answer on average and sounded more conversational in the discovery-call replies. The careful expert used 33.3 words per answer on average and was more direct. Few-shot system instructions and the brief-plan variant were the shortest on average (31.2 and 31.3 words); zero-shot responses were longest (45.7 words). With this small sample, there is no accuracy winner. I select the careful-expert few-shot system setup for factual guidance because it was concise, used tools in all three cases, and followed the worked example. The friendly advisor is preferable when a warmer tone is desired.

The baseline showed that prompt instructions alone did not always force tool use. The explicit graph guard changed the behavior from 23/24 to 24/24 tool-use checks in these runs. The main implementation challenges were parsing JSON actions and staying within free-tier request limits; JSON mode, a bounded graph, and paced evaluation addressed those issues.

## Full results

### friendly_advisor / few_shot_system / Can you help me with introductory Python?

Answer: Yes, I can certainly help with that! We offer introductory programming tutoring with our tutor Karim Nassar. Would you like to schedule a discovery call to discuss your goals?

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "lookup_business_fact",
      "argument": "introductory Python"
    }
  },
  {
    "phase": "tool",
    "name": "lookup_business_fact",
    "argument": "introductory Python",
    "observation": "Services include one to one mathematics and introductory programming tutoring, small exam preparation groups, and four week study coaching plans. The fictional team is Maya Haddad, learning director and mathematics tutor; Karim Nassar, introductory programming tutor; and Lina Farah, study coach."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "Yes, I can certainly help with that! We offer introductory programming tutoring with our tutor Karim Nassar. Would you like to schedule a discovery call to discuss your goals?"
    }
  }
]
```

### friendly_advisor / few_shot_system / I need a study plan. What fits?

Answer: I can definitely help with that. We offer a four-week study coaching plan designed to help you stay on track and organized. Would you be interested in learning more about how that works?

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "suggest_service",
      "argument": "study planning and academic coaching"
    }
  },
  {
    "phase": "tool",
    "name": "suggest_service",
    "argument": "study planning and academic coaching",
    "observation": "Possible fit: a four week study coaching plan."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "I can definitely help with that. We offer a four-week study coaching plan designed to help you stay on track and organized. Would you be interested in learning more about how that works?"
    }
  }
]
```

### friendly_advisor / few_shot_system / What is the exact hourly price?

Answer: I'm sorry, but specific hourly pricing isn't published. We confirm pricing and tutor availability directly with you after a discovery call. Would you like to schedule one?

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "lookup_business_fact",
      "argument": "pricing"
    }
  },
  {
    "phase": "tool",
    "name": "lookup_business_fact",
    "argument": "pricing",
    "observation": "Prices and tutor availability are confirmed after the call; no fixed prices or guarantees are published."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "I'm sorry, but specific hourly pricing isn't published. We confirm pricing and tutor availability directly with you after a discovery call. Would you like to schedule one?"
    }
  }
]
```

### friendly_advisor / zero_shot_system / Can you help me with introductory Python?

Answer: Hi there! I'd be happy to help. Based on your interest in learning Python, it sounds like our introductory programming tutoring service would be a great fit for you. We can walk through the fundamentals together. To make sure we're a perfect match for your specific goals, I recommend booking a discovery call where we can discuss the exact topics you're looking to cover. Let me know if you'd like more information on how to get started!

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "suggest_service",
      "argument": "introductory Python"
    }
  },
  {
    "phase": "tool",
    "name": "suggest_service",
    "argument": "introductory Python",
    "observation": "Possible fit: introductory programming tutoring. Confirm the exact topic during a discovery call."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "Hi there! I'd be happy to help. Based on your interest in learning Python, it sounds like our introductory programming tutoring service would be a great fit for you. We can walk through the fundamentals together. To make sure we're a perfect match for your specific goals, I recommend booking a discovery call where we can discuss the exact topics you're looking to cover. Let me know if you'd like more information on how to get started!"
    }
  }
]
```

### friendly_advisor / zero_shot_system / I need a study plan. What fits?

Answer: Hi! I'd be happy to help you with your studies. Based on what we offer, our four-week study coaching plan might be a great fit to help you build a personalized strategy. If you'd like to explore how that works, feel free to ask more!

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "suggest_service",
      "argument": "study plan"
    }
  },
  {
    "phase": "tool",
    "name": "suggest_service",
    "argument": "study plan",
    "observation": "Possible fit: a four week study coaching plan."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "Hi! I'd be happy to help you with your studies. Based on what we offer, our four-week study coaching plan might be a great fit to help you build a personalized strategy. If you'd like to explore how that works, feel free to ask more!"
    }
  }
]
```

### friendly_advisor / zero_shot_system / What is the exact hourly price?

Answer: I don't have a fixed hourly rate to share. Our specific pricing and tutor availability are determined during our initial consultation call. I'd be happy to help you get that scheduled so you can get the exact information you need!

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "lookup_business_fact",
      "argument": "pricing"
    }
  },
  {
    "phase": "tool",
    "name": "lookup_business_fact",
    "argument": "pricing",
    "observation": "Prices and tutor availability are confirmed after the call; no fixed prices or guarantees are published."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "I don't have a fixed hourly rate to share. Our specific pricing and tutor availability are determined during our initial consultation call. I'd be happy to help you get that scheduled so you can get the exact information you need!"
    }
  }
]
```

### friendly_advisor / brief_plan_system / Can you help me with introductory Python?

Answer: Yes, I can! Harborlight offers introductory programming tutoring. To make sure it's the right fit for your needs, would you like to schedule a discovery call?

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "suggest_service",
      "argument": "introductory programming"
    }
  },
  {
    "phase": "tool",
    "name": "suggest_service",
    "argument": "introductory programming",
    "observation": "Possible fit: introductory programming tutoring. Confirm the exact topic during a discovery call."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "Yes, I can! Harborlight offers introductory programming tutoring. To make sure it's the right fit for your needs, would you like to schedule a discovery call?"
    }
  }
]
```

### friendly_advisor / brief_plan_system / I need a study plan. What fits?

Answer: We offer a four-week study coaching plan that might be a great fit for your needs. Would you like to learn more about how it works?

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "suggest_service",
      "argument": "study plan"
    }
  },
  {
    "phase": "tool",
    "name": "suggest_service",
    "argument": "study plan",
    "observation": "Possible fit: a four week study coaching plan."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "We offer a four-week study coaching plan that might be a great fit for your needs. Would you like to learn more about how it works?"
    }
  }
]
```

### friendly_advisor / brief_plan_system / What is the exact hourly price?

Answer: Pricing and tutor availability are determined individually during our discovery call. We do not publish fixed hourly rates, but I would be happy to help you get started with a consultation.

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "lookup_business_fact",
      "argument": "pricing"
    }
  },
  {
    "phase": "tool",
    "name": "lookup_business_fact",
    "argument": "pricing",
    "observation": "Prices and tutor availability are confirmed after the call; no fixed prices or guarantees are published."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "Pricing and tutor availability are determined individually during our discovery call. We do not publish fixed hourly rates, but I would be happy to help you get started with a consultation."
    }
  }
]
```

### friendly_advisor / in_message / Can you help me with introductory Python?

Answer: Yes, I can certainly help with that! We offer one-to-one introductory programming tutoring with our tutor, Karim Nassar. Would you like to schedule a discovery call to learn more?

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "lookup_business_fact",
      "argument": "introductory Python"
    }
  },
  {
    "phase": "tool",
    "name": "lookup_business_fact",
    "argument": "introductory Python",
    "observation": "Services include one to one mathematics and introductory programming tutoring, small exam preparation groups, and four week study coaching plans. The fictional team is Maya Haddad, learning director and mathematics tutor; Karim Nassar, introductory programming tutor; and Lina Farah, study coach."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "Yes, I can certainly help with that! We offer one-to-one introductory programming tutoring with our tutor, Karim Nassar. Would you like to schedule a discovery call to learn more?"
    }
  }
]
```

### friendly_advisor / in_message / I need a study plan. What fits?

Answer: I'd be happy to help you get organized! We offer a four-week study coaching plan designed to create a structured approach to your learning. Would you like to hear more about how this plan works or schedule a time to chat about your goals?

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "suggest_service",
      "argument": "study planning"
    }
  },
  {
    "phase": "tool",
    "name": "suggest_service",
    "argument": "study planning",
    "observation": "Possible fit: a four week study coaching plan."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "I'd be happy to help you get organized! We offer a four-week study coaching plan designed to create a structured approach to your learning. Would you like to hear more about how this plan works or schedule a time to chat about your goals?"
    }
  }
]
```

### friendly_advisor / in_message / What is the exact hourly price?

Answer: I'd love to help with that! To ensure you get the most accurate information tailored to your specific needs, we discuss pricing and tutor availability directly during our discovery call. We don't publish fixed rates online, but I'm happy to help you get that conversation started. Would you like to schedule a time to chat?

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "lookup_business_fact",
      "argument": "pricing"
    }
  },
  {
    "phase": "tool",
    "name": "lookup_business_fact",
    "argument": "pricing",
    "observation": "Prices and tutor availability are confirmed after the call; no fixed prices or guarantees are published."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "I'd love to help with that! To ensure you get the most accurate information tailored to your specific needs, we discuss pricing and tutor availability directly during our discovery call. We don't publish fixed rates online, but I'm happy to help you get that conversation started. Would you like to schedule a time to chat?"
    }
  }
]
```

### careful_expert / few_shot_system / Can you help me with introductory Python?

Answer: Yes. Harborlight provides introductory programming tutoring that may accommodate your interest in Python. I recommend scheduling a discovery call to discuss your specific learning objectives and confirm the alignment of our curriculum with your goals.

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "suggest_service",
      "argument": "introductory Python"
    }
  },
  {
    "phase": "tool",
    "name": "suggest_service",
    "argument": "introductory Python",
    "observation": "Possible fit: introductory programming tutoring. Confirm the exact topic during a discovery call."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "Yes. Harborlight provides introductory programming tutoring that may accommodate your interest in Python. I recommend scheduling a discovery call to discuss your specific learning objectives and confirm the alignment of our curriculum with your goals."
    }
  }
]
```

### careful_expert / few_shot_system / I need a study plan. What fits?

Answer: Based on your needs, Harborlight offers a four-week study coaching plan designed to help students structure their academic progress. Would you like to schedule a discovery call to discuss how this fits your specific requirements?

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "suggest_service",
      "argument": "study plan"
    }
  },
  {
    "phase": "tool",
    "name": "suggest_service",
    "argument": "study plan",
    "observation": "Possible fit: a four week study coaching plan."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "Based on your needs, Harborlight offers a four-week study coaching plan designed to help students structure their academic progress. Would you like to schedule a discovery call to discuss how this fits your specific requirements?"
    }
  }
]
```

### careful_expert / few_shot_system / What is the exact hourly price?

Answer: Harborlight does not publish fixed hourly rates. Pricing and tutor availability are confirmed following a discovery call. Would you like to schedule one to discuss your specific needs?

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "lookup_business_fact",
      "argument": "pricing"
    }
  },
  {
    "phase": "tool",
    "name": "lookup_business_fact",
    "argument": "pricing",
    "observation": "Prices and tutor availability are confirmed after the call; no fixed prices or guarantees are published."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "Harborlight does not publish fixed hourly rates. Pricing and tutor availability are confirmed following a discovery call. Would you like to schedule one to discuss your specific needs?"
    }
  }
]
```

### careful_expert / zero_shot_system / Can you help me with introductory Python?

Answer: Harborlight Learning Studio provides one-to-one introductory programming tutoring, which encompasses support for Python. I recommend contacting the studio directly to discuss your specific learning requirements and objectives.

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "lookup_business_fact",
      "argument": "tutoring services"
    }
  },
  {
    "phase": "tool",
    "name": "lookup_business_fact",
    "argument": "tutoring services",
    "observation": "Harborlight Learning Studio is a fictional Beirut based tutoring and study coaching service. Services include one to one mathematics and introductory programming tutoring, small exam preparation groups, and four week study coaching plans."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "Harborlight Learning Studio provides one-to-one introductory programming tutoring, which encompasses support for Python. I recommend contacting the studio directly to discuss your specific learning requirements and objectives."
    }
  }
]
```

### careful_expert / zero_shot_system / I need a study plan. What fits?

Answer: For your academic needs, we offer a four-week study coaching plan. This service is designed to help you organize your coursework and develop structured study habits. While this program provides a framework for progress, please understand that individual student outcomes depend on the consistent application of these strategies. Please let me know if you would like more information on the structure of this coaching plan.

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "suggest_service",
      "argument": "study plan"
    }
  },
  {
    "phase": "tool",
    "name": "suggest_service",
    "argument": "study plan",
    "observation": "Possible fit: a four week study coaching plan."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "For your academic needs, we offer a four-week study coaching plan. This service is designed to help you organize your coursework and develop structured study habits. While this program provides a framework for progress, please understand that individual student outcomes depend on the consistent application of these strategies. Please let me know if you would like more information on the structure of this coaching plan."
    }
  }
]
```

### careful_expert / zero_shot_system / What is the exact hourly price?

Answer: The business does not publish fixed hourly prices. Specific pricing and tutor availability are confirmed during the initial consultation call.

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "lookup_business_fact",
      "argument": "pricing"
    }
  },
  {
    "phase": "tool",
    "name": "lookup_business_fact",
    "argument": "pricing",
    "observation": "Prices and tutor availability are confirmed after the call; no fixed prices or guarantees are published."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "The business does not publish fixed hourly prices. Specific pricing and tutor availability are confirmed during the initial consultation call."
    }
  }
]
```

### careful_expert / brief_plan_system / Can you help me with introductory Python?

Answer: Yes, our firm provides one-to-one introductory programming tutoring, which includes support for Python. Our dedicated tutor for this subject is Karim Nassar. If you would like to explore your specific learning objectives, I can assist you in scheduling a discovery call.

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "lookup_business_fact",
      "argument": "introductory programming"
    }
  },
  {
    "phase": "tool",
    "name": "lookup_business_fact",
    "argument": "introductory programming",
    "observation": "Services include one to one mathematics and introductory programming tutoring, small exam preparation groups, and four week study coaching plans. The fictional team is Maya Haddad, learning director and mathematics tutor; Karim Nassar, introductory programming tutor; and Lina Farah, study coach."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "Yes, our firm provides one-to-one introductory programming tutoring, which includes support for Python. Our dedicated tutor for this subject is Karim Nassar. If you would like to explore your specific learning objectives, I can assist you in scheduling a discovery call."
    }
  }
]
```

### careful_expert / brief_plan_system / I need a study plan. What fits?

Answer: Harborlight offers a four-week study coaching plan designed to help students organize their academic goals and develop effective habits. Would you like to schedule a discovery call to discuss if this fits your specific requirements?

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "suggest_service",
      "argument": "study plan"
    }
  },
  {
    "phase": "tool",
    "name": "suggest_service",
    "argument": "study plan",
    "observation": "Possible fit: a four week study coaching plan."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "Harborlight offers a four-week study coaching plan designed to help students organize their academic goals and develop effective habits. Would you like to schedule a discovery call to discuss if this fits your specific requirements?"
    }
  }
]
```

### careful_expert / brief_plan_system / What is the exact hourly price?

Answer: Harborlight does not publish fixed hourly rates. Pricing and tutor availability are determined individually following a discovery call. Would you like to schedule one to discuss your specific needs?

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "lookup_business_fact",
      "argument": "pricing"
    }
  },
  {
    "phase": "tool",
    "name": "lookup_business_fact",
    "argument": "pricing",
    "observation": "Prices and tutor availability are confirmed after the call; no fixed prices or guarantees are published."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "Harborlight does not publish fixed hourly rates. Pricing and tutor availability are determined individually following a discovery call. Would you like to schedule one to discuss your specific needs?"
    }
  }
]
```

### careful_expert / in_message / Can you help me with introductory Python?

Answer: Yes, we offer introductory programming tutoring, which includes support for Python. Would you like to schedule a discovery call to discuss your learning goals?

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "lookup_business_fact",
      "argument": "introductory Python"
    }
  },
  {
    "phase": "tool",
    "name": "lookup_business_fact",
    "argument": "introductory Python",
    "observation": "Services include one to one mathematics and introductory programming tutoring, small exam preparation groups, and four week study coaching plans. The fictional team is Maya Haddad, learning director and mathematics tutor; Karim Nassar, introductory programming tutor; and Lina Farah, study coach."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "Yes, we offer introductory programming tutoring, which includes support for Python. Would you like to schedule a discovery call to discuss your learning goals?"
    }
  }
]
```

### careful_expert / in_message / I need a study plan. What fits?

Answer: Harborlight offers a four-week study coaching plan designed to assist students with structure and goal setting. Would you like to schedule a discovery call to discuss how this aligns with your specific needs?

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "suggest_service",
      "argument": "study plan"
    }
  },
  {
    "phase": "tool",
    "name": "suggest_service",
    "argument": "study plan",
    "observation": "Possible fit: a four week study coaching plan."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "Harborlight offers a four-week study coaching plan designed to assist students with structure and goal setting. Would you like to schedule a discovery call to discuss how this aligns with your specific needs?"
    }
  }
]
```

### careful_expert / in_message / What is the exact hourly price?

Answer: I cannot provide an exact hourly rate. According to our business profile, pricing and tutor availability are finalized following a discovery call. No fixed prices are publicly listed.

Factual check: True; tool used: True

Trace:

```json
[
  {
    "phase": "model",
    "decision": {
      "action": "lookup_business_fact",
      "argument": "pricing"
    }
  },
  {
    "phase": "tool",
    "name": "lookup_business_fact",
    "argument": "pricing",
    "observation": "Prices and tutor availability are confirmed after the call; no fixed prices or guarantees are published."
  },
  {
    "phase": "model",
    "decision": {
      "answer": "I cannot provide an exact hourly rate. According to our business profile, pricing and tutor availability are finalized following a discovery call. No fixed prices are publicly listed."
    }
  }
]
```
