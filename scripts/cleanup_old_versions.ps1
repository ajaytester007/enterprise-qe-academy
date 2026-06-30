# Enterprise QE Academy local cleanup helper
# Run from C:\GitHub\Enterprise_QE_Academy_Consumable_GitSolution
# This script only reports by default. Use -Delete to remove older extracted folders/ZIPs.

param(
    [switch]$Delete
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================"
Write-Host " Enterprise QE Academy Cleanup Helper"
Write-Host "============================================"

$Root = Get-Location
Write-Host "Current folder: $Root"
Write-Host ""

$Keep = @(
    "enterprise_qe_academy_consumable_solution",
    "enterprise_qe_academy_v23_cleanup_patch"
)

$Candidates = Get-ChildItem -Path $Root -Force | Where-Object {
    $_.Name -like "enterprise_qe_academy_v*" -or
    $_.Name -like "Enterprise_QE_Academy_v*" -or
    $_.Name -like "*.zip"
} | Where-Object {
    $Keep -notcontains $_.Name
}

if (!$Candidates) {
    Write-Host "No cleanup candidates found."
    exit 0
}

Write-Host "Cleanup candidates:"
$Candidates | ForEach-Object {
    $size = if ($_.PSIsContainer) {
        (Get-ChildItem $_.FullName -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
    } else {
        $_.Length
    }
    $mb = [math]::Round(($size / 1MB), 2)
    Write-Host " - $($_.Name) [$mb MB]"
}

if (!$Delete) {
    Write-Host ""
    Write-Host "Dry run only. To delete candidates, rerun:"
    Write-Host "  .\enterprise_qe_academy_consumable_solution\scripts\cleanup_old_versions.ps1 -Delete"
    exit 0
}

Write-Host ""
Write-Host "Deleting candidates..."
foreach ($item in $Candidates) {
    Remove-Item $item.FullName -Recurse -Force
    Write-Host "Deleted: $($item.Name)"
}

Write-Host "Cleanup complete."
