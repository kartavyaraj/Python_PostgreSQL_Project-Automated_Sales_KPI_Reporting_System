from scripts.data_fetching import get_engine, fetch_merged_data, data_validation
from scripts.kpis import calculated_kpis
from scripts.charts import all_chart_files
from scripts.report import create_pdf_report
from scripts.email_send import send_email

# ------------------------ FULL WORKING PIPEINE ------------------------
def main():
    print("Initialzing Report Generation Pipeline...")

    # Fetching Data & Data Validation
    engine = get_engine()
    merged_df = fetch_merged_data(engine)
    data_validation(merged_df)
    print("Data fetched and validated.")

    # Calculating KPIs
    kpis = calculated_kpis(merged_df)
    print("KPIs calculated.")

    # Generating Chart
    chart_files = all_chart_files(merged_df)
    print("Charts generated.")

    # Creating PDF
    create_pdf_report()
    print("PDF report created.")

    # Sending Email
    send_email()
    print("Report emailed successfully.")

    print("All steps completed successfully!")

if __name__ == "__main__":
    main()