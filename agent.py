"""C4: a manual ReAct cycle modeled as a LangGraph state machine."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Annotated, Literal, TypedDict

from dotenv import load_dotenv
from google import genai
from google.genai import types
from langgraph.graph import END, StateGraph

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
PROFILE = (ROOT / "business_summary.txt").read_text(encoding="utf-8")

# Goal: advise prospective Harborlight students using the published business facts.
# Audience: secondary school and first year university students and their families.
# Constraints: no invented prices, booking status, availability, or guarantees.
# Tools: lookup_business_fact and suggest_service. They are local, deterministic tools.
PERSONAS = {
    "friendly_advisor": {
        "persona": "You are Noor, an approachable study advisor. Use warm, plain language and concise suggestions.",
        "thinking_level": "low", "max_output_tokens": 1024,
    },
    "careful_expert": {
        "persona": "You are Dr. Sami, a precise academic advisor. Use measured language and short evidence-based explanations.",
        "thinking_level": "medium", "max_output_tokens": 1536,
    },
}

INSTRUCTIONS = """You receive a user question, a business profile, and observations from tools.
Return exactly one JSON object: either {"action":"lookup_business_fact","argument":"topic"},
{"action":"suggest_service","argument":"student need"}, or {"answer":"final reply"}.
Use a tool before answering any question about business facts or service fit.
Use only tool observations as evidence for business claims.
If the observation lacks an answer, state that the detail is unavailable.
Never claim a booking was made or guarantee a student outcome.
Keep the final answer under 120 words.
Example: User: Do you teach Python? Output: {"action":"lookup_business_fact","argument":"introductory programming"}.
After observation: "Introductory programming tutoring is offered", output:
{"answer":"Yes. Harborlight offers introductory programming tutoring. Would you like a discovery call?"}
Do not reveal hidden reasoning; a tool request or final answer is sufficient."""

TOOL_DESCRIPTIONS = """Available tools:
- lookup_business_fact(topic): returns relevant lines from the published business summary.
- suggest_service(need): matches a student need to a listed service; gives no availability or price."""


def lookup_business_fact(topic: str) -> str:
    terms = [term for term in topic.lower().split() if len(term) > 3]
    sentences = [s.strip() for s in PROFILE.replace("\n", " ").split(".") if s.strip()]
    matches = [s for s in sentences if any(term in s.lower() for term in terms)]
    return ". ".join(matches[:3]) + ("." if matches else "") if matches else "No published fact found."


def suggest_service(need: str) -> str:
    lower = need.lower()
    if any(word in lower for word in ("python", "code", "program", "software")):
        return "Possible fit: introductory programming tutoring. Confirm the exact topic during a discovery call."
    if any(word in lower for word in ("math", "calculus", "algebra")):
        return "Possible fit: one to one mathematics tutoring or a small exam preparation group."
    if any(word in lower for word in ("study", "habit", "plan", "organize")):
        return "Possible fit: a four week study coaching plan."
    return "No clear service match. Offer a free 20 minute discovery call to discuss the need."


def _merge(left: list, right: list) -> list:
    return left + right


class State(TypedDict):
    question: str
    persona: str
    prompt_variant: str
    observations: Annotated[list[str], _merge]
    trace: Annotated[list[dict], _merge]
    step: int
    decision: dict
    answer: str


def build_graph(client=None):
    """Explicit model -> action -> observation -> model loop, with a step limit."""
    client = client or genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def think(state: State) -> dict:
        selected = PERSONAS[state["persona"]]
        variant = state.get("prompt_variant", "few_shot_system")
        rules = INSTRUCTIONS if variant != "zero_shot_system" else INSTRUCTIONS.split("Example:")[0]
        if variant == "brief_plan_system":
            rules += "\nReason step by step internally about which tool is needed before selecting the JSON response. Do not print the reasoning."
        base = f"{selected['persona']}\n\nINSTRUCTIONS:\n{rules}\n\n{TOOL_DESCRIPTIONS}"
        content = f"Business profile:\n{PROFILE}\n\nUser question: {state['question']}\n"
        if state["observations"]:
            content += "\nTool observations:\n" + "\n".join(state["observations"])
        if variant == "in_message":
            content = base + "\n\n" + content
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite"), contents=content,
            config=types.GenerateContentConfig(
                system_instruction=None if variant == "in_message" else base,
                response_mime_type="application/json",
                thinking_config=types.ThinkingConfig(thinking_level=(
                    "medium" if variant == "brief_plan_system" else selected["thinking_level"])),
                max_output_tokens=selected["max_output_tokens"]))
        raw = response.text or "{}"
        try:
            decision = json.loads(raw)
        except json.JSONDecodeError:
            decision = {"answer": "I could not interpret the response. Please try again."}
        return {"decision": decision, "step": state["step"] + 1,
                "trace": [{"phase": "model", "decision": decision}]}

    def route(state: State) -> Literal["act", "finish"]:
        decision = state["decision"]
        if state["step"] >= 4 or decision.get("action") not in ("lookup_business_fact", "suggest_service"):
            return "finish"
        return "act"

    def act(state: State) -> dict:
        decision = state["decision"]
        name, argument = decision["action"], str(decision.get("argument", ""))
        observation = (lookup_business_fact(argument) if name == "lookup_business_fact"
                       else suggest_service(argument))
        return {"observations": [f"{name}({argument!r}): {observation}"],
                "trace": [{"phase": "tool", "name": name, "argument": argument,
                           "observation": observation}]}

    def finish(state: State) -> dict:
        decision = state["decision"]
        answer = decision.get("answer")
        if not isinstance(answer, str) or not answer.strip():
            answer = "I could not confirm that detail from the published profile. Please ask the team during a discovery call."
        return {"answer": answer}

    graph = StateGraph(State)
    graph.add_node("think", think)
    graph.add_node("act", act)
    graph.add_node("finish", finish)
    graph.set_entry_point("think")
    graph.add_conditional_edges("think", route, {"act": "act", "finish": "finish"})
    graph.add_edge("act", "think")
    graph.add_edge("finish", END)
    return graph.compile()


def ask(question: str, persona: str = "friendly_advisor", variant: str = "few_shot_system",
        client=None) -> dict:
    if persona not in PERSONAS:
        raise ValueError(f"Unknown persona: {persona}")
    if variant not in ("few_shot_system", "zero_shot_system", "brief_plan_system", "in_message"):
        raise ValueError(f"Unknown variant: {variant}")
    state = {"question": question, "persona": persona, "prompt_variant": variant,
             "observations": [], "trace": [], "step": 0, "decision": {}, "answer": ""}
    result = build_graph(client).invoke(state)
    return {"answer": result["answer"], "trace": result["trace"],
            "persona": persona, "variant": variant}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument("--persona", choices=PERSONAS, default="friendly_advisor")
    parser.add_argument("--variant", choices=["few_shot_system", "zero_shot_system",
                                              "brief_plan_system", "in_message"],
                        default="few_shot_system")
    args = parser.parse_args()
    print(json.dumps(ask(args.question, args.persona, args.variant), indent=2))
