import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import calendar

sns.set(style='dark')

def create_total_customer_df(df):
    total_customer_df = df.pivot_table(
        index='order_month', values='customer_id', 
        columns='order_year', aggfunc='nunique').reset_index()
    #mengurutkan hasil pivot table berdasarkan urutan bulan pada kalender
    month_order = list(calendar.month_name[1:])
    total_customer_df = total_customer_df.set_index('order_month').reindex(month_order)
    return total_customer_df

def create_order_status_df(df):
    order_status_df = df.pivot_table(
        index='order_status', values='order_id', 
        aggfunc='nunique', margins=True)
    #mengubah nilai menjadi persentase dari total
    order_status_df['percentage_of_total'] = order_status_df['order_id'].apply(lambda x: (x / order_status_df['order_id']['All']) * 100)
    #mengubah nama kolom dan mereset indeks
    order_status_df = order_status_df.rename(columns={'order_id': 'total_order'}).reset_index()
    order_status_df['percentage_of_total'] = order_status_df['percentage_of_total'].round(2)
    return order_status_df

def create_order_review_df(df):
    df['review_score'].fillna('No Review', inplace=True)
    order_review_df = df.pivot_table(
        index='review_score', values='order_id', aggfunc='nunique')
    #mengubah nama kolom
    order_review_df = order_review_df.set_axis(['total_order'], axis=1).reset_index()
    return order_review_df

def create_customer_state_df(df):
    customer_state_df = df.pivot_table(
        index='customer_state', values='customer_id', 
        aggfunc='nunique').sort_values(by='customer_id', ascending=False)
    #mengubah nama kolom dan mereset indeks
    customer_state_df = customer_state_df.rename(
        columns={'customer_id': 'number_of_customer'}).reset_index()
    return customer_state_df

def create_customer_spending_df(df):
    customer_spending_df = df.pivot_table(
        index='order_month', values='payment_value', 
        columns='order_year', aggfunc='mean').reset_index()
    #mengurutkan hasil pivot table berdasarkan urutan bulan pada kalender
    month_order = list(calendar.month_name[1:])
    customer_spending_df = customer_spending_df.set_index('order_month').reindex(month_order)
    return customer_spending_df

all_df = pd.read_csv("all_data_projek.csv")

datetime_columns = ["order_purchase_timestamp"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)

st.header('Customer Behaviour Analysis')

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

# Mengambil start_date & end_date dari date_input
start_date, end_date = st.date_input(
label='Select Period',min_value=min_date,
max_value=max_date,
value=[min_date, max_date]
)

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

total_customer_df = create_total_customer_df(main_df)
order_status_df = create_order_status_df(main_df)
order_review_df = create_order_review_df(main_df)
customer_state_df = create_customer_state_df(main_df)
customer_spending_df = create_customer_spending_df(main_df)

#MEMBUAT GRAFIK 1
st.subheader('Trend of the Number of Customer')
fig, ax = plt.subplots(figsize=(12, 5))  # Mengatur ukuran grafik
colors = ["#E66F4E", "#E8C567", "#2B9C90"]
for i, column in enumerate(total_customer_df.columns):
    ax.plot(total_customer_df.index, total_customer_df[column], 
            marker='o', label=str(column), color=colors[i])
# mengatur label sumbu
ax.set_xlabel('Month')
ax.set_ylabel('Number of Customer')
# menempatkan legend di luar kotak grafik
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# menampilkan grafik
st.pyplot(fig)

#MEMBUAT GRAFIK 2 DAN 3
col1, col2 = st.columns(2)
 
with col1:
    st.subheader('Percentage of Customer Order Status')
    order_status_df.rename(columns={
        'order_status': 'Order Status',
        'total_order': 'Total Order',
        'percentage_of_total': 'Percentage'
    }, inplace=True)
    order_status_df

with col2:
    st.subheader('Customer Review Based on Their Order')
    fig, ax = plt.subplots(figsize=(8, 8))  # Mengatur ukuran grafik
    
    sns.barplot( 
        x="review_score", 
        y="total_order",
        data=order_review_df,
        color='#2B9C90',
        ax=ax)

    # Mengatur rotasi label pada sumbu x
    plt.xticks(rotation=0)

    # Mengatur judul dan label sumbu
    plt.xlabel('Review Score')
    plt.ylabel('Number of Order')

    # Menampilkan grafik batang di Streamlit
    st.pyplot(fig)

#MEMBUAT GRAFIK 4
st.subheader('Trend of Customer Average Spending')
fig, ax = plt.subplots(figsize=(12, 5))  # Mengatur ukuran grafik
for i, column in enumerate(total_customer_df.columns):
    ax.plot(customer_spending_df.index, 
            customer_spending_df[column], marker='o', 
            label=str(column), color=colors[i])

#mengatur sumbu
ax.set_xlabel('Month')
ax.set_ylabel('Spending')

ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
st.pyplot(fig)

#MEMBUAT GRAFIK 5
st.subheader('Number of Customer Based on State')
fig, ax = plt.subplots(figsize=(12, 5))  # Mengatur ukuran grafik

sns.barplot( 
        x="customer_state", 
        y="number_of_customer",
        data=customer_state_df,
        color='#E66F4E',
        ax=ax)

# mengatur judul dan label sumbu
ax.set_xlabel('State Name')
ax.set_ylabel('Number of Customer')

# menempatkan legend di luar kotak grafik
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
st.pyplot(fig)