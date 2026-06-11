"""
Lab 11 - Part 4: Human-in-the-loop design.

TODO 12: Confidence router
TODO 13: HITL decision points
"""
from dataclasses import dataclass


HIGH_RISK_ACTIONS = [
    "transfer_money",
    "close_account",
    "change_password",
    "delete_data",
    "update_personal_info",
]


@dataclass
class RoutingDecision:
    """Result of the confidence router."""

    action: str
    confidence: float
    reason: str
    priority: str
    requires_human: bool


class ConfidenceRouter:
    """Route responses based on confidence and action risk.

    This component is needed because high-risk banking actions should not be
    automated solely because a model sounds confident.
    """

    HIGH_THRESHOLD = 0.9
    MEDIUM_THRESHOLD = 0.7

    def route(self, response: str, confidence: float,
              action_type: str = "general") -> RoutingDecision:
        """Route a response based on confidence score and action type."""
        confidence = max(0.0, min(1.0, confidence))

        if action_type in HIGH_RISK_ACTIONS:
            return RoutingDecision(
                action="escalate",
                confidence=confidence,
                reason=f"High-risk action: {action_type}",
                priority="high",
                requires_human=True,
            )

        if confidence >= self.HIGH_THRESHOLD:
            return RoutingDecision(
                action="auto_send",
                confidence=confidence,
                reason="High confidence",
                priority="low",
                requires_human=False,
            )

        if confidence >= self.MEDIUM_THRESHOLD:
            return RoutingDecision(
                action="queue_review",
                confidence=confidence,
                reason="Medium confidence - needs review",
                priority="normal",
                requires_human=True,
            )

        return RoutingDecision(
            action="escalate",
            confidence=confidence,
            reason="Low confidence - escalating",
            priority="high",
            requires_human=True,
        )


hitl_decision_points = [
    {
        "id": 1,
        "name": "High-value transfer approval",
        "trigger": "The assistant detects a transfer, beneficiary change, or payment above the bank's risk threshold.",
        "hitl_model": "human-in-the-loop",
        "context_needed": "Customer identity status, amount, beneficiary, fraud signals, recent account activity, and model rationale.",
        "example": "A customer asks to transfer 500,000,000 VND to a new beneficiary after a password reset.",
    },
    {
        "id": 2,
        "name": "Ambiguous compliance or complaint case",
        "trigger": "The answer affects fees, disputes, chargebacks, account freezes, KYC, AML, or legal obligations with medium confidence.",
        "hitl_model": "human-as-tiebreaker",
        "context_needed": "Conversation transcript, relevant policy section, confidence score, retrieved evidence, and unresolved ambiguity.",
        "example": "A customer disputes an international card transaction and asks whether VinBank will guarantee a refund.",
    },
    {
        "id": 3,
        "name": "Safety anomaly monitoring",
        "trigger": "Monitoring detects repeated blocked prompts, prompt injection attempts, judge failures, or unusual session behavior.",
        "hitl_model": "human-on-the-loop",
        "context_needed": "User/session risk score, blocked prompt history, guardrail layer decisions, and audit log excerpt.",
        "example": "One user sends multiple system-prompt extraction attempts followed by a request to update personal information.",
    },
]


def test_confidence_router():
    """Test ConfidenceRouter with sample scenarios."""
    router = ConfidenceRouter()

    test_cases = [
        ("Balance inquiry", 0.95, "general"),
        ("Interest rate question", 0.82, "general"),
        ("Ambiguous request", 0.55, "general"),
        ("Transfer $50,000", 0.98, "transfer_money"),
        ("Close my account", 0.91, "close_account"),
    ]

    print("Testing ConfidenceRouter:")
    print("=" * 80)
    print(f"{'Scenario':<25} {'Conf':<6} {'Action Type':<18} {'Decision':<15} {'Priority':<10} {'Human?'}")
    print("-" * 80)

    for scenario, conf, action_type in test_cases:
        decision = router.route(scenario, conf, action_type)
        print(
            f"{scenario:<25} {conf:<6.2f} {action_type:<18} "
            f"{decision.action:<15} {decision.priority:<10} "
            f"{'Yes' if decision.requires_human else 'No'}"
        )

    print("=" * 80)


def test_hitl_points():
    """Display HITL decision points."""
    print("\nHITL Decision Points:")
    print("=" * 60)
    for point in hitl_decision_points:
        print(f"\n  Decision Point #{point['id']}: {point['name']}")
        print(f"    Trigger:  {point['trigger']}")
        print(f"    Model:    {point['hitl_model']}")
        print(f"    Context:  {point['context_needed']}")
        print(f"    Example:  {point['example']}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_confidence_router()
    test_hitl_points()
