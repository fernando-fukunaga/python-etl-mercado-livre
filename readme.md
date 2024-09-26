# ETL Mercado Livre
This is an ETL application that works with the Mercado Livre website. Mercado Livre is the Brazilian subsidiary of the Argentine e-commerce Mercado Libre.

The application will consume the website searching for the product prompted by the user, with filters and stuff. Then, it will transform that data into a JSON response and save it on a MongoDB database, also saving the operation logs on a PostgreSQL instance. There's also gonna be an API developed with FastAPI for consulting the data and logs saved on the databases.

The database instances can be run with Docker, using the docker-compose files on the /docker folder. And then you get to choose if you want to start the ETL app or the API.