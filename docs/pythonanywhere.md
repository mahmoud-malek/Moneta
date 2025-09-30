# Deploying Moneta on PythonAnywhere

This guide walks through setting up the Moneta Flask application on [PythonAnywhere](https://www.pythonanywhere.com/). It assumes you already have a PythonAnywhere account on the **Beginner** plan or higher.

## 1. Prepare your account

1. Log in to PythonAnywhere.
2. Note your username – you will use it when configuring the MySQL database and WSGI paths.

## 2. Create the MySQL database

1. Open the **Databases** tab and click **Create a new MySQL database**.
2. PythonAnywhere will provision a database named `username$default` (you can add more databases if your plan allows).
3. Copy the credentials and hostname – PythonAnywhere uses the form `username.mysql.pythonanywhere-services.com`.

## 3. Start a Bash console and pull the project

1. Open a **Bash** console from the **Consoles** tab.
2. Clone the project (or pull your fork):

   ```bash
   git clone https://github.com/<your-user>/Moneta.git ~/Moneta
   ```

3. Change into the project directory:

   ```bash
   cd ~/Moneta
   ```

## 4. Create and activate a virtual environment

PythonAnywhere strongly recommends using a virtual environment per web app.

```bash
python3.10 -m venv ~/.virtualenvs/moneta
source ~/.virtualenvs/moneta/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

> **Tip:** PythonAnywhere does not allow system-level package installs. Using `PyMySQL` (already listed in `requirements.txt`) avoids the need to compile native MySQL drivers.

## 5. Configure environment variables

In the PythonAnywhere **Web** tab, scroll to the **Environment Variables** section and add the following entries:

| Key                   | Value                                                                                                                           |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `MONETA_DATABASE_URL` | `mysql+pymysql://username:password@username.mysql.pythonanywhere-services.com/username$default` (replace with your credentials) |
| `SECRET_KEY`          | A long random string                                                                                                            |
| `FLASK_ENV`           | `production`                                                                                                                    |
| `PYTHONPATH`          | `/home/<username>/Moneta` (optional but keeps imports explicit)                                                                 |

If you prefer, you can create a `.env` file and load it manually inside `passenger_wsgi.py`, but the Web UI variables are easier to maintain.

## 6. Configure the WSGI entry point

1. In the **Web** tab, create a new **Manual configuration** web app using **Python 3.10** (or the version that matches your virtual environment).
2. Click the link to edit the WSGI configuration file (typically `/var/www/<username>_pythonanywhere_com_wsgi.py`).
3. Replace its contents with something like the template provided in `deploy/pythonanywhere/passenger_wsgi.py`:

   ```python
   import os
   import sys
   from pathlib import Path

   PROJECT_ROOT = Path(os.path.expanduser("~/Moneta"))
   if str(PROJECT_ROOT) not in sys.path:
      sys.path.insert(0, str(PROJECT_ROOT))

   os.environ.setdefault("MONETA_DATABASE_URL", "mysql+pymysql://username:password@username.mysql.pythonanywhere-services.com/username$default")
   os.environ.setdefault("SECRET_KEY", "change-me")
   os.environ.setdefault("FLASK_ENV", "production")

   from wsgi import application
   ```

4. Save the file.

## 7. Point the web app to the virtual environment

Still in the **Web** tab:

- Set **Virtualenv** to `/home/<username>/.virtualenvs/moneta`.
- Set **Source code** to `/home/<username>/Moneta`.
- Ensure **Working directory** is the project root.

## 8. Initialize the database schema

The SQLAlchemy metadata creates tables automatically when the app first imports `models.storage`. If you want to confirm manually:

```bash
source ~/.virtualenvs/moneta/bin/activate
cd ~/Moneta
python - <<'PY'
from models import storage
print("Database tables ensured.")
PY
```

## 9. Reload the web app

Click the **Reload** button at the top of the **Web** tab. Visit your new site – it should load the Moneta dashboard.

## 10. Optional: schedule tasks or seed data

- Use the **Tasks** tab for scheduled jobs.
- To seed data, run scripts via Bash console or PythonAnywhere **IPython** consoles using the same virtual environment.

## Troubleshooting checklist

- **ImportError / ModuleNotFoundError**: Verify the project path and virtualenv paths are added to `sys.path` in the WSGI file.
- **Database connection errors**: Check that `MONETA_DATABASE_URL` uses the correct username, password, and hostname. Remember that PythonAnywhere restricts external MySQL connections – use their internal hostname.
- **403/500 errors**: View the server logs at `/var/log/<app_name>.error.log` and `/var/log/<app_name>.server.log` via the **Logs** section.
- **Static assets missing**: Flask serves `/web/static` automatically. Ensure the `static` folder resides inside `web/` and you are not using `STATIC_URL_PATH` overrides.

With these steps, Moneta should run smoothly on PythonAnywhere. Need help with a specific step? Open the project’s issue tracker or ping the support team.
