# Risk Engine & Recommendation System

## Overview
The Risk Engine bridges the gap between raw ML predictions (which are purely statistical) and actionable academic interventions. It uses a deterministic, rule-based approach to calculate an **Academic Risk Score (0-100)** and generate personalized recommendations. 

*Important Note:* **Correlation or model importance does not establish causation.** The ML models identify patterns, while the Risk Engine highlights deterministic academic thresholds. The Risk Score is an academic analytics indicator, not a guaranteed prediction or medical diagnosis.

## 1. Why is Risk Scoring separate from ML Prediction?
1. **Explainability**: ML models (like Random Forests) can act as black boxes. A student needs to know *why* they are at risk, not just that a model flagged them.
2. **Actionability**: The Risk Engine extracts exact components (e.g., "Attendance is 62%") to formulate specific interventions.
3. **Threshold Enforcement**: Institutions have hard rules (e.g., 75% attendance minimum) that ML models might smooth over. The Risk Engine enforces these boundaries strictly.

## 2. Risk Formula & Weights
The engine normalizes contributing factors against ideal maximums and weights them to produce a final score out of 100. Higher scores indicate higher academic risk.

| Factor | Weight | Normalization / Logic |
|---|---|---|
| **Internal Marks** | 25% | `max(0, 100 - marks) * 0.25` |
| **Attendance** | 20% | `max(0, 100 - attendance) * 0.20` |
| **Assignment Completion** | 15% | `max(0, 100 - completion) * 0.15` |
| **Previous Percentage** | 15% | `max(0, 100 - previous_percentage) * 0.15` |
| **Study Hours** | 10% | `max(0, 100 - (hours / 10 * 100)) * 0.10` |
| **Backlogs** | 10% | `(backlogs / 5 * 100) * 0.10` |
| **Participation** | 5% | `max(0, 100 - participation) * 0.05` |

## 3. Risk Categories (Thresholds)
- **Low Risk**: 0 – 33
- **Medium Risk**: 34 – 66
- **High Risk**: 67 – 100

## 4. Risk Factors & Severity
When a metric crosses a critical threshold, it is logged as a "Risk Factor" with an assigned severity level:
- **Attendance**: < 75% (High if < 60%)
- **Internal Marks**: < 50% (High if < 40%)
- **Assignment Completion**: < 70% (Medium)
- **Previous Percentage**: < 60% (Medium)
- **Study Hours**: < 2 hours (Medium)
- **Backlogs**: >= 2 (High if >= 3)
- **Participation**: < 40% (Low)

## 5. Recommendation Rules
Recommendations are deterministically mapped from identified Risk Factors and prioritized (High -> Medium -> Low). They are customized to inject the student's actual metrics into the text.

**Example Triggers:**
- *Condition*: `attendance < 75`
  - *Recommendation*: "Your attendance is {X}%. Improve class attendance and maintain at least 75% attendance where institution policy requires it."
- *Condition*: `backlogs >= 2`
  - *Recommendation*: "You currently have {X} backlogs. Create a backlog-clearing plan and prioritize previously incomplete subjects."
- *Condition*: No risk factors detected
  - *Recommendation*: "No major academic risk factors were detected from the provided indicators. Continue maintaining your current academic habits."

## 6. Limitations
- Does not account for qualitative, psychological, or socioeconomic factors.
- Relies heavily on accurate, timely data entry into the system.
- Designed as an early warning system, not an automated disciplinary mechanism.
