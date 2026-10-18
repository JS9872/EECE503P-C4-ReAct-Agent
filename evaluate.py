"""Run live persona and prompt experiments; writes evaluation_live.jsonl."""
import json
import re
import time
from pathlib import Path

from agent import PERSONAS, ask
from google.genai.errors import ClientError

CASES = [
    {"question": "Can you help me with introductory Python?", "expected": "programming"},
    {"question": "I need a study plan. What fits?", "expected": "study coaching"},
    {"question": "What is the exact hourly price?", "expected": "unavailable"},
]
VARIANTS = ("few_shot_system", "zero_shot_system", "brief_plan_system", "in_message")


def score(answer: str, expected: str) -> bool:
    lower = answer.lower()
    if expected == "unavailable":
        says_unknown = any(term in lower for term in ("not published", "not listed", "does not publish", "unavailable", "don't know", "do not know", "confirm"))
        invented_amount = bool(re.search(r"(?:\$|usd\s*)\d|\d+\s*(?:dollars|usd)\b", lower))
        return says_unknown and not invented_amount
    return expected in lower


def main():
    path = Path(__file__).with_name("evaluation_live.jsonl")
    rows = []
    for persona in PERSONAS:
        for variant in VARIANTS:
            for case in CASES:
                while True:
                    try:
                        result = ask(case["question"], persona, variant)
                        break
                    except ClientError as error:
                        if error.code != 429:
                            raise
                        print("Free-tier rate limit reached; waiting 35 seconds before retry.", flush=True)
                        time.sleep(35)
                row = {"persona": persona, "variant": variant, **case, **result,
                       "passes_keyword_check": score(result["answer"], case["expected"]),
                       "used_tool": any(item["phase"] == "tool" for item in result["trace"])}
                rows.append(row)
                print(persona, variant, case["question"], row["passes_keyword_check"], row["used_tool"], flush=True)
                time.sleep(27)
    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")
    report = ["# Live evaluation results", "", "Joey Saade - 202305993", "",
              "Keyword checks are screening aids; inspect answers and traces before drawing conclusions.", "",
              "| Persona | Prompt variant | Keyword checks | Tool use |", "|---|---|---:|---:|"]
    for persona in PERSONAS:
        for variant in VARIANTS:
            group = [row for row in rows if row["persona"] == persona and row["variant"] == variant]
            report.append(f"| {persona} | {variant} | {sum(row['passes_keyword_check'] for row in group)}/3 | {sum(row['used_tool'] for row in group)}/3 |")
    report += ["", "## Full results", ""]
    for row in rows:
        report += [f"### {row['persona']} / {row['variant']} / {row['question']}", "",
                   f"Answer: {row['answer']}", "",
                   f"Keyword check: {row['passes_keyword_check']}; tool used: {row['used_tool']}", "",
                   "Trace:", "", "```json", json.dumps(row["trace"], indent=2, ensure_ascii=False), "```", ""]
    path.with_name("evaluation_results.md").write_text("\n".join(report), encoding="utf-8")
    print(f"Saved {len(rows)} live trials to {path}")


if __name__ == "__main__":
    main()
