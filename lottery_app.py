import streamlit as st
import pandas as pd

# Core functions
def factorial(n):
    final_product = 1
    for i in range(n, 0, -1):
        final_product *= i
    return final_product

def combinations(n, k):
    numerator = factorial(n)
    denominator = factorial(k) * factorial(n - k)
    return numerator / denominator

# Load the CSV file
file_path = "d:\\OneDrive\\Desktop\\649.csv"
lottery_canada = pd.read_csv(file_path)

def extract_numbers(row):
    row = row[4:10]
    row = set(row.values)
    return row

winning_numbers = lottery_canada.apply(extract_numbers, axis=1)

# Core functions continued...
def one_ticket_probability(user_numbers):
    n_combinations = combinations(49, 6)
    probability_one_ticket = 1 / n_combinations
    percentage_form = probability_one_ticket * 100

    return '''Your chances to win the big prize with the numbers {} are {:.7f}%.
In other words, you have a 1 in {:,} chances to win.'''.format(user_numbers, percentage_form, int(n_combinations))

def check_historical_occurrence(user_numbers, historical_numbers):
    user_numbers_set = set(user_numbers)
    check_occurrence = historical_numbers == user_numbers_set
    n_occurrences = check_occurrence.sum()

    if n_occurrences == 0:
        return '''The combination {} has never occurred.
This doesn't mean it's more likely to occur now. Your chances to win the big prize in the next drawing using the combination {} are 0.0000072% (1 in 13,983,816).'''.format(user_numbers, user_numbers)
    else:
        return '''The combination {} has occurred {} times in the past.
Your chances to win the big prize in the next drawing using the combination {} remain the same: 0.0000072% (1 in 13,983,816).'''.format(user_numbers, n_occurrences, user_numbers)

def multi_ticket_probability(n_tickets):
    n_combinations = combinations(49, 6)
    probability = n_tickets / n_combinations
    percentage_form = probability * 100

    if n_tickets == 1:
        return '''Your chances to win the big prize with one ticket are {:.6f}%.
In other words, you have a 1 in {:,} chances to win.'''.format(percentage_form, int(n_combinations))
    else:
        combinations_simplified = round(n_combinations / n_tickets)
        return '''Your chances to win the big prize with {:,} tickets are {:.6f}%.
In other words, you have a 1 in {:,} chances to win.'''.format(n_tickets, percentage_form, combinations_simplified)

def probability_less_6(n_winning_numbers):
    n_combinations_ticket = combinations(6, n_winning_numbers)
    n_combinations_remaining = combinations(43, 6 - n_winning_numbers)
    successful_outcomes = n_combinations_ticket * n_combinations_remaining
    n_combinations_total = combinations(49, 6)
    probability = successful_outcomes / n_combinations_total
    probability_percentage = probability * 100
    combinations_simplified = round(n_combinations_total / successful_outcomes)

    return '''Your chances of matching {} winning numbers are {:.6f}%.
In other words, you have a 1 in {:,} chances to win.'''.format(n_winning_numbers, probability_percentage, int(combinations_simplified))

# Streamlit App
st.set_page_config(page_title="Lottery Probability Calculator", layout="wide")

st.title("🎲 Lottery Probability Calculator")
st.write("This app helps you calculate your chances of winning the lottery based on historical data and statistical probability.")

st.sidebar.header("🔢 Choose an option:")
user_option = st.sidebar.selectbox(
    "Select what you want to calculate:",
    ["Single Ticket Probability", "Check Historical Occurrence", "Multi-Ticket Probability", "Less than 6 Winning Numbers"]
)

st.sidebar.write("---")

# User Inputs and Actions
if user_option == "Single Ticket Probability":
    st.header("🎟️ 1. Single Ticket Probability")
    st.write("Enter your numbers below to see the probability of winning with a single ticket.")
    
    user_numbers = st.text_input("Enter six unique numbers (separated by commas):", "1, 2, 3, 4, 5, 6")
    try:
        user_numbers = [int(num.strip()) for num in user_numbers.split(",")]
        
        if len(user_numbers) != 6 or len(set(user_numbers)) != 6 or not all(1 <= n <= 49 for n in user_numbers):
            st.error("Please enter exactly 6 unique numbers between 1 and 49.")
        else:
            if st.button("Calculate Probability"):
                result = one_ticket_probability(user_numbers)
                st.success(result)
    except ValueError:
        st.error("Invalid input! Please enter six numbers separated by commas.")

if user_option == "Check Historical Occurrence":
    st.header("📊 2. Check Historical Occurrence")
    st.write("Find out how often your combination has appeared in past draws.")

    if st.button("Check Occurrence"):
        result = check_historical_occurrence(user_numbers, winning_numbers)
        st.success(result)

if user_option == "Multi-Ticket Probability":
    st.header("🎟️ 3. Multi-Ticket Probability")
    st.write("Calculate your chances of winning with multiple tickets.")

    n_tickets = st.number_input("Enter the number of tickets you want to play:", min_value=1, max_value=13983816, value=1, step=1)
    
    if st.button("Calculate for Multiple Tickets"):
        result = multi_ticket_probability(n_tickets)
        st.success(result)

if user_option == "Less than 6 Winning Numbers":
    st.header("📉 4. Probability for Less Than Six Winning Numbers")
    st.write("Estimate your chances of having 2 to 5 winning numbers.")

    st.write("Before slider")
    n_winning_numbers = st.slider("Select the number of winning numbers expected (between 2 and 5):", 2, 5, value=2, step=1)
    st.write(f"Slider value: {n_winning_numbers}")  # Debugging slider value

    if st.button("Calculate for Less than 6 Numbers"):
        result = probability_less_6(n_winning_numbers)
        st.success(result)
