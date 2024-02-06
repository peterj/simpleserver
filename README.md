# How to preserve case of header names in Envoy?

- [Background on the header casing options in Envoy](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_conn_man/header_casing)


Note that using httpbin or other tools to test the headers will not work as expected, as they will normalize the headers to lowercase.

## Building the test application

The `simpleserver` is Python server, listening on port 8080 and when called, returns the list of headers it received, without any normalization.

After you've forked the repository, you can build the image using the provided `Dockerfile`:

```shell
docker build -t simpleserver:0.1.0 .
```

## Running in Kubernetes

This example assumes you had kind cluster with Istio installed. You'll be using `sleep` deployment as the client and `simpleserver` as the server.


```shell
# Load the image to the kind cluster
kind load docker-image simpleserver:0.1.0
```

Deploy the `simpleserver`:

```shell
kubectl apply -f simpleserver.yaml
```

## Testing 

1. Test the header casing without the Envoy filter:

```shell
kubectl exec -it deploy/sleep -- curl -H "helloWorld: 123" simpleserver:8080
```

2. Check the logs of the `simpleserver`:

```shell
kubectl logs deploy/simpleserver
```

```console
--------HEADERS--------
host: simpleserver:8080
user-agent: curl/8.6.0
accept: */*
helloworld: 123
x-forwarded-proto: http
x-request-id: 874f6526-ed5a-95bb-9d7d-0c12be213e73
x-envoy-attempt-count: 1
x-forwarded-client-cert: By=spiffe://cluster.local/ns/default/sa/default;Hash=6a6d95d31f856f191364f585966b64c58116e4e78a9e4eb01283a98f40423199;Subject="";URI=spiffe://cluster.local/ns/default/sa/sleep
x-b3-traceid: c9da4c8c3f050819f1a594ecb6dc1aa7
x-b3-spanid: 9c29316b41195aba
x-b3-parentspanid: f1a594ecb6dc1aa7
x-b3-sampled: 1
-----------------------
```

Notice the `helloworld` header is normalized (all lower-case).


3. Deploy the Envoy filter:

```shell
kubectl apply -f envoyfilter.yaml
```

4. Repeat the same request as before:


```shell
kubectl logs deploy/simpleserver
```

```console
--------HEADERS--------
Host: simpleserver:8080
User-Agent: curl/8.6.0
Accept: */*
helloWorld: 123
x-forwarded-proto: http
x-request-id: 94d6e011-df75-9465-bfee-aa7412945d81
x-envoy-attempt-count: 1
x-forwarded-client-cert: By=spiffe://cluster.local/ns/default/sa/default;Hash=6a6d95d31f856f191364f585966b64c58116e4e78a9e4eb01283a98f40423199;Subject="";URI=spiffe://cluster.local/ns/default/sa/sleep
x-b3-traceid: 46d42cc4d99c7966a77a0ab07c77f4a8
x-b3-spanid: a3cfe566ed75a955
x-b3-parentspanid: a77a0ab07c77f4a8
x-b3-sampled: 1
-----------------------
```

Notice this time the `helloWorld` header is preserved as it was sent by the client.
