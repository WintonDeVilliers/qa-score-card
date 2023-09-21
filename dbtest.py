import streamlit as st
import mysql.connector
import pandas as pd


def submit_form_db_connect():
    try:
        db_connection = mysql.connector.connect(**st.secrets.db_credentials)
        # db_cursor = db_connection.cursor()
        print("Connection Establito")
    except():
        print("DB Connection Error")

    return db_connection


def dbtest():
    interaction_id = "sdhjfk"
    other = "UIDO"
    submitted = st.sidebar.button("DBTESTSubmit")
    if submitted:
        sql_input_fields = """INSERT INTO qa_score_card (interaction_id, other) VALUES (%s, %s)"""
        val_input_fields = (interaction_id, other)
        try:
            get_db_connection = submit_form_db_connect()
            get_db_connection_cursor = get_db_connection.cursor()
            get_db_connection_cursor.execute(sql_input_fields, val_input_fields)
            # get_db_connection_cursor.execute(sql_intro_section, val_intro_section)
            # get_db_connection_cursor.execute(sql_customer_validation_section, val_customer_validation_section)
            # get_db_connection_cursor.execute(sql_presentation_and_legal_section, val_presentation_and_legal_section)
            # get_db_connection_cursor.execute(sql_form_scores, val_form_scores)
            print(get_db_connection_cursor.rowcount, "record inserted.")
            get_db_connection.commit()
            print("Data inserted successfully!")
            st.sidebar.success("Data Inserted Successfully")
            get_db_connection_cursor.close()
            get_db_connection.close()
        except():
            print("DB Connection CURSOR Error")
