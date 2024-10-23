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
file_path = "649.csv"  # Update the path as needed
lottery_canada = pd.read_csv(file_path)

def extract_numbers(row):
    row = row[4:10]  # Adjust as necessary
    return set(row.values)  # Return a set directly

# Convert winning numbers to a list of sets
winning_numbers = lottery_canada.apply(extract_numbers, axis=1).tolist()

# Single function to handle all types of calculations
def lottery_calculator(mode, user_numbers=None, n_tickets=None, n_winning_numbers=None):
    if mode == 'single_ticket':
        n_combinations = combinations(49, 6)
        probability_one_ticket = 1 / n_combinations
        percentage_form = probability_one_ticket * 100

        return f'🎟️ Your chances to win the big prize with the numbers {user_numbers} are **{percentage_form:.7f}%**.\nIn other words, you have a 1 in {int(n_combinations):,} chances to win.'
    
    elif mode == 'multi_ticket':
        n_combinations = combinations(49, 6)
        probability = n_tickets / n_combinations
        percentage_form = probability * 100

        if n_tickets == 1:
            return f'🎟️ Your chances to win the big prize with one ticket are **{percentage_form:.6f}%**.\nIn other words, you have a 1 in {int(n_combinations):,} chances to win.'
        else:
            combinations_simplified = round(n_combinations / n_tickets)
            return f'🎟️ Your chances to win the big prize with **{n_tickets:,} different tickets** are **{percentage_form:.6f}%**.\nIn other words, you have a 1 in {combinations_simplified:,} chances to win.'

    elif mode == 'less_6':
        n_combinations_ticket = combinations(6, n_winning_numbers)
        n_combinations_remaining = combinations(43, 6 - n_winning_numbers)
        successful_outcomes = n_combinations_ticket * n_combinations_remaining
        n_combinations_total = combinations(49, 6)
        probability = successful_outcomes / n_combinations_total
        probability_percentage = probability * 100
        combinations_simplified = round(n_combinations_total / successful_outcomes)

        return f'🎟️ Your chances of having **{n_winning_numbers} winning numbers** with this ticket are **{probability_percentage:.6f}%**.\nIn other words, you have a 1 in {int(combinations_simplified):,} chances to win.'

    elif mode == 'historical_occurrence':
        user_numbers_set = set(user_numbers)
        n_occurrences = sum(1 for winning_set in winning_numbers if user_numbers_set == winning_set)

        if n_occurrences == 0:
            return f'🔍 The combination **{user_numbers}** has never occurred.\nYour chances to win the big prize with this combination remain **0.0000072% (1 in 13,983,816)**.'
        else:
            return f'🔍 The combination **{user_numbers}** has occurred **{n_occurrences} times** in the past.\nYour chances to win the big prize remain **0.0000072% (1 in 13,983,816)**.'

# Streamlit App UI
st.title("🎰 Lottery Probability Calculator")

# Add a sidebar for navigation
st.sidebar.header("Navigation")
options = st.sidebar.selectbox(
    "Choose an option",
    ["Single Ticket Probability", "Check Historical Occurrence", "Multi-Ticket Probability", "Probability for Less Than Six Winning Numbers"]
)

if options == "Single Ticket Probability":
    st.header("🎟️ Single Ticket Probability")
    user_numbers = st.text_input("Enter six unique numbers (separated by commas):", "1, 2, 3, 4, 5, 6")
    user_numbers = [int(num.strip()) for num in user_numbers.split(",") if num.strip().isdigit()]

    if st.button("Calculate Probability"):
        result = lottery_calculator('single_ticket', user_numbers=user_numbers)
        st.write(result)

elif options == "Check Historical Occurrence":
    st.header("🔍 Check Historical Occurrence")
    user_numbers = st.text_input("Enter six unique numbers (separated by commas):", "1, 2, 3, 4, 5, 6")
    user_numbers = [int(num.strip()) for num in user_numbers.split(",") if num.strip().isdigit()]

    if st.button("Check Occurrence"):
        result = lottery_calculator('historical_occurrence', user_numbers=user_numbers)
        st.write(result)

elif options == "Multi-Ticket Probability":
    st.header("🎟️ Multi-Ticket Probability")
    n_tickets = st.number_input("Enter the number of tickets you want to play:", min_value=1, max_value=13983816, value=1, step=1)

    if st.button("Calculate Probability"):
        result = lottery_calculator('multi_ticket', n_tickets=n_tickets)
        st.write(result)

elif options == "Probability for Less Than Six Winning Numbers":
    st.header("🎟️ Probability for Less Than Six Winning Numbers")
    n_winning_numbers = st.slider("Select the number of winning numbers expected (between 2 and 5):", 2, 5)

    if st.button("Calculate Probability"):
        result = lottery_calculator('less_6', n_winning_numbers=n_winning_numbers)
        st.write(result)
