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
2. Run `SQLite $DATABASE_NAME`
3. Run `.database` and check that the new DB is listed
4. Repeat for `$TEST_DATABASE_NAME`

Run `python3 test_db_connection.py` to test you can connect to the databases.