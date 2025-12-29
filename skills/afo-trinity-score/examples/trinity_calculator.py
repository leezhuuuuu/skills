#!/usr/bin/env python3
"""
AFO Trinity Score Calculator.

Calculate the Trinity Score (眞善美孝永) for evaluating system quality.

Usage:
    python trinity_calculator.py --truth 95 --goodness 90 --beauty 85 --risk 5 --friction 3 --eternity 88

Source: Derived from anthropics/skills PR #174 (MIT License)
"""

import argparse
import json


# Pillar weights
WEIGHTS = {
    "truth": 0.35,
    "goodness": 0.35,
    "beauty": 0.20,
    "filial_serenity": 0.08,
    "eternity": 0.02
}


def calculate_trinity_score(truth, goodness, beauty, risk, friction, eternity):
    """
    Calculate the Trinity Score.

    Args:
        truth: Technical accuracy (0-100)
        goodness: Ethical soundness (0-100)
        beauty: Design quality (0-100)
        risk: Risk factor (0-100, lower is better)
        friction: Cognitive load (0-100, lower is better)
        eternity: Sustainability (0-100)

    Returns:
        dict with trinity_score, decision, and pillar_scores
    """
    # Calculate adjusted scores
    truth_score = truth / 100.0
    goodness_score = goodness / 100.0
    beauty_score = beauty / 100.0
    serenity_score = (100 - friction) / 100.0  # Invert friction
    eternity_score = eternity / 100.0

    # Risk penalty (applies to goodness)
    risk_penalty = risk / 100.0
    adjusted_goodness = goodness_score * (1 - risk_penalty * 0.5)

    # Calculate weighted Trinity Score
    trinity_score = (
        WEIGHTS["truth"] * truth_score +
        WEIGHTS["goodness"] * adjusted_goodness +
        WEIGHTS["beauty"] * beauty_score +
        WEIGHTS["filial_serenity"] * serenity_score +
        WEIGHTS["eternity"] * eternity_score
    )

    # Determine balance status
    if trinity_score >= 0.95:
        balance_status = "outstanding"
    elif trinity_score >= 0.85:
        balance_status = "balanced"
    elif trinity_score >= 0.70:
        balance_status = "acceptable"
    else:
        balance_status = "needs_work"

    # Determine decision based on thresholds
    score_percentage = trinity_score * 100
    if score_percentage >= 90 and risk <= 10:
        decision = "AUTO_RUN"
    elif score_percentage >= 70 and risk <= 30:
        decision = "ASK_COMMANDER"
    else:
        decision = "BLOCK"

    return {
        "trinity_score": round(trinity_score, 2),
        "balance_status": balance_status,
        "decision": decision,
        "pillar_scores": {
            "truth": round(truth_score, 2),
            "goodness": round(adjusted_goodness, 2),
            "beauty": round(beauty_score, 2),
            "filial_serenity": round(serenity_score, 2),
            "eternity": round(eternity_score, 2)
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Calculate AFO Trinity Score (眞善美孝永)"
    )
    parser.add_argument(
        '--truth', '-t',
        type=float, default=90,
        help="Truth score (0-100, default: 90)"
    )
    parser.add_argument(
        '--goodness', '-g',
        type=float, default=90,
        help="Goodness score (0-100, default: 90)"
    )
    parser.add_argument(
        '--beauty', '-b',
        type=float, default=85,
        help="Beauty score (0-100, default: 85)"
    )
    parser.add_argument(
        '--risk', '-r',
        type=float, default=5,
        help="Risk score (0-100, lower is better, default: 5)"
    )
    parser.add_argument(
        '--friction', '-f',
        type=float, default=5,
        help="Friction score (0-100, lower is better, default: 5)"
    )
    parser.add_argument(
        '--eternity', '-e',
        type=float, default=85,
        help="Eternity score (0-100, default: 85)"
    )
    parser.add_argument(
        '--json', '-j',
        action='store_true',
        help="Output as JSON"
    )

    args = parser.parse_args()

    result = calculate_trinity_score(
        args.truth, args.goodness, args.beauty,
        args.risk, args.friction, args.eternity
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"\n{'='*50}")
        print(f"  AFO Trinity Score Calculator")
        print(f"{'='*50}")
        print(f"\n  Trinity Score: {result['trinity_score']:.2f}")
        print(f"  Balance Status: {result['balance_status']}")
        print(f"  Decision: {result['decision']}")
        print(f"\n  Pillar Scores:")
        print(f"    眞 (Truth): {result['pillar_scores']['truth']:.2f}")
        print(f"    善 (Goodness): {result['pillar_scores']['goodness']:.2f}")
        print(f"    美 (Beauty): {result['pillar_scores']['beauty']:.2f}")
        print(f"    孝 (Serenity): {result['pillar_scores']['filial_serenity']:.2f}")
        print(f"    永 (Eternity): {result['pillar_scores']['eternity']:.2f}")
        print(f"\n{'='*50}\n")


if __name__ == "__main__":
    main()
