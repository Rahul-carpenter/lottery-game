import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt

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

# Central function for all calculations
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

# Additional Feature: Simulate Lottery Draw
def simulate_lottery_draw(user_numbers):
    winning_draw = random.sample(range(1, 50), 6)
    matches = set(user_numbers).intersection(winning_draw)
    return winning_draw, matches

# Additional Feature: Fun Facts & Tips
def lottery_fun_fact():
    facts = [
        "Did you know? The odds of winning the lottery are 1 in 13,983,816.",
        "Playing more tickets doesn't change the overall odds, but it does increase your individual chances!",
        "Some numbers like 7 and 3 are often considered lucky, but statistically, they’re no different from others.",
        "The number 38 has historically appeared more frequently in Canadian lotteries."
    ]
    return random.choice(facts)

# Additional Feature: Expected Value Calculation
def expected_value():
    ticket_cost = 3  # Assuming each ticket costs ₹3
    average_jackpot = 5000000  # Average lottery jackpot
    n_combinations = combinations(49, 6)
    ev = (1 / n_combinations) * average_jackpot - ticket_cost
    return f'💸 **Expected Value**: For each lottery ticket you buy (cost ₹{ticket_cost}), your expected return is **₹{ev:.2f}**. This means you lose money on average for each ticket.'

# Additional Feature: Cost vs. Return Simulator
def cost_vs_returns_simulator(n_tickets):
    ticket_cost = 3
    total_cost = n_tickets * ticket_cost
    n_combinations = combinations(49, 6)
    average_jackpot = 5000000
    total_expected_return = n_tickets * (1 / n_combinations) * average_jackpot
    return total_cost, total_expected_return

# Additional Feature: Better Investment Alternatives
def better_investment_alternatives(n_tickets):
    ticket_cost = 3
    total_cost = n_tickets * ticket_cost
    stock_market_return = total_cost * 1.07  # Assuming a 7% annual return in the stock market
    savings_return = total_cost * 1.02  # Assuming a 2% return in a savings account
    return stock_market_return, savings_return

# Additional Feature: Most Frequent Numbers in History
def most_frequent_numbers(df):
    all_numbers = pd.concat([df[col] for col in df.columns[4:10]])
    most_common = all_numbers.value_counts().nlargest(5)
    return most_common

# Streamlit App UI
st.title("🎰 Lottery Probability Calculator")

# Add a sidebar for navigation
st.sidebar.header("Navigation")
options = st.sidebar.selectbox(
    "Choose an option",
    ["Single Ticket Probability", "Check Historical Occurrence", "Multi-Ticket Probability", "Probability for Less Than Six Winning Numbers", "Simulate Lottery Draw", "Fun Facts", "Frequent Winning Numbers", "Expected Value", "Cost vs. Returns Simulator", "Better Investment Alternatives"]
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

elif options == "Simulate Lottery Draw":
    st.header("🔀 Simulate Lottery Draw")
    user_numbers = st.text_input("Enter six unique numbers (separated by commas):", "1, 2, 3, 4, 5, 6")
    user_numbers = [int(num.strip()) for num in user_numbers.split(",") if num.strip().isdigit()]

    if st.button("Simulate Draw"):
        winning_draw, matches = simulate_lottery_draw(user_numbers)
        st.write(f"The drawn numbers were: {winning_draw}")
        st.write(f"You matched: {len(matches)} numbers. Matched numbers: {matches}")

elif options == "Fun Facts":
    st.header("🎉 Fun Lottery Facts & Tips")
    st.write(lottery_fun_fact())

elif options == "Frequent Winning Numbers":
    st.header("📊 Most Frequent Winning Numbers in History")
    most_frequent = most_frequent_numbers(lottery_canada)
    st.bar_chart(most_frequent)

elif options == "Expected Value":
    st.header("💸 Expected Value")
    st.write(expected_value())

elif options == "Cost vs. Returns Simulator":
    st.header("📈 Cost vs. Returns Simulator")

    # User input: number of tickets
    n_tickets = st.number_input("Enter the number of tickets you want to simulate:", min_value=1, value=100)
    
    # When the user clicks the button, the simulator will calculate the results
    if st.button("Simulate"):
        # Call the simulator function to calculate total cost and expected returns
        total_cost, total_expected_return = cost_vs_returns_simulator(n_tickets)

        # Show the total cost (how much the user will spend)
        st.write(f"Total cost of buying **{n_tickets:,} tickets**: **₹{total_cost:,}**")
        
        # Show the expected return (on average, how much the user would win back)
        st.write(f"Total expected return from buying **{n_tickets:,} tickets**: **₹{total_expected_return:.2f}**")
        
        # Calculate net loss (total money spent minus the expected return)
        net_loss = total_cost - total_expected_return
        
        # Display the net loss
        st.write(f"On average, you would lose **₹{net_loss:.2f}** after buying **{n_tickets:,} tickets**.")
        
        # Add a closing message explaining the risk
        st.write("""
            🚨 **Important Note:** The lottery is a game of chance. While it can be fun to play, the odds are extremely low, and you are likely to lose more than you win in the long run.
            Consider better alternatives, like saving or investing, to grow your money over time.
        """)

elif options == "Better Investment Alternatives":
    st.header("💡 Better Investment Alternatives")
    n_tickets = st.number_input("Enter the number of tickets you want to compare:", min_value=1, value=100)

    if st.button("Compare Investments"):
        stock_market_return, savings_return = better_investment_alternatives(n_tickets)
        st.write(f"Potential return from investing in stock market: ₹{stock_market_return:.2f}")
        st.write(f"Potential return from savings account: ₹{savings_return:.2f}")

# Show some closing notes
st.write("---")
st.write("Remember, the lottery is mostly for entertainment. While winning can be life-changing, it’s a long shot! Consider better alternatives to grow your money.")
