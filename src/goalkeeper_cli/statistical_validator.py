#!/usr/bin/env python3
"""
Statistical Validation Module for A/B Testing Framework

This module provides statistical analysis capabilities including sample size
calculations, hypothesis testing, and confidence interval calculations
for A/B testing of template validation.
"""

import math
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import scipy.stats as stats
import numpy as np

@dataclass
class StatisticalTestResult:
    """Results from a statistical hypothesis test."""
    test_type: str
    statistic: float
    p_value: float
    confidence_interval: Tuple[float, float]
    effect_size: float
    is_significant: bool
    power: float
    sample_size_needed: int

@dataclass
class SampleSizeCalculation:
    """Results from sample size calculation."""
    metric_name: str
    baseline_rate: float
    minimum_detectable_effect: float
    alpha: float  # Significance level
    beta: float   # 1 - power
    sample_size_per_group: int
    total_sample_size: int
    expected_duration_days: int

class StatisticalValidator:
    """Provides statistical validation for A/B testing."""

    def __init__(self):
        self.alpha = 0.05  # Default significance level
        self.power = 0.80  # Default power (1 - beta)
        self.minimum_detectable_effects = {
            'clarification_rate': 0.20,  # 20% reduction
            'response_quality': 1.0,     # 1 point improvement on 10-point scale
            'template_usage': 0.30,      # 30% increase
            'user_satisfaction': 0.15    # 15% improvement
        }

    def calculate_sample_size(self, metric_name: str, baseline_rate: float,
                           minimum_detectable_effect: float = None,
                           alpha: float = None, power: float = None) -> SampleSizeCalculation:
        """Calculate required sample size for A/B test."""

        if alpha is None:
            alpha = self.alpha
        if power is None:
            power = self.power
        if minimum_detectable_effect is None:
            minimum_detectable_effect = self.minimum_detectable_effects.get(metric_name, 0.20)

        # Calculate effect size (Cohen's h for proportions, Cohen's d for means)
        if metric_name in ['clarification_rate', 'template_usage', 'user_satisfaction']:
            # Proportion-based metrics
            pooled_proportion = (baseline_rate + (baseline_rate - minimum_detectable_effect)) / 2
            effect_size = (minimum_detectable_effect) / math.sqrt(pooled_proportion * (1 - pooled_proportion))
        else:
            # Mean-based metrics (assuming unit variance for simplicity)
            effect_size = minimum_detectable_effect

        # Calculate sample size per group
        z_alpha = stats.norm.ppf(1 - alpha / 2)
        z_beta = stats.norm.ppf(power)

        if metric_name in ['clarification_rate', 'template_usage', 'user_satisfaction']:
            # Proportions test
            sample_size_per_group = (
                2 * (z_alpha + z_beta) ** 2 * pooled_proportion * (1 - pooled_proportion)
            ) / (minimum_detectable_effect ** 2)
        else:
            # Means test
            sample_size_per_group = (
                2 * (z_alpha + z_beta) ** 2
            ) / (effect_size ** 2)

        sample_size_per_group = math.ceil(sample_size_per_group)
        total_sample_size = sample_size_per_group * 2

        # Estimate duration (assuming 10 interactions per user per day)
        interactions_per_user_per_day = 10
        users_per_day_per_group = math.ceil(sample_size_per_group / (interactions_per_user_per_day * 7))  # Weekly estimate
        expected_duration_days = math.ceil(sample_size_per_group / users_per_day_per_group)

        return SampleSizeCalculation(
            metric_name=metric_name,
            baseline_rate=baseline_rate,
            minimum_detectable_effect=minimum_detectable_effect,
            alpha=alpha,
            beta=1-power,
            sample_size_per_group=sample_size_per_group,
            total_sample_size=total_sample_size,
            expected_duration_days=expected_duration_days
        )

    def run_proportion_test(self, group_a_successes: int, group_a_total: int,
                          group_b_successes: int, group_b_total: int) -> StatisticalTestResult:
        """Run two-proportion z-test for binary outcomes."""

        # Calculate proportions
        p_a = group_a_successes / group_a_total if group_a_total > 0 else 0
        p_b = group_b_successes / group_b_total if group_b_total > 0 else 0

        # Calculate pooled proportion
        p_pooled = (group_a_successes + group_b_successes) / (group_a_total + group_b_total)

        # Calculate standard error
        se = math.sqrt(p_pooled * (1 - p_pooled) * (1/group_a_total + 1/group_b_total))

        # Calculate test statistic
        z_stat = (p_a - p_b) / se if se > 0 else 0

        # Calculate p-value (two-tailed)
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

        # Calculate confidence interval
        diff = p_a - p_b
        margin = 1.96 * se  # 95% confidence
        ci_lower = diff - margin
        ci_upper = diff + margin

        # Calculate effect size (Cohen's h)
        effect_size = 2 * (math.asin(math.sqrt(p_a)) - math.asin(math.sqrt(p_b)))

        # Calculate power
        power = self._calculate_power_proportion(
            p_a, p_b, group_a_total, group_b_total, self.alpha
        )

        return StatisticalTestResult(
            test_type="two_proportion_z_test",
            statistic=z_stat,
            p_value=p_value,
            confidence_interval=(ci_lower, ci_upper),
            effect_size=effect_size,
            is_significant=p_value < self.alpha,
            power=power,
            sample_size_needed=max(group_a_total, group_b_total)
        )

    def run_means_test(self, group_a_values: List[float], group_b_values: List[float]) -> StatisticalTestResult:
        """Run two-sample t-test for continuous outcomes."""

        if not group_a_values or not group_b_values:
            return StatisticalTestResult(
                test_type="two_sample_t_test",
                statistic=0,
                p_value=1.0,
                confidence_interval=(0, 0),
                effect_size=0,
                is_significant=False,
                power=0,
                sample_size_needed=0
            )

        # Calculate means and standard deviations
        mean_a = np.mean(group_a_values)
        mean_b = np.mean(group_b_values)
        std_a = np.std(group_a_values, ddof=1)
        std_b = np.std(group_b_values, ddof=1)
        n_a = len(group_a_values)
        n_b = len(group_b_values)

        # Calculate pooled standard error
        se_pooled = math.sqrt((std_a**2 / n_a) + (std_b**2 / n_b))

        # Calculate t-statistic
        t_stat = (mean_a - mean_b) / se_pooled if se_pooled > 0 else 0

        # Calculate degrees of freedom
        df = n_a + n_b - 2

        # Calculate p-value (two-tailed)
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))

        # Calculate confidence interval
        diff = mean_a - mean_b
        margin = stats.t.ppf(1 - self.alpha/2, df) * se_pooled
        ci_lower = diff - margin
        ci_upper = diff + margin

        # Calculate effect size (Cohen's d)
        pooled_std = math.sqrt(((n_a - 1) * std_a**2 + (n_b - 1) * std_b**2) / (n_a + n_b - 2))
        effect_size = (mean_a - mean_b) / pooled_std if pooled_std > 0 else 0

        # Calculate power
        power = self._calculate_power_means(
            mean_a, mean_b, std_a, std_b, n_a, n_b, self.alpha
        )

        return StatisticalTestResult(
            test_type="two_sample_t_test",
            statistic=t_stat,
            p_value=p_value,
            confidence_interval=(ci_lower, ci_upper),
            effect_size=effect_size,
            is_significant=p_value < self.alpha,
            power=power,
            sample_size_needed=max(n_a, n_b)
        )

    def _calculate_power_proportion(self, p_a: float, p_b: float, n_a: int, n_b: int,
                                  alpha: float) -> float:
        """Calculate statistical power for proportion test."""
        p_pooled = (p_a + p_b) / 2
        se = math.sqrt(p_pooled * (1 - p_pooled) * (1/n_a + 1/n_b))
        effect_size = abs(p_a - p_b) / se if se > 0 else 0

        z_alpha = stats.norm.ppf(1 - alpha / 2)
        z_beta = effect_size - z_alpha

        return stats.norm.cdf(z_beta)

    def _calculate_power_means(self, mean_a: float, mean_b: float, std_a: float,
                             std_b: float, n_a: int, n_b: int, alpha: float) -> float:
        """Calculate statistical power for means test."""
        pooled_std = math.sqrt(((n_a - 1) * std_a**2 + (n_b - 1) * std_b**2) / (n_a + n_b - 2))
        se = pooled_std * math.sqrt(1/n_a + 1/n_b)
        effect_size = abs(mean_a - mean_b) / se if se > 0 else 0

        z_alpha = stats.norm.ppf(1 - alpha / 2)
        z_beta = effect_size - z_alpha

        return stats.norm.cdf(z_beta)

    def analyze_test_results(self, group_a_data: List[float], group_b_data: List[float],
                           metric_name: str) -> Dict[str, Any]:
        """Analyze A/B test results and provide comprehensive report."""

        # Determine if this is a proportion or means test
        if metric_name in ['clarification_rate', 'template_usage', 'user_satisfaction']:
            # Convert to binary data for proportion test
            threshold = np.median(group_a_data + group_b_data) if group_a_data + group_b_data else 0.5
            group_a_binary = [1 if x >= threshold else 0 for x in group_a_data]
            group_b_binary = [1 if x >= threshold else 0 for x in group_b_data]

            result = self.run_proportion_test(
                sum(group_a_binary), len(group_a_binary),
                sum(group_b_binary), len(group_b_binary)
            )
        else:
            # Use means test for continuous data
            result = self.run_means_test(group_a_data, group_b_data)

        # Calculate practical significance
        mean_a = np.mean(group_a_data) if group_a_data else 0
        mean_b = np.mean(group_b_data) if group_b_data else 0
        relative_improvement = ((mean_b - mean_a) / mean_a) if mean_a != 0 else 0

        return {
            "metric_name": metric_name,
            "statistical_test": result,
            "group_A": {
                "mean": mean_a,
                "sample_size": len(group_a_data),
                "std_dev": np.std(group_a_data) if group_a_data else 0
            },
            "group_B": {
                "mean": mean_b,
                "sample_size": len(group_b_data),
                "std_dev": np.std(group_b_data) if group_b_data else 0
            },
            "relative_improvement": relative_improvement,
            "is_practically_significant": abs(relative_improvement) >= 0.05,  # 5% threshold
            "recommendation": self._generate_recommendation(result, relative_improvement)
        }

    def _generate_recommendation(self, result: StatisticalTestResult,
                               relative_improvement: float) -> str:
        """Generate recommendation based on test results."""
        if not result.is_significant:
            return "Continue testing - results not statistically significant yet"

        if abs(relative_improvement) < 0.05:
            return "Statistically significant but small effect - consider if practically meaningful"

        if relative_improvement > 0:
            return "Implement variant B - shows statistically and practically significant improvement"
        else:
            return "Keep current version - variant B performs worse"

    def calculate_test_duration_estimate(self, daily_active_users: int,
                                       interactions_per_user: int = 10) -> Dict[str, int]:
        """Estimate test duration for different metrics."""

        estimates = {}

        for metric, baseline_rate in [
            ('clarification_rate', 0.15),
            ('response_quality', 7.0),
            ('template_usage', 0.30),
            ('user_satisfaction', 0.75)
        ]:
            calc = self.calculate_sample_size(metric, baseline_rate)
            daily_interactions = daily_active_users * interactions_per_user
            estimated_days = math.ceil(calc.total_sample_size / daily_interactions)
            estimates[metric] = estimated_days

        return estimates