# Sheets to IP-XACT

This is a Python script designed to convert register description spreadsheets in a specific format into IP-XACT XML files. see `example.xlsx` for an example.

## Key Features

- **Efficient Processing**: Uses the [Polars](https://www.pola.rs/) library to provide fast DataFrame operations for large datasets.
- **Standard Compliance**: Validate XML format compatibility with [IEEE 1685-2014](https://ieeexplore.ieee.org/document/6898803) (IP-XACT) standard
 via [lxml](https://lxml.de/).

## How to Use

### Dependencies

- Python 3.11+
- [polars](https://www.pola.rs/)
- [pydantic](https://docs.pydantic.dev/latest/)
- [pydantic-xml](https://pydantic-xml.readthedocs.io/en/latest/index.html)
- [lxml](https://lxml.de/)

### Configuration

see examples in `config/common.toml`. 
```toml
# spreadsheet path, also can be specified in args
excel_name = "demo.xlsx"
# the path of the output xml file, also can be specified in args
xml_name = "example.xml"
# the name of the sheet about vendor and version information
vendor_sheet = "version"
# the name of the sheet giving an address map of the system
address_sheet = "address_map"
```

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
   sheets_to_ipxact
   # options:
   # -h, --help                     show this help message and exit
   # -d, --debug                    Enable debug logging.
   # --excel EXCEL                  Path to the input Excel file
   # -o OUTPUT, --output OUTPUT     Path for the output XML file.
   ```
   or
   ```shell
   python -u src/main.py
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
   sheets_to_ipxact
   # options:
   # -h, --help                     show this help message and exit
   # -d, --debug                    Enable debug logging.
   # --excel EXCEL                  Path to the input Excel file
   # -o OUTPUT, --output OUTPUT     Path for the output XML file.
   ```
   or
   ```shell
   uv run src/main.py
   ```


## Warning
IP-XACT IEEE-1685-2014 standard is not completely implemented by `schema.py`
