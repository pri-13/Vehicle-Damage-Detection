# estimate vehicle damage severity using:
# Damage type
# Bounding box coverage
# Detection confidence

from src.config import SEVERITY_THRESHOLDS

class SeverityEstimator:

    def estimate(
        self,
        damage_type,
        confidence,
        bbox,
        image_width,
        image_height
    ):

        x1, y1, x2, y2 = bbox

        width = max(0, x2 - x1)
        height = max(0, y2 - y1)

        damage_area = width * height
        image_area = image_width * image_height

        coverage = damage_area / image_area if image_area else 0

        coverage_percent = round(coverage * 100, 2)

        # damage size
        if coverage < 0.05:
            damage_size = "Small"
        elif coverage < 0.20:
            damage_size = "Medium"
        else:
            damage_size = "Large"
        damage_type = damage_type.lower()
        thresholds = SEVERITY_THRESHOLDS.get(
            damage_type,
            {"minor": 0.05, "medium": 0.15}
        )

        # base severity
        if damage_type == "tire flat":
            severity = "Severe"
        elif damage_type == "glass shatter":
            severity = "Medium" if coverage < 0.20 else "Severe"
        elif damage_type == "lamp broken":
            severity = "Medium" if coverage < 0.15 else "Severe"
        elif damage_type == "crack":
            severity = "Medium" if coverage < thresholds["medium"] else "Severe"
        elif damage_type == "scratch":
            if coverage < thresholds["minor"]:
                severity = "Minor"
            else:
                severity = "Medium"
        else:   # dent
            if coverage < thresholds["minor"]:
                severity = "Minor"
            elif coverage < thresholds["medium"]:
                severity = "Medium"
            else:
                severity = "Severe"

        # confidence adjustment
        if confidence >= 0.90:
            confidence_level = "Very High"
        elif confidence >= 0.80:
            confidence_level = "High"
        elif confidence >= 0.60:
            confidence_level = "Moderate"
        else:
            confidence_level = "Low"

        # downgrade if confidence low
        if confidence < 0.40 and severity == "Severe":
            severity = "Medium"
        if confidence < 0.30 and severity == "Medium":
            severity = "Minor"
        return {
            "severity": severity,
            "coverage": coverage_percent,
            "damage_size": damage_size,
            "confidence_level": confidence_level
        }