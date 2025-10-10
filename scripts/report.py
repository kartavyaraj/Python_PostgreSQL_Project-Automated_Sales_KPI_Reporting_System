import os
from fpdf import FPDF  # type: ignore
from .data_fetching import get_engine, fetch_merged_data, data_validation
from .kpis import calculated_kpis
from .charts import all_chart_files

# ------------------------ GENERATING PDF ------------------------
def create_pdf_report():
    os.makedirs("report", exist_ok=True)
    
    engine = get_engine()
    merged_df = fetch_merged_data(engine)
    data_validation(merged_df)

    kpis = calculated_kpis(merged_df)

    chart_files = all_chart_files(merged_df)

    # Initializing PDF
    pdf = FPDF()
    pdf.add_page()

    # PDF Title
    pdf.set_font("Arial", "B", 30)
    pdf.cell(0, 10, "Retail Sales Report", ln=True, align="C")
    pdf.ln(25)

    # Adding KPI metrics   
    pdf.set_font("Arial", "", 20)
    for key, value in kpis.items():
        # Bold for title
        pdf.set_font("Arial", "B", 20)
        title = f"{key.replace('_',' ').title()}: "
        pdf.cell(pdf.get_string_width(title), 10, title, ln=0)
        
        # Normal for value
        pdf.set_font("Arial", "", 20)
        if key in ["total_revenue", "total_profit", "total_discount_loss"]:
            pdf.cell(0, 10, f"Rs.{int(value)}", ln=True)
        else:
            pdf.cell(0, 10, f"{int(value)}", ln=True)

    # Adding charts
    for chart_path in chart_files:
        pdf.add_page()

        img_width = 180
        img_height = 180 

        x_position = (pdf.w - img_width) / 2
        y_position = (pdf.h - img_height) / 2

        pdf.image(chart_path, x=x_position, y=y_position, w=img_width, h=img_height)

    # Saving PDF
    pdf.output("report/retail_sales_report.pdf")
