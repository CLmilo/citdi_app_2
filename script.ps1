try {
    $LNKFILE = "$HOME\OneDrive\Escritorio\Kallpa Proccessor.lnk"

    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut("$LNKFILE")
    $Shortcut.TargetPath = "$env:ProgramFiles\kallpa_app\kallpa_app.exe"
    $Shortcut.WorkingDirectory = "$env:ProgramFiles\kallpa_app"
    $Shortcut.Save()
}
catch {
    $LNKFILE = "$HOME\Escritorio\Kallpa Proccessor.lnk"

    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut("$LNKFILE")
    $Shortcut.TargetPath = "$env:ProgramFiles\kallpa_app\kallpa_app.exe"
    $Shortcut.WorkingDirectory = "$env:ProgramFiles\kallpa_app\"
    $Shortcut.Save()
}
