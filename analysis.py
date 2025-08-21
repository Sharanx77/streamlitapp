import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("💸 Expense Tracker Dashboard")

df=pd.read_csv("data.csv")
# 2️⃣ Clean & Categorize
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.dropna(subset=['Date'])
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)
df['Category'] = df['Category'].fillna("Uncategorized")

# 3️⃣ Grouping
category_summary = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
monthly_summary = df.groupby(df['Date'].dt.to_period('M'))['Amount'].sum()

# 4️⃣ Visuals
st.subheader("📊 Expense Breakdown by Category")
fig1, ax1 = plt.subplots()
ax1.pie(category_summary, labels=category_summary.index, autopct='%1.1f%%')
st.pyplot(fig1)

st.subheader("📆 Monthly Spending")
fig2, ax2 = plt.subplots()
monthly_summary.plot(kind='bar', ax=ax2)
st.pyplot(fig2)

# 5️⃣ Budget Alerts
st.subheader("🚨 Budget Monitor")
budget = st.number_input("Set Monthly Budget", value=5000)
latest_month = monthly_summary.index[-1]
spent = monthly_summary.iloc[-1]

if spent > budget:
    st.error(f"⚠️ Budget exceeded! ₹{spent} spent in {latest_month}.")
else:
    st.success(f"✅ Within budget. ₹{spent} spent in {latest_month}.")

# 6️⃣ Export to Excel
output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name='Expenses')
    category_summary.to_frame().to_excel(writer, sheet_name='Category Summary')
    monthly_summary.to_frame().to_excel(writer, sheet_name='Monthly Summary')

st.download_button("📥 Download Report", data=output.getvalue(), file_name="expense_report.xlsx")