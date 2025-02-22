# ETL Energy Consumption Project 

## Overview 
This project implements a simple ETL (Extract, Transform, Load) pipeline using the following technologies:

- **Python**: For data extraction, transformation, and loading.
- **Docker**: To containerize PostgreSQL and the ETL script.
- **PostgreSQL**: As the database to store transformed data.

### Project Structure
```
├── data               # Contains downloaded datasets from Kaggle
├── etl                # Python scripts for ETL process
├── Dockerfile         # Docker configuration for ETL script
├── docker-compose.yml # Docker Compose file for PostgreSQL and PgAdmin
└── README.md          # Project documentation
```

## ETL Process

### 1. Extract
- Extract data from CSV files using `pandas`.
- Load CSV data into a DataFrame.

### 2. Transform
- Remove unnecessary columns (`Continent`, `Country`, and the last column only).
- Handle missing values using `.dropna()`.
- Round float values in the last column to two decimal places.
- Replace the old column with the transformed values.

### 3. Load
- Load transformed data into PostgreSQL.
- Use `psycopg2` for database connectivity.
- Implement command-line arguments using `argparse` for flexible execution.

## Setup Instructions

### Prerequisites
Ensure you have the following installed:
- **Docker**
- **Python 3.x**
- **pgcli** (Optional, for PostgreSQL command-line interaction)

### 1. Clone the Repository
```sh
$ git clone https://github.com/your-repo-name.git
$ cd etl-energy-consumption
```

### 2. Create a Docker Volume
```sh
$ docker volume create etl_energy_consumption
```

### 3. Pull PostgreSQL and PgAdmin Images
```sh
$ docker pull postgres
$ docker pull dpage/pgadmin4
```

### 4. Create a Docker Network
```sh
$ docker network create energy_consumption_network
```

### 5. Run Docker Compose
```sh
$ docker-compose up -d
```

### 6. Build the ETL Docker Image
```sh
$ docker build -t python-etl .
```

### 7. Run the ETL Process
```sh
$ docker run -it --network=energy_consumption_network \
    python-etl \
    -f /data/Energy_Statistics/Consumption_Data/Consumption_Coal.csv \
    -db energy_consumption \
    -hs pgdatabase \
    -u postgres \
    -pass 123456 \
    -p 5432
```

### 8. Verify Data in PostgreSQL
Install `pgcli` (if not installed):
```sh
$ pip install pgcli
```
Access PostgreSQL:
```sh
$ pgcli -h localhost -p 5432 -u postgres -d energy_consumption
```

## Note
- When connecting Docker containers via a network, use the container name instead of `localhost`.
- To find the container IP, run:
  ```sh
  $ docker network inspect energy_consumption_network
  ```

## Conclusion
This ETL project automates the extraction, transformation, and loading of global energy consumption data into a PostgreSQL database using Docker. The modular design allows for easy scalability and modifications.

