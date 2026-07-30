$ErrorActionPreference = "Stop"

python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install -r .\portable_build_requirements.txt
python .\build_portable.py

& .\dist\ProteinFoldingPractical\ProteinFoldingPractical.exe --self-test
if ($LASTEXITCODE -ne 0) {
    throw "Portable build self-test failed."
}

Write-Host "Build ready in dist\ProteinFoldingPractical"
