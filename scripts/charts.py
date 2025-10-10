import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from .data_fetching import get_engine,fetch_merged_data,data_validation

engine = get_engine()
merged_df = fetch_merged_data(engine)
data_validation(merged_df)

# ------------------------ PIE CHART ------------------------
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

# ------------------------ BAR CHART ------------------------
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

# ------------------------ CREATING ALL CHARTS ------------------------
def all_chart_files(merged_df):
    os.makedirs("visuals", exist_ok=True)
    chart_files = []

    # Calculate revenues for charts
    merged_df['revenue'] = merged_df['quantity'] * merged_df['unitprice'] * (1 - merged_df['discount'])
    category_revenue = merged_df.groupby('category')['revenue'].sum().reset_index()
    store_revenue = merged_df.groupby('storename')['revenue'].sum().reset_index()
    payment_revenue = merged_df.groupby('paymentmethod')['revenue'].sum().reset_index()
    gender_revenue = merged_df.groupby('gender')['revenue'].sum().reset_index()
    top_products = merged_df.groupby('productname')['revenue'].sum().reset_index().sort_values(by='revenue', ascending=False).head(10)
    sub_category_revenue = merged_df.groupby('subcategory')['revenue'].sum().reset_index().sort_values(by='revenue', ascending=False)

    # Pie-Chart
    chart_files.append(pie_chart(category_revenue['revenue'], category_revenue['category'],
                                 "Revenue by Product Category", "visuals/revenue_by_category.png"))
    chart_files.append(pie_chart(store_revenue['revenue'], store_revenue['storename'],
                                 "Revenue by Stores", "visuals/revenue_by_stores.png"))
    chart_files.append(pie_chart(payment_revenue['revenue'], payment_revenue['paymentmethod'],
                                 "Revenue by Payment Method", "visuals/revenue_by_payment.png"))
    chart_files.append(pie_chart(gender_revenue['revenue'], gender_revenue['gender'],
                                 "Revenue by Gender", "visuals/revenue_by_gender.png"))

    # Bar-Chart
    chart_files.append(bar_chart(top_products, 'productname', "Top 10 Products by Revenue",
                                 "Product Name", "visuals/top_10_products.png"))
    chart_files.append(bar_chart(sub_category_revenue, 'subcategory', "Sub Category wise Revenue",
                                 "Sub Category", "visuals/subcategory_revenue.png"))

    return chart_files