**#ByteGenie Full-stack Challenge**


**Project Overview**

In this project, I've crafted two of the features listed on the original challenge document: document summarization and document question answering.

**Quick Links to Other readme files**
- API readme: [api/README.md](api/README.md)
- Client readme: [client/README.md](client/README.md)

**Running the Application with Docker**

**Prerequisites:**

- Docker ([https://www.docker.com/get-started](https://www.docker.com/get-started))
- Docker Compose ([https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/))

**File Structure:**

- `api/`: Python project
- `client/`: React project
- `docker-compose.yml`: Docker Compose configuration file

**Steps:**

1. **Navigate to the project root directory:**

   ```bash
   cd /path/to/project
   ```

2. **Build the Docker images:**

   ```bash
   docker-compose build
   ```

3. **Start the containers:**

   ```bash
   docker-compose up
   ```

**Accessing the Application:**

- **API:** 
   - Open http://127.0.0.1:5001/
- **Client:** 
   - Open http://127.0.0.1:3000/

**Additional Notes:**

- **Stopping the Containers:**
   ```bash
   docker-compose down
   ```
- **Rebuilding Images:**
   ```bash
   docker-compose build
   ```
- **Viewing Container Logs:**
   ```bash
   docker-compose logs
   ```
- **Customizing Ports and Environment Variables:**
   - Modify the `docker-compose.yml` file for any port or environment variable adjustments.
