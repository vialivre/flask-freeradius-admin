# flask-freeradius-admin

Flask-FreeRadius-Admin is a visual editor for the FreeRadius server tables. You can use to visualize the FreeRadius authentication flow and edit users, groups and NAS data.

![Users screen](images/users.png)  
![Groups screen](images/groups.png)  
![NAS screnn](images/nas.png)  

## Installing

Flask-FreeRadius-Admin comes with a *Docker Compose* file to configure your FreeRadius server to use the SQL module, a Postgres database, and the Flask app. If you already have a FreeRadius server with SQL configured, feel free to use only the `flask_app` directory and follow the Dockerfile installation instructions to build it in your machine. You may need to check the `docker-compose.yml` file to set the right environment variables.

1. Install Docker and Docker-Compose
```
apt install docker docker-compose
```

2. Clone the repository
```
git clone https://github.com/juliarizza/flask-freeradius-admin.git
```

3. Enter the project
```
cd flask-freeradius-admin
```

4. Run Docker-Compose
```
docker-compose up -d
```

If you want to check the container logs, get the container ID using `ps`:
```
docker ps
docker logs {container_id}
```

If you want to access either the database or the freeradius shell:
```
docker ps
docker exec -it {container_id} /bin/bash
```

If you want to access the application shell:
```
docker ps
docker exec -it {container_id} /bin/sh
```

# License

Now under MIT license. Have fun :)