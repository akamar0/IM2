# UniFix — Django Account Feature (IM2 Phase 1)

UniFix is a centralized university IT support, equipment maintenance, and equipment borrowing portal proposed for Cebu Institute of Technology – University (CIT-U).

This starter project implements the **Account Feature** required for the first IM2 development phase:

- Account registration with required username, first name, last name, valid email, password confirmation, and optional department/contact details.
- Django's built-in password hashing and authentication.
- Login and POST-based logout.
- Role-based dashboards for University Personnel, IT Support Administrators, IT Technicians, and System Administrators.
- Dashboard access protection using login checks and role checks.
- A profile page and self-service profile editing for the currently logged-in user.
- PostgreSQL database configuration. SQLite is not configured.

The ticket submission, technician workflow, equipment borrowing/return transactions, notifications, maintenance history, and analytics are shown as planned modules only. They are **not implemented in this Account Feature phase**.

## 1. Requirements

- Python 3.10 or later (Python 3.12+ is required if you choose Django 6.x; this project pins Django 5.2.19).
- PostgreSQL 14 or later.
- Visual Studio Code.
- Internet connection for installing Python packages.

## 2. Open the project in VS Code

1. Extract the `UniFix_Django_Project.zip` file.
2. Open VS Code.
3. Select **File → Open Folder** and choose the extracted `UniFix_Django_Project` folder.
4. Open **Terminal → New Terminal**.

## 3. Create and activate a virtual environment (Windows)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

## 4. Install the dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Create the PostgreSQL database

Make sure the PostgreSQL service is running. Open pgAdmin's Query Tool or `psql` and execute the following SQL. Change the sample password before using it:

```sql
CREATE USER unifix_user WITH PASSWORD 'change-this-password';
CREATE DATABASE unifix_db OWNER unifix_user;
```

If the user or database already exists, do not run the corresponding `CREATE` command again. You can instead update the existing user's password and database ownership in pgAdmin.

## 6. Configure the environment variables

1. In the project root, make a copy of `.env.example`.
2. Rename the copy to `.env`.
3. Set the PostgreSQL database name, username, password, host, and port to match your PostgreSQL setup.
4. Replace `DJANGO_SECRET_KEY` with a long random secret value.

Example local configuration:

```env
DJANGO_SECRET_KEY=use-a-long-random-secret-value-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DB_NAME=unifix_db
DB_USER=unifix_user
DB_PASSWORD=change-this-password
DB_HOST=127.0.0.1
DB_PORT=5432
```

Do not upload `.env` to GitHub. It is excluded by `.gitignore`.

## 7. Create database tables

Run these commands in the VS Code terminal:

```powershell
python manage.py migrate
```

## 8. Create the first System Administrator account

```powershell
python manage.py createsuperuser
```

Enter the username, email, and password. Django hashes the password. A superuser is automatically assigned the **System Administrator** UniFix role.

## 9. Run UniFix

```powershell
python manage.py runserver
```

Open these addresses in your browser:

- Portal: http://127.0.0.1:8000/
- Login: http://127.0.0.1:8000/accounts/login/
- Registration: http://127.0.0.1:8000/accounts/register/
- Django Admin: http://127.0.0.1:8000/admin/

## 10. Create and assign the other roles

Public registration always creates a **University Personnel** account. This prevents visitors from choosing privileged roles for themselves.

To create IT Support Administrator or IT Technician accounts:

1. Log in using the System Administrator account.
2. Open http://127.0.0.1:8000/admin/.
3. Select **Users → Add user** or open an existing user.
4. Set the role to **IT Support Administrator** or **IT Technician**.
5. Save the user.

Only authorized administrators should assign these roles. The `is_staff` permission controls access to Django Admin separately from the UniFix role.

## 11. Account Feature routes

| Route | Purpose | Access |
|---|---|---|
| `/accounts/register/` | Create an account | Public |
| `/accounts/login/` | Log in | Public |
| `/accounts/logout/` | End the session (POST only) | Logged-in users |
| `/accounts/dashboard/` | Redirect to the user's role dashboard | Logged-in users |
| `/accounts/dashboard/personnel/` | University Personnel dashboard | University Personnel |
| `/accounts/dashboard/it-admin/` | IT Support Administrator dashboard | IT Support Administrator |
| `/accounts/dashboard/technician/` | IT Technician dashboard | IT Technician |
| `/accounts/dashboard/system-admin/` | System Administrator dashboard | System Administrator |
| `/accounts/profile/` | View own profile | Logged-in users |
| `/accounts/profile/edit/` | Edit own profile | Logged-in users |

Trying to open a dashboard for a different role returns **403 Forbidden**. Profile pages use `request.user`, so users cannot provide another user's ID to edit somebody else's profile.

## 12. Run the account tests

With PostgreSQL configured and the virtual environment active:

```powershell
python manage.py test accounts
```

The tests cover registration/password hashing, login protection for profile pages, role-based dashboard restrictions, and profile access.

## 13. Useful commands

```powershell
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Notes for the project presentation

- **Backend and frontend:** Django views, forms, authentication, and Django templates.
- **Database:** PostgreSQL.
- **Security:** CSRF protection, session authentication, Django password hashing, password validators, login-required views, and role-based dashboard authorization.
- **Phase scope:** This folder provides the Account Feature only. The ticketing and equipment borrowing modules can be implemented in later phases using separate models and workflows.
