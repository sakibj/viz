# Vizness card application repository. 

#### This is a Flask App still in development.

## To get set up on the project:

1. Set up virtualenv
    - run "virtualenv -p python3 venv"
    - to activate run "source venv/bin/activate"
    - to deactivate run "deactivate"
2. Use pip to install dependencies (in the virtualenv)
    ```shell
    pip install -r requirements.txt
    ```
3. Run `python run.py`

## Database stuff:

#### Ubuntu: sudo apt-get install mysql-server libmysqlclient-dev
#### Fedora: yum install python-migrate

Run the following commands:
```shell
sudo mysql
create database viz;
create user 'viz'@'localhost' identified by 'viz';
grant all privileges on viz.* to 'viz'@'localhost'; 
```

Quit out of mysql with "quit". Then:
```shell
./migrate.py db migrate
./migrate.py db upgrade
```
To check the database subsequently, run `mysql -uviz -pviz`
To change database structure, edit viz/models.py, then run migrate and upgrade again.
If you happen to remove the migrations folder, then run init, migrate, then upgrade.
If all else fails, `rm -rf migrations`, then run `init/migrate/upgrade`. 
