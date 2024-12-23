import numpy as np
import numpy_financial as npf

def retirement_shortfall(
    current_salary, replacement_rate, inflation_rate, years_to_retirement, # replacememt rate is retirement income goal as % of current salary
    retirement_duration, annual_rate_of_return, current_savings, 
    current_contributions, contribution_escalation_rate, 
):
    # 1 - required savings at retirement
    monthly_goal_today = current_salary * replacement_rate
    future_monthly_goal = monthly_goal_today * (1 + inflation_rate) ** years_to_retirement
    # Calculate present value of retirement annuity goal
    required_savings = npf.pv(
        annual_rate_of_return,
        retirement_duration,
        -future_monthly_goal * 12,  # annualised
        0
    )
    
    # 2 a - Future value of current savings
    future_value_savings = npf.fv(annual_rate_of_return, years_to_retirement, 0, -current_savings)
    
    # 2 b - future value of contributions
    current_contributions = current_contributions * 12 # annaul contribution
    future_value_contributions = sum(
        current_contributions * (1 + contribution_escalation_rate) ** year * (1 + annual_rate_of_return) ** (years_to_retirement - year)
        for year in range(years_to_retirement)
    )
    
    # 3 - shortfall
    future_value_total = future_value_savings + future_value_contributions
    shortfall = required_savings - future_value_total
    
    # 4 - required monthly contributions
    required_contributions = npf.pmt(
        annual_rate_of_return / 12,
        years_to_retirement * 12,
        0,
        shortfall
    )
    
    return {
        "Required Savings": round(required_savings, 2),
        "Future Value": round(future_value_total, 2),
        "Shortfall": round(shortfall, 2),
        "Required Monthly Contributions": round(-required_contributions, 2) 
    }

# exmaple calculation
result = retirement_shortfall(
    current_salary=50000,
    replacement_rate=0.7,
    inflation_rate=0.05,
    years_to_retirement=11,
    retirement_duration=25,
    annual_rate_of_return=0.065,
    current_savings=610000,
    current_contributions=4500,
    contribution_escalation_rate=0.04
)
print(result)
