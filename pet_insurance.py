spending = 2**30
rates = [.5, .6, .7, .8]
deductables = [250, 500, 750, 1000]
monthly_cost = [
    [32.56, 27.68, 24.57, 23.01], # .5 @ diff deductable points
    [36.34, 30.89, 27.40, 25.66], # .6 @ diff deductable points
    [41.05, 34.89, 30.93, 28.96], # .7 @ diff deductable points
    [46.06, 39.15, 34.70, 32.47], # .8 @ diff deductable points
]

lowest_spending = 2**31
best_rate_info = None

for i in range(len(rates)):
    for j in range(len(deductables)):
        # how much you pay annually = (spendings from deductable and monthly costs) - (savings from coverage at given rate)
        spent_at_rate = (spending + (monthly_cost[i][j] * 12)) - (rates[i] * (spending - deductables[j]))
        print(f"rate: {rates[i]} | deductable: {deductables[i]} | spent_at_rate: {spent_at_rate:.2f}") 
        if spent_at_rate < lowest_spending:
            best_rate_info, lowesgbt_spending = {
                'rate': rates[i],
                'deductable': deductables[j]
            }, spent_at_rate

print(f"best_rate_info: {best_rate_info} | lowest_spending: {lowest_spending}")