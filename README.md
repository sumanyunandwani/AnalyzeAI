# AnalyzeAI Backend

This repository contains the backend codebase for AnalyzeAI, structured as three independent microservices:

- `user_service`
- `bdoc_generator_sql_service`
- `payment_service`

Each service is containerized using Docker and includes its own infrastructure setup for local development.

---

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) installed and running on your local machine.

---

## Project Structure

```
/AnalyzeAI/
│
├── user_service/
│   └── ... (service code)
│
├── bdoc_generator_sql_service/
│   └── ... (service code)
│
├── payment_service/
│   └── ... (service code)
│
└── infrastructure/
    ├── user_service/
    │   ├── Dockerfile
    │   └── docker-compose.yml
    ├── bdoc_generator_sql_service/
    │   ├── Dockerfile
    │   └── docker-compose.yml
    └── payment_service/
        ├── Dockerfile
        └── docker-compose.yml
```

---

## Running a Microservice Locally

Each microservice can be built and run independently. Follow these steps for any service (replace `user_service` with the desired service name):

1. **Navigate to the Service Directory**

   ```sh
   cd <service_name>
   # Example:
   cd user_service
   ```

2. **Build the Docker Image**

   ```sh
   docker build -f ..\..\infrastructure\<service_name>\Dockerfile -t <service_name>_app .
   # Example:
   docker build -f ..\..\infrastructure\user_service\Dockerfile -t user_service_app .
   ```

3. **Start the Service and Database**

   ```sh
   docker-compose.exe -f ..\..\infrastructure\<service_name>\docker-compose.yml up -d
   # Example:
   docker-compose.exe -f ..\..\infrastructure\user_service\docker-compose.yml up -d
   ```

   This will start the service and its associated database in detached mode.

---

## Stopping a Microservice

To stop and remove the containers:

```sh
docker-compose.exe -f ..\..\infrastructure\<service_name>\docker-compose.yml down
```

---

## Notes

- Each microservice is isolated and can be developed, built, and run independently.
- All infrastructure code (Dockerfile, docker-compose.yml) is located in the `infrastructure/<service_name>/` directory.
- Ensure Docker is running before executing the above commands.

---

## Troubleshooting

- If you encounter port conflicts, update the `docker-compose.yml` file for the respective service.
- For logs, use `docker logs <container_id>`.

---

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes.

---

## License

This project is licensed under the MIT License.
