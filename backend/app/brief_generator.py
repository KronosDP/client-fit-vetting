"""
brief_generator.py — Generates a structured candidate preparation brief.
"""

from datetime import datetime, timezone

from . import seed


def generate_brief(
    candidate, client, score
) -> dict:
    """
    Build a candidate interview preparation brief.

    Returns a dictionary containing all brief content, suitable for
    JSON serialization and frontend rendering.
    """
    archetype = client.archetype.value if hasattr(client.archetype, "value") else client.archetype
    competencies = [
        ("Communication", score.communication, client.min_communication),
        ("Adaptability", score.adaptability, client.min_adaptability),
        ("Collaboration", score.collaboration, client.min_collaboration),
        ("Problem Solving", score.problem_solving, client.min_problem_solving),
        ("Leadership", score.leadership, client.min_leadership),
    ]

    competency_scores = []
    for name, scored, min_req in competencies:
        competency_scores.append({
            "name": name,
            "score": scored,
            "min_required": min_req,
            "status": "pass" if scored >= min_req else "warning",
        })

    # Gather coaching tips for all competencies
    archetype_tips = seed.COACHING_TIPS.get(archetype, {})
    coaching_tips: list[str] = []
    for key in ["communication", "adaptability", "collaboration", "problem_solving", "leadership"]:
        tips = archetype_tips.get(key, [])
        if tips:
            coaching_tips.append(tips[0])  # Take the top tip from each competency
    # If we have fewer than 3, pad; if more, take top 3
    coaching_tips = coaching_tips[:3] if len(coaching_tips) >= 3 else coaching_tips

    # Get the archetype-specific tips more strategically:
    # Focus on competencies where the candidate scored lowest
    sorted_competencies = sorted(competency_scores, key=lambda c: c["score"])
    focused_tips: list[str] = []
    for comp in sorted_competencies:
        comp_key = comp["name"].lower().replace(" ", "_")
        tips = archetype_tips.get(comp_key, [])
        for tip in tips:
            if tip not in focused_tips:
                focused_tips.append(tip)
            if len(focused_tips) >= 3:
                break
        if len(focused_tips) >= 3:
            break

    practice_questions = seed.PRACTICE_QUESTIONS.get(archetype, [])

    return {
        "candidate_name": candidate.name,
        "client_name": client.name,
        "client_archetype": archetype,
        "client_expectations": client.expectations or "",
        "competency_scores": competency_scores,
        "coaching_tips": focused_tips,
        "practice_questions": practice_questions,
        "overall_match_percentage": round(score.overall_match * 100, 1),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
