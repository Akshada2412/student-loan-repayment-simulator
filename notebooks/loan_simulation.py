# notebooks/loan_simulation.py

import pandas as pd

def generate_amortization_schedule(principal, annual_rate, years, monthly_income=None, income_based=False):
    """
    Generates an amortization schedule for a loan.
    
    Parameters:
    - principal: total loan amount
    - annual_rate: interest rate in percent (e.g. 6.8)
    - years: loan term in years
    - monthly_income: used for income-based repayment
    - income_based: True for IDR (income-driven repayment)

    Returns:
    - Pandas DataFrame of payment schedule
    """
    schedule = []
    monthly_rate = annual_rate / 12 / 100
    months = years * 12

    # Fixed repayment plan
    if not income_based:
        monthly_payment = (principal * monthly_rate) / (1 - (1 + monthly_rate) ** -months)
    else:
        # IDR plan (simplified): 10% of monthly income, capped at $1500
        monthly_payment = min((monthly_income or 3000) * 0.10, 1500)

    balance = principal
    for i in range(1, months + 1):
        interest = balance * monthly_rate
        principal_paid = monthly_payment - interest
        balance -= principal_paid
        balance = max(balance, 0)
        schedule.append([i, round(monthly_payment, 2), round(interest, 2), round(principal_paid, 2), round(balance, 2)])
        if balance <= 0:
            break

    return pd.DataFrame(schedule, columns=["Month", "Payment", "Interest", "Principal", "Balance"])


# Test run
if __name__ == "__main__":
    df = generate_amortization_schedule(principal=30000, annual_rate=6.8, years=10)
    print(df.head())
    df.to_csv("../data/sample_amortization_schedule.csv", index=False)
