# The Pizzeria project for sem 1 of fhict

# Installation instructions

## Windows

This tutorial assumes you are using PowerShell

1. `cd` to the folder where you wish to clone the project

2. ```powershell
   git clone https://github.com/mbjd05/projectpizza.git
   ```

   ⚠️ **Make sure you run every command from here on from the `projectpizza` folder** ⚠️

3. create a virtual environment in the `projectpizza` folder called `.venv`:

   ```powershell
   python -m venv .venv
   ```

4. activate your venv:

   ```powershell
   & "c:/pathtoyourfolder/pizzaproject/src/.venv/Scripts/Activate.ps1"
   ```

   If you get an error trying to run `Activate.ps1`, open `powershell` as Administrator and change your execution policy to allow for execution of scripts:

   ```powershell
   Set-ExecutionPolicy RemoteSigned
   ```

5.  When you activated your virtual environment, set the FLASK_APP environment variable to the `src` folder:

   ```powershell
	$env:FLASK_APP = ".\src"
   ```

6. Install the required dependencies:

    ```powershell
    python .\installdeps.py
    ```

7. edit the template `config.ini` file to allow the flask app to connect to your MySQL database. Here is an example of a filled out config file:

    ```ini
    [mysql]
    host = studmysql01.fhict.local
    user = dbi532486
    password = yourpasswd
    db = dbi532486
    cursorclass = DictCursor
    
    [app]
    secret_key = zmIjviApsqlV3Js1RT41Dg
    ```

    You can easily generate a secret key  with python 3.6+ using the interactive shell:

    ```python
    >>> import secrets
    >>> key = secrets.token_urlsafe(16)
    >>> print(key)
    ```

8. Run your app!

   ```powershell
   flask run
   ```