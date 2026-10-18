# C4 - Custom ReAct Agent with Configurable Personas

**Joey Saade - 202305993**

## Use case

Harborlight Learning Studio is the fictional tutoring business from C3. The agent helps secondary school and first year university students choose a tutoring or study coaching service. Its audience includes students and parents. It can look up published business facts and suggest a service. It cannot confirm availability, prices, bookings, or outcomes.

## Design

`agent.py` implements the ReAct cycle as a LangGraph state machine: `think -> act -> think -> finish`. The `think` node asks the LLM for a JSON action or final answer; `route` detects an action; `act` executes a local tool and adds its observation to state; `finish` parses a final answer. The cycle stops after four model calls. This is a manually wired graph, not a prebuilt agent executor.

The `PERSONAS` block defines two distinct prompt styles and Gemini reasoning settings. The friendly advisor uses low thinking and a 1024 token cap; the careful expert uses medium thinking and a 1536 token cap. `INSTRUCTIONS` is a separate, focused block defining input, output format, limits, and a worked example. The four variants compare few shot vs. zero shot, an added private decision check, and system prompt vs. in-message instructions. The private decision check asks the model to choose its next step but does not expose chain of thought.

The default model is the free-tier `gemini-3.1-flash-lite`. The persona configurations vary its supported `thinking_level` and `max_output_tokens` settings.

## Run

1. Install: `python -m pip install -r requirements.txt`
2. Get a free-tier key from [Google AI Studio](https://aistudio.google.com/app/apikey). Copy `.env.example` to `.env`, then replace `replace_with_your_key` with the key. Do not commit `.env`.
3. From `C4`, run `python agent.py "Can you help with Python?"`.
4. Run `python app.py` for the visual demo.
5. Run `python evaluate.py` to test 2 personas x 4 prompt variants x 3 questions. The outputs are `evaluation_live.jsonl` and `evaluation_results.md`.

The copied `business_summary.txt` makes this folder independently runnable while preserving the C3 use case.

## Evaluation and reflection

The live experiment used three cases: a programming fit, a study coaching fit, and an unpublished price. It ran 2 personas x 4 prompt variants x 3 cases on `gemini-3.1-flash-lite`. The final graph achieved **24/24** task-specific factual checks and **24/24** tool-use checks. The baseline graph achieved **23/24** tool-use checks: the careful expert once answered the price question without a tool. Adding a tool-first graph guard fixed that failure in the second run. Read [evaluation_results.md](evaluation_results.md) for the table, interpretation, answers, and traces; [evaluation_baseline_results.md](evaluation_baseline_results.md) records the earlier failure.

The friendly advisor sounded warmer and used 38.5 words per answer on average; the careful expert was more direct at 33.3. All eight persona/variant combinations handled the small test set correctly, so the experiment did not establish an accuracy winner. For factual advising I select the careful expert with few-shot system instructions: it was concise, followed the worked example, and used tools in all three final cases. The friendly advisor is a better fit for a discovery conversation. Few-shot and brief-plan responses averaged about 31 words, while zero-shot responses averaged 45.7 words. The separate instructions and tool-first guard made the evidence path visible and consistent. The largest challenges were reliable JSON action parsing and free-tier rate limits; JSON mode, a bounded graph, and paced testing addressed them. These results are limited to three questions, so the keyword check is not a general quality measure.

## Files

- `agent.py`: persona settings, instructions, tools, and manual LangGraph loop
- `app.py`: optional interactive demo
- `evaluate.py`: repeatable live comparison
- `evaluation_live.jsonl` and `evaluation_results.md`: final live results
- `evaluation_baseline.jsonl` and `evaluation_baseline_results.md`: earlier run before the tool-first guard
- `agent_personas.ipynb`: annotated notebook with setup, experiments, and reflection
