import streamlit as st
import mysql.connector
import pandas as pd
# import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def page_scenario_2():
    try:
        db_connection = mysql.connector.connect(**st.secrets.db_credentials)
        db_cursor = db_connection.cursor()
        print("Connection Established")
    except Exception as e:
        # Detailed error handling to provide feedback if there's an issue with the database connection or query execution
        st.error("An error occurred while fetching data from the database.")
        st.error(str(e))
    # mycursor = mydb.cursor()
    # db_connection = mysql.connector.connect()
    db_cursor.execute("SELECT * FROM qa_score_card")
    # db_supervisor_names = db_cursor.execute("SELECT supervisor_name FROM qa_score_card")
    myresult = db_cursor.fetchall()
    # Convert the fetched results to a DataFrame
    df = pd.DataFrame(myresult, columns=db_cursor.column_names)
    st.write(df)

    distinct_supervisors = df["supervisor_name"].unique()
    


    selected_supervisor = st.sidebar.selectbox("Select a Supervisor", distinct_supervisors)
    filtered_df_supervisor = df[df["supervisor_name"] == selected_supervisor]

    distinct_agents = filtered_df_supervisor["agent_name"].unique().tolist()

    selected_agent = st.sidebar.selectbox("Select an Agent", distinct_agents)
    filtered_df_agent = filtered_df_supervisor[filtered_df_supervisor["agent_name"] == selected_agent]


    # Retrieve distinct values for 'split-call', 'product-type', and 'date' columns
    distinct_split_calls = df["split_call"].unique().tolist()
    distinct_product_types = df["product_type"].unique().tolist()
    distinct_evaluation_dates = df["evaluation_date"].unique().tolist()
    distinct_call_dates = df["call_date"].unique().tolist()

    # Add selectboxes for 'split-call', 'product-type', 'evaluation_date', and 'call_date' in the sidebar
    selected_split_call = st.sidebar.selectbox("Select a Split Call", distinct_split_calls)
    selected_product_type = st.sidebar.selectbox("Select a Product Type", distinct_product_types)
    selected_evaluation_date = st.sidebar.selectbox("Select an Evaluation Date", distinct_evaluation_dates)
    selected_call_date = st.sidebar.selectbox("Select a Call Date", distinct_call_dates)


    filtered_df_split_call = filtered_df_agent[filtered_df_agent["split_call"] == selected_split_call]
    filtered_df_product_type = filtered_df_split_call[filtered_df_split_call["product_type"] == selected_product_type]
    filtered_df_evaluation_date = filtered_df_product_type[filtered_df_product_type["evaluation_date"] == selected_evaluation_date]
    filtered_df_date = filtered_df_evaluation_date[filtered_df_evaluation_date["call_date"] == selected_call_date]


    st.write(filtered_df_date)


     # Calculate the average score for all records
    avg_score = df['final_score'].mean()

    # Create a bar chart for the average score
    fig, ax = plt.subplots()
    ax.bar('Average Score', avg_score)
    ax.set_ylabel('Score')
    ax.set_title('Average Score for All Records')
    st.pyplot(fig)

    # Calculate the average score by product category
    avg_score_by_category = df.groupby('product_type')['final_score'].mean()

    # Create a bar chart for the average score by product category
    fig, ax = plt.subplots()
    ax.bar(avg_score_by_category.index, avg_score_by_category.values)
    ax.set_xlabel('Product Category')
    ax.set_ylabel('Average Score')
    ax.set_title('Average Score by Product Category')
    ax.grid(False)
    st.pyplot(fig)
    
    
    # Select the columns of interest
    score_columns = ['intro_score', 'customer_validation_score', 'presentation_and_legal_score']

    # Calculate the average score for each column
    avg_scores = df[score_columns].mean()

    # Create a bar chart for the average scores
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figsize to change the width and height of the visualization
    ax.bar(avg_scores.index, avg_scores.values)
    ax.set_xlabel('')  # Remove the x-axis label
    ax.set_ylabel('Average Score')
    ax.set_title('Average Scores')
    ax.grid(False)  # Remove the grid lines
    ax.spines['top'].set_visible(False)  # Remove the top border
    ax.spines['right'].set_visible(False)  # Remove the right border
    ax.spines['left'].set_visible(False)  # Remove the left border
    ax.spines['bottom'].set_visible(False)  # Remove the bottom border
    ax.tick_params(axis='x', which='both', bottom=False)  # Remove the x-axis ticks
    st.pyplot(fig)
    

    # Select the columns of interest
    response_columns = ['greeting', 'introduce_bank', 'call_reason', 'pre_qualifying', 'reg_statement']

    # Filter the DataFrame for the selected supervisor
    filtered_df_supervisor = df[df["supervisor_name"] == selected_supervisor]

    # Create a bar chart for each agent in the supervisor's team
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figsize to change the width and height of the visualization

    # Iterate over each agent in the supervisor's team
    for agent in filtered_df_supervisor['agent_name'].unique():
        # Filter the DataFrame for the current agent
        filtered_df_agent = filtered_df_supervisor[filtered_df_supervisor['agent_name'] == agent]
        
        # Count the number of 'Yes' and 'No' responses for each column
        response_counts = filtered_df_agent[response_columns].apply(pd.Series.value_counts)
        
        # Plot the 'Yes' and 'No' counts as stacked bars
        response_counts.plot(kind='bar', stacked=True, ax=ax, label=agent)

    ax.set_xlabel('Response')
    ax.set_ylabel('Count')
    ax.set_title('Comparison of Responses for Introduction')
    ax.legend(title='Agent')
    ax.grid(False)  # Remove the grid lines
    ax.spines['top'].set_visible(False)  # Remove the top border
    ax.spines['right'].set_visible(False)  # Remove the right border
    ax.spines['left'].set_visible(False)  # Remove the left border
    ax.spines['bottom'].set_visible(False)  # Remove the bottom border
    ax.tick_params(axis='x', which='both', bottom=False)  # Remove the x-axis ticks

    # Add text annotation for the selected supervisor's name
    ax.text(0.5, 1.05, f"Supervisor: {selected_supervisor}", transform=ax.transAxes, ha='center')
    st.pyplot(fig)


    # Select the columns of interest
    response_columns = ['greeting', 'introduce_bank', 'call_reason', 'pre_qualifying', 'reg_statement']

    # Group the data by agent name and count the number of 'Yes' and 'No' responses for each column
    response_counts = df.groupby('agent_name')[response_columns].apply(lambda x: x.stack().value_counts()).unstack()

    # Create a bar chart for the response counts
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figsize to change the width and height of the visualization

    # Plot the 'Yes' and 'No' counts as stacked bars
    response_counts.plot(kind='bar', stacked=True, ax=ax)

    ax.set_xlabel('Response')
    ax.set_ylabel('Count')
    ax.set_title('Comparison of Responses')
    ax.legend(title='Agent')
    ax.grid(False)  # Remove the grid lines
    ax.spines['top'].set_visible(False)  # Remove the top border
    ax.spines['right'].set_visible(False)  # Remove the right border
    ax.spines['left'].set_visible(False)  # Remove the left border
    ax.spines['bottom'].set_visible(False)  # Remove the bottom border
    ax.tick_params(axis='x', which='both', bottom=False)  # Remove the x-axis ticks
    st.pyplot(fig)


    db_cursor.close()
    db_connection.close()




    """ we want to create a dashboard that essentially allows us to walk-through the data."""

    # st.sidebar(st.selectbox("Supervisor", db_supervisor_names))
