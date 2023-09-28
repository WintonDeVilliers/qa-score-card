# QA SCORE CARD (SALES)


    QA SCORE CARD (SALES)
    Project Summary
    
    This project aims to develop a desktop or web application that replaces the existing
    Excel-based quality assurance score-cards. The application will provide a user-friendly
    form interface resembling the Excel sheet while maintaining the same score calculations.
    It will leverage data science capabilities to gather insights from captured data, and
    provide data visualisation enabling improved analysis and decision-making.
  
    '''FORM TEXT-INPUT/SELECTOR FIELDS CONTAINERS/LISTS'''

    
    # Form Rules
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

    
