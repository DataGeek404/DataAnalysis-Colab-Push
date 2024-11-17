# Combine all steps into a single Python script, from Data Preparation to Interactive Dashboard Creation

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
data_path = 'Police_Bulk_Data_2014_20241027(1).csv'  # Update with your dataset file
data = pd.read_csv(data_path)

# Data Preparation
data['offensedate'] = pd.to_datetime(data['offensedate'], errors='coerce')
data['offensereporteddate'] = pd.to_datetime(data['offensereporteddate'], errors='coerce')
data['offenseage'] = pd.to_numeric(data['offenseage'], errors='coerce')
data['offenserace'] = data['offenserace'].fillna('Unknown')
data['offensegender'] = data['offensegender'].fillna('Unknown')

# Standardize offense types
data['offense_category'] = data['offensedescription'].apply(
    lambda x: 'Burglary' if 'BURGLARY' in str(x).upper() else (
        'Theft' if 'THEFT' in str(x).upper() else 'Other'
    )
)

# Streamlit Dashboard
st.title("Crime Analysis Dashboard")

# Sidebar for filtering offense category
offense_filter = st.sidebar.selectbox(
    'Select Offense Category',
    options=['All', 'Burglary', 'Theft'],
    index=0
)

# Filter data based on user selection
filtered_data = data if offense_filter == 'All' else data[data['offense_category'] == offense_filter]

# Visualization 1: Offenses Over Time
st.header(f"Offense Trends for {offense_filter}")
offense_trend = filtered_data['offensedate'].dt.year.value_counts().sort_index()
fig1, ax1 = plt.subplots()
offense_trend.plot(kind='bar', ax=ax1)
ax1.set_title("Offenses Over Years")
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Offenses")
st.pyplot(fig1)

# Visualization 2: Top 10 Offense Types
st.header("Top 10 Offense Types")
top_offenses = filtered_data['offensedescription'].value_counts().head(10)
fig2, ax2 = plt.subplots()
top_offenses.plot(kind='bar', ax=ax2)
ax2.set_title("Top 10 Offense Types")
ax2.set_xlabel("Offense Type")
ax2.set_ylabel("Frequency")
ax2.tick_params(axis='x', rotation=45)
st.pyplot(fig2)

# Visualization 3: Age Distribution
st.header("Age Distribution")
fig3, ax3 = plt.subplots()
sns.histplot(filtered_data['offenseage'], kde=True, bins=30, ax=ax3)
ax3.set_title("Age Distribution of Offenders")
ax3.set_xlabel("Age")
st.pyplot(fig3)

# Visualization 4: Correlation Heatmap
st.header("Correlation Heatmap")
numeric_cols = filtered_data[['offensereportingarea', 'offenseage']].dropna()
fig4, ax4 = plt.subplots(figsize=(8, 6))
sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', fmt='.2f', ax=ax4)
ax4.set_title("Correlation Heatmap")
st.pyplot(fig4)

# Visualization 5: Reporting Area vs Age
st.header("Age vs. Reporting Area")
fig5, ax5 = plt.subplots()
sns.scatterplot(x='offenseage', y='offensereportingarea', data=filtered_data, alpha=0.5, ax=ax5)
ax5.set_title("Age vs. Reporting Area")
ax5.set_xlabel("Age")
ax5.set_ylabel("Reporting Area")
st.pyplot(fig5)

# Visualization 6: Theft vs Burglary Trends
st.header("Theft vs Burglary Trends")
theft_burglary_trends = data.groupby(['offensedate', 'offense_category']).size().unstack(fill_value=0)
theft_burglary_trends = theft_burglary_trends.resample('Y').sum()  # Resample by year
fig6, ax6 = plt.subplots()
theft_burglary_trends.plot(ax=ax6)
ax6.set_title("Theft vs Burglary Trends Over Time")
ax6.set_xlabel("Year")
ax6.set_ylabel("Number of Offenses")
st.pyplot(fig6)

# Save the full project script to a Python file
full_project_path = '/mnt/data/full_project_dashboard.py'

with open(full_project_path, 'w') as file:
    file.write(full_project_code)

full_project_path
