# backend_basic_2021

### lb with failover

```
sudo docker build -t flask-application:latest .
sudo docker run -d -e APPNAME=app1 -p 18000:5000 flask-application
sudo docker run -d -e APPNAME=app2 -p 18001:5000 flask-application
```
