
## Schema and Description

### 1. Job Trace

#### Description

Provides rich information on all jobs submitted to scheduler in each cluster.

+ `trace_seren.csv` Example

| job_id  | user  | node_num | gpu_num | cpu_num | type  | state     | submit_time               | start_time                | end_time                  | duration | queue | gpu_time |
|---------|-------|----------|---------|---------|-------|-----------|---------------------------|---------------------------|---------------------------|----------|-------|----------|
| 5778432 | u5907 | 1        | 8       | 128     | Other | FAILED    | 2023-03-01 00:18:22+08:00 | 2023-03-01 00:18:54+08:00 | 2023-03-01 00:20:51+08:00 | 117      | 32    | 936.0    |
| 5778469 | u5907 | 1        | 8       | 128     | Other | COMPLETED | 2023-03-01 00:23:58+08:00 | 2023-03-01 00:24:11+08:00 | 2023-03-01 01:09:04+08:00 | 2693     | 13    | 21544.0  |


+ `trace_kalos.csv` Example

| job_id           | user  | node_num | gpu_num | cpu_num | mem_per_pod_GB | shared_mem_per_pod | type  | state     | submit_time               | start_time                | end_time                  | fail_time                 | stop_time                 | duration | queue | gpu_time |
|------------------|-------|----------|---------|---------|----------------|--------------------|-------|-----------|---------------------------|---------------------------|---------------------------|---------------------------|---------------------------|----------|-------|----------|
| dlctk696s0jbvitv | uf794 | 8        | 64      | 960     | 1000           | 100.0              | Other | FAILED    | 2023-05-17 11:00:58+00:00 | 2023-05-17 11:01:08+00:00 | 2023-05-17 11:01:16+00:00 | 2023-05-17 11:01:16+00:00 |                           | 18       | 10.0  | 1152.0   |
| dlc1t2ypl09b8qtp | uf794 | 8        | 64      | 960     | 1000           | 100.0              | Other | CANCELLED | 2023-05-17 11:28:42+00:00 | 2023-05-17 11:28:54+00:00 | 2023-05-17 11:30:04+00:00 |                           | 2023-05-17 11:30:04+00:00 | 82       | 12.0  | 5248.0   |


#### Schema

| Field         | Description                                         |
| ------------- | --------------------------------------------------- |
| `job_id`      | unique id of the job                |
| `user`        | hashed id for the user, prefix is '*u*'             |
| `node_num`    | number of nodes in the job                          |
| `gpu_num`     | number of GPUs required for the job                 |
| `cpu_num`     | number of CPUs required for the job                 |
| `type`     | workload type in LLM development                 |
| `state`       | the job's status upon termination  <sup>1</sup>     |
| `submit_time` | the job's submission time                           |
| `start_time`  | the job's start execution time                      |
| `end_time`    | the job's termination time                          |
| `duration`    | total job execution time of the job <sup>2</sup>    |
| `queue`       | total job queue time of the job <sup>3</sup>        |
| `gpu_time`       | total GPU resource consumed by the job <sup>4</sup>        |

Only in Kalos:
| Field         | Description                                         |
| ------------- | --------------------------------------------------- |
| `mem_per_pod_GB`      | Pod memory resource configuration               |
| `shared_mem_per_pod`        | Pod memory resource configuration             |
| `fail_time`    | the time that failure occurs                          |
| `stop_time`     | the time that job stops                 |



#### Notes
1. A job can end up with one of five statuses: (1) `COMPLETED`: it is finished successfully; (2) `CANCELLED`: it is terminated by the user; (3) `FAILED`: it is terminated due to internal or external errors; (4) `TIMEOUT`: the execution time is out of limit; (5) `NODE_FAIL`: it is terminated due to the node crash. `TIMEOUT` and `NODE_FAIL` are very rare in our traces, and are regarded as failed in our analysis.
2. Calculated from the difference between `end_time` and `start_time`. (Unit: seconds)
3. Calculated from the difference between `start_time` and `submit_time`. (Unit: seconds)
4. Calculated from the product between `duration` and `gpu_num`.
