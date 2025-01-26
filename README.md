# fastapi-orchestrator
A basic implementation of Python's FastAPI handling external services and local storage to serve a web client through HTTP requests.
# 1. Setup and Run
Required Python Version: 3.10.12
<br><br>
Use the start script (*run_orchestrator.sh*) to setup the environment and and run the server.
<br><br>
Or, run the orchestrator dockerised with the extended script (*run_orchestrator_dockerised.sh*).
<br><br>
Alternatively, you can setup and run manually using the following instructions.

## 1.1. Activate Virtial Environment
Run the following command in the projects root dir to setup the virtual enviroment:\
`. .venv/bin/activate`

## 1.2. Run the Orchestrator
Run the following command to run the fastapi server in development mode:\
`fastapi dev orchestrator.py`

Or use the following for production:\
`fastapi run orchestrator.py`

## 1.3. Stop the Orchestrator
Use `Ctrl + C` in the terminal you used to run to stop the server.
<br><br>
Alternatively, kill the process with the following:\
`ps aux | grep uvicorn`\
`kill -9 <PID>`

## 1.4. Orchestrator Documentation
When the Orchestrator is live in dev mode, you can read the auto generated fastapi documentation at: http://127.0.0.1:8000/docs

# 2. Testing the Orchestrator
Use the following example curl commands to test the endpoints.

## 2.1. Distance
`curl "http://127.0.0.1:8000/distance?origin_lat=52.954&origin_long=1.1550&dest_lat=51.4545&dest_lon=2.5879"`

## 2.2. Weather
`curl "http://127.0.0.1:8000/weather?lat=52.9540&lon=1.1550"`

# 3. Linting
When developing, use the flake script to run flake8 on your code.