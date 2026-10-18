# C4 demo recording guide

1. In this folder, run `python app.py` and open the printed local URL.
2. Select `friendly_advisor` and ask: `Can you help with introductory Python?` Show the answer and the model/action/observation trace.
3. Select `careful_expert` and ask the same question. Compare wording and the tool trace.
4. Ask: `What is the exact hourly price?` Show that the agent uses a tool and does not invent a price.
5. Briefly show `PERSONAS`, `INSTRUCTIONS`, and the explicit `think -> act -> think -> finish` graph in `agent.py`.
6. Show `evaluation_results.md` when the live evaluation has completed.

The free Gemini tier can pause with a quota message. Wait about a minute before retrying. The app displays the tool trace for easy recording.
