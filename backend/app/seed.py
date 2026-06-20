"""
seed.py — Hardcoded BARS competency data, coaching tips, and archetype defaults.

This module contains all the standardized behavioral interview content
derived from the Staffinc Standardized Vetting Framework.
"""

# ---------------------------------------------------------------------------
# BARS Questions — one per competency
# ---------------------------------------------------------------------------
BARS_QUESTIONS: dict[str, str] = {
    "communication": (
        "Tell me about a time you had to explain a complex technical concept "
        "or process to a non-technical stakeholder. How did you structure your "
        "explanation, and how did you verify they understood?"
    ),
    "adaptability": (
        "Describe a situation where a project or priority suddenly changed "
        "directions due to unexpected circumstances. How did you react, and "
        "what actions did you take to adjust?"
    ),
    "collaboration": (
        "Tell me about a time you had to work with a colleague or stakeholder "
        "whose personality or working style was vastly different from yours. "
        "How did you manage the relationship to achieve success?"
    ),
    "problem_solving": (
        "Give me an example of a complex, ambiguous problem you encountered "
        "where there was no clear template or guideline to follow. How did you "
        "dissect the problem and arrive at a solution?"
    ),
    "leadership": (
        "Tell me about a time you noticed an inefficiency, risk, or "
        "opportunity in your project or team and took initiative to address it "
        "without being formally asked. What was the outcome?"
    ),
}

# ---------------------------------------------------------------------------
# BARS Anchors — behavioral descriptions for scoring 1, 3, 5
# ---------------------------------------------------------------------------
BARS_ANCHORS: dict[str, dict[int, str]] = {
    "communication": {
        5: (
            "Communicates top-down, starting with the main conclusion. "
            "Uses clear analogies to simplify complexity. Actively listens, "
            "pauses for feedback, and validates understanding."
        ),
        3: (
            "Delivers a structured, easy-to-follow story (e.g., STAR format). "
            "Uses professional language. Answers the question directly."
        ),
        1: (
            "Answers are disorganized, rambling, or missing key context. "
            "Relies heavily on technical jargon without explaining it. "
            "Struggles to maintain logical flow."
        ),
    },
    "adaptability": {
        5: (
            "Welcomes change proactively. Instantly pivots plans, manages own "
            "stress, and helps others align with the new direction. Focuses "
            "immediately on next steps and solutions."
        ),
        3: (
            "Accepts changes without resistance. Adjusts schedule or tasks "
            "accordingly. Delivers expected quality despite the pivot."
        ),
        1: (
            "Becomes visibly frustrated or paralyzed by change. Complains or "
            "clings to the old process. Fails to deliver work due to the "
            "disruption."
        ),
    },
    "collaboration": {
        5: (
            "Proactively seeks to understand the other person's perspective. "
            "Uses conflict-resolution techniques (e.g., finding common "
            "ground). Puts team success above personal ego."
        ),
        3: (
            "Maintains a polite, professional relationship. Communicates "
            "constructively to resolve differences. Delivers their part of "
            "the group workload."
        ),
        1: (
            "Avoids contact, becomes defensive, or blames the colleague. "
            "Refuses to compromise, causing project delays or toxic team "
            "dynamics."
        ),
    },
    "problem_solving": {
        5: (
            "Gathers facts systematically from multiple sources. Breaks down "
            "complex variables into manageable parts. Proposes multiple "
            "hypotheses and verifies the best solution with data."
        ),
        3: (
            "Uses logic and resourcefulness to solve standard problems. "
            "Escalates appropriately when blocked. Reaches a functional, "
            "working solution."
        ),
        1: (
            "Relies on guesswork or repeats past mistakes. Gives up easily or "
            "experiences analysis paralysis. Proposes solutions that do not "
            "solve the root cause."
        ),
    },
    "leadership": {
        5: (
            "Demonstrates extreme ownership. Spots a systemic issue, proposes "
            "a concrete solution, and rallies others to execute it without "
            "formal mandate."
        ),
        3: (
            "Takes responsibility for their assigned tasks. Speaks up when "
            "they see a problem. Suggests improvements during retrospects."
        ),
        1: (
            "Passive attitude ('not my job'). Ignores obvious problems. "
            "Requires constant supervision and prompting to complete basic "
            "tasks."
        ),
    },
}

# ---------------------------------------------------------------------------
# Coaching tips — per archetype, per competency
# ---------------------------------------------------------------------------
COACHING_TIPS: dict[str, dict[str, list[str]]] = {
    "consulting": {
        "communication": [
            "Structure answers top-down using the Minto Pyramid Principle: lead with the conclusion, then supporting arguments.",
            "Use formal, diplomatic language. Avoid slang and overly casual phrasing.",
            "Pause after key points and ask if the interviewer would like you to elaborate.",
        ],
        "adaptability": [
            "Frame changes as opportunities to demonstrate structured risk assessment.",
            "Highlight how you communicated the change to stakeholders with a clear plan.",
            "Emphasize maintaining quality and process discipline despite the pivot.",
        ],
        "collaboration": [
            "Focus on consensus-building and managing diverse senior stakeholders.",
            "Demonstrate respect for organizational protocols and hierarchies.",
            "Show how you navigated differing opinions diplomatically.",
        ],
        "problem_solving": [
            "Use structured frameworks like MECE (Mutually Exclusive, Collectively Exhaustive).",
            "Walk through your analysis step-by-step, showing rigorous methodology.",
            "Present multiple options with a clear recommendation backed by data.",
        ],
        "leadership": [
            "Emphasize influence through data and persuasion, not just authority.",
            "Show examples of driving cross-functional alignment on complex initiatives.",
            "Highlight how you managed stakeholder expectations proactively.",
        ],
    },
    "startup": {
        "communication": [
            "Be direct, transparent, and concise. Get to the point quickly.",
            "Value honesty about failures — demonstrate 'fail fast, learn fast' mentality.",
            "Show comfort with high-frequency, informal status updates (Slack-style).",
        ],
        "adaptability": [
            "Highlight times you thrived with zero guidance and constantly shifting priorities.",
            "Show comfort with ambiguity and making decisions with incomplete information.",
            "Demonstrate speed of execution — how quickly you pivoted and shipped.",
        ],
        "collaboration": [
            "Show examples of wearing multiple hats and stepping outside your role.",
            "Emphasize flat communication — talking directly to anyone in the org.",
            "Demonstrate scrappy teamwork: unblocking yourself and others rapidly.",
        ],
        "problem_solving": [
            "Value scrappy, 'good enough' solutions over perfect but slow analysis.",
            "Show rapid prototyping: build → test → iterate instead of plan → plan → plan.",
            "Demonstrate resourcefulness with limited tools, budget, or time.",
        ],
        "leadership": [
            "Show extreme ownership — you saw a problem and just fixed it.",
            "Highlight times you wore multiple hats and operated with zero guidance.",
            "Demonstrate bias for action: shipping over perfecting.",
        ],
    },
}

# ---------------------------------------------------------------------------
# Practice questions — per archetype
# ---------------------------------------------------------------------------
PRACTICE_QUESTIONS: dict[str, list[str]] = {
    "consulting": [
        "Walk me through a complex project you managed. How did you structure the approach and communicate progress to senior stakeholders?",
        "Describe a time you had to explain a highly technical solution to a non-technical executive. How did you simplify it?",
        "Tell me about a situation where you had to push back on a client or stakeholder diplomatically. How did you handle it?",
    ],
    "startup": [
        "Describe a time you built something quickly with very limited resources. What tradeoffs did you make?",
        "Tell me about a time you had to make a major decision with incomplete information. What did you do?",
        "Give an example of when you took ownership of something completely outside your job description. What happened?",
    ],
}

# ---------------------------------------------------------------------------
# Archetype defaults — minimum BARS scores per archetype
# ---------------------------------------------------------------------------
ARCHETYPE_DEFAULTS: dict[str, dict[str, int]] = {
    "consulting": {
        "min_communication": 4,
        "min_adaptability": 3,
        "min_collaboration": 4,
        "min_problem_solving": 3,
        "min_leadership": 3,
    },
    "startup": {
        "min_communication": 3,
        "min_adaptability": 4,
        "min_collaboration": 3,
        "min_problem_solving": 3,
        "min_leadership": 4,
    },
}
