<#
.SYNOPSIS
    Set environment variable for current user
.DESCRIPTION
    This script sets an environment variable for the current user using PowerShell
    It handles both creation and updates of environment variables
.PARAMETER Name
    The name of the environment variable
.PARAMETER Value
    The value to set for the environment variable
.PARAMETER Scope
    The scope of the environment variable (User or Machine)
.PARAMETER Action
    The action to perform (Set, Get, or Delete)
.EXAMPLE
    .\Set-EnvironmentVariable.ps1 -Name "TEST_VAR" -Value "test_value" -Scope "User" -Action "Set"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Name,

    [Parameter(Mandatory=$false)]
    [string]$Value = "",

    [Parameter(Mandatory=$true)]
    [ValidateSet("User", "Machine")]
    [string]$Scope = "User",

    [Parameter(Mandatory=$true)]
    [ValidateSet("Set", "Get", "Delete", "List")]
    [string]$Action
)

# Function to set environment variable
function Set-EnvironmentVariableInternal {
    param(
        [string]$VarName,
        [string]$VarValue,
        [string]$TargetScope
    )

    try {
        if ($TargetScope -eq "User") {
            [System.Environment]::SetEnvironmentVariable($VarName, $VarValue, "User")
            # Also update the registry for immediate effect
            $RegPath = "HKCU:\Environment"
            Set-ItemProperty -Path $RegPath -Name $VarName -Value $VarValue -Force
        } else {
            [System.Environment]::SetEnvironmentVariable($VarName, $VarValue, "Machine")
            # Also update the registry for immediate effect
            $RegPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
            Set-ItemProperty -Path $RegPath -Name $VarName -Value $VarValue -Force
        }

        # Broadcast environment change
        if ($TargetScope -eq "Machine") {
            # For machine scope, we need to broadcast to all windows
            $Signature = @"
[DllImport"user32.dll", SetLastError=true, CharSet=CharSet.Auto)]
public static extern IntPtr SendMessageTimeout(
    IntPtr hWnd, uint Msg, IntPtr wParam, string lParam,
    uint fuFlags, uint uTimeout, out IntPtr lpdwResult);
"@

            $Type = Add-Type -MemberDefinition $Signature -Name "Win32" -PassThru
            $Result = [IntPtr]::Zero
            $Type::SendMessageTimeout(0xffff, 0x001A, [IntPtr]::Zero, "Environment", 0, 5000, [ref]$Result)
        } else {
            # For user scope, just update current process
            Set-Item -Path "env:$VarName" -Value $VarValue
        }

        return @{
            Success = $true
            Message = "Environment variable '$VarName' set to '$VarValue' for $TargetScope scope"
            Value = $VarValue
        }
    }
    catch {
        return @{
            Success = $false
            Message = "Failed to set environment variable '$VarName': $($_.Exception.Message)"
            Error = $_.Exception.Message
        }
    }
}

# Function to get environment variable
function Get-EnvironmentVariableInternal {
    param(
        [string]$VarName,
        [string]$TargetScope
    )

    try {
        if ($TargetScope -eq "User") {
            $Value = [System.Environment]::GetEnvironmentVariable($VarName, "User")
            if (-not $Value) {
                # Try to get from registry
                $RegPath = "HKCU:\Environment"
                $Prop = Get-ItemProperty -Path $RegPath -Name $VarName -ErrorAction SilentlyContinue
                $Value = if ($Prop) { $Prop.$VarName } else { "" }
            }
        } else {
            $Value = [System.Environment]::GetEnvironmentVariable($VarName, "Machine")
            if (-not $Value) {
                # Try to get from registry
                $RegPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
                $Prop = Get-ItemProperty -Path $RegPath -Name $VarName -ErrorAction SilentlyContinue
                $Value = if ($Prop) { $Prop.$VarName } else { "" }
            }
        }

        return @{
            Success = $true
            Message = "Environment variable '$VarName' retrieved successfully"
            Value = $Value
        }
    }
    catch {
        return @{
            Success = $false
            Message = "Failed to get environment variable '$VarName': $($_.Exception.Message)"
            Error = $_.Exception.Message
        }
    }
}

# Function to delete environment variable
function Remove-EnvironmentVariableInternal {
    param(
        [string]$VarName,
        [string]$TargetScope
    )

    try {
        if ($TargetScope -eq "User") {
            [System.Environment]::SetEnvironmentVariable($VarName, $null, "User")
            # Remove from registry
            $RegPath = "HKCU:\Environment"
            Remove-ItemProperty -Path $RegPath -Name $VarName -ErrorAction SilentlyContinue -Force
        } else {
            [System.Environment]::SetEnvironmentVariable($VarName, $null, "Machine")
            # Remove from registry
            $RegPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
            Remove-ItemProperty -Path $RegPath -Name $VarName -ErrorAction SilentlyContinue -Force
        }

        return @{
            Success = $true
            Message = "Environment variable '$VarName' deleted from $TargetScope scope"
        }
    }
    catch {
        return @{
            Success = $false
            Message = "Failed to delete environment variable '$VarName': $($_.Exception.Message)"
            Error = $_.Exception.Message
        }
    }
}

# Function to list environment variables
function Get-EnvironmentVariablesList {
    param(
        [string]$TargetScope
    )

    try {
        $Variables = @{}

        if ($TargetScope -eq "User") {
            $RegPath = "HKCU:\Environment"
            $Props = Get-ItemProperty -Path $RegPath -ErrorAction SilentlyContinue
            if ($Props) {
                $Props.PSObject.Properties | Where-Object { $_.Name -ne "PSPath" -and $_.Name -ne "PSParentPath" } | ForEach-Object {
                    $Variables[$_.Name] = $_.Value
                }
            }
        } else {
            $RegPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
            $Props = Get-ItemProperty -Path $RegPath -ErrorAction SilentlyContinue
            if ($Props) {
                $Props.PSObject.Properties | Where-Object { $_.Name -ne "PSPath" -and $_.Name -ne "PSParentPath" } | ForEach-Object {
                    $Variables[$_.Name] = $_.Value
                }
            }
        }

        return @{
            Success = $true
            Message = "Environment variables list retrieved successfully"
            Variables = $Variables
            Count = $Variables.Count
        }
    }
    catch {
        return @{
            Success = $false
            Message = "Failed to list environment variables: $($_.Exception.Message)"
            Error = $_.Exception.Message
        }
    }
}

# Main execution logic
$Result = switch ($Action) {
    "Set" {
        Set-EnvironmentVariableInternal -VarName $Name -VarValue $Value -TargetScope $Scope
    }
    "Get" {
        Get-EnvironmentVariableInternal -VarName $Name -TargetScope $Scope
    }
    "Delete" {
        Remove-EnvironmentVariableInternal -VarName $Name -TargetScope $Scope
    }
    "List" {
        Get-EnvironmentVariablesList -TargetScope $Scope
    }
}

# Output result as JSON
$Result | ConvertTo-Json -Depth 3