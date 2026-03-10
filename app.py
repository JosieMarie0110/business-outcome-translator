import json
import os
import gradio as gr
from openai import OpenAI
from prompts import build_outcome_prompt, build_fallback_outcome

APP_TITLE = "Business Outcome Translator"
APP_SUBTITLE = "Translate product capabilities into business outcomes and customer-facing value narratives."

PROFILE_DIR = "company_profiles"

CUSTOM_CSS = """
body, .gradio-container {
    background: #edf3fb !important;
}

.gradio-container {
    max-width: 1600px !important;
    width: 95% !important;
    margin: 0 auto !important;
    padding-top: 22px !important;
    padding-bottom: 24px !important;
}

#app-title {
    text-align: center;
    margin-bottom: 2px;
}

#app-subtitle {
    text-align: center;
    color: #52657d;
    margin-bottom: 24px;
    font-size: 16px;
}

.panel {
    background: white;
    border: 1px solid #d8e4f2;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}

textarea, input {
    border-radius: 12px !important;
}

button.primary-btn {
    background: #2f6fdd !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
}

button.secondary-btn {
    border-radius: 12px !important;
    font-weight: 600 !important;
}

.output-box textarea {
    font-size: 15px !important;
    line-height: 1.7 !important;
}

footer {
    visibility: hidden !important;
}
"""


def get_profile_files():
    if not os.path.exists(PROFILE_DIR):
        return []
    return sorted([f for f in os.listdir(PROFILE_DIR) if f.endswith(".json")])


def load_profile(filename):
    path = os.path.join(PROFILE_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_capability_names(profile):
    return [cap["name"] for cap in profile.get("product_capabilities", [])]


def update_capabilities(profile_file):
    if not profile_file:
        return gr.update(choices=[], value=None)
    profile = load_profile(profile_file)
    capabilities = get_capability_names(profile)
    default_value = capabilities[0] if capabilities else None
    return gr.update(choices=capabilities, value=default_value)


def find_capability(profile, capability_name):
    for cap in profile.get("product_capabilities", []):
        if cap.get("name") == capability_name:
            return cap
    return None


def generate_outcome(profile_file, customer_goal, customer_challenge, capability_name, audience):
    if not profile_file:
        return "Please select a company profile."

    profile = load_profile(profile_file)
    capability = find_capability(profile, capability_name)

    if not capability:
        return "Please select a valid product capability."

    company_name = profile.get("company_name", "")
    company_description = profile.get("company_description", "")
    audience_messages = profile.get("default_audience_messages", {})
    audience_guidance = audience_messages.get(audience, "")
    sample_message = capability.get("sample_stakeholder_messages", {}).get(audience, "")

    prompt = build_outcome_prompt(
        company_name=company_name,
        company_description=company_description,
        capability_name=capability.get("name", ""),
        capability_description=capability.get("description", ""),
        operational_outcomes=capability.get("operational_outcomes", []),
        business_values=capability.get("business_values", []),
        audience_guidance=audience_guidance,
        sample_message=sample_message,
        customer_goal=(customer_goal or "").strip(),
        customer_challenge=(customer_challenge or "").strip(),
        audience=audience,
    )

    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if not api_key:
        return build_fallback_outcome(
            capability_name=capability.get("name", ""),
            operational_outcomes=capability.get("operational_outcomes", []),
            business_values=capability.get("business_values", []),
            customer_goal=(customer_goal or "").strip(),
            customer_challenge=(customer_challenge or "").strip(),
        )

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            temperature=0.2,
        )
        return response.output_text.strip()
    except Exception as exc:
        return f"Error generating outcome:\n\n{exc}"


def clear_form():
    return "", "", None, "Executive", ""


profile_files = get_profile_files()
default_profile = profile_files[0] if profile_files else None
default_profile_data = load_profile(default_profile) if default_profile else {}
default_capabilities = get_capability_names(default_profile_data)
default_capability = default_capabilities[0] if default_capabilities else None

with gr.Blocks(title=APP_TITLE, css=CUSTOM_CSS) as demo:
    gr.Markdown(f"# {APP_TITLE}", elem_id="app-title")
    gr.Markdown(APP_SUBTITLE, elem_id="app-subtitle")

    with gr.Row():
        with gr.Column(scale=6):
            with gr.Group(elem_classes=["panel"]):
                gr.Markdown("### Customer Context")

                customer_goal = gr.Textbox(
                    label="Customer Goal",
                    lines=4,
                    placeholder="Example: Improve network security visibility and reduce unmanaged asset risk.",
                )

                customer_challenge = gr.Textbox(
                    label="Customer Challenge",
                    lines=6,
                    placeholder="Example: The customer has limited visibility into unmanaged devices connecting to the network.",
                )

        with gr.Column(scale=5):
            with gr.Group(elem_classes=["panel"]):
                gr.Markdown("### Product and Audience")

                profile_dropdown = gr.Dropdown(
                    choices=profile_files,
                    value=default_profile,
                    label="Company Profile",
                )

                capability_dropdown = gr.Dropdown(
                    choices=default_capabilities,
                    value=default_capability,
                    label="Product Capability",
                )

                audience_dropdown = gr.Dropdown(
                    choices=["Executive", "Security", "Operations"],
                    value="Executive",
                    label="Audience",
                )

                with gr.Row():
                    generate_btn = gr.Button("Generate Business Outcome", elem_classes=["primary-btn"])
                    clear_btn = gr.Button("Clear", elem_classes=["secondary-btn"])

    with gr.Row():
        with gr.Column():
            with gr.Group(elem_classes=["panel"]):
                gr.Markdown("### Outcome Draft")
                output = gr.Textbox(
                    label=None,
                    lines=20,
                    placeholder="Generated outcome language will appear here...",
                    elem_classes=["output-box"],
                )

    profile_dropdown.change(
        fn=update_capabilities,
        inputs=[profile_dropdown],
        outputs=[capability_dropdown],
    )

    generate_btn.click(
        fn=generate_outcome,
        inputs=[profile_dropdown, customer_goal, customer_challenge, capability_dropdown, audience_dropdown],
        outputs=[output],
    )

    clear_btn.click(
        fn=clear_form,
        inputs=[],
        outputs=[customer_goal, customer_challenge, capability_dropdown, audience_dropdown, output],
    )

if __name__ == "__main__":
    demo.launch()
