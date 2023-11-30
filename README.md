# Emerging Optimization Methods in Online Food Delivery Services

Objective: The aim is to minimize the overall cost of delivering food. The cost consists of two parts:

The weekly fixed cost (r1) of hiring permanent drivers (z).
The variable cost, which is the traveling cost for both permanent drivers (r2) and on-demand drivers (r3).

Components:

z * r1: This is the fixed cost of hiring permanent drivers for the entire week.

pulp.lpSum(): This is a function provided by the PuLP library to calculate the sum of a list of numbers or expressions. In this context, it sums up the traveling costs across all hours and days.

[(xij[i, j] * r2 + yij[i, j] * r3) for i in range(24) for j in range(1, 8)]: This is a list comprehension that generates the variable costs across all hours (i) of all days (j).

xij[i, j] * r2: This gives the cost for the permanent drivers for hour i on day j.
yij[i, j] * r3: This gives the cost for the on-demand drivers for hour i on day j.
The list comprehension goes through every combination of hour and day, calculates the costs for both types of drivers, and puts them all in a list.

Putting it all together: The objective function is the sum of the fixed cost of hiring permanent drivers and the total traveling costs of both types of drivers across all hours and days. The += in prob += ... adds this objective function to the linear programming problem with the aim to minimize it.

Overall, we want to minimize the total cost, which is a combination of the weekly cost of hiring permanent drivers and the hourly cost for both permanent and on-demand drivers delivering food across all hours and days of the week.
