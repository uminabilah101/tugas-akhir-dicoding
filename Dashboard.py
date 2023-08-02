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

def create_order_dayofweek_df(df):
    #membuat kolom baru berisi day of week customer melakukan pesanan
    df['order_date_dayofweek_name'] = df['order_purchase_timestamp'].apply(lambda x: x.strftime('%A'))
    days_order = list(calendar.day_name)

    #membuat tabel pivot berisi total order berdasarkan hari
    order_dayofweek_df = df.pivot_table(index='order_date_dayofweek_name', values='order_id', aggfunc='nunique').reset_index().sort_values(by='order_id', ascending=False)
    order_dayofweek_df.rename(columns={'order_id': 'total_order'}, inplace=True)
    
    # Urutkan hari berdasarkan urutan alami (Senin, Selasa, Rabu, dst.)
    order_dayofweek_df['order_date_dayofweek_name'] = pd.Categorical(order_dayofweek_df['order_date_dayofweek_name'], categories=days_order, ordered=True)
    order_dayofweek_df.sort_values('order_date_dayofweek_name', inplace=True)

    return order_dayofweek_df

def create_order_review_df(df):
    df['review_score'].fillna('No Review', inplace=True)
    order_review_df = df.pivot_table(
        index='review_score', values='order_id', aggfunc='nunique')
    #mengubah nama kolom
    order_review_df = order_review_df.set_axis(['total_order'], axis=1).reset_index()
    return order_review_df

def create_clustering_state_df(df):
    #membuat tabel pivot baru
    customer_state_df = df.pivot_table(index='customer_state', values='customer_id', aggfunc='nunique').sort_values(by='customer_id', ascending=False)
    transaction_state_df = df.pivot_table(index='customer_state', values='payment_value', aggfunc='mean').reset_index()

    #menggabungkan tabel
    clustering_state_df = pd.merge(customer_state_df, transaction_state_df, on='customer_state', how='inner')
    clustering_state_df = clustering_state_df.rename(columns={'customer_id': 'number_of_customer', 'payment_value': 'average_of_transaction'})
    clustering_state_df['state_name'] = clustering_state_df.index
    clustering_state_df = clustering_state_df.reset_index(drop=True)
    return clustering_state_df

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
order_dayofweek_df = create_order_dayofweek_df(main_df)
order_review_df = create_order_review_df(main_df)
clustering_state_df = create_clustering_state_df(main_df)
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
    st.subheader('Total Orders by Day of Week')
    fig, ax = plt.subplots(figsize=(8, 8))  # Mengatur ukuran grafik
    
    sns.barplot( 
        x="order_date_dayofweek_name", 
        y="total_order",
        data=order_dayofweek_df,
        color='#2B9C90',
        ax=ax)

    # Mengatur rotasi label pada sumbu x
    plt.xticks(rotation=0)

    # Mengatur judul dan label sumbu
    plt.xlabel('Day of Week')
    plt.ylabel('Total Orders')

    # Menampilkan grafik batang di Streamlit
    st.pyplot(fig)

with col2:
    st.subheader('Customer Review on Their Orders')
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
st.subheader('Number of Customers and Average of Transactions by State')
fig, ax = plt.subplots(figsize=(12, 5))  # Mengatur ukuran grafik

sns.barplot(
    x="state_name",
    y="number_of_customer",
    data=clustering_state_df,
    color='#2B9C90',
    ax=ax
)

#mengaktifkan sumbu kanan (axis 2)
ax2 = ax.twinx()

#plot data average_of_transaction pada sumbu kanan (axis 2)
sns.lineplot(
    x='state_name',
    y='average_of_transaction',
    data=clustering_state_df,
    color='#E66F4E',
    marker='o',
    ax=ax2
)

# mengatur judul dan label sumbu
ax.set_xlabel('State Name')
ax.set_ylabel('Number of Customer')
ax2.set_ylabel('Average of Transactions')

ax.legend(labels=['Number of Customers'], loc='lower right')
ax2.legend(labels=['Average of Transactions'], loc='upper right')

st.pyplot(fig)
