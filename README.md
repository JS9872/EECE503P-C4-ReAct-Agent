# C4 - Custom ReAct Agent with Configurable Personas

**Joey Saade - 202305993**

## Use case

Harborlight Learning Studio is the fictional tutoring business from C3. The agent helps secondary school and first year university students choose a tutoring or study coaching service. Its audience includes students and parents. It can look up published business facts and suggest a service. It cannot confirm availability, prices, bookings, or outcomes.

## Design

`agent.py` implements the ReAct cycle as a LangGraph state machine: `think -> act -> think -> finish`. The `think` node asks the LLM for a JSON action or final answer; `route` detects an action; `act` executes a local tool and adds its observation to state; `finish` parses a final answer. The cycle stops after four model calls. This is a manually wired graph, not a prebuilt agent executor.

The `PERSONAS` block defines two distinct prompt styles and Gemini reasoning settings. The friendly advisor uses low thinking and a 1024 token cap; the careful expert uses medium thinking and a 1536 token cap. `INSTRUCTIONS` is a separate, focused block defining input, output format, limits, and a worked example. The four variants compare few shot vs. zero shot, an added private decision check, and system prompt vs. in-message instructions. The private decision check asks the model to choose its next step but does not expose chain of thought.

## Run

1. Install: `python -m pip install -r requirements.txt`
2. Get a free-tier key from [Google AI Studio](https://aistudio.google.com/app/apikey). Copy `.env.example` to `.env`, then replace `replace_with_your_key` with the key. Do not commit `.env`.
3. From `C4`, run `python agent.py "Can you help with Python?"`.
4. Run `python app.py` for the visual demo.
5. Run `python evaluate.py` to test 2 personas x 4 prompt variants x 3 questions. The outputs are `evaluation_live.jsonl` and `evaluation_results.md`.

The copied `business_summary.txt` makes this folder independently runnable while preserving the C3 use case.

## Evaluation and reflection

The experiment uses three cases: a programming fit, a study coaching fit, and an unknown price. `passes_keyword_check` is a quick automatic check; review each answer and trace manually for helpfulness, naturalness, factual support, and whether the tool was used. The live results file is generated only after an API key is supplied. No live comparison is claimed before running it.

The careful expert is expected to be more consistent for factual answers because it has more reasoning budget. The friendly advisor is expected to answer more quickly and naturally for discovery calls. These are hypotheses to check against live results, not measured findings. The tool trace should show a lookup before business claims. If the model repeatedly requests tools, the four-step cap prevents an endless loop. The separate instructions block should reduce invented prices and encourage a tool lookup; compare the variants to test whether it does. The main implementation challenge is turning free-form model output into a reliable action. JSON output, explicit action names, argument validation, and a bounded graph handle that risk.

## Files

- `agent.py`: persona settings, instructions, tools, and manual LangGraph loop
- `app.py`: optional interactive demo
- `evaluate.py`: repeatable live comparison
- `agent_personas.ipynb`: annotated notebook with setup, experiments, and reflection
