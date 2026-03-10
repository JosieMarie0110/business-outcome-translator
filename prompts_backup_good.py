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
        You are helping a Customer Success Manager translate product capabilities into business outcomes.

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

        Write the response with these exact sections:
        1. Operational Outcome
        2. Business Value
        3. Executive Narrative
        4. QBR Talking Point

        Requirements:
        - Translate the capability into business language.
        - Do not just restate the product feature.
        - Tie the output to the customer challenge and goal.
        - Keep the tone professional and customer-facing.
        - Avoid unnecessary jargon.
        """
    ).strip()


def build_fallback_outcome(
    capability_name: str,
    operational_outcomes: list[str],
    business_values: list[str],
    customer_goal: str,
    customer_challenge: str,
) -> str:
    op_outcome = operational_outcomes[0] if operational_outcomes else "supports a relevant operational improvement"
    biz_value = business_values[0] if business_values else "supports stronger business outcomes"

    return dedent(
        f"""
        Operational Outcome
        {capability_name} helps the customer by enabling a capability that {op_outcome}.

        Business Value
        This supports the customer’s goal by helping address the challenge of {customer_challenge or "an identified business issue"} and {biz_value}.

        Executive Narrative
        By using {capability_name}, the customer can better support the goal of {customer_goal or "improving business performance"} while addressing the challenge of {customer_challenge or "current operational limitations"}.

        QBR Talking Point
        This initiative helps connect product capability to a meaningful customer outcome by improving execution against a key business priority.
        """
    ).strip()
