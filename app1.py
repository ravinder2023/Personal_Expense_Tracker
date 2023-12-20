import streamlit as st
from datetime import datetime
import plotly.express as px
import pandas as pd


class ExpenseTracker:
    def __init__(self):
        self.entries = pd.DataFrame(columns=["Amount", "Category", "Date"])

    def add_expense(self, amount, category, date):
        new_entry = pd.DataFrame([[amount, category, date]], columns=["Amount", "Category", "Date"])
        self.entries = pd.concat([self.entries, new_entry], ignore_index=True)

    def view_spending_patterns(self):
        # Convert "Category" to string to fix Plotly Express issue
        self.entries["Category"] = self.entries["Category"].astype(str)

        # Generate charts with plotly express
        overall_chart = px.bar(
            self.entries,
            x="Category",
            y="Amount",
            color="Category",
            title="Overall Expense Breakdown",
            labels={"Amount": "Total Expenses"},
        )

        # Group by category and sum the total amount spent
        category_totals = self.entries.groupby("Category")["Amount"].sum().reset_index()

        category_pie_chart = px.pie(
            category_totals,
            names="Category",
            values="Amount",
            title="Category Distribution",
        )

        expense_line_chart = px.line(
            self.entries,
            x="Date",
            y="Amount",
            title="Expense Over Time",
            labels={"Amount": "Total Expenses", "Date": "Expense Date"},
        )

        # Streamlit API for charts and data
        st.header("Spending Patterns:")
        st.write(overall_chart)
        st.write(category_pie_chart)
        st.write(expense_line_chart)

    def clear_expenses(self):
        self.entries = pd.DataFrame(columns=["Amount", "Category", "Date"])
        st.success("Expenses cleared!")


if __name__ == "__main__":
    st.title("Personal Expense Tracker")

    # Get or create the ExpenseTracker object in the session state
    if 'tracker' not in st.session_state:
        st.session_state.tracker = ExpenseTracker()

    # Get user inputs
    amount = st.number_input("Enter the expense amount:", min_value=0.01, step=0.01)
    date = st.date_input("Enter the expense date:", datetime.now())
    category = st.selectbox("Choose category:",
                            ["Food", "Grocery", "Shopping", "Entertainment", "Rent", "Transportation", "Medical",
                             "Others"])

    # Add expense
    if st.button("Add Expense"):
        if amount and category and date:
            st.session_state.tracker.add_expense(amount, category, date)
            st.success("Expense added!")  # Confirmation message
        else:
            st.error("Please fill in all the details.")

    # View spending patterns
    if st.button("View Spending Patterns"):
        if not st.session_state.tracker.entries.empty:
            st.session_state.tracker.view_spending_patterns()
        else:
            st.info("No expenses added yet.")

    # Clear expenses
    if st.button("Clear Expenses"):
        st.session_state.tracker.clear_expenses()
