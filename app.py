import sys
import pandas as pd
import gradio as gr
from pathlib import Path

# Add project root directory to path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config import get_groq_api_key
from src.vectorstore import format_sources
from src.engine import ai_analyst

def analyst_ui(question, api_key):
    """
    Gradio wrapper callback for AI Analyst.
    """
    if not question or not question.strip():
        return "⚠️ Please enter a question.", "", "", None, ""

    key_to_use = api_key.strip() if api_key and api_key.strip() else get_groq_api_key()
    
    if not key_to_use:
        return "❌ Error: Groq API Key is required. Please set GROQ_API_KEY environment variable or enter it in the API Key box.", "", "", None, ""

    try:
        result = ai_analyst(question, api_key=key_to_use)
        
        answer = result.get("answer", "No answer generated.")
        route = result.get("route", "")
        sql = result.get("sql", "")
        data = result.get("result", None)

        if not isinstance(data, pd.DataFrame):
            data = None

        sources = ""
        if result.get("sources"):
            sources = format_sources(result["sources"])

        route_label = f"🔀 Route Selected: {route}"
        if route == "SQL":
            route_label += " (Structured Database Query)"
        elif route == "RAG":
            route_label += " (PDF Vector Search)"
        elif route == "BOTH":
            route_label += " (Hybrid Data + Document Analysis)"

        return answer, route_label, sql, data, sources

    except Exception as e:
        return f"❌ Execution Error: {str(e)}", "ERROR", "", None, ""

# Custom Gradio Blocks UI Definition
with gr.Blocks(
    title="AI Analyst - Event Management Intelligence",
    theme=gr.themes.Soft(
        primary_hue="indigo",
        secondary_hue="purple"
    ),
    css="""
        .gradio-container { max-width: 1200px !important; margin: auto; }
        .header-box { text-align: center; margin-bottom: 20px; }
    """
) as demo:

    gr.Markdown(
        """
        <div class="header-box">
            <h1>🤖 AI Business Analyst</h1>
            <h3>Event Management Intelligence Assistant (Text-to-SQL + PDF RAG)</h3>
        </div>
        """
    )

    with gr.Row():
        with gr.Column(scale=3):
            question_input = gr.Textbox(
                label="Business Question",
                placeholder="e.g. Which city generated the highest revenue?",
                lines=3
            )
        with gr.Column(scale=1):
            api_key_input = gr.Textbox(
                label="Groq API Key (Optional if set in .env)",
                placeholder="gsk_...",
                type="password"
            )
            with gr.Row():
                ask_btn = gr.Button("🤖 Analyze", variant="primary")
                clear_btn = gr.Button("🗑️ Clear")

    gr.Markdown("---")

    with gr.Row():
        route_output = gr.Textbox(label="Analysis Route", interactive=False)

    with gr.Tabs():
        with gr.TabItem("🤖 AI Answer"):
            answer_output = gr.Markdown(label="Synthesized Answer")

        with gr.TabItem("💻 SQL Query"):
            sql_output = gr.Code(label="Generated SQL Query", language="sql", interactive=False)

        with gr.TabItem("📈 Data Table"):
            data_output = gr.Dataframe(label="Query Result Data", interactive=False)

        with gr.TabItem("📚 PDF Sources"):
            sources_output = gr.Markdown(label="Retrieved Document Citations")

    gr.Examples(
        examples=[
            ["Which city generated the highest revenue?"],
            ["List the top 3 vendors by rating and their contact details."],
            ["What are the vendor selection criteria?"],
            ["What are the key operational guidelines for venue setup?"],
            ["Which event type generates the most revenue and what strategy should management use?"],
            ["Identify high-revenue events with relatively low satisfaction."],
            ["Give management 5 recommendations based on the business data."]
        ],
        inputs=question_input
    )

    ask_btn.click(
        fn=analyst_ui,
        inputs=[question_input, api_key_input],
        outputs=[answer_output, route_output, sql_output, data_output, sources_output]
    )

    clear_btn.click(
        fn=lambda: ("", "", "", "", None, ""),
        inputs=[],
        outputs=[question_input, api_key_input, answer_output, route_output, sql_output, data_output, sources_output]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
