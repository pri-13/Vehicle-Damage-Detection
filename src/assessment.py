# insurance assessment

from statistics import mean

from src.config import (
    CONFIDENCE_THRESHOLD,
    RECOMMENDATIONS,
    ESTIMATED_COST,
    SEVERITY_SCORE
)

from src.severity import SeverityEstimator
from src.location import LocationEstimator

class DamageAssessment:
    def __init__(self):
        self.severity_estimator = SeverityEstimator()
        self.location_estimator = LocationEstimator()

    def assess(self, detections):
        damages = []
        severity_order = {
            "Minor": 1,
            "Medium": 2,
            "Severe": 3
        }
        scores = []

        # process each detection
        for d in detections:
            if d["confidence"] < CONFIDENCE_THRESHOLD:
                continue
            severity = self.severity_estimator.estimate(
                d["damage_type"],
                d["confidence"],
                d["bbox"],
                d["image_width"],
                d["image_height"]
            )
            location = self.location_estimator.estimate(
                d["damage_type"],
                d["bbox"],
                d["image_width"],
                d["image_height"]
            )
            damage = {
                "damage_type": d["damage_type"].title(),
                "confidence": round(d["confidence"] * 100, 2),
                "confidence_level": severity["confidence_level"],
                "location": location,
                "severity": severity["severity"],
                "coverage": severity["coverage"],
                "damage_size": severity["damage_size"],
                "recommendation":
                    RECOMMENDATIONS[d["damage_type"]],
                "estimated_cost":
                    ESTIMATED_COST[d["damage_type"]]
            }
            damage["repair_priority"] = self._repair_priority(
                damage["damage_type"],
                damage["severity"]
            )
            damages.append(damage)
            scores.append(
                SEVERITY_SCORE[damage["severity"]]
            )
        # sort by severity
        damages.sort(
            key=lambda x: severity_order[x["severity"]],
            reverse=True
        )

        # summary
        if len(damages) == 0:
            summary = {
                "total_damages": 0,
                "overall_severity": "None",
                "vehicle_health": "Excellent",
                "risk_score": 0,
                "inspection_status": "No Damage Detected"
            }
        else:
            overall = damages[0]["severity"]
            risk = round(mean(scores))
            summary = {
                "total_damages": len(damages),
                "overall_severity": overall,
                "vehicle_health":
                    self._vehicle_health(risk),
                "risk_score": risk,
                "inspection_status":
                    self._inspection_status(risk)
            }
        return {
            "summary": summary,
            "damages": damages
        }

    def _repair_priority(
        self,
        damage_type,
        severity
    ):
        if damage_type.lower() == "tire flat":
            return "Immediate"
        if severity == "Severe":
            return "High"
        if severity == "Medium":
            return "Medium"
        return "Low"
    def _vehicle_health(self, score):
        if score < 15:
            return "Excellent"
        if score < 35:
            return "Good"
        if score < 60:
            return "Fair"
        if score < 80:
            return "Poor"
        return "Critical"
    def _inspection_status(self, score):
        if score < 20:
            return "Good Condition"
        if score < 60:
            return "Needs Inspection"
        return "Immediate Repair Required"
    def to_dataframe(self, assessment):
        import pandas as pd
        return pd.DataFrame(assessment["damages"])