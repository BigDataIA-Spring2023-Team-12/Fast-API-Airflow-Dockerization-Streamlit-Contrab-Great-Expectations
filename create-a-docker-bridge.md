To create a bridge network between two Docker containers running on the same EC2 instance, you can follow these steps:

1. Create a bridge network using the docker network create command:\
```
$ docker network create my-bridge-network
```

2. Start the first container and attach it to the bridge network: \
```
$ docker run -d --name container1 --network my-bridge-network my-image1
```

3. Start the second container and attach it to the same bridge network: \
```
$ docker run -d --name container2 --network my-bridge-network my-image2
```

4. Create a shared volume that both containers can access: \
```
$ docker volume create my-shared-volume
```

5. Mount the shared volume in both containers using the -v option: \
```
$ docker run -d --name container1 --network my-bridge-network -v my-shared-volume:/shared-data my-image1
$ docker run -d --name container2 --network my-bridge-network -v my-shared-volume:/shared-data my-image2
```

6. Now both containers can access the shared file at  `/shared-data`

Note: The above steps assume that you have already created and configured your EC2 instance to run Docker. If you haven't done so already, you will need to install Docker on your EC2 instance before proceeding.
