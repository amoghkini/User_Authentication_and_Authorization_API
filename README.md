# User_Authentication_and_Authorization_API
The RestAPIs built using flask which can handle user authentication and authorization.

Please follow the following pre-requisites to setup the application.
1. Change the logfile directory in server.json file of config directory. Make sure that this directory is present in the operating system. If not, the system will throw the valid error during server bootup.
2. Create the database structure. We are using postgres database in this projet. We need to execute several sql files present inside the sql directory. The order to execute the sql files is as follows:
    1. roles.sql
    2. endpoints.sql
    3. accessibility.sql
    4. accessibility_view.sql
    5. users.sql
    6. blacklisted_tokens.sql
    7. one_time_data_load.sql

The server can be run by using command "python main.py" inside src directory.

Once the server is runnig, you can access the endpoints at '127.0.0.1:5000'.
