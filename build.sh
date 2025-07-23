#!/bin/bash

# check if JAVA_HOME is set
if [ -z "$JAVA_HOME" ]; then
    echo "JAVA_HOME is not set. Please set JAVA_HOME to your JDK installation."
    exit 1
fi

# check if maven is installed.
if ! command -v mvn &> /dev/null; then
    echo "Maven is not installed. Please install Maven to proceed."
    exit 1
fi

if [ ! -d "schema"]; then
    echo "schema directory not found."
    exit 1
fi

cd schema

# clean and package the java project

mvn clean package

# check if the build was successful
if [ $? -ne 0 ]; then
    echo "Build failed. Please check the errors above."
    exit 1
fi

# download dependencies
mvn dependency:copy-dependencies

# check if the dependencies were downloaded successfully
if [ $? -ne 0 ]; then
    echo "Failed to download dependencies. Please check the errors above."
    exit 1
fi

cd -

if [ ! -d "irgen"]; then
    echo "irgen directory not found."
    exit 1
fi

cd irgen

if command -v uv &> /dev/null; then
    uv venv
    source .venv/bin/activate
    uv sync
elif command -v python3 &> /dev/null; then
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e .
else 
    echo "No python3 found to create a virtual environment."
    exit 1
fi

cd -

irgen --help