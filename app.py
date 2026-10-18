"""Gradio demo for the C4 LangGraph ReAct agent."""
import gradio as gr
from google.genai.errors import ClientError
from agent import PERSONAS, ask


def respond(question, persona, variant):
    try:
        result = ask(question, persona, variant)
        return result["answer"], "\n".join(
            f"{item['phase']}: {item.get('name', item.get('decision'))} -> {item.get('observation', '')}"
            for item in result["trace"])
    except ClientError as error:
        if error.code == 429:
            return "The free Gemini quota is temporarily full. Please wait about a minute and try again.", ""
        return f"Gemini error: {error.message}", ""
    except Exception as error:
        return f"Error: {error}", ""


with gr.Blocks(title="Harborlight ReAct Advisor") as demo:
    gr.Markdown("# Harborlight ReAct Advisor\nCompare two personas and inspect the action/observation trace.")
    question = gr.Textbox(label="Student question")
    persona = gr.Dropdown(choices=list(PERSONAS), value="friendly_advisor", label="Persona")
    variant = gr.Dropdown(choices=["few_shot_system", "zero_shot_system",
                                   "brief_plan_system", "in_message"],
                          value="few_shot_system", label="Prompt variant")
    button = gr.Button("Ask")
    answer = gr.Textbox(label="Answer")
    trace = gr.Textbox(label="ReAct trace", lines=8)
    button.click(respond, [question, persona, variant], [answer, trace])

if __name__ == "__main__":
    demo.launch()
