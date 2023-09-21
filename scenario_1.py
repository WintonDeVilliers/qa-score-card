from datetime import date
import mysql
import pandas as pd
import streamlit as st

from sales_normal_call_flow import normal_call_assessment_criteria


def submit_form(sql, val):
    submitted = st.sidebar.button("submit")
    # submitted = st.form_submit_button("Submit")
    if submitted:
        try:
            print("Connection Established")
            db_connection = mysql.connector.connect(**st.secrets.db_credentials)
            db_cursor = db_connection.cursor()
            print("Connection ZZZZZEstablished")
        except():
            print("DB Connection Error")

        db_cursor.execute(sql, val)
        db_connection.commit()
        print("Data inserted successfully!")
        db_cursor.close()
        db_connection.close()


# def submit_form_db_connect():
#     try:
#         db_connection = mysql.connector.connect(**st.secrets.db_credentials)
#         # db_cursor = db_connection.cursor()
#         print("Connection Establito")
#     except():
#         print("DB Connection Error")
#
#     return db_connection


def page_scenario_1():
    st.title("QA SCORE CARD (SALES)")
    st.header("Project Summary")
    st.markdown('''
    This project aims to develop a desktop or web application that replaces the existing
    Excel-based quality assurance score-cards. The application will provide a user-friendly
    form interface resembling the Excel sheet while maintaining the same score calculations.
    It will leverage data science capabilities to gather insights from captured data, and
    provide data visualisation enabling improved analysis and decision-making.
    ''')
    '''FORM TEXT-INPUT/SELECTOR FIELDS CONTAINERS/LISTS'''

    st.markdown("---")
    st.markdown('''# Form Rules
    Form rules pertain to how the form responds when the below radio buttons
    are changed/selected as well as score calculations.
    Form Logic can be edit through underlying code changes.

    NOTE: scores in this prototype are not weighted
    Yes response will add 1 point
    No response will subtract 1 point
    

    Auto-Zero 
    Questions in the form that result in a Total Score of zero when answer is "No".

    - Regulatory Statement
    - Credit Compliance 
    - Banking Details
    - Credit Life
    - Credit Benefits
    - Credit life Waiting Period

    Auto-Zero
    Questions in the form that result in a Total Score of zero when answer is "Yes".

    - Overstated Expenses
    - Understated Expenses

    Score Calculation

    Introduction Score Calculation:   
    - intro_score = section_points_out_of_5 / 5 * 100

    Customer Validation score Calculation:
    - customer_validation_score = section_points_out_of_2 / 2 * 100

    Presentation & Compliance Score Calculation:
    - presentation_&_compliance_score = section_points_out_of_21 / 21 * 100

    Total Score Calculation:
    - total_score = combined_points_for_each_section / 28 * 100

    ''')
    st.markdown("---")

    # normal_call_fields()
    normal_call_assessment_criteria()
    st.markdown("---")



