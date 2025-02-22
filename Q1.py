import math
quarters = ["Q1'26", "Q2'26", "Q3'26", "Q4'26", "Q1'27", "Q2'27", "Q3'27", "Q4'27"]
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

# Iterate over quarters starting from 1 because we can skip Q1'26
for q in range(1, len(quarters)):
    
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

    # PRINTING 
    #print(f"Optimized weekly loading for {quarters[q]}:")
    #for node in loading:
    #    print(f"{node}: {loading[node][q]} wafers")
    #print()

    # Checking
    #current_output_check = total_output(current)
    #print(f"Total output for {quarters[q]} (in billion GB): {current_output_check / 1e9:.2f} billion GB")
    #print(f"Target TAM for {quarters[q]} (in billion GB): {TAM[q]}")
    #print()


'''
LOADING
        Q1'26   Q2'26   Q3'26   Q4'26   Q1'27   Q2'27   Q3'27   Q4'27   
Node 1	12000	12000	12000	12000	12000	12000	11468	11468
Node 2	5000	7026	9526	11490	11490	11490	11490	11490
Node 3	1000	1000	1000	1000	3267	4778	4778	4922

'''

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

tools_required_per_quarter_per_workstation = {quarter: [] for quarter in quarters}
tools_required_per_quarter = {quarter : 0 for quarter in quarters}
# Calculate tool requirements for each quarter
for i, quarter in enumerate(quarters):
    # Initialize the total tool requirement for each quarter
    quarter_tool_requirements = {}
    
    for station in workstation_minute_load:
        tool_time = 0  # Reset tool time for each workstation
        
        # Calculate the total loading for the current quarter for all nodes
        for node_index, node in enumerate(["Node 1", "Node 2", "Node 3"]):
            tool_time += workstation_minute_load[station][node_index] * loading[node][i]
        
        # Calculate the tool requirement for the workstation in the current quarter
        tool_requirement = tool_time / (7*24*60) * workstation_utilization[station]
        
        # Add the tool requirement to the dictionary, rounded up to the nearest integer
        quarter_tool_requirements[station] = math.ceil(tool_requirement)
    
    # Store the tool requirements for the current quarter
    tools_required_per_quarter_per_workstation[quarter] = quarter_tool_requirements
        
for quarter in tools_required_per_quarter:
    tools_required_per_quarter[quarter] = sum(tools_required_per_quarter_per_workstation[quarter].values())
        
    
#print(tools_required_per_quarter)
'''
Number of Tools per quarter
 "Q1'26": 56,
 "Q2'26": 62,
 "Q3'26": 68,
 "Q4'26": 76,
 "Q1'27": 81,
 "Q2'27": 83,
 "Q3'27": 81,
 "Q4'27": 82
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

CAPEX_cost = {quarter : 0 for quarter in quarters}
for quarter, workstation_tools in tools_required_per_quarter_per_workstation.items():
    #print(workstation_tools)
    cost = 0
    for workshop, value in workstation_tools.items():
        #print(workshop, value)
        cost += value * workstation_CAPEX_cost[workshop]
    CAPEX_cost[quarter] = round(cost, 1)
    

'''
CAPEX COST PER QUARTER
"Q1'26": 192.9,
"Q2'26": 217.4,
"Q3'26": 242.4,
"Q4'26": 272.6,
"Q1'27": 288.0,
"Q2'27": 292.2,
"Q3'27": 286.6,
"Q4'27": 288.7
'''

## III
net_profit = 0 
# Do not count Q1'26 since its fully paid for (given)
for i, quarter in enumerate(quarters[1:]):
    net_profit += TAM[i] * 0.002 * 1000000000 
    net_profit -= CAPEX_cost[quarter] * 1000000

print(net_profit)
