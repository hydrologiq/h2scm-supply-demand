import json
from dotenv import load_dotenv
import sys
from api_run_simulation.run_simulation import run_simulation_with_env
from api_run_simulation.simulation.business import BusinessInput

load_dotenv()
print(run_simulation_with_env(BusinessInput(**json.loads(sys.argv[1]))).dumps())

exit(0)
