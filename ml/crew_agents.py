"""
TruthLens CrewAI 4-agent analysis — researcher, fact-checker, analyst, report-writer.

Used for deep-dive analysis of news/claims. Optional for MVP.
"""

from __future__ import annotations

from typing import Any

# from crewai import Agent, Task, Crew
# import os


def create_crew() -> Any:
    """Create Crew with researcher, fact-checker, analyst, report-writer agents."""
    raise NotImplementedError("CrewAI Crew + 4 agents, OpenAI API key from env")


def run_analysis(topic: str, crew: Any) -> str:
    """Run multi-agent analysis and return report."""
    raise NotImplementedError("Crew.kickoff or sequential tasks")
