"""Marketplace Alpha metrics simulation and threshold gates."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AlphaMetricsReport:
    total_orders: int
    cancelled_orders: int
    refunded_orders: int
    average_first_response_seconds: float
    average_agent_delivery_hours: float
    average_freelancer_delivery_hours: float

    @property
    def cancellation_rate(self) -> float:
        return self.cancelled_orders / self.total_orders

    @property
    def refund_rate(self) -> float:
        return self.refunded_orders / self.total_orders

    @property
    def delivery_speed_improvement(self) -> float:
        return 1 - (self.average_agent_delivery_hours / self.average_freelancer_delivery_hours)


@dataclass(frozen=True)
class AlphaMetricGateResult:
    passed: bool
    failures: tuple[str, ...]


class AlphaMetricGate:
    def __init__(
        self,
        *,
        min_orders: int = 100,
        max_cancellation_rate: float = 0.10,
        max_refund_rate: float = 0.05,
        max_first_response_seconds: float = 120,
        min_delivery_speed_improvement: float = 0.50,
    ):
        self.min_orders = min_orders
        self.max_cancellation_rate = max_cancellation_rate
        self.max_refund_rate = max_refund_rate
        self.max_first_response_seconds = max_first_response_seconds
        self.min_delivery_speed_improvement = min_delivery_speed_improvement

    def evaluate(self, report: AlphaMetricsReport) -> AlphaMetricGateResult:
        failures: list[str] = []
        if report.total_orders < self.min_orders:
            failures.append("total_orders below alpha threshold")
        if report.cancellation_rate >= self.max_cancellation_rate:
            failures.append("cancellation_rate above threshold")
        if report.refund_rate >= self.max_refund_rate:
            failures.append("refund_rate above threshold")
        if report.average_first_response_seconds >= self.max_first_response_seconds:
            failures.append("average_first_response_seconds above threshold")
        if report.delivery_speed_improvement < self.min_delivery_speed_improvement:
            failures.append("delivery_speed_improvement below threshold")
        return AlphaMetricGateResult(passed=not failures, failures=tuple(failures))


def run_alpha_metrics_simulation() -> AlphaMetricsReport:
    """Create a deterministic 100-order alpha metrics proxy.

    This is an executable readiness gate, not evidence of real customer traffic.
    Real alpha completion still requires observed production orders.
    """

    total_orders = 100
    cancelled_orders = 7
    refunded_orders = 3
    response_seconds = [18 + (index % 37) for index in range(total_orders)]
    agent_delivery_hours = [0.75 + (index % 10) * 0.35 for index in range(total_orders)]
    freelancer_delivery_hours = [24 + (index % 5) * 6 for index in range(total_orders)]
    return AlphaMetricsReport(
        total_orders=total_orders,
        cancelled_orders=cancelled_orders,
        refunded_orders=refunded_orders,
        average_first_response_seconds=sum(response_seconds) / total_orders,
        average_agent_delivery_hours=sum(agent_delivery_hours) / total_orders,
        average_freelancer_delivery_hours=sum(freelancer_delivery_hours) / total_orders,
    )

