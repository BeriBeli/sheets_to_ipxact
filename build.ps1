Set-StrictMode -Version Latest

function Handle-Error {
    param(
        [string]$Message
    )
    Write-Error $Message
    exit 1
}

# check if JAVA_HOME is set
if (-not (Test-Path Env:\JAVA_HOME)) {
    Handle-Error "JAVA_HOME is not set. Please set JAVA_HOME to your JDK installation."
}

# check if maven is installed.
if (-not (Get-Command mvn -ErrorAction SilentlyContinue)) {
    Handle-Error "Maven is not installed. Please install Maven to proceed."
}

$javaDir = "java"
if (-not (Test-Path -Path $javaDir -PathType Container)) {
    Handle-Error "'$javaDir' directory not found."
}

try {
    Push-Location -Path $javaDir

    Write-Host "INFO: Building Java project in '$((Get-Location).Path)'..."
    mvn clean package *>&1 | Write-Host
    if ($LASTEXITCODE -ne 0) {
        Handle-Error "Maven build failed. Please check the errors above."
    }

    Write-Host "INFO: Downloading dependencies..."
    mvn dependency:copy-dependencies *>&1 | Write-Host
    if ($LASTEXITCODE -ne 0) {
        Handle-Error "Failed to download Maven dependencies."
    }
}
finally {
    Pop-Location
}

$pythonDir = "python"
if (-not (Test-Path -Path $pythonDir -PathType Container)) {
    Handle-Error "'$pythonDir' directory not found."
}

try {
    Push-Location -Path $pythonDir
    Write-Host "INFO: Setting up Python environment in '$((Get-Location).Path)'..."

    if (Get-Command uv -ErrorAction SilentlyContinue) {
        Write-Host "INFO: Found 'uv'. Using it to create virtual environment."
        uv venv *>&1 | Write-Host
        & ".\.venv\Scripts\activate"
        uv sync *>&1 | Write-Host
    }
    else {
        $pythonExe = Get-Command python3, python -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($pythonExe) {
            Write-Host "INFO: Found '$($pythonExe.Name)'. Using it to create virtual environment."
            & $pythonExe.Source -m venv .venv
            & ".\.venv\Scripts\activate"
            pip install -e . *>&1 | Write-Host
        }
        else {
            Handle-Error "No python3 or python found to create a virtual environment."
        }
    }
}
finally {
    Pop-Location
}

irgen --help