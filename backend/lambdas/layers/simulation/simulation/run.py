import json
from dotenv import load_dotenv
import sys
from run_simulation import run_simulation_with_env
from simulation.business import BusinessInput

load_dotenv()
print(run_simulation_with_env(BusinessInput(**json.loads(sys.argv[1]))).dumps())

exit(0)
