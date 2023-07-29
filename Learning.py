import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import calendar

sns.set(style='dark')

#data preparing
order_df = pd.read_csv("order_data.csv")
country_df = pd.read_csv("country_data.csv")
spending_df = pd.read_csv("spending_data.csv")

st.header('Customer Behaviour Analysis')

#Membuat Grafik 1
st.subheader('Trend of Customer')
pivot1 = order_df.pivot_table(index='order_month', values='customer_id',columns='order_year', aggfunc='nunique').reset_index()

# Mengurutkan hasil pivot table berdasarkan urutan bulan pada kalender
month_order = list(calendar.month_name[1:])
pivot1 = pivot1.set_index('order_month').reindex(month_order)

#menghapus kolom tahun 2016 karena memiliki banyak nilai kosong
pivot1 = pivot1.drop(columns=[2016])

# membuat grafik garis
fig, ax = plt.subplots(figsize=(12, 5))  # Mengatur ukuran grafik
for column in pivot1.columns:
    ax.plot(pivot1.index, pivot1[column], marker='o', label=str(column))

# mengatur label sumbu
ax.set_xlabel('Month')
ax.set_ylabel('Number of Customer')

# menempatkan legend di luar kotak grafik
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# menampilkan grafik
st.pyplot(fig)

st.caption("Berdasarkan grafik diatas dapat diketahui bahwa jumlah pembeli per bulan terus bertambah dari tahun 2017 hingga 2018. Selain itu, informasi yang dapat digaris bawahi adalah bahwa jumlah pembeli cendeung menurun pada bulan April dan Juni, serta meningkat pada bulan Maret dan Mei")


#Membuat grafik 2
st.subheader('Number of Customer from 2017 to 2018')
#membuat tabel pivot jumlah konsumen yang melakukan transaksi berdasarkan negara
pivot2 = country_df.pivot_table(index='customer_state', values='customer_id', aggfunc='nunique').sort_values(by='customer_id', ascending=False)

# membuat grafik batang
fig, ax = plt.subplots(figsize=(12, 5))  # Mengatur ukuran grafik
ax.bar(pivot2.index, pivot2['customer_id'])

# mengatur judul dan label sumbu
ax.set_xlabel('State Name')
ax.set_ylabel('Number of Customer')

# menempatkan legend di luar kotak grafik
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
st.pyplot(fig)

#Membuat Grafik 3
st.subheader('Customer Average Spending in 2017 - 2018')
pivot3 = spending_df.pivot_table(index='order_month', values='payment_value',columns='order_year', aggfunc='mean').reset_index()

# Mengurutkan hasil pivot table berdasarkan urutan bulan pada kalender
month_order = list(calendar.month_name[1:])
pivot3 = pivot3.set_index('order_month').reindex(month_order)

#menghapus kolom tahun 2016 karena memiliki banyak nilai kosong
pivot3 = pivot3.drop(columns=[2016])

# membuat grafik garis
fig, ax = plt.subplots(figsize=(12, 5))  # Mengatur ukuran grafik
for column in pivot1.columns:
    ax.plot(pivot3.index, pivot1[column], marker='o', label=str(column))

#mengatur sumbu
ax.set_xlabel('Month')
ax.set_ylabel('Spending')

ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
st.pyplot(fig)