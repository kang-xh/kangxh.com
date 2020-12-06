# performance data query

## check memory usage for container: 

    Perf
    | where TimeGenerated >= ago(2h)
    | where InstanceName  contains "jenkins" or InstanceName contains "kangxhweb" or InstanceName contains "kangzianweb"
    | where (CounterName == "memoryWorkingSetBytes" )
    | summarize avg(CounterValue / 1024/1024) by strcat(split(InstanceName, "/")[-1], "-", CounterName), bin(TimeGenerated, 1m)
    | render timechart