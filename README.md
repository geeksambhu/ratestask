# Flask API with Docker Compose

To run the Flask API with Docker Compose, follow these steps:

Clone the repository:
```bash
git clone https://github.com/geeksambhu/ratestask.git
```
Navigate to the project directory:

```bash
cd ratestask
```
Build the Docker images:

```bash
docker-compose build
```

Start the containers:

```bash
docker-compose up
```

This will start the Flask API in a Docker container, listening on port 1300.

To test the API, you can send a GET request to the following URL:

http://localhost:1300/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main

This should return a list of average prices for each day on a route between port codes origin and destination. The date_from and date_to parameters specify the date range for the prices.

Finally,to stop the containers, use the following command:

```bash
docker-compose down
```




