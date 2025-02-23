import math

# Question 1A)
QUARTERS = ["Q1'26", "Q2'26", "Q3'26", "Q4'26", "Q1'27", "Q2'27", "Q3'27", "Q4'27"]
TAM = [21.8, 27.4, 34.9, 39.0, 44.7, 51.5, 52.5, 53.5]  # in billion GB
weeks_per_quarter = 13

loading = {
    "Node 1": [12000],
    "Node 2": [5000],
    "Node 3": [1000]
}

gb_per_wafer = {
    "Node 1": 100000,
    "Node 2": 150000,
    "Node 3": 270000
}

yield_data = {
    "Node 1": [0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98],
    "Node 2": [0.60, 0.82, 0.95, 0.98, 0.98, 0.98, 0.98, 0.98],
    "Node 3": [0.20, 0.25, 0.35, 0.50, 0.65, 0.85, 0.95, 0.98]
}

max_delta = 2500  

# Iterate over QUARTERS starting from 1 because we can skip Q1'26
for q in range(1, len(QUARTERS)):
    
    # Set initial guess
    current = {node: loading[node][-1] for node in loading}
    prev = {node: loading[node][-1] for node in loading}

    # Calculate effective yield
    effective_yields = {
        node: gb_per_wafer[node] * yield_data[node][q]
        for node in gb_per_wafer
    }

    # Calculate desired total output
    target_output = TAM[q] * 1e9

    # Compute total GB Output
    def total_output(loadings):
        return weeks_per_quarter * sum(loadings[node] * effective_yields[node] for node in loadings)

    current_output = total_output(current)
    deficit = target_output - current_output

    # Sort nodes by effective yield descending
    nodes_sorted = sorted(effective_yields.keys(), key=lambda n: effective_yields[n], reverse=True)

    # Adjusting the load based on the deficit
        # Low output > we need to increase the node with the highest yield
    if deficit > 0:
        for node in nodes_sorted:
            required_increase = deficit / (weeks_per_quarter * effective_yields[node])
            # Ensure that the increment is not more than prev load + 2.5k
            allowed_increase = min(max_delta, prev[node] + max_delta)
            delta = min(required_increase, allowed_increase)
            if delta > 0:
                current[node] = prev[node] + delta
                break
        # High output > we need to decrease the node with the lowest yield 
    else:
        for node in reversed(nodes_sorted):
            required_decrease = abs(deficit) / (weeks_per_quarter * effective_yields[node])
            # Ensure that the increment is not less than prev load - 2.5k
            allowed_decrease = min(max_delta, prev[node] - max_delta)
            delta = min(required_decrease, allowed_decrease)
            if delta > 0:
                current[node] = prev[node] - delta
                break
            
    # Append and round nearest integer
    for node in loading:
        loading[node].append(int(round(current[node])))
'''
LOADING
        Q1'26   Q2'26   Q3'26   Q4'26   Q1'27   Q2'27   Q3'27   Q4'27   
Node 1	12000	12000	12000	12000	12000	12000	11468	11468
Node 2	5000	7026	9526	11490	11490	11490	11490	11490
Node 3	1000	1000	1000	1000	3267	4778	4778	4922

'''
print(loading)
# PART B
## I

workstation_minute_load = {
    "A" : [4.0, 4.0, 4.0],
    "B" : [6.0, 9.0, 2.0],
    "C" : [2.0, 2.0, 5.4],
    "D" : [5.0, 5.0, 0.0],
    "E" : [5.0, 10.0, 0.0],
    "F" : [0.0, 1.8, 5.8],
    "G" : [12.0, 0.0, 16.0],
    "H" : [2.1, 0.0, 0.0],
    "I" : [0.0, 6.0, 0.0],
    "J" : [0.0, 0.0, 2.1]
}

workstation_utilization = {
    "A": 0.78,
    "B": 0.76,
    "C": 0.80,
    "D": 0.80,
    "E": 0.76,
    "F": 0.80,
    "G": 0.70,
    "H": 0.85,
    "I": 0.75,
    "J": 0.60
}

#loading
tools_required_per_quarter_per_workstation = {quarter: [] for quarter in QUARTERS}

# Calculate tool requirements for each quarter
for i, quarter in enumerate(QUARTERS):
    quarter_tool_requirements = {}
    
    for station in workstation_minute_load:
        tool_time = 0  

        # Calculate the tool_time
        for node_index, node in enumerate(["Node 1", "Node 2", "Node 3"]):
            tool_time += workstation_minute_load[station][node_index] * loading[node][i]
        
        # Calculate the tool requirement
        tool_requirement = tool_time / (7*24*60) * workstation_utilization[station]
        
        # Add the rounded up tool requirement to the dictionary 
        quarter_tool_requirements[station] = math.ceil(tool_requirement)
    
    # Store the tool requirements for the current quarter
    tools_required_per_quarter_per_workstation[quarter] = quarter_tool_requirements
            
''' OUTPUT
Number of Tools per quarter per workstation
Q1'26   6   9   4   7   9   2   12  3   3   1
Q2'26	7	11	4	8	10	2	12	2	4	1
Q3'26	3	13	4	8	12	2	12	2	5	1
Q4'26	8	14	5	10	14	3	12	3	6	1
Q1'27	9	14	6	10	14	4	14	3	6	1
Q2'27	9	14	6	10	14	4	16	3	6	1
Q3'27	9	14	6	10	13	4	15	3	6	1
Q4'27	9	14	6	10	13	4	16	3	6	1
'''

# II
workstation_CAPEX_cost = {
    "A": 3.0,
    "B": 6.0,
    "C": 2.2,
    "D": 3.0,
    "E": 3.5,
    "F": 6.0,
    "G": 2.1,
    "H": 1.8,
    "I": 3.0,
    "J": 8.0
}

workstation_tools_count = {
    "A": 10,
    "B": 18,
    "C": 5,
    "D": 11,
    "E": 15,
    "F": 2,
    "G": 23,
    "H": 3,
    "I": 4,
    "J": 1
}

additional_tools_required = {quarter: {} for quarter in QUARTERS}
for quarter, requirements in tools_required_per_quarter_per_workstation.items():

    for station, required in requirements.items():
        available = workstation_tools_count[station]
        additional_needed = required - available
    
        # Only add tools if needed
        additional_tools_required[quarter][station] = max(0, additional_needed)
        
        # Update the tool count 
        workstation_tools_count[station] += max(0, additional_needed)

''' OUTPUT
Q1'26  0  0  0  0  0  0  0  0  0  0
Q2'26  0  0  0  0  0  0  0  0  0  0
Q3'26  0  0  0  0  0  0  0  0  1  0
Q4'26  0  0  0  0  0  1  0  0  1  0
Q1'27  0  0  1  0  0  1  0  0  0  0
Q2'27  0  0  0  0  0  0  0  0  0  0
Q3'27  0  0  0  0  0  0  0  0  0  0
Q4'27  0  0  0  0  0  0  0  0  0  0
'''


CAPEX_cost = {quarter : 0 for quarter in QUARTERS}

## Calculating the CAPEX incurred each quarter
for quarter, workstation_tools in additional_tools_required.items():
    #print(workstation_tools)
    cost = 0
    for workstation, value in workstation_tools.items():
        #print(workshop, value)
        cost += value * workstation_CAPEX_cost[workstation]



         
    CAPEX_cost[quarter] = round(cost, 1)

'''
CAPEX COST PER QUARTER
Q1'26: 0.0
Q2'26: 0.0
Q3'26: 3.0
Q4'26: 9.0
Q1'27: 8.2
Q2'27: 0.0
Q3'27: 0.0
Q4'27: 0.0
'''

## III
## Kinda has issues becuase it uses TAM from qn and not TAM from us
## Change it manually since no need to change code
net_profit = 0 
for i, quarter in enumerate(QUARTERS):
    revenue = TAM[i] * 0.002 * 1000000000 
    cost = CAPEX_cost[quarter] * 1000000
    net_profit += revenue - cost
    
#print(net_profit)
# Net: 

