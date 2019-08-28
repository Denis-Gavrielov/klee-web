Debugging Dockerized Services 
==========
TODO: 
* debugging Docker containers
	* restarting containers, rerunning everything etc. 
	* viewing logs
* deleting and restarting the database 
* How to update to new versions (of redis e.g., or the Python versions, ...)
* networking

Working with Docker has advantages of isolating dependencies in containers and being able to quickly replicate services. However, it does also come with a new workflow. The Ansible provisioning rules take care of starting up all the services, but if you want to debug services or change functionalities it is good to go over the following commands.

## Building Images
Docker images are either pulled from the [Docker Hub](https://docs.docker.com/docker-hub/) or built with a Dockerfile as a configuration the configuration. Currently, all the images, with the exception of the redis service, are being built during provisioning. 

If you want to change some installations of an existing image you should first look into modifying the relevant Dockerfile. The Dockerfiles are placed in the relevant folders. For example, the Dockerfile for the Worker service is placed in the `src/worker` folder. 

To extend the application by building a new service you would either have to find a Docker image from the Docker Hub or create a custom one by writing a new Dockerfile. [This is a good place to start for documentation](https://docs.docker.com/engine/reference/builder/).

## Volumes

### Bind Mounts 

Bind Mount volumes are used to mount folders between a Docker Host and a running Docker Container. For example, the Worker container needs to access its source code to run. It also needs to be able to launch new Docker containers. 

See the file `provisioning/roles/worker/tasks/deploy.yml` as an example:

```yml
- name: Start docker Worker
  docker_container:
    name: "worker-{{ item }}"
    image: celery_worker
    restart_policy: always
    volumes: 
    # can start other containers:
    - /var/run/docker.sock:/var/run/docker.sock
    # can place results into /tmp/ folder
    - /tmp/:/tmp/
    # connect source code paths 
    - "{{ klee_env_path_etc }}:{{ klee_env_path_etc }}"
    - "{{ python_runner }}:{{ python_runner }}"
    - "{{ worker_dir }}:{{ worker_dir }}"
    network_mode: "{{ 'host' if (ci) else 'bridge' }}"
    recreate: yes
  with_sequence: start=1 end=2
```

To connect the source code, the `worker_dir` is connected between the Docker Host and the running container. This is an Ansible variable which is expanded to the file path `/titb/src/worker`, the file path to the source code of the worker within the Worker VM. 

By connecting to the Docker socket (`docker.sock`), the Worker container can issue commands to the Docker daemon to launch new containers. 

### Volumes
Volumes, in contrast to Bind Mounts, are used to e.g. persist storage of a container. The PostgreSQL container needs to persist the storage of the user logins. 

A volume is created as part of the Ansible `provisioning/roles/db/tasks/build.yml` file:

```yml
- name: Create postgres volume
  docker_volume:
    name: postgres_data
```

This creates the volume when it does not exist, but Ansible ensures that if the volume exists it is not recreated, which makes it safe to re-run this Ansible task without losing the PostgreSQL data.

When the container is started this volume is attached to the starting container. `provisioning/roles/db/tasks/deploy.yml`:

```yml
- name: Run Docker postgres container
  docker_container:
    name: postgres_container
    image: klee_postgres
    restart_policy: always
    env:
      POSTGRES_PASSWORD: "{{ db_password }}"
      POSTGRES_USER: "{{ db_user }}"
      POSTGRES_DB: "{{ db_name }}"
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    networks:
      - name: "{{ container_network }}"
    recreate: yes
```

To inspect all the volumes on a machine run

	$ sudo docker volume ls

## Starting and Restarting Containers
Talk about restarting the database and what it means 

Above you can find examples on how containers are started by Ansible. Running a container can accept multiple optional flags which are [documented here](https://docs.docker.com/engine/reference/run/) and for the Ansible documentation see [this resource](https://docs.ansible.com/ansible/latest/modules/docker_container_module.html).

The Ansible provisioning rules are configured such that whenever the application is provisioned, all the running containers are restarted. Be aware that the PostgreSQL container will persist its memory, because the volume is not restarted by default. 

However, if you e.g. changed the PostgreSQL user or password and want to start the service fresh without persisting data, you would need to manually delete the volume.

First kill and remove any container that are using the volume. To investigate the current running containers do

	$ sudo docker ps

From the output you can see that the container name for the `klee_postgres` image is `postgres_container`. `klee_postgres` is the custom PostgreSQL image that was built for the Klee-Web application. Now to stop and remove the running container do

	$ sudo docker container kill postgres_container
	$ sudo docker container rm postgres_container

Now the volume can also be removed with 

	$ sudo docker volume rm postgres_data

You need to provision the Master VM again to reload the volume and restart the PostgreSQL container. 

## Inspecting a container
In general, you can see the volumes, network configurations and other information about a running Docker container with the command 

	$ sudo docker inspect <container name>


## Networking

When working with Docker containers you can create private networks between the containers which isolate the communication between different services and only expose ports which really need to be exposed.

For example, a Docker network is created with the following Ansible task

```yml
- name: Create docker network {{ container_network }}
  docker_network:
    name: "{{ container_network }}"
    ipam_config:
      - subnet: "{{ network_subnet }}"
        gateway: "{{ network_gateway }}"
```

Again, variables are used to keep the code base [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself). On container startup this network can be joined. Containers within this network can reach another on any port, while any service outside this network can only reach containers which have opened a specific port. For example, in the `provisioning/roles/web/tasks/nginx_deploy.yml` file you can see that the port 80 is being forwarded from the Docker Host to port 80 on the NGINX container. 

```yml
---
- name: Run Docker nginx container
  docker_container:
    name: nginx_container
    image: nginx_image
    restart_policy: always
    networks:
      - name: "{{ container_network }}"
    ports: 
      - "80:80"
    volumes:
      - /tmp:/tmp
      - /titb:/titb
    recreate: yes
```

You can also see that this container is joining the private network, so the Django container can communicate with the NGINX container, whiel the Django container does not need to expose any ports publically. 

To see which networks are currently available run

	$ sudo docker network ls

Now, to inspect a specific network run

	$ sudo docker network inspect <network-name>

This will provide information such as all the containers that have joined this network, and their assigned internal IP address. Note that containers within one network do not need to communicate with each other via their IP address, but can do so via their container name; this is convenient, because the IP address is allocated dynamically, while the container name is defined in Ansible on startup of the container.

There are also convenient commands to find the dynamically allocated IP address at run time. This can be useful if a container needs to be addressed directly from the Docker Host from outside the Docker network.

For example, with 

	$ sudo docker inspect nginx_container

information about the NGINX container is exposed in a format similar to nested Python dictionaries. After inspecting the structure of this nested dictionaries, you could return the IP address of the container within the private netwrok with the following command

	$ sudo docker inspect -f "{{ .NetworkSettings.Networks.web_network.IPAddress }}" nginx_container


## Logs
restarting the container with a different log level.

Inspecting logs in Docker containers is standardised. With the command 

	$ sudo docker logs <container name> 

you can inspect the logs. In Docker standard output and standard error are merged. You can also follow the logging output with 

	$ sudo docker logs <container name> -f

Sometimes, when debugging in the development stage, you might want to change the log level for services from `WARNING` to `DEBUG`. For that every Docker container will need to be approached individually, but usually you will need to restart the container with different settings or with a different command.

For example, the Dockerfile of the Worker image has the following command: 

```docker
CMD /src/python_runner.sh celery -A worker.worker worker
```

To change logging at `DEBUG` level for this service change this command to 

```docker
CMD /src/python_runner.sh celery -l DEBUG -A worker.worker worker
```

Now you need to rebuild the image and restart the container. Simply provisioning again in Ansible will do these steps.

## Updates of Dependencies
how to look for updated versions. -> say can think about an extension to the project.

Looking for updates of any dependencies is currently a manual process. These dependencies could either be a base image, e.g. the values to the right of a `FROM` command in the Dockerfile:

```docker
FROM postgres:11-alpine
```

The dependencies could also be for example Python libraries from the requirements.txt files. For example, the Worker image has the following requirements in the `src/worker/requirements.txt` file:

```python
celery==4.3.*
boto==2.49.*
requests==2.22.*
redis==3.2.*
fakeredis==1.0.*
gcovparse==0.0.*
```

Minor versions are updated automatically, but for that to happen you would need to rebuild the image and restart the worker, which happens automatically every time you provision with Ansible. Equally, in the example above the minor version of the postgres base image are updated automatically, but only when the image is built again.

A possible extension to this application would be to create a scanner for all the dependencies which alerts the maintainer of the project once major updates are released.
