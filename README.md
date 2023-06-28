# godwoken-readonly-monitor

## Description
1. API status monior
   
2. Godwoken BlockChain Height monitor

## Usage
1. Build container images
   
2. Edit Kubernetes Deployment File
   
3. Create Deploy, Service Source
   
4. Apploy Deploy
   
5. Access Metrics

```
curl http://gw-readonly-monitor:5000/metrics
```
##  Alert
The monitoring is implemented using Prometheus, and the job configuration is as follows:
```
# godwoken 
- job_name: 'godwoken'
  scrape_interval: 10s
  scrape_timeout: 5s
  metrics_path: "/metrics"
  static_configs:
    - targets: 
        - gw-readonly-monitor.testnet:5000
        - gw-readonly-monitor.mainnet:5000
```

Alerting is done using Alertmanager, and standard configuration is sufficient.

Grafana dashboard is used to display the panels.