Getting started
1. Ensure you have Poetry installed
2. Activate the poetry shell

To set environment variables required: 
1. Install direnv 
2. Ensure you have a .envrc file with the following fields:
```
export DATABASE_NAME="word_game"
export TEST_DATABASE_NAME="test_word_game"
```
3. Run `direnv allow .` from the root of the project to set the env vars in the terminal session. 

To initialise databases locally:
1. Install SQLite3
2. Run `SQLite3 $DATABASE_NAME`
3. Run `.database` and check that the new DB is listed in the 'main' property
4. Add the main property value (this is the DB URL) to the .envrc file with the prefix 'sqlite///' 
    e.g. `export DATABASE_URL = '/Users/my_profile/Projects/project_name/word_game'`
5. Repeat for `$TEST_DATABASE_NAME`

Run `python3 test_db_connection.py` to test you can connect to the databases.