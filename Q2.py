import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


## QN 2

## Loading the given excel data set
df = pd.read_excel('Q2DataSet.xlsx')

## node 1
workstation_H = df.iloc[:,0]
node1_mean = workstation_H.mean()
node1_sd = workstation_H.std()


## node 2 
workstation_I = df.iloc[:,1]
node2_mean = workstation_I.mean()
node2_sd = workstation_I.std()


## node 3
workstation_J = df.iloc[:,2]
node3_mean = workstation_J.mean()
node3_sd = workstation_J.std()

## Mean
# Node 1: 2.1316261381378303
# Node 2: 5.99186175928513
# Node 3: 3.0244601990777378

## SD
# Node 1: 0.5007105720083864
# Node 2: 3.292673621732793
# Node 3: 2.0549047002372025

mean_rpt = {
    'Node 1' : node1_mean,
    'Node 2' : node2_mean,
    'Node 3' : node3_mean
}

sd_rpt = {
    'Node 1' : node1_sd,
    'Node 2' : node2_sd,
    'Node 3' : node3_sd
}

ultilization = {
    'Node 1' : 0.85,
    'Node 2' : 0.75,
    'Node 3' : 0.60
}

# Expected Value
expected_value = {}
for i in mean_rpt:
    expected_value[i] = mean_rpt[i] * ultilization[i]

# Expected Value Node 1': 1.8118822174171556
# Expected Value Node 2': 4.493896319463848
# Expected Value Node 3': 1.8146761194466425


## TODO CHANGE 
loading = {
    'Node 1' : 12000,   #np.array([12000, 14500, 17000, 19500, 22000, 24500, 27000, 24500]), 
    'Node 2' : 5000,    #np.array([13000, 14500, 17000, 19500, 22000, 24500, 27000, 24500]),
    'Node 3' : 1000     #np.array([12000, 14500, 17000, 19500, 22000, 24500, 27000, 24500])
}
#minute load is expect rpt

tool_requirement = 0
for node in expected_value:
    minute_load_node = expected_value[node]
    ultil_node = ultilization[node]
    loading_node = loading[node]
    
    tool_requirement += (loading_node * minute_load_node) / ((7 * 24 * 60) * ultil_node)


## PART IV
num_wafers = 10000

total_times = { 'Node 1': [], 'Node 2': [], 'Node 3': [] } # Store total time for each node
np.random.seed(1)
# The simulation
for node in mean_rpt:
    for _ in range(num_wafers):
        
        # Generate random RPTs for X wafers assume its following normal distribution
        # Since the number of simulations used is very large, 
        # we approximate the distribution of the total time taken to process num_wafers to be normal
        rpt_samples = np.random.normal(mean_rpt[node], sd_rpt[node], loading[node])
        
        # Total time for this X num of wafers 
        total_time = np.sum(rpt_samples)
        total_times[node].append(total_time)
        

def checkCI(node):
    simulated_mean = np.mean(node)
    simulated_sd = np.std(node)

    # Calculate 95% Confidence Interval
    ci_lower = simulated_mean - 1.96 * (simulated_sd / np.sqrt(num_wafers))
    ci_upper = simulated_mean + 1.96 * (simulated_sd / np.sqrt(num_wafers))
    
    return ci_lower, ci_upper

for node in total_times:
    plt.figure(figsize=(10, 6))
    plt.hist(total_times[node], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    plt.title(f'{node} Total Processing Time')
    plt.xlabel('Total Time (Minutes)')
    plt.ylabel('Frequency')
    plt.show()

    print(f"\n{node} Total Time Percentiles:")
    print(f"Mean: {np.mean(total_times[node])}")
    print(f"95th Percentile: {np.percentile(total_times[node], 95)}")
    print(f"99th Percentile: {np.percentile(total_times[node], 99)}")
    
        
    ci_lower, ci_upper = checkCI(total_times[node])
    if ci_lower <= mean_rpt[node] * num_wafers <= ci_upper:
        print(f"Pop Mean {mean_rpt[node] * num_wafers} lies within 95% Conf Int")
    else:
        print(f"Pop Mean {mean_rpt[node] * num_wafers} does not lie within 95% Conf Int")
    
'''
Node 1 Total Time Percentiles:
Mean: 25578.80240232993
95th Percentile: 25669.22200812859
99th Percentile: 25707.709715058514
Pop Mean 21316.261381378303 does not lie within 95% Conf Int

Node 2 Total Time Percentiles:
Mean: 29959.811611384062
95th Percentile: 30343.873773942465
99th Percentile: 30504.9211404563
Pop Mean 59918.6175928513 does not lie within 95% Conf Int

Node 3 Total Time Percentiles:
Mean: 3024.7873544340296
95th Percentile: 3132.6655450631847
99th Percentile: 3179.383101445847
Pop Mean 30244.601990777377 does not lie within 95% Conf Int
'''
    
## PART V 
