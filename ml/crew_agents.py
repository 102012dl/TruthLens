"""
TruthLens CrewAI 4-agent analysis — researcher, fact-checker, analyst, report-writer.

Sequential process: News Researcher → Fact Checker → Trend Analyst → Report Writer.
Uses GPT-4o-mini, temperature=0.2. Optional for MVP.
"""

from __future__ import annotations

from typing import Any

from crewai import Agent, Crew, LLM, Process, Task


# Shared LLM for all agents (GPT-4o-mini, temperature=0.2)
_TRUTHLENS_LLM = LLM(model="gpt-4o-mini", temperature=0.2)


def _news_researcher(llm: LLM) -> Agent:
    return Agent(
        role="News Researcher",
        goal="Find 5–10 relevant, diverse news articles and sources on the given topic.",
        backstory=(
            "You are an experienced news researcher. You identify high-signal articles, "
            "avoid echo chambers, and prioritize authoritative and varied sources."
        ),
        llm=llm,
        allow_delegation=False,
    )


def _fact_checker(llm: LLM) -> Agent:
    return Agent(
        role="Fact Checker",
        goal="Verify claims and rate credibility of sources and statements on a 1–10 scale.",
        backstory=(
            "You are a meticulous fact checker. You cross-reference claims, "
            "assess source reliability, and assign clear credibility scores (1–10)."
        ),
        llm=llm,
        allow_delegation=False,
    )


def _trend_analyst(llm: LLM) -> Agent:
    return Agent(
        role="Trend Analyst",
        goal="Identify patterns, trends, and insights across the collected news and fact-checks.",
        backstory=(
            "You are a strategic analyst. You spot narratives, biases, and emerging patterns "
            "and summarize them in a structured way for the report writer."
        ),
        llm=llm,
        allow_delegation=False,
    )


def _report_writer(llm: LLM) -> Agent:
    return Agent(
        role="Report Writer",
        goal="Compile a clear, analytical report in Ukrainian for the reader.",
        backstory=(
            "You are a professional report writer. You turn research, fact-checks, and trends "
            "into a well-structured Ukrainian-language analytical report with clear sections."
        ),
        llm=llm,
        allow_delegation=False,
    )


def create_crew(llm: LLM | None = None) -> Crew:
    """Create Crew with 4 agents and sequential process.

    Args:
        llm: Optional LLM; if not set, uses GPT-4o-mini with temperature=0.2.

    Returns:
        Configured Crew (News Researcher → Fact Checker → Trend Analyst → Report Writer).
    """
    model = llm or _TRUTHLENS_LLM

    researcher = _news_researcher(model)
    fact_checker = _fact_checker(model)
    trend_analyst = _trend_analyst(model)
    report_writer = _report_writer(model)

    research_task = Task(
        description=(
            "Find 5–10 relevant news articles or sources about the topic: {topic}. "
            "List each with title, source, date (if known), and a short summary. "
            "Prioritize variety and credibility of sources."
        ),
        expected_output=(
            "A structured list of 5–10 relevant articles/sources: for each, title, "
            "source, date, and a brief summary. Clear and scannable format."
        ),
        agent=researcher,
    )

    fact_check_task = Task(
        description=(
            "Using the research context provided, verify the main claims and rate "
            "credibility of each source and key statement. Assign a credibility score "
            "from 1 (low) to 10 (high) with brief justification for each."
        ),
        expected_output=(
            "Fact-check summary: for each major claim/source, credibility score 1–10 "
            "and short justification. Highlight any red flags or high-confidence facts."
        ),
        agent=fact_checker,
        context=[research_task],
    )

    trend_task = Task(
        description=(
            "Using the research and fact-check context, identify patterns, recurring "
            "narratives, possible biases, and key insights. Summarize trends and "
            "notable findings for the final report."
        ),
        expected_output=(
            "Structured trend analysis: main patterns, narrative themes, bias indicators, "
            "and 3–5 key insights. Concise and ready for the report writer."
        ),
        agent=trend_analyst,
        context=[research_task, fact_check_task],
    )

    report_task = Task(
        description=(
            "Using all previous context (research, fact-checks, trends), compile a "
            "full analytical report in Ukrainian. Include: executive summary, key facts, "
            "credibility assessment, trends and insights, and recommendations. "
            "Write only in Ukrainian, use clear headings and bullet points."
        ),
        expected_output=(
            "A complete analytical report in Ukrainian: summary, facts, credibility, "
            "trends, and recommendations. Markdown formatting, professional tone."
        ),
        agent=report_writer,
        context=[research_task, fact_check_task, trend_task],
        markdown=True,
    )

    return Crew(
        agents=[researcher, fact_checker, trend_analyst, report_writer],
        tasks=[research_task, fact_check_task, trend_task, report_task],
        process=Process.sequential,
    )


def run_analysis(topic: str, crew: Crew | None = None) -> str:
    """Run multi-agent analysis and return the final report.

    Args:
        topic: News topic, headline, or claim to analyze.
        crew: Optional pre-built Crew; if None, one is created with create_crew().

    Returns:
        Final analytical report string (Ukrainian, from Report Writer).

    Raises:
        ValueError: If topic is empty.
    """
    if not topic or not str(topic).strip():
        raise ValueError("Topic must be a non-empty string.")

    if crew is None:
        crew = create_crew()

    result: Any = crew.kickoff(inputs={"topic": topic})

    # CrewOutput or similar: final task output is the report
    if hasattr(result, "raw") and result.raw is not None:
        return str(result.raw)
    if hasattr(result, "output") and result.output is not None:
        return str(result.output)
    if hasattr(result, "tasks") and result.tasks:
        last = result.tasks[-1]
        if hasattr(last, "output") and last.output:
            return str(last.output)
        if hasattr(last, "result") and last.result:
            return str(last.result)
    return str(result)
