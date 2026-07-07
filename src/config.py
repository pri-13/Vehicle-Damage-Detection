import os

# project paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(PROJECT_ROOT,"models","best.pt")
REPORTS_PATH = os.path.join(PROJECT_ROOT,"reports")
CSV_PATH = os.path.join(REPORTS_PATH,"csv")
PDF_PATH = os.path.join(REPORTS_PATH,"pdf")
FIGURES_PATH = os.path.join(REPORTS_PATH,"figures")
TEMP_PATH = os.path.join(PROJECT_ROOT,"temp")

# detection
CONFIDENCE_THRESHOLD = 0.30

# severity thresholds
SEVERITY_THRESHOLDS = {
    "scratch": {"minor": 0.05, "medium": 0.15},
    "dent": {"minor": 0.08, "medium": 0.18},
    "crack": {"minor": 0.00, "medium": 0.10},
    "glass shatter": {"minor": 0.00, "medium": 0.05},
    "lamp broken": {"minor": 0.00, "medium": 0.05},
    "tire flat": {"minor": 0.00, "medium": 0.00}
}

# repair recommendations
RECOMMENDATIONS = {
    "scratch":"Buffing and repainting recommended.",
    "dent":"Dent removal and panel inspection recommended.",
    "crack":"Inspect structural integrity and repair the damaged panel.",
    "glass shatter":"Replace the damaged windshield/glass immediately.",
    "lamp broken":"Replace the damaged lamp assembly.",
    "tire flat":"Replace or repair the tire before driving."
}

# estimated repair cost
ESTIMATED_COST = {
    "scratch":"₹2,000 - ₹6,000",
    "dent":"₹5,000 - ₹15,000",
    "crack":"₹8,000 - ₹20,000",
    "glass shatter":"₹10,000 - ₹25,000",
    "lamp broken":"₹3,000 - ₹12,000",
    "tire flat":"₹4,000 - ₹10,000"
}

# severity score
SEVERITY_SCORE = {
    "Minor": 20,
    "Medium": 55,
    "Severe": 90
}