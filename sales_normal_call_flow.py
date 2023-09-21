import time
from datetime import date
import streamlit as st
import mysql
import pandas as pd

from dbtest import dbtest


def submit_form_db_connect():
    try:
        db_connection = mysql.connector.connect(**st.secrets.db_credentials)
        # db_cursor = db_connection.cursor()
        print("Connection Establito")
    except():
        print("DB Connection Error")

    return db_connection


def intro_score_calc_points(intro_radio_btn_responses):
    intro_points = 5
    for i in range(len(intro_radio_btn_responses)):
        if intro_radio_btn_responses[i] == "No":
            intro_points -= 1
    # st.write(intro_points)
    # intro_score = (intro_points / 5) * 100
    return intro_points


def customer_validation_score_calc_points(customer_validation_radio_btn_responses):
    customer_validation_points = 2
    for i in range(len(customer_validation_radio_btn_responses)):
        if customer_validation_radio_btn_responses[i] == "No":
            customer_validation_points -= 1
    # st.write(customer_validation_points)
    # customer_validation_score = (customer_validation_points / 2) * 100
    return customer_validation_points


def presentation_and_compliance_calc_points(presentation_compliance_radio_btn_responses,
                                            presentation_compliance_radio_btn_responses_inverse):
    presentation_and_compliance_points = 21
    for i in range(len(presentation_compliance_radio_btn_responses)):
        if presentation_compliance_radio_btn_responses[i] == "No":
            presentation_and_compliance_points -= 1
    for i in range(len(presentation_compliance_radio_btn_responses_inverse)):
        if presentation_compliance_radio_btn_responses_inverse[i] == "Yes":
            presentation_and_compliance_points -= 1
    # st.write(presentation_and_compliance_points)
    # presentation_and_compliance_score = (presentation_and_compliance_points / 21) * 100
    return presentation_and_compliance_points

def search_db_for_existing_assessment_with_application_id(application_id):
    try:
        get_db_connection = submit_form_db_connect()
        get_db_connection_cursor = get_db_connection.cursor()
        query = f"SELECT *  FROM qa_score_card WHERE application_id = '{application_id}'"
        get_db_connection_cursor.execute(query)
        myresult = get_db_connection_cursor.fetchall()
        df = pd.DataFrame(myresult, columns=get_db_connection_cursor.column_names)
        st.write(df)
        print(get_db_connection_cursor.rowcount, "record found.")
        success_message = st.sidebar.success("Record Found Successfully")
        time.sleep(3)  # Wait for 3 seconds
        success_message.empty()  # Clear the alert
        get_db_connection_cursor.close()
        get_db_connection.close()
    except():
        print("DB Connection CURSOR Error")

def normal_call_assessment_criteria():
    st.markdown("## Data Frame")
    st.markdown('''A data frame is a dynamic table, akin to a digital database display. It reveals database content and 
                accommodates data from the score card form.''')
    get_db_connection = submit_form_db_connect()
    db_cursor = get_db_connection.cursor()
    db_cursor.execute("SELECT * FROM qa_score_card")
    myresult = db_cursor.fetchall()
    df = pd.DataFrame(myresult, columns=db_cursor.column_names)
    st.write(df)
    db_cursor.close()
    get_db_connection.close()
    st.markdown("---")
    st.markdown("## SCORE CARD FORM")
    st.markdown("### Step 1")
    st.markdown("-- Interaction Search --")
    st.markdown(
        "This will allow you to view what was evaluated on the previous call, and establish N/A fields for current assessment.")
    st.markdown(
        "If search returns previous interactions use the checkbox below to denote current assessment as split call.")

    find_initial_call_app_id = st.text_input("Insert Application ID for your current assessment")
    button_find_previous_call = st.button("Find existing assessment")
    if button_find_previous_call:
        search_db_for_existing_assessment_with_application_id(find_initial_call_app_id)
    
    split_call = "No"
    split_call_check = st.checkbox("Split Call/Partial Call")
    if split_call_check:
        split_call = "Yes"
    '''if st.button:
        we create a SQL STATEMENT that would select record
          need to provide a way to view record
            '''
    st.markdown("### Step 2")
    st.markdown("Evaluate: Fill in the form fields and make relevant radio button(s) selections.")
    text_field_col1, text_field_col2 = st.columns([5, 5])
    with text_field_col1:
        application_id = st.text_input("Application ID", key="ss_application_id")
        agent_name = st.text_input('Agent Name')
        qa_assessor = st.text_input('QA Assessor')
        product_type = st.selectbox('Product Type', ['Loan', 'Credit Card', 'Funeral'])
        evaluation_date = st.date_input('Evaluation Date')
    with text_field_col2:
        interaction_id = st.text_input('Interaction ID')
        supervisor = st.text_input('Supervisor')
        business_unit = st.selectbox('Business Unit', ['Sales', 'Service', 'Back Office'])
        if product_type in ['Loan', 'Credit Card']:
            call_type = st.selectbox('Call Type', ['Option Not Selected', 'First Call', 'ROF Call'])
        elif product_type == "Funeral":
            call_type = st.selectbox('Call Type', ['Option Not Selected', 'New Policy', 'Update Policy'])
        # business_unit = st.selectbox('Business Unit', ['Sales', 'Service', 'Back Office'])
        call_date = st.date_input('Call Date')
    st.markdown("---")

    intro_user_selection_list = []
    customer_validation_user_selection_list = []
    presentation_and_compliance_list = []
    presentation_and_compliance_list_inverse = []
    auto_zero_yes_list = []
    auto_zero_no_list = []
    # form_section_header_col_1, form_section_header_col_2 = st.columns([4, 2])
    '''FORM RESPONSE CONTAINERS/LISTS END'''

    '''INTRODUCTION SECTION'''
    st.markdown("## Form Criteria Section(s)")

    if split_call == "No":
        split_call_check = st.checkbox(
            "Split Call: if previous Step 1 returns no Interaction but current call is partial/split. ")
        if split_call_check:
            split_call = "Yes"
    # split_call_check = st.checkbox("Split Call/Partial Call")
    # split_call_check = st.checkbox("Split Call/Partial Call")
    (introduction_tab_1, customer_validation_tab_2, presentation_compliance_tab_3) = st.tabs(["Introduction",
                                                                                              "Customer Validation",
                                                                                              "Presentation and Compliance"])
    with introduction_tab_1:
        st.markdown("## Introduction")
        # st.markdown("---")
        question_col1, answer_col1 = st.columns([5, 1])
        with question_col1:
            st.markdown("Did the Agent greet client in a professional way.(Including introducing themselves) ?")
            st.markdown("- Selecting Yes would add the prescribed weight/points")
            st.markdown("- Selecting No would subtract the prescribed weight/points")
            st.markdown("- The N/A option is disabled because there is no follow up in this scenario")
        with answer_col1:
            greeting = st.radio("Greeting", ['Yes', 'No', 'N/A'], key="ss_radio_greeting", index=0)
            intro_user_selection_list.append(greeting)
        st.markdown("---")
        question_col2, answer_col2 = st.columns([5, 1])
        with question_col2:
            st.markdown("Did the Agent introduce the bank (African Bank) ?")
        with answer_col2:
            introduce_bank = st.radio("Introduction", ['Yes', 'No', 'N/A'], key="ss_radio_introduce_bank", index=0)
            intro_user_selection_list.append(introduce_bank)
            intro_score_calc_points(intro_user_selection_list)
        st.markdown("---")
        question_col3, answer_col3 = st.columns([5, 1])
        with question_col3:
            st.markdown("Did the agent inform the customer of the reason for the call as per script ?")
        with answer_col3:
            call_reason = st.radio("Reason for Call", ['Yes', 'No', 'N/A'], key="ss_radio_call_reason", index=0)
            intro_user_selection_list.append(call_reason)
            intro_score_calc_points(intro_user_selection_list)
        st.markdown("---")
        question_col4, answer_col4 = st.columns([5, 1])
        with question_col4:
            st.markdown("Did the agent ask pre-qualifying questions ?")
        with answer_col4:
            pre_qualifying = st.radio("Pre-qualifying", ['Yes', 'No', 'N/A'], key="ss_radio_pre_qualifying", index=0)
            intro_user_selection_list.append(pre_qualifying)
            intro_score_calc_points(intro_user_selection_list)
        st.markdown("---")
        question_col5, answer_col5 = st.columns([5, 1])
        with question_col5:
            st.markdown("Did the Agent read out the regulatory statement ?")
        with answer_col5:
            reg_statement = st.radio("Regulatory statement", ['Yes', 'No', 'N/A'], key="ss_radio_reg_statement",
                                     index=0)
            intro_user_selection_list.append(reg_statement)
            auto_zero_no_list.append(reg_statement)
            intro_score_calc_points(intro_user_selection_list)
        '''INTRODUCTION SECTION END'''

    '''CUSTOMER VALIDATION SECTION'''
    with customer_validation_tab_2:
        st.markdown("## Customer Validation ")
        st.markdown("---")
        question_col6, answer_col6 = st.columns([5, 1])
        with question_col6:
            st.markdown("Did the agent ID and V the client ? ")
        with answer_col6:
            id_and_v = st.radio("ID and V", ['Yes', 'No', 'N/A'], key="ss_radio_id_and_v", index=0)
            customer_validation_user_selection_list.append(id_and_v)
            customer_validation_score_calc_points(customer_validation_user_selection_list)
        st.markdown("---")
        question_col7, answer_col7 = st.columns([5, 1])
        with question_col7:
            st.markdown("Did the agent adhere to Intersekt authentication process ? ")
        with answer_col7:
            intersekt_auth = st.radio("Intersekt", ['Yes', 'No', 'N/A'], key="ss_radio_intersekt_auth", index=0)
            customer_validation_user_selection_list.append(intersekt_auth)
            customer_validation_score_calc_points(customer_validation_user_selection_list)
        '''CUSTOMER VALIDATION SECTION END'''

    '''PRESENTATION AND COMPLIANCE SECTION'''
    with presentation_compliance_tab_3:
        st.markdown("## Presentation & Legal Compliance")
        st.markdown("---")
        question_col8, answer_col8 = st.columns([5, 1])
        with question_col8:
            st.markdown(
                '''Did the Agent ask for permission to process and share Clients 
                personal information with the Credit Bureau and the underwriter Guardrisk ? "A clear Yes"''')
        with answer_col8:
            info_process_consent = st.radio("Process Personal Information", ['Yes', 'No', 'N/A'],
                                            key="ss_radio_info_process_consent", index=0)
            presentation_and_compliance_list.append(info_process_consent)
            presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                    presentation_and_compliance_list_inverse)
        st.markdown("---")
        question_col9, answer_col9 = st.columns([5, 1])
        with question_col9:
            st.markdown("Did the Agent address all credit compliance questions as per OMNI ? ")
        with answer_col9:
            credit_compliance = st.radio("Credit Compliance", ['Yes', 'No', 'N/A'], key="ss_radio_credit_compliance",
                                         index=0)
            presentation_and_compliance_list.append(credit_compliance)
            auto_zero_no_list.append(credit_compliance)
            presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                    presentation_and_compliance_list_inverse)
        st.markdown("---")
        question_col10, answer_col10 = st.columns([5, 1])
        with question_col10:
            st.markdown("Can we inform you of African Bank offers via marketing campaigns? ")
            st.markdown("(Follow campaign removal process as per SOP) ?")
        with answer_col10:
            marketing_consent = st.radio("Marketing Consent", ['Yes', 'No', 'N/A'], key="ss_radio_marketing_consent",
                                         index=0)
            presentation_and_compliance_list.append(marketing_consent)
            presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                    presentation_and_compliance_list_inverse)
        st.markdown("---")
        question_col11, answer_col11 = st.columns([5, 1])
        with question_col11:
            st.markdown("Did the Agent obtain the customers banking details ? ")
        with answer_col11:
            banking_details = st.radio("Banking Details", ['Yes', 'No', 'N/A'], key="ss_radio_banking_details", index=0)
            presentation_and_compliance_list.append(banking_details)
            auto_zero_no_list.append(banking_details)
            presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                    presentation_and_compliance_list_inverse)
        st.markdown("---")
        question_col12, answer_col12 = st.columns([5, 1])
        with question_col12:
            st.markdown("Did  the Agent obtain consent for OBS ? ")
        with answer_col12:
            obs_process = st.radio("OBS Consent", ['Yes', 'No', 'N/A'], key="ss_radio_obs_process", index=0)
            presentation_and_compliance_list.append(obs_process)
            presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                    presentation_and_compliance_list_inverse)
        st.markdown("---")
        question_col13, answer_col13 = st.columns([5, 1])
        with question_col13:
            st.markdown("Did the Agent confirm customers employment details ? ")
        with answer_col13:
            employment_details = st.radio("Employment Details", ['Yes', 'No', 'N/A'], key="ss_radio_employment_details",
                                          index=0)
            presentation_and_compliance_list.append(employment_details)
            presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                    presentation_and_compliance_list_inverse)
        st.markdown("---")
        question_col14, answer_col14 = st.columns([5, 1])
        with question_col14:
            st.markdown("Did the Agent get a income and expense disclaimer ? ")
        with answer_col14:
            income_expense_disclaimer = st.radio("Expense Declaration", ['Yes', 'No', 'N/A'],
                                                 key="ss_radio_income_expense_disclaimer", index=0)
            presentation_and_compliance_list.append(income_expense_disclaimer)
            presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                    presentation_and_compliance_list_inverse)
        st.markdown("---")
        question_col15, answer_col15 = st.columns([5, 1])
        with question_col15:
            # st.markdown("Did the Agent overstate expenses declared by the customer ?")
            st.markdown("Income captured by the Agent is **NOT HIGHER THAN Customer declaration** ?")
        with answer_col15:
            overstated_expenses = st.radio("Overstated Expenses", ['Yes', 'No', 'N/A'],
                                           key="ss_radio_overstated_expenses", index=0)
            # inverted_presentation_and_compliance_list.append(overstated_expenses)
            # presentation_and_compliance_list_inverse.append(overstated_expenses)
            presentation_and_compliance_list.append(overstated_expenses)
            # auto_zero_yes_list.append(overstated_expenses)
            auto_zero_no_list.append(overstated_expenses)
            presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                    presentation_and_compliance_list_inverse)
            # inverted_presentation_and_compliance_calc_points(inverted_presentation_and_compliance_list)
        st.markdown("---")
        question_col16, answer_col16 = st.columns([5, 1])
        with question_col16:
            st.markdown("Income captured by the Agent is **NOT LOWER THAN Customer declaration** ?")
        with answer_col16:
            understated_expenses = st.radio("Understated Expenses", ['Yes', 'No', 'N/A'],
                                            key="ss_radio_understated_expenses", index=0)
            # inverted_presentation_and_compliance_list.append(understated_expenses)
            # presentation_and_compliance_list_inverse.append(understated_expenses)
            presentation_and_compliance_list.append(understated_expenses)
            # auto_zero_yes_list.append(understated_expenses)
            auto_zero_no_list.append(understated_expenses)
            presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                    presentation_and_compliance_list_inverse)
            # inverted_presentation_and_compliance_calc_points(inverted_presentation_and_compliance_list)
        st.markdown("---")
        question_col17, answer_col17 = st.columns([5, 1])
        with question_col17:
            st.markdown("Did the Agent confirm with the customer if the information used is true and correct ? ")
        with answer_col17:
            info_authenticity = st.radio("Information Declaration", ['Yes', 'No', 'N/A'],
                                         key="ss_radio_info_authenticity", index=0)
            presentation_and_compliance_list.append(info_authenticity)
            presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                    presentation_and_compliance_list_inverse)
        st.markdown("---")
        question_col18, answer_col18 = st.columns([5, 1])
        with question_col18:
            st.markdown("Did the Agent present all offers to the customer ?")
        with answer_col18:
            present_offers = st.radio("Present Offers", ['Yes', 'No', 'N/A'], key="ss_radio_present_offers", index=0)
            presentation_and_compliance_list.append(present_offers)
            presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                    presentation_and_compliance_list_inverse)
        st.markdown("---")
        question_col19, answer_col19 = st.columns([5, 1])
        with question_col19:
            st.markdown("Did the Agent read out the customer's credit bureau accounts and got acknowledgement ?")
        with answer_col19:
            bureau_accounts = st.radio("Credit Bureau", ['Yes', 'No', 'N/A'], key="ss_radio_bureau_accounts", index=0)
            presentation_and_compliance_list.append(bureau_accounts)
            presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                    presentation_and_compliance_list_inverse)
        st.markdown("---")
        question_col20, answer_col20 = st.columns([5, 1])
        with question_col20:
            st.markdown("Did the Agent inform the customer of the credit life insurance ?")
        with answer_col20:
            credit_life = st.radio("Credit Life", ['Yes', 'No', 'N/A'], key="ss_radio_credit_life", index=0)
            presentation_and_compliance_list.append(credit_life)
            auto_zero_no_list.append(credit_life)
            presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                    presentation_and_compliance_list_inverse)
        st.markdown("---")
        question_col21, answer_col21 = st.columns([5, 1])
        with question_col21:
            st.markdown("Did the Agent inform the customer of the credit life benefits ?")
        with answer_col21:
            credit_life_benefits = st.radio("Credit Benefits", ['Yes', 'No', 'N/A'],
                                            key="ss_radio_credit_life_benefits",
                                            index=0)
            presentation_and_compliance_list.append(credit_life_benefits)
            auto_zero_no_list.append(credit_life_benefits)
            presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                    presentation_and_compliance_list_inverse)
        st.markdown("---")
        question_col22, answer_col22 = st.columns([5, 1])
        with question_col22:
            st.markdown("Did the Agent inform the customer of 90 days waiting period for all benefits ?")
        with answer_col22:
            credit_life_waiting = st.radio("Credit life Waiting Period", ['Yes', 'No', 'N/A'],
                                           key="ss_radio_credit_life_waiting", index=0)
            presentation_and_compliance_list.append(credit_life_waiting)
            auto_zero_no_list.append(credit_life_waiting)
            presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                    presentation_and_compliance_list_inverse)
        st.markdown("---")
        question_col23, answer_col23 = st.columns([5, 1])
        with question_col23:
            st.markdown("Did the Agent give option for own credit life cover ?")
        with answer_col23:
            own_credit_life = st.radio("Credit Life Swap", ['Yes', 'No', 'N/A'], key="ss_radio_own_credit_life",
                                       index=0)
            presentation_and_compliance_list.append(own_credit_life)
            presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                    presentation_and_compliance_list_inverse)
        st.markdown("---")
        question_col24, answer_col24 = st.columns([5, 1])
        with question_col24:
            st.markdown("Did the agent inform the customer of the underwriter ?")
        with answer_col24:
            credit_life_underwriter = st.radio("Credit Life Underwriter", ['Yes', 'No', 'N/A'],
                                               key="ss_radio_credit_life_underwriter", index=0)
            presentation_and_compliance_list.append(credit_life_underwriter)
            presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                    presentation_and_compliance_list_inverse)
        st.markdown("---")
        question_col25, answer_col25 = st.columns([5, 1])
        with question_col25:
            st.markdown("Did the Agent inform the customer that the offer is provisional ?")
        with answer_col25:
            offer_provisional = st.radio("Provisional Offer", ['Yes', 'No', 'N/A'], key="ss_radio_offer_provisional",
                                         index=0)
            presentation_and_compliance_list.append(offer_provisional)
            presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                    presentation_and_compliance_list_inverse)
        st.markdown("---")
        question_col26, answer_col26 = st.columns([5, 1])
        with question_col26:
            st.markdown("Did the Agent inform the customer of the T's & C's  (5 days, change in income)")
        with answer_col26:
            provisional_expiration = st.radio("Provisional Expiration", ['Yes', 'No', 'N/A'],
                                              key="ss_radio_provisional_expiration", index=0)
            presentation_and_compliance_list.append(provisional_expiration)
            presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                    presentation_and_compliance_list_inverse)
        st.markdown("---")
        question_col27, answer_col27 = st.columns([5, 1])
        with question_col27:
            st.markdown("Did the Agent adhere to full close-out protocol ?")
        with answer_col27:
            close_out = st.radio("Close Out", ['Yes', 'No', 'N/A'], key="ss_radio_close_out", index=0)
            presentation_and_compliance_list.append(close_out)
            presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                    presentation_and_compliance_list_inverse)
        st.markdown("---")
        question_col28, answer_col28 = st.columns([5, 1])
        with question_col28:
            # st.markdown("Did the call have any negative Risk impact Not on ScoreCard( Auto Zero + misconduct)?")
            st.markdown("Call did **NOT** contain negative indicators, in terms of risk OR misconduct ?")
        with answer_col28:
            misconduct_indicators = st.radio("Misconduct Indicators", ['Yes', 'No', 'N/A'],
                                             key="ss_radio_misconduct_indicators", index=0)
            # inverted_presentation_and_compliance_list.append(misconduct_indicators)
            presentation_and_compliance_list.append(misconduct_indicators)
            presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                    presentation_and_compliance_list_inverse)
            # inverted_presentation_and_compliance_calc_points(inverted_presentation_and_compliance_list)
        '''PRESENTATION AND COMPLIANCE SECTION END'''
        st.sidebar.markdown("---")

    intro_score = intro_score_calc_points(intro_user_selection_list) / 5 * 100
    customer_validation_score = customer_validation_score_calc_points(
        customer_validation_user_selection_list) / 2 * 100
    pres_and_legal_score = (presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                                    presentation_and_compliance_list_inverse)) / 21 * 100
    final_score = ((intro_score_calc_points(intro_user_selection_list)
                    + customer_validation_score_calc_points(customer_validation_user_selection_list)
                    + presentation_and_compliance_calc_points(presentation_and_compliance_list,
                                                              presentation_and_compliance_list_inverse)) / 28 * 100)
    
    # Auto-Zero
    # if value of i in this list is 0 then total score is zero
    for i in range(len(auto_zero_yes_list)):
        if auto_zero_yes_list[i] == "Yes":
            final_score = 0
    for i in range(len(auto_zero_no_list)):
        if auto_zero_no_list[i] == "No":
            final_score = 0

    st.sidebar.markdown(f"Introduction: {intro_score:.2f} %")
    st.sidebar.markdown(f"Customer Validation: {customer_validation_score:.2f} %")
    st.sidebar.markdown(f"Presentation & Legal Compliance: {pres_and_legal_score:.2f} %")
    st.sidebar.markdown(f"Total Score: {final_score:.2f}%")

    st.sidebar.markdown("## Step 3")
    submitted = st.sidebar.button("Submit")
    if submitted:
        sql_input_fields = """INSERT INTO qa_score_card (application_id, interaction_id, split_call, agent_name,
        supervisor_name, qa_assessor_name, business_unit, product_type, call_type, evaluation_date,
        call_date, greeting, introduce_bank, call_reason, pre_qualifying, reg_statement,
        id_and_v, intersekt_auth, info_process_consent, credit_compliance, marketing_consent,
        banking_details, obs_process, employment_details, income_expense_disclaimer,
        overstated_expenses,understated_expenses, info_authenticity, present_offers,bureau_accounts,
        credit_life, credit_life_benefits, credit_life_waiting, own_credit_life,
        credit_life_underwriter, offer_provisional, provisional_expiration, close_out,
        misconduct_indicators, intro_score, customer_validation_score, presentation_and_legal_score,
        final_score)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        val_input_fields = [application_id, interaction_id, split_call, agent_name, supervisor, qa_assessor,
                            business_unit, product_type, call_type, evaluation_date, call_date, greeting,
                            introduce_bank, call_reason, pre_qualifying, reg_statement, id_and_v, intersekt_auth,
                            info_process_consent, credit_compliance, marketing_consent, banking_details, obs_process,
                            employment_details, income_expense_disclaimer, overstated_expenses,
                            understated_expenses, info_authenticity, present_offers, bureau_accounts,
                            credit_life, credit_life_benefits, credit_life_waiting, own_credit_life,
                            credit_life_underwriter, offer_provisional, provisional_expiration, close_out,
                            misconduct_indicators, intro_score, customer_validation_score, pres_and_legal_score,
                            final_score]
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
            success_message = st.sidebar.success("Data Inserted Successfully")
            st.write("The warning is cleared in 3 seconds!")
            time.sleep(3)  # Wait for 3 seconds
            success_message.empty()  # Clear the alert
            get_db_connection_cursor.close()
            get_db_connection.close()
            normal_call_assessment_criteria()
        except():
            print("DB Connection CURSOR Error")
