# IP-XACT REGISTER GENERATOR

This is a Python script designed to convert register description spreadsheets in a specific format into IP-XACT XML files. see `example.xlsx` for an example.

## Key Features

- **Efficient Processing**: Uses the [Polars](https://www.pola.rs/) library to provide fast DataFrame operations for large datasets.

## How to Use

### Dependencies

- Python 3.11+
- [polars](https://www.pola.rs/)

### Installation and Execution

We provide two recommended setup methods: using the standard `venv` or [uv](https://docs.astral.sh/uv/).

#### Method 1: Using Python `venv`

1. **Create and activate a virtual environment:**

   ```shell
   # Create a virtual environment in the project root directory  
   # python version >= 3.11
   python3 -m venv .venv  
   
   # Activate the environment  
   # Linux/macOS  
   source .venv/bin/activate  
   # Windows  
   .venv\Scripts\activate  
   ```

2. **Install dependencies:**

   ```shell
   # Install the project and its dependencies  
   pip install -e .  
   ```

3. **Run the script:**

   ```shell
   irgen
   # see options:
   # irgen --help
   ```

#### Method 2: Using `uv`

`uv` is an emerging, ultra-fast Python package management tool.

1. **Create and activate a virtual environment:**

   ```shell
   # Create a virtual environment using Python 3.12 for an example
   uv venv --python 3.12  
   
   # Activate the environment  
   # Linux/macOS  
   source .venv/bin/activate  
   # Windows  
   .venv\Scripts\activate  
   ```

2. **Sync dependencies:**

   ```shell
   uv sync
   ```

3. **Run the script:**

   ```shell
   irgen
   # see options:
   # irgen --help
   ```
