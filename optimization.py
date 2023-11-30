import pulp
import pandas as pd


# Define the problem
prob = pulp.LpProblem("Food_Delivery_Optimization", pulp.LpMinimize)


# Given parameters (for this example, I'll assume some constants for r1, r2, r3, but you can replace with actual values)
#r1 is the fixed cost per permanent driver for a week
r1 = 863.5
#r2 is the traveling cost for a permanent driver per hour
r2 = 6
#r3 is the traveling cost for a on-demand driver per hour
r3 = 28
#o1 is the number of orders that a permanent driver can deliver per hour
#o2 is the number of orders that an on-demand driver can deliver per hour
o1 = o2 = 2 # As given in the constraints
# Decision variables
z = pulp.LpVariable("z", 0, None, pulp.LpInteger) # Total number of permanent drivers
xij = pulp.LpVariable.dicts("x", ((i, j) for i in range(24) for j in range(1, 8)), 0, None, pulp.LpInteger) #number of permanent drivers at ith hour of jth day used
yij = pulp.LpVariable.dicts("y", ((i, j) for i in range(24) for j in range(1, 8)), 0, None, pulp.LpInteger) #number of on-demand drivers at ith hour of jth day used




# Demand matrix
dij_matrix = [
[0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0],
[1, 0, 2, 2, 2, 0, 0],
[3, 3, 1, 1, 4, 3, 3],
[7, 10, 8, 10, 14, 9, 8],
[15, 26, 20, 29, 27, 19, 16],
[16, 20, 24, 22, 28, 25, 26],
[20, 17, 21, 19, 20, 23, 33],
[18, 12, 15, 17, 22, 26, 38],
[17, 9, 15, 20, 14, 29, 34],
[21, 19, 14, 18, 25, 30, 31],
[28, 27, 26, 26, 33, 27, 35],
[26, 34, 31, 34, 38, 31, 29],
[29, 32, 28, 28, 30, 31, 31],
[21, 20, 26, 22, 25, 28, 32],
[11, 12, 12, 18, 21, 17, 20],
[5, 6, 7, 8, 10, 11, 9],
[0, 0, 0, 1, 5, 4, 1],
[0, 0, 0, 0, 4, 4, 0],
[0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0]
]


# Convert the 2D matrix to a dictionary for easy access
dij = {(i, j): dij_matrix[i][j-1] for i in range(24) for j in range(1, 8)} # Note the j-1, because Python lists are 0-indexed


# Objective function
prob += z * r1 + pulp.lpSum([(xij[i, j] * r2 + yij[i, j] * r3) for i in range(24) for j in range(1, 8)])


# Constraints
for i in range(24):
for j in range(1, 8):
prob += xij[i, j] <= z
prob += dij[i, j] <= xij[i, j] * o1 + yij[i, j] * o2


# Permanent drivers are off work for all hours of day 1 and day 2
for i in range(24):
for j in [1, 2]:
prob += xij[i, j] == 0


# Permanent drivers are off work for certain hours of days 3 to 7
for i in [0,1,2,3,4,5,6,7,12,17,18,19,20,21,22,23]:
for j in range(3, 8):
prob += xij[i, j] == 0


# Solve the problem
prob.solve()


# Check if a valid solution was found
if pulp.LpStatus[prob.status] != "Optimal":
print("An optimal solution could not be found.")
exit()


# After solving the problem, you can display the results like this:


# Results
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def hour_format(hour):
"""Converts the 24-hour format to AM/PM format."""
if hour == 0:
return "12 AM"
elif hour < 12:
return f"{hour} AM"
elif hour == 12:
return "12 PM"
else:
return f"{hour - 12} PM"


# Total on-demand driver hours
total_on_demand_hours = 0
# Total costs for permanent and on-demand drivers
total_cost_permanent = 0
total_cost_on_demand = 0


for j in range(1, 8):
for i in range(24):
num_permanent = xij[i, j].value()
num_on_demand = yij[i, j].value()
total_cost_permanent += num_permanent * r2
total_cost_on_demand += num_on_demand * r3
if dij_matrix[i][j-1] != 0: # check if there's demand
print(f"At {hour_format(i)} on {days[j-1]}, {num_permanent} permanent drivers and {num_on_demand} on-demand drivers are scheduled.")
else:
if num_permanent != 0 or num_on_demand !=0:
print("Error - no demand but drivers scheduled.")
else:
print(f"At {hour_format(i)} on {days[j-1]}, there is no demand so 0 drivers are scheduled.")
total_on_demand_hours += num_on_demand


# The fixed cost of hiring permanent drivers
total_cost_permanent += z.value() * r1


print(f"\nTotal number of permanent drivers to be hired: {int(z.value())}")
print(f"Total hours on-demand drivers are used: {int(total_on_demand_hours)}")
print(f"Total cost for permanent drivers: ${total_cost_permanent:.2f}")
print(f"Total cost for on-demand drivers: ${total_cost_on_demand:.2f}")




# Preparing Data for Export
matrix_permanent = [[0 for _ in range(7)] for _ in range(24)]
matrix_on_demand = [[0 for _ in range(7)] for _ in range(24)]


for i in range(24):
for j in range(1, 8):
permanent_drivers = int(xij[i, j].varValue)
on_demand_drivers = int(yij[i, j].varValue)
# Fill the matrix
matrix_permanent[i][j-1] = permanent_drivers
matrix_on_demand[i][j-1] = on_demand_drivers


# Convert data to DataFrames
df_permanent = pd.DataFrame(matrix_permanent, columns=days, index=[hour_format(h) for h in range(24)])
df_on_demand = pd.DataFrame(matrix_on_demand, columns=days, index=[hour_format(h) for h in range(24)])


# Save to Excel
with pd.ExcelWriter('results.xlsx') as writer:
df_permanent.to_excel(writer, sheet_name='Permanent Drivers')
df_on_demand.to_excel(writer, sheet_name='On-Demand Drivers')


print("Results exported to results.xlsx")
