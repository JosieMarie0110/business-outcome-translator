from textwrap import dedent


def build_outcome_prompt(
    company_name: str,
    company_description: str,
    capability_name: str,
    capability_description: str,
    operational_outcomes: list[str],
    business_values: list[str],
    audience_guidance: str,
    sample_message: str,
    customer_goal: str,
    customer_challenge: str,
    audience: str,
) -> str:
    return dedent(
        f"""
        You are a senior Customer Success Manager helping translate technical product capabilities into clear business outcomes and executive-friendly value narratives.

        Your job is to explain how a product capability helps a customer achieve a meaningful operational or business result. Focus on value realization, risk reduction, efficiency, visibility, adoption, or strategic impact where relevant.

        Company:
        {company_name}

        Company description:
        {company_description}

        Product capability:
        {capability_name}

        Capability description:
        {capability_description}

        Relevant operational outcomes:
        {", ".join(operational_outcomes) if operational_outcomes else "Not provided."}

        Relevant business values:
        {", ".join(business_values) if business_values else "Not provided."}

        Audience:
        {audience}

        Audience guidance:
        {audience_guidance or "Focus on clear business relevance."}

        Sample stakeholder message:
        {sample_message or "Not provided."}

        Customer goal:
        {customer_goal or "Not provided."}

        Customer challenge:
        {customer_challenge or "Not provided."}

        Write the response using these exact section headings:
        Operational Outcome
        Business Value
        Executive Narrative
        QBR Talking Point

        Requirements:
        - Translate the capability into business language, not just product language.
        - Do not repeat the customer goal or challenge word-for-word unless necessary.
        - Explain what operationally improves for the customer.
        - Tie the output to the customer's challenge, priorities, and desired outcomes.
        - Make the Business Value section specific and meaningful.
        - Make the Executive Narrative sound appropriate for leadership stakeholders.
        - Make the QBR Talking Point concise, polished, and customer-facing.
        - Keep the tone professional, strategic, and clear.
        - Avoid unnecessary jargon, fluff, and repetitive phrasing.
        - Do not use bullet points.
        - Keep each section concise but substantive.

        Good output should sound like something a Customer Success Manager, TAM, or account leader could actually use in an EBR, QBR, or executive update.
        """
    ).strip()


def build_fallback_outcome(
    capability_name: str,
    operational_outcomes: list[str],
    business_values: list[str],
    customer_goal: str,
    customer_challenge: str,
) -> str:
    op_outcome = (
        operational_outcomes[0]
        if operational_outcomes
        else "improves operational execution and visibility"
    )
    biz_value = (
        business_values[0]
        if business_values
        else "supports stronger business outcomes and risk reduction"
    )

    goal_text = customer_goal or "a key business priority"
    challenge_text = customer_challenge or "an identified operational challenge"

    return dedent(
        f"""
        Operational Outcome
        {capability_name} enables the customer to improve how they operate by supporting a capability that {op_outcome}.

        Business Value
        This creates business value by helping address {challenge_text} while supporting {biz_value}. It helps connect product capability to a clearer operational and strategic outcome.

        Executive Narrative
        By using {capability_name}, the customer is better positioned to support the goal of {goal_text}. This capability helps improve execution against an important business priority while strengthening the organization’s ability to operate more effectively.

        QBR Talking Point
        This capability helps advance the customer’s goal of {goal_text} by improving operational execution and delivering clearer business value against a meaningful priority.
        """
    ).strip()
