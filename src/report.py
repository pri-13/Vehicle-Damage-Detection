import os
from datetime import datetime

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from src.config import REPORTS_PATH

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image
)


class ReportGenerator:
    # generates CSV and PDF reports from damage assessment results.
    def __init__(self):

        self.output_dir = REPORTS_PATH

        os.makedirs(
            os.path.join(self.output_dir, "csv"),
            exist_ok=True
        )

        os.makedirs(
            os.path.join(self.output_dir, "pdf"),
            exist_ok=True
        )

        self.styles = getSampleStyleSheet()

        self.title_style = self.styles["Title"]
        self.title_style.alignment = TA_CENTER

        self.heading_style = self.styles["Heading2"]
        self.normal_style = self.styles["BodyText"]

    # convert assessment to dataframe
    def to_dataframe(self, assessment):
        rows = []
        for damage in assessment["damages"]:
            rows.append({
                "Damage Type": damage["damage_type"],
                "Confidence (%)": damage["confidence"],
                "Confidence Level": damage["confidence_level"],
                "Severity": damage["severity"],
                "Location": damage["location"],
                "Damage Size": damage["damage_size"],
                "Estimated Cost": damage["estimated_cost"],
                "Repair Priority": damage["repair_priority"],
                "Recommendation": damage["recommendation"]
            })
        columns = [
            "Damage Type",
            "Confidence (%)",
            "Confidence Level",
            "Severity",
            "Location",
            "Damage Size",
            "Estimated Cost",
            "Repair Priority",
            "Recommendation"
        ]
        return pd.DataFrame(rows, columns=columns)

    # export csv
    def export_csv(
        self,
        assessment,
        filename="damage_report.csv"
    ):

        df = self.to_dataframe(assessment)

        csv_path = os.path.join(
            self.output_dir,
            "csv",
            filename
        )

        df.to_csv(
            csv_path,
            index=False
        )

        return csv_path

    # vehivle summary
    def _build_summary(
        self,
        story,
        assessment
    ):

        summary = assessment["summary"]

        story.append(
            Paragraph(
                "Vehicle Summary",
                self.heading_style
            )
        )

        summary_table = [
            ["Total Damages",
             summary["total_damages"]],
            ["Overall Severity",
             summary["overall_severity"]],
            ["Vehicle Health",
             summary["vehicle_health"]],
            ["Risk Score",
             summary["risk_score"]],
            ["Inspection Status",
             summary["inspection_status"]]
        ]

        table = Table(
            summary_table,
            colWidths=[2.8*inch, 3.5*inch]
        )

        table.setStyle(
            TableStyle([
                ("GRID",(0,0),(-1,-1),0.5,colors.grey),
                ("BACKGROUND",(0,0),(0,-1),
                 colors.lightgrey),
                ("FONTNAME",(0,0),(-1,-1),
                 "Helvetica"),
                ("BOTTOMPADDING",
                 (0,0),(-1,-1),8)
            ])
        )
        story.append(table)
        story.append(Spacer(1,0.25*inch))

    # damage details table
    def _build_damage_table(
        self,
        story,
        assessment
    ):

        story.append(
            Paragraph(
                "Damage Details",
                self.heading_style
            )
        )

        data = [[
            "Damage",
            "Severity",
            "Location",
            "Confidence",
            "Priority",
            "Estimated Cost"
        ]]

        for damage in assessment["damages"]:
            data.append([
                damage["damage_type"],
                damage["severity"],
                damage["location"],
                f"{damage['confidence']}%",
                damage["repair_priority"],
                damage["estimated_cost"]
            ])

        table = Table(data)
        table.setStyle(
            TableStyle([
                ("BACKGROUND",
                 (0,0),(-1,0),
                 colors.darkblue),
                ("TEXTCOLOR",
                 (0,0),(-1,0),
                 colors.white),
                ("GRID",
                 (0,0),(-1,-1),
                 0.5,
                 colors.black),
                ("BACKGROUND",
                 (0,1),(-1,-1),
                 colors.beige),
                ("ALIGN",
                 (0,0),(-1,-1),
                 "CENTER"),
                ("BOTTOMPADDING",
                 (0,0),(-1,0),
                 10)
            ])
        )

        story.append(table)
        story.append(Spacer(1,0.25*inch))

    def _build_recommendation(
        self,
        story,
        assessment
    ):

        summary = assessment["summary"]
        if summary["total_damages"] == 0:
            recommendation = """
            <b>Overall Recommendation</b><br/><br/>
            No visible damages were detected by the AI model.<br/><br/>
            The vehicle appears to be in good condition based on the uploaded image.<br/><br/>
            Manual inspection is still recommended before making repair or insurance decisions.
            """
        else:
            recommendation = f"""
            <b>Overall Recommendation</b><br/><br/>
            • Total detected damages :
            <b>{summary['total_damages']}</b><br/>
            • Overall Severity :
            <b>{summary['overall_severity']}</b><br/>
            • Vehicle Health :
            <b>{summary['vehicle_health']}</b><br/>
            • Inspection Status :
            <b>{summary['inspection_status']}</b><br/><br/>
            Professional inspection is recommended before insurance claim approval.
            """
        story.append(
            Paragraph(
                recommendation,
                self.normal_style
            )
        )

        story.append(
            Spacer(1,0.25*inch)
        )

    def _build_footer(self, story):
        footer = """
        <br/><br/>
        ------------------------------------------------------------<br/>
        <b>Disclaimer</b><br/>
        This report has been generated automatically using the
        Vehicle Damage Detection System powered by YOLOv8.
        The assessment is AI-assisted and should be verified by
        a qualified vehicle inspector before insurance claim
        approval or repair estimation.
        """
        story.append(
            Paragraph(
                footer,
                self.normal_style
            )
        )

    # export pdf
    def export_pdf(
        self,
        assessment,
        filename="damage_report.pdf",
        prediction_image_path=None
    ):
        pdf_path = os.path.join(
            self.output_dir,
            "pdf",
            filename
        )
        doc = SimpleDocTemplate(
            pdf_path
        )
        story = []

        #title
        story.append(
            Paragraph(
                "Vehicle Damage Inspection Report",
                self.title_style
            )
        )
        story.append(
            Spacer(1,0.20*inch)
        )
        current_time = datetime.now().strftime(
            "%d %B %Y, %I:%M %p"
        )
        story.append(
            Paragraph(
                f"<b>Generated On :</b> {current_time}",
                self.normal_style
            )
        )
        story.append(
            Spacer(1,0.30*inch)
        )

        #vehicle summary
        self._build_summary(
            story,
            assessment
        )
        #damage table
        self._build_damage_table(
            story,
            assessment
        )
        #damage rec

        story.append(
            Paragraph(
                "Damage Recommendations",
                self.heading_style
            )
        )

        if not assessment["damages"]:

            story.append(

                Paragraph(

                    "No damages were detected in the uploaded image.",

                    self.normal_style

                )

            )

        else:

            for index, damage in enumerate(
                assessment["damages"],
                start=1
            ):

                recommendation = f"""
                <b>Damage #{index}</b><br/>

                Damage Type :
                <b>{damage['damage_type']}</b><br/>

                Severity :
                <b>{damage['severity']}</b><br/>

                Location :
                <b>{damage['location']}</b><br/>

                Estimated Cost :
                <b>{damage['estimated_cost']}</b><br/>

                Repair Priority :
                <b>{damage['repair_priority']}</b><br/>

                Recommendation :
                {damage['recommendation']}

                <br/><br/>
                """

                story.append(

                    Paragraph(

                        recommendation,

                        self.normal_style

                    )

                )

        story.append(
            Spacer(1, 0.20 * inch)
        )

        self._build_recommendation(
            story,
            assessment
        )

        # prediction image
        if (prediction_image_path is not None
            and
            os.path.exists(prediction_image_path)):
            story.append(Paragraph("Detected Damage Image", self.heading_style))
            story.append(Spacer(1,0.15*inch))
            image = Image(prediction_image_path, width=5.8*inch, height=4.0*inch)
            story.append(image)
            story.append(Spacer(1,0.25*inch))

        # footer
        self._build_footer(story)

        # create pdf
        try:
            doc.build(story)
            print("PDF report generated successfully.")
            print(pdf_path)
        except Exception as e:
            print("Error generating PDF:")
            print(e)
        return pdf_path