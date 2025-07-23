#!/bin/bash

if ! command -v pyinstaller &> /dev/null; then
    echo "pyinstaller is not found. Please source the virtual environment."
    exit 1
fi

if [ ! -d "jre"]; then
    echo "Running PyInstaller without JRE..."
    pyinstaller -F irgen/src/irgen/main.py \
        --name irgen \
        --paths irgen/src \
        --add-data "schema/target/ipxact-schema-1.0.0.jar:jar/" \
        --add-data "schema/target/dependency/*:jar/dependency" \
        --exclude-module pytest \
        --exclude-module ruff \
        --exclude-module mypy \
        --console
else
    echo "Running PyInstaller with JRE..."
    pyinstaller -F irgen/src/irgen/main.py \
        --name irgen \
        --paths irgen/src \
        --add-data "jre/:jre/" \
        --add-data "schema/target/ipxact-schema-1.0.0.jar:jar/" \
        --add-data "schema/target/dependency/*:jar/dependency" \
        --exclude-module pytest \
        --exclude-module ruff \
        --exclude-module mypy \
        --console
fi

