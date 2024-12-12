import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    # Set global font to Times New Roman
    plt.rcParams["font.family"] = "Times New Roman"


        # Load the restructured data
    file_path = "restructured_data_2.csv"  # Update with your actual path
    df = pd.read_csv(file_path)
    df.fillna(0, inplace=True)

        # Sidebar Filters
    # years = sorted(df['Year'].unique())
    # universities = sorted(df['Uviversity'].unique())

    years = ["Ählisi"] + sorted(df['Year'].unique())
    universities = ["Ählisi"] + sorted(df['Uviversity'].unique())

    selected_years = st.multiselect("Ýyl saýlaň", years, default='Ählisi')
    selected_universities = st.multiselect("Uniwersitet saýlaň", universities, default='Ählisi')
    # selected_faculties = st.multiselect("Select Faculty/Faculties", faculties, default=faculties)

        # Filter data based on selection
    filtered_df = df[
        ((df['Year'].isin(selected_years)) | ("Ählisi" in selected_years)) &
        ((df['Uviversity'].isin(selected_universities)) | ("Ählisi" in selected_universities))
    ]

        # Display filtered data
    # st.write("### Filtered Data")
    # st.dataframe(filtered_df)

        # 1. Enrollment Trends Over Years
    st.write("### Ýyllaryň dowamynda umumy hasaba alyş tendendi")
    enrollment_trend = filtered_df.groupby('Year')[['Tölegli talyp sany', 'BŽ talyp sany']].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=enrollment_trend, x='Year', y='Tölegli talyp sany', marker='o', label='Tölegli talyplar', ax=ax)
    sns.lineplot(data=enrollment_trend, x='Year', y='BŽ talyp sany', marker='o', label='BŽ talyplar', ax=ax)
    ax.set_title("Ýyl boýunça umumy hasaba alyş tendendi", fontsize=18, weight='bold')
    ax.set_xlabel("Ýyl", fontsize=14)
    ax.set_ylabel("Talyp sany", fontsize=14)
    ax.legend(fontsize=12)
    st.pyplot(fig)

        # 2. University-Wise Enrollment
    st.write("### Uniwersitet ara hasaba alyş")
    university_totals = filtered_df.groupby('Uviversity')[['Tölegli talyp sany', 'BŽ talyp sany']].sum()
    if not university_totals.empty and university_totals.sum().sum() > 0:
        fig, ax = plt.subplots(figsize=(12, 8))
        university_totals.plot(kind='bar', stacked=True, ax=ax, color=["#87cefa", "#f59393"])
        ax.set_title("Uniwersitet ara hasaba alyş", fontsize=18, weight='bold')
        ax.set_xlabel("Uniwersitet", fontsize=14)
        ax.set_ylabel("Talyp sany", fontsize=14)
        st.pyplot(fig)
    else:
        st.warning("Bu uniwersitetde hiç hili hünärmen ugur yok.")

        # 3. Faculty Analysis
    st.write("### Hünärmen ugurlary boýunça hasaba alyş")
    faculty_totals = filtered_df.groupby('Hünärler')[['Tölegli talyp sany', 'BŽ talyp sany']].sum()
    if not faculty_totals.empty and faculty_totals.sum().sum() > 0:
        faculty_totals = faculty_totals[faculty_totals.sum(axis=1) > 0]  # Remove faculties with zero students
        fig, ax = plt.subplots(figsize=(12, 8))
        faculty_totals.plot(kind='bar', stacked=True, ax=ax, color=["#90ee90", "#f2f277"])
        ax.set_title("Hünärmen ugurlary boýunça hasaba alyş", fontsize=18, weight='bold')
        ax.set_xlabel("Hünärmen ugurlary", fontsize=14)
        ax.set_ylabel("Talyp sany", fontsize=14)
        st.pyplot(fig)
    else:
        st.warning("Bu uniwersitetde hiç hili hünärmen ugur yok.")


    # 5. Yearly Enrollment Summary
    st.write("### Ýyl boýunça hasaba alyş")
    yearly_totals = filtered_df.groupby('Year')[['Tölegli talyp sany', 'BŽ talyp sany']].sum()
    if not yearly_totals.empty and yearly_totals.sum().sum() > 0:
            st.bar_chart(yearly_totals)
    else:
        st.warning("Bu uniwersitetde hiç hili hünärmen ugur yok.")


    ol1, col2, col3 = st.columns(3)

    with col2:
        st.write("### Tölegli talyplar we BŽ talyplar göterim gatnaşygy")

        total_students = filtered_df[['Tölegli talyp sany', 'BŽ talyp sany']].sum().sum()
        paid_percentage = (filtered_df['Tölegli talyp sany'].sum() / total_students) * 100
        unpaid_percentage = (filtered_df['BŽ talyp sany'].sum() / total_students) * 100

        if total_students.sum().sum() > 0:
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(
                [paid_percentage, unpaid_percentage],
                labels=["Tölegli talyp sany", "BŽ talyp sany"],
                autopct='%1.1f%%',
                colors=["#87cefa", "#f59393"],
                startangle=90,
                textprops={"fontsize": 18}
            )
            ax.set_title("Tölegli talyplar we BŽ talyplar göterim gatnaşygy", fontsize=16, weight='bold')
            st.pyplot(fig)
        else:
            st.warning("Bu uniwersitetde hiç hili hünärmen ugur yok.")



# ???????????????????????????????
    st.write("### Ýyl-ýyla hasaba alyşynyň göterim üýtgeýşi")
    enrollment_trend['Total Students'] = enrollment_trend['Tölegli talyp sany'] + enrollment_trend['BŽ talyp sany']
    if 'Total Students' in enrollment_trend.columns and (enrollment_trend['Total Students'] > 0).any():

        enrollment_trend['YoY Change (%)'] = enrollment_trend['Total Students'].pct_change() * 100

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(
            x='Year', y='YoY Change (%)', data=enrollment_trend, palette="viridis", ax=ax
        )
        ax.axhline(0, color="gray", linestyle="--", linewidth=1)
        ax.set_title("Ýyl-ýyla hasaba alyşynyň göterim üýtgeýşi", fontsize=16, weight='bold')
        ax.set_xlabel("Ýyl", fontsize=14)
        ax.set_ylabel(" Göterim üýtgeýşi (%)", fontsize=14)
        st.pyplot(fig)
    else:
        st.warning("Bu uniwersitetde hiç hili hünärmen ugur yok.")

# ????????????
    st.write("### Hümärmen ugurlary boýunça ýokary 10 sany görkeziji")
    faculty_totals['Total Students'] = faculty_totals['Tölegli talyp sany'] + faculty_totals['BŽ talyp sany']
    if 'Total Students' in faculty_totals.columns and (faculty_totals['Total Students'] > 0).any():

        top_faculties = faculty_totals.sort_values('Total Students', ascending=False).head(10)

        fig, ax = plt.subplots(figsize=(10, 8))
        top_faculties['Total Students'].plot(kind='barh', color="#90ee90", ax=ax)
        ax.set_title("Hümärmen ugurlary boýunça ýokary 10 sany görkeziji", fontsize=16, weight='bold')
        ax.set_xlabel("Talyplar", fontsize=14)
        ax.set_ylabel("Hümärmen ugur", fontsize=14)
        ax.invert_yaxis()
        st.pyplot(fig)
    else:
        st.warning("Bu uniwersitetde hiç hili hünärmen ugur yok.")


