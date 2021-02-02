一、创建Cloudformation 
1.下载Cloudformation Yaml文件：
timestream-workshop-2021.yaml

2.在AWS控制台，选择Cloudformation，并创建stack。
 

其它都选择缺省， 点击Create Stack button.
 
 
Cloud Formation 创建成功

二、连接到新建的Ec2堡垒机
For Windows users: We will use PuTTY and PuTTY Key Generator to connect to the workstation using SSH. If you do not have these applications already installed please use the steps in Appendix 1 - Setting up PuTTY and connecting via SSH below.
For macOS or Linux users: You can connect using the following command from a terminal, however you will need to change the permissions of the certificate file first:
chmod 0600 [path to downloaded .pem file]
1.连接
ssh -i [path to downloaded .pem file] ec2-user@[bastionEndpoint]

2.执行aws configure
aws configure
Then select the defaults for everything except the default region name.  For the default region name, enter “us-east-1”.

 
三、创建Timestream数据库
1.使用 Amazon Timestream
在本教程中，您将学习如何创建环境来运行 Timestream 数据库和表，连接到该数据库和表，导入样本时序数据，以及查询和分析时序数据。 在本教程中，我们将使用 Amazon Timestream执行此操作。
单击此处时，AWS 管理控制台将在新的浏览器窗口中打开，因此您可以将本分步指南保持打开状态。加载此屏幕后，在数据库下找到 Amazon Timestream，然后单击以打开 Amazon Timestream 控制台。
 
2.创建 Timestream 数据库和表
在此步骤中，我们将使用 Amazon Timestream 创建数据库
 
a. 在 Amazon Timestream 控制台的右上角，选择要在其中创建数据库实例的地区。
注意：Amazon 云计算资源位于世界不同地区的高可用性数据中心设施中。每个地区包含多个不同的位置，称为“可用区”或 AZ。您可以选择托管 Amazon Timestream 活动的地区。 
 
 
b.  在console右侧, 单击创建数据库。
  
 
c. 输入数据库名，保留其它缺省设置，然后单击 create database（选择）。
  
 
d.选中刚创建的数据库，创建表。
  

 
e. 创建Timestream表， 设置表名和内存数据和磁性存储数据保留时长：
单击 Create table
  
 
3.在Timestream表中 查看新导入的时序样本数据。 单击Query Table
 
4.创建另外一个数据库devops 包含一张表metrics
 
 


四、连接到EC2堡垒机 安装Timesteam Sample python程序库
1.安装相应软件
设置时区
TZ='Asia/Shanghai'; export TZ

Install python3
sudo yum install -y python3

Install python3 pip
sudo yum install -y python3-pip

pip3 install boto3
sudo pip3 install boto3

pip3 install numpy
sudo pip3 install numpy

install git 
sudo yum install -y git

2.下载Github Timesteram python Sample 程序
git clone https://github.com/awslabs/amazon-timestream-tools amazon-timestream-tools

3.执行Python Sample程序 持续导入数据
cd amazon-timestream-tools/tools/continuous-ingestor

python3 timestream_sample_continuous_data_ingestor_application.py --database-name iot --table-name host_metrics --endpoint us-east-1

4.观测python运行一段时间 可以先将程序终止 CTRL+C
5.用python sample程序导入csv文件数据：
cd /home/ec2-user/amazon-timestream-tools/sample_apps/python

vi Constant.py 

将Costant.py修改成；

DATABASE_NAME = "iot"
TABLE_NAME = "host_metrics"

执行以下Python程序
python3 SampleApplication.py --csv_file_path ../data/sample.csv

五、安装Grafana Server
1.连接到EC2堡垒机：

sudo vi /etc/yum.repos.d/grafana.repo

For OSS releases:(拷贝以下内容到grafana.repo)
[grafana]
name=grafana
baseurl=https://packages.grafana.com/oss/rpm
repo_gpgcheck=1
enabled=1
gpgcheck=1
gpgkey=https://packages.grafana.com/gpg.key
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt

sudo yum install -y grafana


2.Start the server with service
To start the service and verify that the service has started:
sudo service grafana-server start
sudo service grafana-server status
Configure the Grafana server to start at boot:
sudo /sbin/chkconfig --add grafana-server

3.安装timestream Plugin
sudo grafana-cli plugins install grafana-timestream-datasource

4.重启grafana
sudo service grafana-server restart
配置Grafana 要访问Timesteam服务所用的IAM Role
 
5.选择IAM服务， 选择要修改的role, role name: grafanaEC2rolelabview

 
修改trust relationship:
  
将Policy document 全部选中， 替换成以下内容：
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid":"",
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Sid":"",
      "Effect": "Allow",
      "Principal": {
        "AWS": "[请替换成CloudFormation output中的role arn]"
      },
      "Action": "sts:AssumeRole"
    } 
  ]
}
修改后的trust relationship:
 
6.登录到Grafana server
To log in to Grafana for the first time:
1.	Open your web browser and go to http://[Grafana server public ip]:3000
2.	
3.	 The default HTTP port that Grafana listens to is 3000 unless you have configured a different port.
如何获取Ec2 Public IP地址， 如下图所示：
 
4.	On the login page, enter admin for username and password.(输入用户名和密码都是admin)
5.	Click Log In. If login is successful, then you will see a prompt to change the password.
6.	Click OK on the prompt, then change your password.

7.配置Grafana
增加Timestream数据源
 
配置Timestream数据源

拷贝配置所需要role ARN信息 （从cloudformation output tab）
 
 
创建时间数据分析仪表版 Dashboard1 IOT
 
8.数据准备 导入csv文件数据
登录到EC2堡垒机
cd amazon-timestream-tools/sample_apps/python
vi Constant.py
更改以下信息：
DATABASE_NAME = "iot"
TABLE_NAME = "host_metrics"
执行python程序 持续从csv文件导入数据：

wget https://bigdata-bingbing.s3-ap-northeast-1.amazonaws.com/run_csv_load.sh .

执行shell 脚本
sh run_csv_load.sh
创建Dashboard查询时 请设定时区为本地浏览器时区
 
1.	查询host_metrics 最后插入的十条记录（以表格为展现方式）

select * from iot.host_metrics
order by time desc
limit 10

 
2.	降采样 重新设定统计时间间隔
在Grafana Dashboard中创建Panel 查询Amazon Timestream数据
查询在过去的2个小时内，找出一台主机在过去2小时内的平均利用率， 以30秒为统计间隔:
SELECT BIN(time, 30s) AS binned_timestamp, ROUND(AVG(measure_value::double), 2) AS avg_cpu_utilization
FROM "iot".host_metrics
WHERE measure_name = 'cpu_utilization'
    AND hostname = 'host-fj2hx'
    AND time > ago(2h)
GROUP BY hostname, BIN(time, 30s)
ORDER BY binned_timestamp ASC

 
3.	查询平均值
在Grafana Dashboard中创建Panel 查询Amazon Timestream数据
查询基于以下sql 构建 （计算过去2小时内特定EC2主机的平均CPU利用率p90、p95和p99。以15秒为一个采样间隔）:


SELECT region, az, hostname, BIN(time, 15s) AS binned_timestamp,
    ROUND(AVG(measure_value::double), 2) AS avg_cpu_utilization,
    ROUND(APPROX_PERCENTILE(measure_value::double, 0.9), 2) AS p90_cpu_utilization,
    ROUND(APPROX_PERCENTILE(measure_value::double, 0.95), 2) AS p95_cpu_utilization,
    ROUND(APPROX_PERCENTILE(measure_value::double, 0.99), 2) AS p99_cpu_utilization
FROM "iot".host_metrics
WHERE measure_name = 'cpu_utilization'
    AND hostname = 'host-fj2hx'
    AND time > ago(2h)
GROUP BY region, hostname, az, BIN(time, 15s)
ORDER BY binned_timestamp ASC

 

保存刚创建的Panel:
 

保存刚创建的Dashboard Dashboard1

4.	统计分析 查询异常主机 
发现EC2主机的CPU利用率比过去2小时内整个机群的平均CPU利用率高

WITH avg_fleet_utilization AS (
    SELECT COUNT(DISTINCT hostname) AS total_host_count, AVG(measure_value::double) AS fleet_avg_cpu_utilization
    FROM "iot".host_metrics
    WHERE measure_name = 'cpu_utilization'
        AND time > ago(2h)
), avg_per_host_cpu AS (
    SELECT region, az, hostname, AVG(measure_value::double) AS avg_cpu_utilization
    FROM "iot".host_metrics
    WHERE measure_name = 'cpu_utilization'
        AND time > ago(2h)
    GROUP BY region, az, hostname
)
SELECT region, az, hostname, avg_cpu_utilization, fleet_avg_cpu_utilization
FROM avg_fleet_utilization, avg_per_host_cpu
WHERE avg_cpu_utilization > 1.0 * fleet_avg_cpu_utilization
ORDER BY avg_cpu_utilization DESC

 

创建时间序列

select hostname, CREATE_TIME_SERIES(time, measure_value::double) as cpu_utilization FROM iot.host_metrics
                WHERE measure_name= 'cpu_utilization'
                and hostname= 'host-fj2hx'
                GROUP BY hostname
 
线性插值
找出过去2小时内特定EC2主机以30秒为间隔的平均CPU利用率，使用线性插值填充缺失的值

WITH binned_timeseries AS (
    SELECT hostname, BIN(time, 30s) AS binned_timestamp, ROUND(AVG(measure_value::double), 2) AS avg_cpu_utilization
    FROM "iot".host_metrics
    WHERE measure_name = 'cpu_utilization'
        AND hostname = 'host-fj2hx'
        AND time > ago(2h)
    GROUP BY hostname, BIN(time, 30s)
), interpolated_timeseries AS (
    SELECT hostname,
        INTERPOLATE_LINEAR(
            CREATE_TIME_SERIES(binned_timestamp, avg_cpu_utilization),
                SEQUENCE(min(binned_timestamp), max(binned_timestamp), 30s)) AS interpolated_avg_cpu_utilization
    FROM binned_timeseries
    GROUP BY hostname
)
SELECT time, ROUND(value, 2) AS interpolated_cpu
FROM interpolated_timeseries
CROSS JOIN UNNEST(interpolated_avg_cpu_utilization)
 


列出过去2小时内某个特定EC2主机的CPU利用率低于5%的测量值，使用线性插值填充缺失值
WITH time_series_view AS (
    SELECT min(time) AS oldest_time, INTERPOLATE_LINEAR(
        CREATE_TIME_SERIES(time, ROUND(measure_value::double, 2)),
        SEQUENCE(min(time), max(time), 10s)) AS cpu_utilization
    FROM "iot".host_metrics
    WHERE hostname = 'host-fj2hx'
        AND measure_name = 'cpu_utilization'
        AND time > ago(2h)
    GROUP BY hostname
)
SELECT FILTER(cpu_utilization, x -> x.value < 5 AND x.time > oldest_time + 1m)
FROM time_series_view

 


保存Dashboard 为IOT
 
设定Dashboard iot自动刷新数据 （每5秒1次）
 
创建时间数据分析Dashboard2 Devops
数据准备
登录到EC2堡垒机
cd amazon-timestream-tools/tools/continuous-ingestor

python3 timestream_sample_continuous_data_ingestor_application.py --database-name devops --table-name metrics --endpoint us-east-1
创建时间数据分析仪表版 Dashboard1 devops
 

1.	过去时间段 统计每个微服务从多少个主机收集指标
SELECT CASE WHEN microservice_name = 'apollo' THEN num_instances ELSE NULL END AS apollo,
    CASE WHEN microservice_name = 'athena' THEN num_instances ELSE NULL END AS athena,
    CASE WHEN microservice_name = 'demeter' THEN num_instances ELSE NULL END AS demeter,
    CASE WHEN microservice_name = 'hercules' THEN num_instances ELSE NULL END AS hercules,
    CASE WHEN microservice_name = 'zeus' THEN num_instances ELSE NULL END AS zeus
FROM (
    SELECT microservice_name, SUM(num_instances) AS num_instances
    FROM (
        SELECT microservice_name, COUNT(DISTINCT instance_name) as num_instances
        FROM devops.metrics
        WHERE $__timeFilter
            AND measure_name = 'cpu_user'
            AND region = 'us-east-1'
        GROUP BY region, cell, silo, availability_zone, microservice_name
    )
    GROUP BY microservice_name
)


选择图形显示 select Gauge
 

2.	微服务Zeus中 高cpu主机比例
SELECT ROUND(COUNT(IF(p90Cpu > 80, 1, NULL)) * 100 / CAST(COUNT(*) AS DOUBLE)) AS PercentageHigh
FROM
    (
        SELECT instance_name, approx_percentile(measure_value::double, 0.9) as p90Cpu
        FROM devops.metrics
        WHERE $__timeFilter
            AND measure_name = 'cpu_user'
            AND region = 'ap-northeast-1' AND cell = 'ap-northeast-1-cell-5' AND microservice_name = 'zeus'
        GROUP BY region, cell, silo, availability_zone, microservice_name, instance_name
    )

选择Panel图形类型：
 
 

3.	GC Pause distribution for high memory utilization hosts
WITH per_instance_memory_used AS (
    SELECT region, cell, silo, availability_zone, microservice_name, instance_name, BIN(time, 5m) AS time_bin,
        MAX(measure_value::double) AS max_memory
    FROM devops.metrics
    WHERE $__timeFilter
        AND measure_name = 'memory_used'
        AND region = 'us-east-1' AND cell = 'us-east-1-cell-1'
    GROUP BY region, cell, silo, availability_zone, 
        microservice_name, instance_name, BIN(time, 5m)
), per_microservice_memory AS (
    SELECT region, cell, silo, microservice_name,
        APPROX_PERCENTILE(max_memory, 0.95) AS p95_max_memory
    FROM per_instance_memory_used
    GROUP BY region, cell, silo, microservice_name
), per_silo_ranked AS (
    SELECT region, cell, silo, microservice_name,
        DENSE_RANK() OVER (PARTITION BY region, cell, silo ORDER BY p95_max_memory DESC) AS rank
    FROM per_microservice_memory
), instances_with_high_memory AS (
    SELECT r.region, r.cell, r.silo, r.microservice_name, m.instance_name,
        APPROX_PERCENTILE(max_memory, 0.95) AS p95_max_memory
    FROM per_silo_ranked r INNER JOIN per_instance_memory_used m
        ON r.region = m.region AND r.cell = m.cell AND r.silo = m.silo AND r.microservice_name = m.microservice_name
    WHERE r.rank = 1
    GROUP BY r.region, r.cell, r.silo, r.microservice_name, m.instance_name
), ranked_instances AS (
    SELECT region, cell, silo, microservice_name, instance_name,
        DENSE_RANK() OVER (PARTITION BY region, cell, silo, microservice_name ORDER BY p95_max_memory DESC) AS rank
    FROM instances_with_high_memory
)
SELECT t.region, t.cell, t.silo, t.microservice_name, t.instance_name, t.process_name, t.jdk_version,
    MIN(measure_value::double) AS min_gc_pause,
    ROUND(AVG(measure_value::double), 2) AS avg_gc_pause,
    ROUND(STDDEV(measure_value::double), 2) AS stddev_gc_pause,
    ROUND(APPROX_PERCENTILE(measure_value::double, 0.5), 2) AS p50_gc_pause,
    ROUND(APPROX_PERCENTILE(measure_value::double, 0.9), 2) AS p90_gc_pause,
    ROUND(APPROX_PERCENTILE(measure_value::double, 0.99), 2) AS p99_gc_pause
FROM ranked_instances r INNER JOIN devops.metrics t ON
    r.region = t.region AND r.cell = t.cell AND r.silo = t.silo AND 
    r.microservice_name = t.microservice_name AND r.instance_name = t.instance_name
WHERE $__timeFilter
    AND measure_name = 'gc_pause'
    AND rank = 1
GROUP BY t.region, t.cell, t.silo, t.microservice_name, t.instance_name, t.process_name, t.jdk_version
 
展示图形选择Bar gauge
 
4.	Memory used distribution for a Micro-service
SELECT region, cell, microservice_name, BIN(time, 1h) AS hour, 
    COUNT(DISTINCT instance_name) AS num_hosts,
    ROUND(AVG(measure_value::double), 2) AS avg_value,
    ROUND(APPROX_PERCENTILE(measure_value::double, 0.9), 2) AS p90_value,
    ROUND(APPROX_PERCENTILE(measure_value::double, 0.95), 2) AS p95_value,
    ROUND(APPROX_PERCENTILE(measure_value::double, 0.99), 2) AS p99_value
FROM devops.metrics
WHERE $__timeFilter
    AND measure_name = 'memory_used'
    AND microservice_name = 'zeus'
GROUP BY region, cell, microservice_name, BIN(time, 1h)
ORDER BY p99_value DESC
 

CPU Usage for a micro-service within a Silo
SELECT BIN(time, 1m) AS time_bin,
    AVG(CASE WHEN measure_name = 'cpu_user' THEN measure_value::double ELSE NULL END) AS avg_cpu_user,
    AVG(CASE WHEN measure_name = 'cpu_system' THEN measure_value::double ELSE NULL END) AS avg_cpu_system,
    AVG(CASE WHEN measure_name = 'cpu_idle' THEN measure_value::double ELSE NULL END) AS avg_cpu_idle,
    AVG(CASE WHEN measure_name = 'cpu_iowait' THEN measure_value::double ELSE NULL END) AS avg_cpu_iowait,
    AVG(CASE WHEN measure_name = 'cpu_steal' THEN measure_value::double ELSE NULL END) AS avg_cpu_steal,
    AVG(CASE WHEN measure_name = 'cpu_nice' THEN measure_value::double ELSE NULL END) AS avg_cpu_nice,
    AVG(CASE WHEN measure_name = 'cpu_si' THEN measure_value::double ELSE NULL END) AS avg_cpu_si,
    AVG(CASE WHEN measure_name = 'cpu_hi' THEN measure_value::double ELSE NULL END) AS avg_cpu_hi
FROM devops.metrics
WHERE $__timeFilter
    AND measure_name IN (
        'cpu_user', 'cpu_system', 'cpu_idle', 'cpu_iowait',
        'cpu_steal', 'cpu_nice', 'cpu_si', 'cpu_hi'
    )
    AND region = 'ap-northeast-1' AND cell = 'ap-northeast-1-cell-5' AND silo = 'ap-northeast-1-cell-5-silo-2'
    AND availability_zone = 'ap-northeast-1-3' AND microservice_name = 'zeus'
    AND instance_type = 'm5.4xlarge' AND os_version = 'AL2'
GROUP BY BIN(time, 1m)
ORDER BY time_bin desc
 
选择Panel图形类型：
 
Hosts with Low CPU Utilization in Microservice Apollo
SELECT COUNT(*) AS NumLowUtilizationHosts FROM (
    SELECT region, cell, silo, availability_zone, microservice_name, instance_name
    FROM devops.metrics
    WHERE $__timeFilter
        AND measure_name ='cpu_used'
        AND microservice_name = 'apollo'
    GROUP BY region, cell, silo, availability_zone, microservice_name, instance_name
    HAVING approx_percentile(measure_value::double, 0.9) < 20
)
 
选择Panel图形类型：
 
查询任务终止状态分布
SELECT measure_value::varchar AS task_end_state, COUNT(*) AS num_tasks
FROM devops.metrics
WHERE $__timeFilter
    AND measure_name = 'task_end_state'
    AND region = 'ap-northeast-1'
    AND cell = 'ap-northeast-1-cell-1'
    AND microservice_name = 'apollo'
GROUP BY measure_value::varchar
ORDER BY 2 DESC
 
查询有 GC Pause的主机
SELECT 
    silo, microservice_name, instance_name, 
    CREATE_TIME_SERIES(time, measure_value::double) AS gc_pause
FROM devops.metrics
WHERE $__timeFilter
    AND measure_name = 'gc_pause'
    AND region = 'ap-northeast-1' 
    AND cell = 'ap-northeast-1-cell-5' 
    AND silo = 'ap-northeast-1-cell-5-silo-2'
    AND availability_zone = 'ap-northeast-1-3' 
    AND microservice_name = 'zeus'
GROUP BY region, 
    cell, 
    silo, 
    availability_zone, 
    microservice_name,
    instance_name, 
    process_name, 
    jdk_version     
ORDER BY AVG(measure_value::double) DESC
LIMIT 3
 

查询主机
SELECT region, cell, silo, availability_zone, microservice_name,
    instance_type, os_version, instance_name
FROM devops.metrics
WHERE $__timeFilter
    AND region = 'us-east-1'
    AND measure_name = 'cpu_user'
GROUP BY region, cell, silo, availability_zone, microservice_name,
    instance_type, os_version, instance_name
ORDER BY region, cell, silo, availability_zone, microservice_name,
    instance_type, os_version, instance_name
 

查询表中指标
SHOW MEASURES FROM devops.metrics

 
查询区域服务分布
SELECT region, cell, silo, availability_zone,
    approx_distinct(microservice_name || instance_name) AS num_instances
FROM devops.metrics
WHERE $__timeFilter
    AND measure_name = 'cpu_user'
GROUP BY region, cell, silo, availability_zone
ORDER BY region, cell, silo, availability_zone
 

 


APPENDIX
Appendix 1 – Setting up PuTTY and connecting via SSH
For Windows users, please download PuTTY (putty) and the PuTTY Key Generator (puttygen) from the following links:
https://aurora-bjs-lab.s3-ap-southeast-1.amazonaws.com/putty64/putty.exe
https://aurora-bjs-lab.s3-ap-southeast-1.amazonaws.com/putty64/puttygen.exe

1.	Once you have downloaded putty and puttygen, open puttygen and click on Load.
 
2.	Please make sure that the file filter is set to “All Files (*.*) and then select dblabkeys.pem.
 
 
3.	Fill in the Key passphrase and Confirm passphrase fields with a password of your choice that will be used to encrypt your private key and then click Save private key.  Please use “dblabkeys.ppk” as your new key name.
 
4.	Next, open putty and enter into the Host Name (or IP address) field the following value:
ubuntu@[bastionEndpoint]
 
 
5.	Next, navigate within PuTTY to Connection  SSH  Auth and browse to the dblabkeys.ppk ppk file that you created with the PuTTY Key Generator previously, and then click Open.
 
6.	When prompted by the PuTTY Security Alert, click Yes.
 
7.	Next, enter the password that you configured when you created the dblabkeys.ppk private file previously.
 


