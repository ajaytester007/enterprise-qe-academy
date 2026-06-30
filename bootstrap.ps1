# Enterprise QE Academy Bootstrap Script
# Creates/uses a local Python virtual environment and installs project dependencies.

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================"
Write-Host " Enterprise QE Academy Bootstrap"
Write-Host "============================================"
Write-Host ""

# Ensure script runs from repo root
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RepoRoot

Write-Host "Repo root: $RepoRoot"

# Check Python
Write-Host ""
Write-Host "Checking Python..."
python --version

# Create .venv if missing
if (!(Test-Path ".venv")) {
    Write-Host ""
    Write-Host "Creating local virtual environment..."
    python -m venv .venv
} else {
    Write-Host ""
    Write-Host ".venv already exists. Reusing it."
}

# Activate venv
Write-Host ""
Write-Host "Activating virtual environment..."
& ".\.venv\Scripts\Activate.ps1"

# Confirm active Python
Write-Host ""
Write-Host "Active Python:"
python -c "import sys; print(sys.executable)"

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
Write-Host ""
Write-Host "Installing requirements..."
python -m pip install -r requirements.txt

# Validate catalog if present
if (Test-Path "scripts\validate_catalog.py") {
    Write-Host ""
    Write-Host "Validating catalog..."
    python scripts\validate_catalog.py
}

# Verify MkDocs
Write-Host ""
Write-Host "MkDocs version:"
mkdocs --version

# Verify Java/Maven sample if present
if (Test-Path "java\core\pom.xml") {
    Write-Host ""
    Write-Host "Running Java Maven tests..."
    Push-Location "java\core"
    mvn clean test
    Pop-Location
}

Write-Host ""
Write-Host "============================================"
Write-Host " Bootstrap Complete"
Write-Host "============================================"
Write-Host ""
Write-Host "Virtual environment is active in this shell."
Write-Host ""
Write-Host "Useful commands:"
Write-Host "  python scripts\search_catalog.py --keyword masking --limit 10"
Write-Host "  python scripts\generate_practice_set.py --count 25 --domain Banking"
Write-Host "  cd docs; mkdocs serve"
Write-Host "  cd docs; mkdocs gh-deploy"
Write-Host ""