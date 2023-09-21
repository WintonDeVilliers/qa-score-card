import streamlit as st
from scenario_1 import page_scenario_1
from scenario_2 import page_scenario_2
# from scenario_3 import page_scenario_3

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def main():
    st.sidebar.title("Navigation")

    scenario_1_button = st.sidebar.button("FORM VIEW", help="")
    scenario_2_button = st.sidebar.button("DATA VIEW", help="")
    # scenario_3_button = st.sidebar.button("DATA OVERVIEW", help="")

    # Track the current page using a state variable
    if "page" not in st.session_state:
        st.session_state.page = "FORM VIEW"

    # Update the current page when a button is clicked
    if scenario_1_button:
        st.session_state.page = "FORM VIEW"
    elif scenario_2_button:
        st.session_state.page = "DATA VIEW"
    # elif scenario_3_button:
    #     st.session_state.page = "DATA OVERVIEW"

    # Display the selected page
    if st.session_state.page == "FORM VIEW":
        page_scenario_1()
    elif st.session_state.page == "DATA VIEW":
        page_scenario_2()
    # elif st.session_state.page == "DATA OVERVIEW":
    #     page_scenario_3()


if __name__ == "__main__":
    main()
