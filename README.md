# Automated Sales KPI Reporting System

_A fully automated system that extracts sales data from PostgreSQL Database, calculates key business KPIs, generates visual reports, and delivers them via email saving manual effort and enabling faster business insights. Built using Python (Pandas, Matplotlib, Seaborn, SQLAlchemy .,etc) & PostgreSQL for scalable analytics automation._


## Table of Contents  

1. <u>[Overview](#overview)</u>  
2. <u>[Project Description](#project-description)</u> 
3. <u>[Project Objective](#project-objective)</u> 
4. <u>[Dataset Description](#dataset-description)</u>  
5. <u>[Project Workflow & Automation Steps](#project-workflow--automation-steps)</u> 
6. <u>[Tools & Skills Used](#tools--skills-used)</u>  
7. <u>[How to Use This Project](#how-to-use-this-project)</u>  
8. <u>[Conclusion](#conclusion)</u>  
9. <u>[Author](#author)</u>  
10. <u>[Contact](#contact)</u>  

## Overview
The _Automated Sales KPI Reporting System_ Project is a Python-based automation system that streamlines the entire data reporting process — from data extraction to final PDF report creation. It connects to a database, performs data validation and KPI calculations, generates insightful charts, compiles them into a well-formatted PDF report, and sends it via email — all in one seamless workflow.

This project eliminates repetitive manual reporting tasks and ensures faster, more accurate business insights, making it ideal for automating reporting operations.

## Project Description

This project automates the entire sales reporting process by connecting directly to a PostgreSQL database, fetching and merging data from multiple sales-related tables, and computing key performance indicators (KPIs) such as total revenue, profit, transactions, and discount loss. Using Matplotlib and Seaborn, it generates insightful visual reports which are automatically compiled into a PDF and delivered via email.

By removing manual reporting tasks, this system ensures consistent, accurate, and timely business insights — enabling data-driven decision-making and improved efficiency across sales operations.

## Project Objective

The goal of this project is to design and implement a fully automated reporting system that extracts, analyzes, and visualizes sales data directly from a database, eliminate manual reporting, ensure accuracy in KPI tracking (revenue, profit, and discounts), and automatically deliver performance reports — enabling faster, data-driven decision-making for business teams.

## Dataset Description

The dataset is sourced from a simulated retail sales environment and stored in a PostgreSQL database. It consists of four interrelated tables that collectively capture customer, product, store, and transaction information.

- ***Customers*** → Contains customer demographics and onboarding details, including CustomerID, Name, Gender, BirthDate, City, and JoinDate.

- ***Products*** → Includes product-level details such as ProductID, ProductName, Category, SubCategory, UnitPrice, and CostPrice.

- ***Stores*** → Provides information about each store, including StoreID, StoreName, City, and Region.

- ***Transactions*** → Records each sales transaction with fields like TransactionID, Trans_Date, CustomerID, ProductID, StoreID, Quantity, Discount, and PaymentMethod.    

These tables are linked using primary–foreign key relationships, allowing efficient joins and generation of consolidated reports for KPI and trend analysis.ns.

## Project Workflow & Automation Steps

This project follows a modular and automated workflow divided into six Python scripts, each handling a specific stage of the reporting pipeline — from data extraction to email delivery.

1. **Database Connection & Data Validation**

    Purpose: Establish connection with the PostgreSQL database and prepare a clean, merged dataset.
    Process:
    - A SQL engine is created using the *SQLAlchemy* library.
    - Multiple database tables are joined using SQL queries to form a single consolidated *merged_df*.
    - A data validation step checks for:
        - Missing (NULL) values
        - Duplicate records
    - If any data quality issue is detected, an error is raised to ensure clean inputs for analysis.

2. **KPI Generation**

    Purpose: Calculate key performance indicators (KPIs) for business insights.
    Process:
    - A function computes Key important metrics:
        - Total Transactions
        - Total Revenue
        - Quantity Sold
        - Total Profit
        - Total Discount Loss
    - The KPIs are stored for later inclusion in the automated report.

3. **Visualization Creation**

    Purpose: Generate visual insights from the data.
    Process:
    - Functions use *Matplotlib* and *Seaborn* to create professional-looking charts:
        - Pie Charts:
            - Revenue by Category
            - Revenue by Store
            - Revenue by Payment
            - Revenue by Gender
        - Bar Charts:
            - Top 10 Products by Revenue
            - Subcategories by Revenue
        - Each chart is saved locally for embedding into the final report.

4. **PDF Report Generation**

    Purpose: Combine KPIs and visualizations into a professional report.
    Process:
    - Using the *FPDF* library, all charts and metrics are compiled into a well-formatted *PDF report*.
    - The PDF includes a header, KPI summary section, and visualization pages for clarity and readability.
    - PDF also saved locally for further use if needed.

5. **Email Automation**

    Purpose: Automatically deliver the generated report via email.
    Process:
    - The *smtplib* library is used to send emails.
    - Email contains:
        - A custom message body 
        - The PDF report attached
    - Ensures stakeholders receive up-to-date sales reports without manual effort.

6. **Main Script Execution**

    Purpose: Orchestrate the entire automation pipeline.
    Process:
    - Sequentially executes all previous functions:
        - Connect to database and validate data
        - Generate KPIs 
        - Create visualizations
        - Compile PDF report
        - Send email with attachment
    - After successful execution, an email with the complete Sales KPI Report will be sent to the Reciever's Email ID — fully automated from start to finish.

Note: You can view an example of the PDF report in the _report/_ folder.

#### Core Implementation Snippets

```Python
Creating SQL Engine

def get_engine():
    engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:5432/{db_name}")
    return engine
```

```Python
Merging Tables 

def fetch_merged_data(engine):
    merged_df = pd.read_sql("""
    SELECT t.transactionid, t.trans_date, t.quantity, t.discount, t.paymentmethod,
        c.name AS customer_name, c.city AS customer_city, c.gender,
        p.productname, p.category, p.subcategory, p.unitprice, p.costprice,
        s.storename, s.city AS store_city, s.region
    FROM transactions t
    LEFT JOIN customers c ON t.customerid = c.customerid
    LEFT JOIN products p ON t.productid = p.productid
    LEFT JOIN stores s ON t.storeid = s.storeid
    """, engine)
    return merged_df
```


```Python
Sending Email

def send_email():
    sender = "SENDER'S EMAIL"
    receiver = "RECIEVER'S EMAIL"
    password = "Gmail's App Password" 

    subject = "Retail Sales Report"
    body = "Please find attached the latest Retail Sales Report."

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.set_content(body)

    with open("report/retail_sales_report.pdf", "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename="retail_sales_report.pdf")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit() 
```   

```Python
Visualizations

# Pie Chart
def pie_chart(value,lable,heading,save_path):
    plt.figure(figsize=(4, 4))
    plt.pie(
        value,
        labels=lable,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'white'}
    )
    plt.title(heading, fontsize=14, fontweight='bold')
    plt.savefig(save_path)  
    plt.close()  
    return save_path

# Bar Chart
def bar_chart(data_value,value,title,x_lable,save_path):
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(
        data=data_value,
        x=value,
        y='revenue',
        palette='rainbow'
    )
    for i, v in enumerate(data_value['revenue']):
        ax.text(i, v + (v * 0.01), f"{v/1000:.1f}k", ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax.set_yticklabels([]) 
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel(x_lable)
    plt.ylabel("Total Revenue (₹)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close() 
    return save_path
```
Note: All project code can be found in the *scripts/* directory.

## Tools & Skills Used

- **Programing Language**: Python
- **Liabraries**:
    - **Data Handling & Analysis**: pandas, os
    - **Data Visualization**: matplotlib, seaborn
    - **Database Connectivity**: sqlalchemy, psycopg2
    - **Reporting & Email**: fpdf, smtplib, email
- **Database & Querying**: SQL, PostgreSQL

## How to Use This Project

Follow these steps to set up and run the Automated Sales KPI Reporting System:

1. Prepare the Dataset
    - Download the dataset from the *Data/* folder.
    - Upload the tables into PostgreSQL.

2. Download Project Scripts
    - Get all scripts from the *scripts/* folder.

3. Configure Database Connection
    - Open *data_fetching.py*.
    - Add your database credentials: *Username, Password, Host*, and *DB_Name*.
    - Ensure the dataset you insert has no null values or duplicate rows to avoid errors.

4. Configure Email Settings
    - Open *email_send.py*.
    - Add details for *Sender's Email Id, Receiver's Email Id*, and *Gmail's App Password*.

5. Run the Main Script
    - Open *main.py* and run the program.
    - You will receive an email from the sender containing the PDF report with KPIs and Charts.

6. Access Local Output
    - The program also saves the PDF in the *report/* folder and the charts in the *visuals/* folder, allowing you to review results locally.




## Conclusion

This **Automated Sales KPI Reporting System** project demonstrates my proficiency in Python-based data automation, SQL data handling, and report generation. It showcases my ability to:

1. Extract, merge, and validate data from multiple PostgreSQL tables using Python (Pandas, SQLAlchemy, psycopg2) ensuring clean and accurate datasets for analysis.

2. Compute key business metrics (KPIs) like Total Transactions, Revenue, Profit, Quantity Sold, and Discount Loss to provide actionable insights.

3. Generate professional visualizations (Seaborn, Matplotlib) such as Pie Charts and Bar Charts for revenue by category, store, subcategory, and top products.

4. Automate report creation by compiling KPIs and charts into a structured PDF report using FPDF, enabling easy sharing and presentation of business insights.

5. Implement automated email delivery of the report via smtplib, ensuring stakeholders receive timely updates without manual intervention.

This project highlights my ability to transform raw sales data into structured, actionable insights, demonstrating strong skills in Python programming, SQL querying, data visualization, automation, and report generation.

## Author

***Kartavya Raj*** – Data Analyst

Passionate about data analysis, visualization, modeling, business insights and automation & reporting. Skilled in Advanced Excel, SQL, Power BI, Python (Pandas, NumPy, Matplotlib, Seaborn, Plotly).

## Contact

For any questions or further information, please contact me.

[![LinkedIn](https://skillicons.dev/icons?i=linkedin&theme=light)](https://www.linkedin.com/in/kartavyaraj) [![Gmail](https://skillicons.dev/icons?i=gmail&theme=light)](mailto:kartavyarajput108@gmail.com)

---

[🔼 Back to Top](#automated-sales-kpi-reporting-system)
