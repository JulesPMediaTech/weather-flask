weather-flask
=============

This project is a learning experiment in: 
- Python web gui development using Flask
- Docker containerisation

** Note that, for the time being, the web gui runs wuth Flask's own developement server in debug mode **

VS

About the app
-------------
This is a simple web gui app that takes a place name, converts it to coordinates and provides hourly temperature readings for a week from the start of the day it is requested.

Uses geopy and openmeteo dependencies: <br>
https://pypi.org/project/geopy/ <br>
https://pypi.org/project/openmeteo-requests/ <br>
https://pypi.org/project/openmeteo-sdk/

(see also requirements.txt file)

## Development with VS Code Dev Container

### Prerequisites
- [Docker](https://www.docker.com/products/docker-desktop) installed and running.
- [Visual Studio Code](https://code.visualstudio.com/) with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

### Getting Started
1. **Clone the repository:**
   ```bash
   git clone https://github.com/JulesPMediaTech/weather-flask.git
   cd weather-flask
   ```
2. **Open the project in VS Code.**
3. **Reopen in Dev Container:**
   - Press `F1` (or `Ctrl+Shift+P`) and select `Dev Containers: Reopen in Container`.
   - VS Code will build the container and open the workspace inside it.
4. **All dependencies are installed automatically.**
   - No need to create a local virtual environment.
   - All development, testing, and debugging should be done inside the container.

### Useful Commands
- **Run the app:**
  ```bash
  python server.py
  ```
- **Run tests:**
  ```bash
  pytest
  ```
- **Install new Python packages:**
  ```bash
  pip install <package>
  # Then add to app/requirements.txt
  ```

### Notes
- The Dev Container automatically installs recommended VS Code extensions (Python, Jupyter, etc.).
- If you want to add more extensions, edit `.devcontainer/devcontainer.json`.
- For production, use Docker Compose as described below.

## Running with Docker Compose

You can run the app in a containerized environment using Docker Compose.

### Build and Run
```bash
docker compose build --no-cache
docker compose up -d
```
- The app will be available at [http://localhost:8000](http://localhost:8000)
- To stop and remove containers, networks, etc.:
```bash
docker compose down
```

### Useful Docker Compose Commands
- View logs:
  ```bash
  docker compose logs -f
  ```
- Run a one-off command in the container:
  ```bash
  docker compose exec weather-app python meteo_API_response.py
  ```

## Production Deployment

For production, you should:
- Use a production WSGI server (e.g., Waitress or Gunicorn) in your `CMD` in the Dockerfile.
- Remove or restrict the volume mount in `docker-compose.yml` to avoid mounting your local code.
- Set `FLASK_ENV=production` in your environment variables.
- Expose only necessary ports.

### Example production Docker Compose override
Create a `docker-compose.prod.yml`:
```yaml
services:
  weather-app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=production
    command: ["waitress-serve", "--host=0.0.0.0", "--port=8000", "server:app"]
```

Then run:
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

**Note:**
- Adjust the `command` as needed for your WSGI server and app entry point.
- For cloud deployment, push your image to a registry and deploy using your provider's instructions.




