#!/usr/bin/env bash

# Create secrets directory
mkdir secrets &> /dev/null

# Read user input
read -p "Enter database name: " database_db
read -p "Enter user: " database_user
read -s -p "Enter password: " database_password

# Create secret files
echo $database_db > secrets/database_db
echo $database_user > secrets/database_user
echo $database_password > secrets/database_password
