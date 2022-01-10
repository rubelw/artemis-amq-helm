Example Artemis 2.20 docker build and helm deployment locally using minikube




## Based on:
* https://github.com/vromero/activemq-artemis-docker
* (Example 1) https://github.com/deviceinsight/activemq-artemis-helm
* (Example 2) https://github.com/vromero/activemq-artemis-helm


## Prerequisites
1. minikube installed
2. kubectl installed
3. helm3 installed
4. docker installed
5. dockerhub account or docker repository


## 1. Docker build

```bash
cd docker
docker build --build-arg ACTIVEMQ_ARTEMIS_VERSION=2.20.0 --build-arg BASE_IMAGE=openjdk:11-jdk-stretch -t <dockerhub name>/activemq-artemis:2.20-latest .

docker login
docker push <dockerhub username>/activemq-artemis:2.20.15-latest
```

## 2. Helm Deployment


Start minikube

```bash
minikube start
  minikube v1.24.0 on Darwin 12.1
  Using the hyperkit driver based on existing profile
  Starting control plane node minikube in cluster minikube
  Updating the running hyperkit "minikube" VM ...
  Preparing Kubernetes v1.22.3 on Docker 20.10.8 ...
  Verifying Kubernetes components...
    ▪ Using image kubernetesui/dashboard:v2.3.1
    ▪ Using image kubernetesui/metrics-scraper:v1.0.7
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
  Enabled addons: storage-provisioner, dashboard
  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```

Start minikube dashboard

```bash
minikube dashboard
  Verifying dashboard health ...
  Launching proxy ...
  Verifying proxy health ...
  Opening http://127.0.0.1:64894/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/ in your default browser...

```


Start minikube tunnel in another terminal or tab

```bash
 minikube tunnel
Status:	
	machine: minikube
	pid: 39839
	route: 10.96.0.0/12 -> 192.168.64.2
	minikube: Running
	services: [amq-artemis]
    errors: 
		minikube: no errors
		router: no errors
		loadbalancer emulator: no errors

```



# Example 1 - Deploy helm

## Update values


Update the repository and tag

```bash
image:
## repository and image tag are required
  repository: <dockerhub username>/activemq-artemis
  tag: 2.20-latest
```

## Deploy the helm chart

```bash

cd helm/charts/artemis
helm install amq -f values.yaml . 

NAME: amq
LAST DEPLOYED: Fri Jan  7 14:36:31 2022
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

## View helm logs

```bash
kubectl logs amq-artemis-0

Error from server (BadRequest): container "activemq-artemis" in pod "amq-artemis-0" is waiting to start: PodInitializing
...
...
...


    / \  ____| |_  ___ __  __(_) _____
   / _ \|  _ \ __|/ _ \  \/  | |/  __/
  / ___ \ | \/ |_/  __/ |\/| | |\___ \
 /_/   \_\|   \__\____|_|  |_|_|/___ /
 Apache ActiveMQ Artemis 2.20.0


2022-01-07 20:36:47,395 INFO  [org.apache.activemq.artemis.integration.bootstrap] AMQ101000: Starting ActiveMQ Artemis Server
2022-01-07 20:36:47,455 INFO  [org.apache.activemq.artemis.core.server] AMQ221000: live Message Broker is starting with configuration Broker Configuration (clustered=true,journalDirectory=data/journal,bindingsDirectory=data/bindings,largeMessagesDirectory=data/large-messages,pagingDirectory=data/paging)
2022-01-07 20:36:47,584 INFO  [org.apache.activemq.artemis.core.server] AMQ221012: Using AIO Journal
2022-01-07 20:36:47,727 INFO  [org.apache.activemq.artemis.core.server] AMQ221057: Global Max Size is being adjusted to 1/2 of the JVM max size (-Xmx). being defined as 67,108,864
2022-01-07 20:36:48,233 INFO  [org.jgroups.protocols.kubernetes.KUBE_PING] namespace [default] set; clustering enabled
2022-01-07 20:36:48,289 INFO  [org.jgroups.protocols.kubernetes.KUBE_PING] Starting UndertowServer on port 8888 for channel address: amq-artemis-0-44731
2022-01-07 20:36:48,317 INFO  [org.xnio] XNIO version 3.3.4.Final
2022-01-07 20:36:48,348 INFO  [org.xnio.nio] XNIO NIO Implementation Version 3.3.4.Final
WARNING: An illegal reflective access operation has occurred
WARNING: Illegal reflective access by org.xnio.nio.NioXnio$2 (file:/opt/apache-artemis-2.20.0/lib/xnio-nio-3.3.4.Final.jar) to constructor sun.nio.ch.EPollSelectorProvider()
WARNING: Please consider reporting this to the maintainers of org.xnio.nio.NioXnio$2
WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations
WARNING: All illegal access operations will be denied in a future release
2022-01-07 20:36:48,478 INFO  [org.jgroups.protocols.kubernetes.KUBE_PING] UndertowServer started.

-------------------------------------------------------------------
GMS: address=amq-artemis-0-44731, cluster=activemq_broadcast_channel, physical address=172.17.0.5:7800
-------------------------------------------------------------------
2022-01-07 20:36:52,057 WARNING [org.jgroups.protocols.kubernetes.KUBE_PING] Problem getting Pod json from Kubernetes Client[masterUrl=https://10.96.0.1:443/api/v1, headers={}, connectTimeout=5000, readTimeout=30000, operationAttempts=3, operationSleep=1000, streamProvider=org.openshift.ping.common.stream.TokenStreamProvider@21f459fc] for cluster [activemq_broadcast_channel], namespace [default], labels [app.kubernetes.io/instance=amq,app.kubernetes.io/name=artemis]; encountered [java.lang.Exception: 3 attempt(s) with a 1000ms sleep to execute [OpenStream] failed. Last failure was [javax.net.ssl.SSLHandshakeException: extension (5) should not be presented in certificate_request]]

```

## Get external port


The EXTERNAL-IP for amq-artemis is the port to utilize in the browser to access the management console (i.e. 10.105.1.11)

NOTE: The IP will change on redeployment, so you may have to run again to get a new IP.

```bash
kubectl get svc
NAME          TYPE           CLUSTER-IP    EXTERNAL-IP   PORT(S)                                                                                       AGE
amq-artemis   LoadBalancer   10.105.1.11   10.105.1.11   8161:32544/TCP,61616:31604/TCP,5672:32594/TCP,61613:30819/TCP,1883:30507/TCP,9404:30172/TCP   27s
kubernetes    ClusterIP      10.96.0.1     <none>        443/TCP

```


# Login to Management Console

In a browser, got to http://10.105.1.11:8161/console/auth/login

Username: artemis
Password: artemis


# Testing AMQ

Update the host to 10.105.1.11 in helm/test/test.py


Create a python virtual environment and install stomp.py

```bash
cd ~/virtualenv
which python3
virtualenv -p /usr/bin/python3 env
source ~/virtualenv/env/bin/activate
pip install stomp.py

```

Run the test script

```bash
cd helm/test
./test.py 
connecting
connecting
received a message "{cmd=MESSAGE,headers=[{'subscription': '1', 'content-length': '14', 'message-id': '21', 'destination': '/queue/test', 'expires': '0', 'redelivered': 'false', 'priority': '4', 'persistent': 'false', 'timestamp': '1641588257144', 'content-type': 'text/blah', 'receipt': '123'}],body=this is a test}"
```



# Logging in to pod

If you want/need to login to the pod

```bash
kubectl exec --stdin --tty amq-artemis-0 -- /bin/bash
```


# Uninstall helm chart

```bash
helm uninstall amq
```
&nbsp;
&nbsp;
&nbsp;
&nbsp;
&nbsp;
# Example 2 - Deploy helm 

## Update values


Update the repository and tag

```bash
image:
## repository and image tag are required
  repository: <dockerhub username>/activemq-artemis
  tag: 2.20-latest
```

## Deploy the helm chart

```bash

cd helm/charts/artemis
helm install amq -f values.yaml . 

NAME: amq
LAST DEPLOYED: Fri Jan  7 14:36:31 2022
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

## View helm logs

```bash
kubectl logs amq-activemq-artemis-master-0

Error from server (BadRequest): container "activemq-artemis" in pod "amq-artemis-0" is waiting to start: PodInitializing
...
...
...


    / \  ____| |_  ___ __  __(_) _____
   / _ \|  _ \ __|/ _ \  \/  | |/  __/
  / ___ \ | \/ |_/  __/ |\/| | |\___ \
 /_/   \_\|   \__\____|_|  |_|_|/___ /
 Apache ActiveMQ Artemis 2.20.0


2022-01-07 20:36:47,395 INFO  [org.apache.activemq.artemis.integration.bootstrap] AMQ101000: Starting ActiveMQ Artemis Server
2022-01-07 20:36:47,455 INFO  [org.apache.activemq.artemis.core.server] AMQ221000: live Message Broker is starting with configuration Broker Configuration (clustered=true,journalDirectory=data/journal,bindingsDirectory=data/bindings,largeMessagesDirectory=data/large-messages,pagingDirectory=data/paging)
2022-01-07 20:36:47,584 INFO  [org.apache.activemq.artemis.core.server] AMQ221012: Using AIO Journal
2022-01-07 20:36:47,727 INFO  [org.apache.activemq.artemis.core.server] AMQ221057: Global Max Size is being adjusted to 1/2 of the JVM max size (-Xmx). being defined as 67,108,864
2022-01-07 20:36:48,233 INFO  [org.jgroups.protocols.kubernetes.KUBE_PING] namespace [default] set; clustering enabled
2022-01-07 20:36:48,289 INFO  [org.jgroups.protocols.kubernetes.KUBE_PING] Starting UndertowServer on port 8888 for channel address: amq-artemis-0-44731
2022-01-07 20:36:48,317 INFO  [org.xnio] XNIO version 3.3.4.Final
2022-01-07 20:36:48,348 INFO  [org.xnio.nio] XNIO NIO Implementation Version 3.3.4.Final
WARNING: An illegal reflective access operation has occurred
WARNING: Illegal reflective access by org.xnio.nio.NioXnio$2 (file:/opt/apache-artemis-2.20.0/lib/xnio-nio-3.3.4.Final.jar) to constructor sun.nio.ch.EPollSelectorProvider()
WARNING: Please consider reporting this to the maintainers of org.xnio.nio.NioXnio$2
WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations
WARNING: All illegal access operations will be denied in a future release
2022-01-07 20:36:48,478 INFO  [org.jgroups.protocols.kubernetes.KUBE_PING] UndertowServer started.

-------------------------------------------------------------------
GMS: address=amq-artemis-0-44731, cluster=activemq_broadcast_channel, physical address=172.17.0.5:7800
-------------------------------------------------------------------
2022-01-07 20:36:52,057 WARNING [org.jgroups.protocols.kubernetes.KUBE_PING] Problem getting Pod json from Kubernetes Client[masterUrl=https://10.96.0.1:443/api/v1, headers={}, connectTimeout=5000, readTimeout=30000, operationAttempts=3, operationSleep=1000, streamProvider=org.openshift.ping.common.stream.TokenStreamProvider@21f459fc] for cluster [activemq_broadcast_channel], namespace [default], labels [app.kubernetes.io/instance=amq,app.kubernetes.io/name=artemis]; encountered [java.lang.Exception: 3 attempt(s) with a 1000ms sleep to execute [OpenStream] failed. Last failure was [javax.net.ssl.SSLHandshakeException: extension (5) should not be presented in certificate_request]]

```

## Get external port


The EXTERNAL-IP for amq-artemis is the port to utilize in the browser to access the management console (i.e. 10.105.1.11)

NOTE: The IP will change on redeployment, so you may have to run again to get a new IP.

```bash
NAME                          TYPE           CLUSTER-IP     EXTERNAL-IP    PORT(S)                                         AGE
amq-activemq-artemis          LoadBalancer   10.105.1.11   10.96.47.204   8161:32116/TCP,61616:30156/TCP,5672:32540/TCP   5m58s
amq-activemq-artemis-master   ClusterIP      None           <none>         8161/TCP,61616/TCP,5672/TCP,9494/TCP            5m58s
amq-activemq-artemis-slave    ClusterIP      None           <none>         8161/TCP,61616/TCP,5672/TCP,9494/TCP            5m58s
kubernetes                    ClusterIP      10.96.0.1      <none>         443/TCP                                         3d21h
```


# Login to Management Console

In a browser, got to http://10.105.1.11:8161/console/auth/login

Username: artemis
Password: artemis


# Testing AMQ

Update the host to 10.105.1.11 in helm/test/test.py


Create a python virtual environment and install stomp.py

```bash
cd ~/virtualenv
which python3
virtualenv -p /usr/bin/python3 env
source ~/virtualenv/env/bin/activate
pip install stomp.py

```

Run the test script

```bash
cd helm/test
./test.py 
connecting
connecting
received a message "{cmd=MESSAGE,headers=[{'subscription': '1', 'content-length': '14', 'message-id': '21', 'destination': '/queue/test', 'expires': '0', 'redelivered': 'false', 'priority': '4', 'persistent': 'false', 'timestamp': '1641588257144', 'content-type': 'text/blah', 'receipt': '123'}],body=this is a test}"
```



# Logging in to pod

If you want/need to login to the pod

```bash
kubectl exec --stdin --tty amq-artemis-0 -- /bin/bash
```


# Uninstall helm chart

```bash
helm uninstall amq
```





