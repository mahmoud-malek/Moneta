"""Example Passenger WSGI entry point for PythonAnywhere deployments.

Copy this file to your PythonAnywhere project (for example to
`/var/www/<username>_pythonanywhere_com_wsgi.py`) and adjust the paths and
environment variables as needed.
"""

import os
import sys
from pathlib import Path

# Absolute path to the Moneta project directory on PythonAnywhere.
PROJECT_ROOT = Path(os.path.expanduser("~/Moneta"))

# Ensure the project root is on the Python path.
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Optionally point to a virtual environment (uncomment and update the path).
# VENV_PATH = Path(os.path.expanduser("~/.virtualenvs/moneta"))
# if str(VENV_PATH / "lib/python3.10/site-packages") not in sys.path:
#     sys.path.insert(0, str(VENV_PATH / "lib/python3.10/site-packages"))

# Default environment variables. Override them in the PythonAnywhere Web UI
# for production secrets.
os.environ.setdefault("MONETA_DATABASE_URL", "mysql+pymysql://<username>:<password>@<host>/<dbname>")
os.environ.setdefault("SECRET_KEY", "change-me")
os.environ.setdefault("FLASK_ENV", "production")

# Import the Flask application from the Moneta wsgi module.
from wsgi import application  # noqa: E402  # pylint: disable=wrong-import-position
