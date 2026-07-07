# Vehicle Damage Detection System

import os
import streamlit as st
from PIL import Image

from src.detector import DamageDetector
from src.assessment import DamageAssessment
from src.report import ReportGenerator
from src.config import MODEL_PATH, TEMP_PATH, CONFIDENCE_THRESHOLD

# page configuration
st.set_page_config(
    page_title="Vehicle Damage Detection",
    page_icon="🚗",
    layout="wide"
)

# temporary upload folder
os.makedirs(TEMP_PATH, exist_ok=True)

# cached resources
@st.cache_resource
def load_components():
    return (
        DamageDetector(MODEL_PATH),
        DamageAssessment(),
        ReportGenerator()
    )
detector, assessor, reporter = load_components()

# title
st.title("🚗 Vehicle Damage Detection System")
st.caption("Upload a vehicle image to detect damages and generate an inspection report.")

# sidebar
st.sidebar.header("Settings")
confidence = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.10,
    max_value=0.90,
    value=CONFIDENCE_THRESHOLD,
    step=0.05
)
st.sidebar.markdown("---")
st.sidebar.success("Model Loaded Successfully")
st.sidebar.info(
    """
**Model**
- YOLOv8 Object Detection

**Supported Formats**
- JPG
- JPEG
- PNG
"""
)

# image upload
uploaded_file = st.file_uploader("Upload Vehicle Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    uploaded_image = Image.open(uploaded_file).convert("RGB")
    session_dir = os.path.join(TEMP_PATH, "session")
    os.makedirs(session_dir, exist_ok=True)
    uploaded_path = os.path.join(session_dir, "uploaded_image.jpg")
    prediction_path = os.path.join(session_dir, "prediction.jpg")
    uploaded_image.save(uploaded_path)
    with st.spinner("Analyzing vehicle image..."):
        annotated_image, detections = detector.detect(uploaded_path, conf=confidence)
        assessment = assessor.assess(detections)
        detector.save_prediction(annotated_image, prediction_path)
    st.success("Detection completed successfully.")
else:
    st.info("Please upload a vehicle image to begin damage detection.")

    st.stop()

# detection results
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Original Image")
    st.image(uploaded_image, use_container_width=True)

with col2:
    st.subheader("Detected Damages")
    st.image(prediction_path, use_container_width=True)

# vehicle summary
summary = assessment["summary"]

st.markdown("---")
st.subheader("Vehicle Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Damages", summary["total_damages"])
col2.metric("Overall Severity", summary["overall_severity"])
col3.metric("Vehicle Health", summary["vehicle_health"])
col4.metric("Risk Score", summary["risk_score"])

if summary["total_damages"] == 0:
    st.success("No visible damages were detected.")
else:
    st.warning(
        f"{summary['total_damages']} damage(s) detected. "
        f"Inspection Status: {summary['inspection_status']}"
    )


# damage details
st.markdown("---")
st.subheader("Damage Details")

damage_df = reporter.to_dataframe(assessment)

if damage_df.empty:
    st.info("No damage details available.")
else:
    damage_df["Confidence (%)"] = (damage_df["Confidence (%)"].astype(float).round(1))
    st.dataframe(damage_df, hide_index=True, use_container_width=True)

# assessment insights
if assessment["damages"]:
    st.markdown("---")
    st.subheader("Assessment Insights")
    for index, damage in enumerate(assessment["damages"], start=1):
        with st.expander(f"Damage {index} • {damage['damage_type']}"):
            st.write(f"**Location:** {damage['location']}")
            st.write(f"**Severity:** {damage['severity']}")
            st.write(f"**Confidence:** {damage['confidence']}%")
            st.write(f"**Confidence Level:** {damage['confidence_level']}")
            st.write(f"**Coverage:** {damage['coverage']}%")
            st.write(f"**Damage Size:** {damage['damage_size']}")
            st.write(f"**Estimated Cost:** {damage['estimated_cost']}")
            st.write(f"**Repair Priority:** {damage['repair_priority']}")
            st.write(f"**Recommendation:** {damage['recommendation']}")

# reports
st.markdown("---")
st.subheader("Generate Reports")

with st.spinner("Generating reports..."):
    csv_path = reporter.export_csv(assessment, filename="damage_report.csv")
    pdf_path = reporter.export_pdf(assessment, filename="damage_report.pdf", prediction_image_path=prediction_path)
st.success("Reports generated successfully.")

# download reports
col1, col2 = st.columns(2)

with col1:
    with open(csv_path, "rb") as file:
        st.download_button(
            label="📄 Download CSV Report",
            data=file,
            file_name="damage_report.csv",
            mime="text/csv",
            use_container_width=True
        )

with col2:
    with open(pdf_path, "rb") as file:
        st.download_button(
            label="📕 Download PDF Report",
            data=file,
            file_name="damage_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# cleanup
try:
    if os.path.exists(uploaded_path):
        os.remove(uploaded_path)
    if os.path.exists(prediction_path):
        os.remove(prediction_path)
    if os.path.isdir(session_dir):
        if not os.listdir(session_dir):
            os.rmdir(session_dir)
except Exception:
    pass

# footer
st.markdown("---")
st.caption(
    "Vehicle Damage Detection System | "
    "YOLOv8 • Streamlit • Python"
)