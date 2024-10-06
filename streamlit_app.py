import streamlit as st
import pandas as pd

# Load the dataset
data = pd.read_csv('Superstore_Sales_utf8.csv')

# Add dropdown for Category if the data is successfully loaded
if not data.empty:
    category = st.selectbox('Select Category', data['Category'].unique())

    # Filter the data based on the selected Category
    filtered_data = data[data['Category'] == category]

    # Add multi-select for Sub_Category based on filtered data
    sub_category = st.multiselect('Select Sub-Category', filtered_data['Sub_Category'].unique())

    # Filter the data based on the selected Sub_Category
    if sub_category:
        sub_filtered_data = filtered_data[filtered_data['Sub_Category'].isin(sub_category)]
    else:
        sub_filtered_data = filtered_data

    # Show line chart of sales for the selected Sub_Category
    if not sub_filtered_data.empty:
        st.line_chart(sub_filtered_data[['Order_Date', 'Sales']].set_index('Order_Date').sort_index())

    # Calculate total sales, total profit, and overall profit margin for the selected items
    total_sales = sub_filtered_data['Sales'].sum()
    total_profit = sub_filtered_data['Profit'].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

    # Calculate overall average profit margin
    overall_total_sales = data['Sales'].sum()
    overall_total_profit = data['Profit'].sum()
    overall_profit_margin = (overall_total_profit / overall_total_sales) * 100 if overall_total_sales != 0 else 0

    # Add metrics with delta for profit margin
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
    st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
    st.metric(label="Profit Margin (%)", value=f"{profit_margin:.2f}%", delta=f"{profit_margin - overall_profit_margin:.2f}%")

else:
    st.error("The data failed to load. Please check the dataset and try again.")
