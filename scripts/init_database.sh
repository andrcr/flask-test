#!/bin/bash

SCRIPT_DIR_NAME=$(sed 's|\(.*\)/.*|\1|' <<< ${BASH_SOURCE})

sqlite3 $SCRIPT_DIR_NAME/../database.db < $SCRIPT_DIR_NAME/database_init/schema.sql
sqlite3 $SCRIPT_DIR_NAME/../database.db < $SCRIPT_DIR_NAME/database_init/data.sql