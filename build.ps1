#!/usr/bin/env pwsh

python3 -m build
foreach ($path in $(ls dist/aoalias-*.tar.gz)) {
    pip install $path
    break
}
# pip uninstall aoalias
