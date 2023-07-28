#!/usr/bin/env pwsh

function wait_update($filepattern) {
    $watcher = New-Object System.IO.FileSystemWatcher
    $watcher.Path = "$(Convert-Path .)"
    $watcher.Filter = "$filepattern"
    $watcher.IncludeSubdirectories = $true
    $watcher.EnableRaisingEvents = $true  
    $changeResult = $watcher.WaitForChanged([IO.WatcherChangeTypes]::All, 1000)
    $updated = (!$changeResult.TimedOut)
    return $updated
}

function update_on_test_succeded() {
    if ("$(git status --porcelain)" -eq "") {
        return
    }
    git add -A | Out-Null
    git commit
}

function check_docker_is_absent() {
    $res = "$(bash -c 'pgrep docker && echo yes || echo no')"
    return ($res -eq "no")
}

# if (check_docker_is_absent) {
#     Write-Error "Docker is not running. Please run 'sudo service docker start'."
#     exit 1
# }

$count = 0
while ($true) {
    $count += 1
    Clear-Host
    Write-Host "[#$("{0:0000}" -f $count)] @$(Get-Date -UFormat "%Y/%m/%d %H:%M:%S")"
    # wsl --exec python3 -m pytest tests
    python3 -m pytest tests
    # wsl --exec python3 -m tox
    # $test_success = $?
    # if ($test_success) {
    #     update_on_test_succeded
    # }
    Start-Sleep -s 1
    $updated = $false
    while (!$updated) {
        $updated = wait_update "*.py"
    }
}