# Business Outcome Translator

A lightweight tool that helps Customer Success Managers translate product capabilities into clear business outcomes and executive-ready value narratives.

Customer Success professionals often need to bridge the gap between technical capabilities and business value. This tool provides a simple interface that helps structure that translation by turning customer context and product capabilities into operational outcomes, business value statements, and leadership-ready messaging.

---

## Overview

One of the key responsibilities of a Customer Success Manager is the ability to connect product usage and technical initiatives to meaningful business outcomes.

Early-career CSMs often understand product features but struggle to communicate how those capabilities support customer goals, reduce risk, or improve operational efficiency. The Business Outcome Translator was designed to help structure that thinking.

The tool takes customer context, product capability, and audience type as inputs, then generates structured outcome narratives that can be used in:

- Executive updates
- QBR discussions
- Customer value storytelling
- Internal alignment conversations

---

## Features

- Translate product capabilities into operational outcomes
- Generate business value statements
- Create executive-ready narratives
- Produce QBR talking points
- Support multiple company product profiles via configurable JSON files


<img width="1755" height="1081" alt="image" src="https://github.com/user-attachments/assets/0f3cfc51-8ac9-49a4-b698-9dd9748362c3" />


---

## Example Workflow

### Customer Context Input

Customer Goal  
Improve visibility into network-connected devices and reduce security blind spots.

Customer Challenge  
The security team cannot reliably identify unmanaged devices connecting to the network.

Product Capability  
Asset Discovery

Audience  
Executive

---

### Generated Outcome Example

**Operational Outcome**

Continuous asset discovery improves visibility into connected devices and identifies unmanaged assets across the environment.

**Business Value**

Improved visibility reduces security risk associated with unknown devices and strengthens the organization’s ability to manage its attack surface.

**Executive Narrative**

By leveraging continuous asset discovery, the organization gains a clearer view of connected devices across the environment. This reduces operational uncertainty and strengthens overall security posture by ensuring unmanaged assets are quickly identified and addressed.

**QBR Talking Point**

Asset discovery initiatives support stronger enterprise visibility and reduce unmanaged asset risk, enabling security and operations teams to respond more effectively to emerging threats.

---

## Project Structure

business-outcome-translator

├── app.py
├── prompts.py
├── requirements.txt
├── README.md
│
└── company_profiles
  ├── forescout.json
  ├── company a
  └── company b


  
Company profiles define product capabilities and value language that the tool uses to generate outcomes.

This allows the same application to be reused across different vendors or product portfolios.

---

## Tech Stack

- Python  
- Gradio (UI framework)  
- OpenAI API  
- JSON configuration for company profiles  

---

## Running the Application

Clone the repository:

