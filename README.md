# Sheets to IP-XACT

This is a Python script designed to convert register description spreadsheets in a specific format into IP-XACT XML files. The spreadsheet file `example.xlsx` is provided as an example in specific format.

## Key Features

- **Efficient Processing**: Uses the [Polars](https://www.pola.rs/) library to provide fast DataFrame operations for large datasets.
- **Standard Compliance**: Validate XML format compatibility with [IEEE 1685-2014](https://ieeexplore.ieee.org/document/6898803) (IP-XACT) standard
 via [lxml](https://lxml.de/).

## How to Use

### Dependencies

- Python 3.12
- [polars](https://www.pola.rs/)
- [pydantic](https://docs.pydantic.dev/latest/)
- [lxml](https://lxml.de/)

### Configuration

see examples in `config/common.toml`. TOML currently has **higher priority** than args, to make script command execution simpler.

### Installation and Execution

We provide two recommended setup methods: using the standard `venv` or [uv](https://docs.astral.sh/uv/).

#### Method 1: Using Python `venv`

1. **Create and activate a virtual environment:**

   ```shell
   # Create a virtual environment in the project root directory  
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
   sheets_to_ipxact
   ```
   or
   ```shell
   python -u src/main.py
   ```

#### Method 2: Using `uv`

`uv` is an emerging, ultra-fast Python package management tool.

1. **Create and activate a virtual environment:**

   ```shell
   # Create a virtual environment using Python 3.12  
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
   sheets_to_ipxact
   ```
   or
   ```shell
   uv run src/main.py
   ```


## Warning
1. Not All IP-XACT standard implemented by `schema.py`
2. `dict_xml.py` Can't completely convert dict format to XML

## TODO
1. add tests
2. fix bugs
