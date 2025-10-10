import pandas as pd
from .data_fetching import get_engine, fetch_merged_data, data_validation

engine = get_engine()
merged_df = fetch_merged_data(engine)
data_validation(merged_df)

# ------------------------ KPIs ------------------------
def calculated_kpis(merged_df):
    # 1) Total Transactions
    total_transactions = len(merged_df)

    # 2) Total Quantity Sold
    total_quantity = merged_df['quantity'].sum()

    # 3) Total Revenue
    merged_df['revenue'] = merged_df['quantity'] * merged_df['unitprice'] * (1 - merged_df['discount'])
    total_revenue = merged_df['revenue'].sum()

    # 4) Profit
    merged_df['profit'] = (merged_df['unitprice'] - merged_df['costprice']) * merged_df['quantity']
    total_profit = merged_df['profit'].sum()

    # 5) Discount Loss
    merged_df['total_sale'] = merged_df['unitprice'] * merged_df['quantity']
    merged_df['discount_loss'] = merged_df['total_sale'] - merged_df['revenue'] 
    total_discount_loss = merged_df['discount_loss'].sum()

    kpis = {
        "total_transactions": total_transactions,
        "total_quantity": total_quantity,
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "total_discount_loss": total_discount_loss
    }

    return kpis