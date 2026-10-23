<#
.SYNOPSIS
    Yangi o'zbek lotin klaviatura layoutlari (Ö Ğ Ş Ç ʼ) uchun Windows o'rnatuvchisi.

.DESCRIPTION
    Parametrsiz ishga tushirilsa — grafik oyna (UI) ochiladi.
    Buyruq satri rejimi:

      .\Setup.ps1 -Action Install   -Layout uzq,uzcw -Language en-US
      .\Setup.ps1 -Action Uninstall -Layout uzq,uzcw
      .\Setup.ps1 -Action Status

    Layoutlar:
      uzq   — Q joylashuvi:    [ ] ; '  ->  ö ğ ş ç
      uzcw  — C/W joylashuvi:  c w ; ,  ->  ç ş ö ğ
    Ikkalasida ham ` -> ʼ (tutuq), eski belgilar esa o'ng Alt (AltGr) orqali.

    Administrator huquqi kerak: skript o'zi so'raydi (UAC).
#>
[CmdletBinding()]
param(
    [ValidateSet('Gui', 'Install', 'Uninstall', 'Status')]
    [string]$Action = 'Gui',

    [string[]]$Layout = @('uzq', 'uzcw'),

    [ValidateSet('en-US', 'uz-Latn-UZ')]
    [string]$Language = 'en-US',

    [switch]$NoLanguageList,

    [switch]$Elevated
)

$ErrorActionPreference = 'Stop'
$Layout = @($Layout | ForEach-Object { $_ -split ',' } | ForEach-Object { $_.Trim().ToLower() } | Where-Object { $_ })

# ───────────────────────────── Katalog ─────────────────────────────────────
$script:Catalog = @(
    [pscustomobject]@{
        Id    = 'uzq'
        Dll   = 'kbduzq.dll'
        Text  = 'New Uzbek (Latin)'
        Title = 'New Uzbek (Latin) — Q joylashuvi'
        Keys  = '[ → ö     ] → ğ     ; → ş     '' → ç     ` → ʼ'
    },
    [pscustomobject]@{
        Id    = 'uzcw'
        Dll   = 'kbduzcw.dll'
        Text  = 'New Uzbek (Latin) - C/W'
        Title = 'New Uzbek (Latin) — C/W joylashuvi'
        Keys  = 'c → ç     w → ş     ; → ö     , → ğ     ` → ʼ'
    }
)
$script:LangMap = @{ 'en-US' = '0409'; 'uz-Latn-UZ' = '0443' }

$script:KlBase = 'HKLM:\SYSTEM\CurrentControlSet\Control\Keyboard Layouts'
$script:BinDir = Join-Path $PSScriptRoot 'bin'
$script:Is64OS = [Environment]::Is64BitOperatingSystem
$script:Sys32  = Join-Path $env:windir 'System32'
if ($script:Is64OS -and -not [Environment]::Is64BitProcess) {
    $script:Sys32 = Join-Path $env:windir 'Sysnative'      # 32-bitli PowerShell'dan haqiqiy System32
}
$script:SysWow = Join-Path $env:windir 'SysWOW64'
$script:OsArch = if ($env:PROCESSOR_ARCHITEW6432) { $env:PROCESSOR_ARCHITEW6432 } else { $env:PROCESSOR_ARCHITECTURE }

$script:LogBox = $null

function Write-Log([string]$Message) {
    if ($script:LogBox) {
        $script:LogBox.AppendText($Message + "`r`n")
        [System.Windows.Forms.Application]::DoEvents()
    }
    else {
        Write-Host $Message
    }
}

# ───────────────────────────── Administrator ───────────────────────────────
function Test-Admin {
    $id = [Security.Principal.WindowsIdentity]::GetCurrent()
    return ([Security.Principal.WindowsPrincipal]$id).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (Test-Admin)) {
    $relaunch = @('-NoProfile', '-ExecutionPolicy', 'Bypass')
    if ($Action -eq 'Gui') { $relaunch += @('-WindowStyle', 'Hidden') }
    $relaunch += @('-File', ('"{0}"' -f $PSCommandPath), '-Action', $Action,
        '-Layout', ($Layout -join ','), '-Language', $Language, '-Elevated')
    if ($NoLanguageList) { $relaunch += '-NoLanguageList' }
    try {
        Start-Process -FilePath 'powershell.exe' -ArgumentList $relaunch -Verb RunAs -WorkingDirectory $PSScriptRoot
    }
    catch {
        Write-Host "Administrator huquqi berilmadi — o'rnatish bekor qilindi."
        exit 1
    }
    exit 0
}

# ───────────────────────────── Reestr yordamchilari ────────────────────────
function Get-OurKlids([string]$Dll) {
    # "Layout File" qiymati bizning DLL bo'lgan hamma KLID kalitlari
    $found = @()
    foreach ($k in (Get-ChildItem -Path $script:KlBase)) {
        $p = Get-ItemProperty -Path $k.PSPath -ErrorAction SilentlyContinue
        if ($p -and $p.'Layout File' -and ($p.'Layout File' -ieq $Dll)) { $found += $k.PSChildName }
    }
    return $found
}

function Get-Status($l) {
    $klids = @(Get-OurKlids $l.Dll)
    $files = Test-Path -LiteralPath (Join-Path $script:Sys32 $l.Dll)
    [pscustomobject]@{ Installed = ($klids.Count -gt 0 -and $files); Klids = $klids }
}

function Register-Layout($l, [string]$LangHex) {
    $existing = @(Get-OurKlids $l.Dll | ForEach-Object { $_ } | Where-Object { $_.Substring(4) -ieq $LangHex })
    if ($existing.Count -gt 0) {
        $klid = $existing[0]
        $layoutId = (Get-ItemProperty -Path "$script:KlBase\$klid").'Layout Id'
    }
    else {
        $all = @(Get-ChildItem -Path $script:KlBase)
        $usedKlids = @($all | ForEach-Object { $_.PSChildName.ToLower() })
        $usedIds = @($all | ForEach-Object { (Get-ItemProperty -Path $_.PSPath -ErrorAction SilentlyContinue).'Layout Id' } |
            Where-Object { $_ } | ForEach-Object { ([string]$_).ToLower() })

        $n = 0
        while ($usedKlids -contains ('a{0:x3}{1}' -f $n, $LangHex)) { $n++ }
        $klid = 'a{0:x3}{1}' -f $n, $LangHex

        $m = 0xC0
        while ($usedIds -contains ('{0:x4}' -f $m)) { $m++ }
        $layoutId = '{0:x4}' -f $m
    }

    $path = "$script:KlBase\$klid"
    New-Item -Path $path -Force | Out-Null
    New-ItemProperty -Path $path -Name 'Layout File' -Value $l.Dll -PropertyType String -Force | Out-Null
    New-ItemProperty -Path $path -Name 'Layout Text' -Value $l.Text -PropertyType String -Force | Out-Null
    New-ItemProperty -Path $path -Name 'Layout Id' -Value $layoutId -PropertyType String -Force | Out-Null
    return $klid
}

# ───────────────────────────── Fayllar ─────────────────────────────────────
function Copy-LayoutDlls($l) {
    if ($script:OsArch -eq 'ARM64') {
        throw "ARM64 Windows hozircha qo'llab-quvvatlanmaydi (x64/x86 DLL'lari ARM64 yadrosida yuklanmaydi)."
    }
    $jobs = @()
    if ($script:Is64OS) {
        $jobs += [pscustomobject]@{ Src = (Join-Path $script:BinDir "x64\$($l.Dll)"); Dst = $script:Sys32 }
        $jobs += [pscustomobject]@{ Src = (Join-Path $script:BinDir "x86\$($l.Dll)"); Dst = $script:SysWow }
    }
    else {
        $jobs += [pscustomobject]@{ Src = (Join-Path $script:BinDir "x86\$($l.Dll)"); Dst = $script:Sys32 }
    }
    foreach ($j in $jobs) {
        if (-not (Test-Path -LiteralPath $j.Src)) {
            throw "Fayl topilmadi: $($j.Src). ZIP arxivni to'liq chiqarib (Extract All), keyin ishga tushiring."
        }
        Unblock-File -LiteralPath $j.Src -ErrorAction SilentlyContinue
        try {
            Copy-Item -LiteralPath $j.Src -Destination $j.Dst -Force
        }
        catch {
            throw "DLL nusxalanmadi ($($j.Dst)). Fayl band bo'lishi mumkin: avval O'chirish, kompyuterni qayta ishga tushirib, so'ng qayta o'rnating. ($($_.Exception.Message))"
        }
        Write-Log "    nusxalandi: $(Join-Path $j.Dst $l.Dll)"
    }
}

function Remove-LayoutDlls($l) {
    $targets = @(Join-Path $script:Sys32 $l.Dll)
    if ($script:Is64OS) { $targets += (Join-Path $script:SysWow $l.Dll) }
    foreach ($t in $targets) {
        if (-not (Test-Path -LiteralPath $t)) { continue }
        try {
            Remove-Item -LiteralPath $t -Force
            Write-Log "    o'chirildi: $t"
        }
        catch {
            # DLL hozir tizim tomonidan band — keyingi qayta ishga tushirishda o'chiriladi
            try {
                Add-Type -Namespace Uz -Name Native -ErrorAction SilentlyContinue -MemberDefinition @'
[System.Runtime.InteropServices.DllImport("kernel32.dll", SetLastError = true, CharSet = System.Runtime.InteropServices.CharSet.Unicode)]
public static extern bool MoveFileEx(string existing, string target, int flags);
'@
                [void][Uz.Native]::MoveFileEx($t, $null, 4)   # MOVEFILE_DELAY_UNTIL_REBOOT
                Write-Log "    band: $t — kompyuter qayta ishga tushganda o'chiriladi."
            }
            catch { Write-Log "    OGOHLANTIRISH: $t o'chirilmadi." }
        }
    }
}

# ───────────────────────────── Foydalanuvchi til ro'yxati ──────────────────
function Add-ToLanguageList([string]$Tag, [string]$Tip) {
    $list = Get-WinUserLanguageList
    $lang = $list | Where-Object { $_.LanguageTag -ieq $Tag } | Select-Object -First 1
    if (-not $lang) {
        $list.Add($Tag)
        $lang = $list | Where-Object { $_.LanguageTag -ieq $Tag } | Select-Object -First 1
    }
    if (-not ($lang.InputMethodTips | Where-Object { $_ -ieq $Tip })) {
        $lang.InputMethodTips.Add($Tip)
    }
    Set-WinUserLanguageList -LanguageList $list -Force
}

function Remove-FromLanguageLists([string]$Klid) {
    $list = Get-WinUserLanguageList
    $changed = $false
    foreach ($lang in $list) {
        $hits = @($lang.InputMethodTips | Where-Object { $_ -match (':' + [regex]::Escape($Klid) + '$') })
        foreach ($h in $hits) { [void]$lang.InputMethodTips.Remove($h); $changed = $true }
    }
    if ($changed) { Set-WinUserLanguageList -LanguageList $list -Force }
}

# ───────────────────────────── Asosiy amallar ──────────────────────────────
function Install-One($l, [string]$Tag, [bool]$AddToList) {
    Write-Log "==> $($l.Text) o'rnatilmoqda..."
    Copy-LayoutDlls $l
    $langHex = $script:LangMap[$Tag]
    $klid = Register-Layout $l $langHex
    Write-Log "    reestr: ${klid}  ($Tag)"
    if ($AddToList) {
        try {
            Add-ToLanguageList $Tag ("{0}:{1}" -f $langHex, $klid.ToUpper())
            Write-Log "    til ro'yxatiga qo'shildi ($Tag)."
        }
        catch {
            Write-Log "    Til ro'yxatiga avtomatik qo'shib bo'lmadi: $($_.Exception.Message)"
            Write-Log "    Qo'lda qo'shing: Sozlamalar > Vaqt va til > Til > $Tag > Klaviatura qo'shish."
        }
    }
    Write-Log "    tayyor."
}

function Uninstall-One($l) {
    Write-Log "==> $($l.Text) o'chirilmoqda..."
    foreach ($klid in @(Get-OurKlids $l.Dll | ForEach-Object { $_ })) {
        try { Remove-FromLanguageLists $klid }
        catch { Write-Log "    Til ro'yxatidan olib bo'lmadi (${klid}): $($_.Exception.Message)" }
        Remove-Item -Path "$script:KlBase\$klid" -Recurse -Force
        Write-Log "    reestr kaliti o'chirildi: ${klid}"
    }
    Remove-LayoutDlls $l
    Write-Log "    tayyor."
}

function Select-Layouts([string[]]$Ids) {
    foreach ($id in $Ids) {
        $l = $script:Catalog | Where-Object { $_.Id -eq $id }
        if (-not $l) { throw "Noma'lum layout: '$id' (uzq yoki uzcw bo'lishi kerak)." }
        $l
    }
}

# ───────────────────────────── Oyna (UI) ───────────────────────────────────
function Show-Gui {
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
    [System.Windows.Forms.Application]::EnableVisualStyles()

    $font = New-Object System.Drawing.Font('Segoe UI', 9.5)
    $bold = New-Object System.Drawing.Font('Segoe UI', 10, [System.Drawing.FontStyle]::Bold)

    $script:Form = New-Object System.Windows.Forms.Form
    $script:Form.Text = "O'zbek klaviatura layouti — o'rnatish"
    $script:Form.ClientSize = New-Object System.Drawing.Size(650, 560)
    $script:Form.StartPosition = 'CenterScreen'
    $script:Form.FormBorderStyle = 'FixedDialog'
    $script:Form.MaximizeBox = $false
    $script:Form.Font = $font

    $title = New-Object System.Windows.Forms.Label
    $title.Text = "Yangi o'zbek lotin klaviaturasi"
    $title.Font = New-Object System.Drawing.Font('Segoe UI', 15, [System.Drawing.FontStyle]::Bold)
    $title.Location = New-Object System.Drawing.Point(20, 14)
    $title.Size = New-Object System.Drawing.Size(610, 32)
    $script:Form.Controls.Add($title)

    $sub = New-Object System.Windows.Forms.Label
    $sub.Text = "Ö  Ğ  Ş  Ç  ʼ  harflari uchun layoutlarni tanlang"
    $sub.Location = New-Object System.Drawing.Point(22, 48)
    $sub.Size = New-Object System.Drawing.Size(610, 22)
    $script:Form.Controls.Add($sub)

    $script:Checks = @{}
    $script:StatusLabels = @{}
    $y = 82
    foreach ($l in $script:Catalog) {
        $panel = New-Object System.Windows.Forms.Panel
        $panel.BorderStyle = 'FixedSingle'
        $panel.Location = New-Object System.Drawing.Point(20, $y)
        $panel.Size = New-Object System.Drawing.Size(610, 80)

        $cb = New-Object System.Windows.Forms.CheckBox
        $cb.Text = $l.Title
        $cb.Font = $bold
        $cb.Checked = $true
        $cb.Location = New-Object System.Drawing.Point(10, 8)
        $cb.Size = New-Object System.Drawing.Size(580, 26)
        $panel.Controls.Add($cb)

        $keys = New-Object System.Windows.Forms.Label
        $keys.Text = $l.Keys
        $keys.Location = New-Object System.Drawing.Point(32, 36)
        $keys.Size = New-Object System.Drawing.Size(560, 20)
        $panel.Controls.Add($keys)

        $st = New-Object System.Windows.Forms.Label
        $st.Location = New-Object System.Drawing.Point(32, 56)
        $st.Size = New-Object System.Drawing.Size(560, 20)
        $panel.Controls.Add($st)

        $script:Checks[$l.Id] = $cb
        $script:StatusLabels[$l.Id] = $st
        $script:Form.Controls.Add($panel)
        $y += 90
    }

    $lblLang = New-Object System.Windows.Forms.Label
    $lblLang.Text = 'Til:'
    $lblLang.Location = New-Object System.Drawing.Point(22, 272)
    $lblLang.Size = New-Object System.Drawing.Size(40, 24)
    $script:Form.Controls.Add($lblLang)

    $script:CmbLang = New-Object System.Windows.Forms.ComboBox
    $script:CmbLang.DropDownStyle = 'DropDownList'
    [void]$script:CmbLang.Items.Add('English (US) — tavsiya etiladi')
    [void]$script:CmbLang.Items.Add('Uzbek (Latin)')
    $script:CmbLang.SelectedIndex = 0
    $script:CmbLang.Location = New-Object System.Drawing.Point(64, 268)
    $script:CmbLang.Size = New-Object System.Drawing.Size(330, 26)
    $script:Form.Controls.Add($script:CmbLang)

    $script:ChkList = New-Object System.Windows.Forms.CheckBox
    $script:ChkList.Text = "Til ro'yxatiga avtomatik qo'shish"
    $script:ChkList.Checked = $true
    $script:ChkList.Location = New-Object System.Drawing.Point(22, 302)
    $script:ChkList.Size = New-Object System.Drawing.Size(400, 24)
    $script:Form.Controls.Add($script:ChkList)

    function New-Button([string]$Text, [int]$X, [int]$W) {
        $b = New-Object System.Windows.Forms.Button
        $b.Text = $Text
        $b.Location = New-Object System.Drawing.Point($X, 338)
        $b.Size = New-Object System.Drawing.Size($W, 38)
        $script:Form.Controls.Add($b)
        return $b
    }
    $script:BtnInstall = New-Button "O'rnatish" 20 150
    $script:BtnRemove = New-Button "O'chirish" 180 150
    $script:BtnSettings = New-Button "Til sozlamalari" 340 160
    $btnClose = New-Button 'Yopish' 510 120

    $script:LogBox = New-Object System.Windows.Forms.TextBox
    $script:LogBox.Multiline = $true
    $script:LogBox.ReadOnly = $true
    $script:LogBox.ScrollBars = 'Vertical'
    $script:LogBox.Font = New-Object System.Drawing.Font('Consolas', 9)
    $script:LogBox.Location = New-Object System.Drawing.Point(20, 390)
    $script:LogBox.Size = New-Object System.Drawing.Size(610, 130)
    $script:Form.Controls.Add($script:LogBox)

    $hint = New-Object System.Windows.Forms.Label
    $hint.Text = "Layoutlarni almashtirish: Win + Space.  Eski belgilar (c w ; , [ ] ' ) — o'ng Alt (AltGr) bilan."
    $hint.Location = New-Object System.Drawing.Point(20, 528)
    $hint.Size = New-Object System.Drawing.Size(610, 22)
    $hint.ForeColor = [System.Drawing.Color]::DimGray
    $script:Form.Controls.Add($hint)

    $script:RefreshStatus = {
        foreach ($l in $script:Catalog) {
            $s = Get-Status $l
            $lbl = $script:StatusLabels[$l.Id]
            if ($s.Installed) {
                $lbl.Text = "● o'rnatilgan"
                $lbl.ForeColor = [System.Drawing.Color]::ForestGreen
            }
            else {
                $lbl.Text = "○ o'rnatilmagan"
                $lbl.ForeColor = [System.Drawing.Color]::Gray
            }
        }
    }

    $script:RunAction = {
        param([string]$Mode)
        $ids = @($script:Catalog | Where-Object { $script:Checks[$_.Id].Checked } | ForEach-Object { $_.Id })
        if ($ids.Count -eq 0) {
            [void][System.Windows.Forms.MessageBox]::Show("Kamida bitta layoutni belgilang.", 'Eslatma')
            return
        }
        $tag = if ($script:CmbLang.SelectedIndex -eq 1) { 'uz-Latn-UZ' } else { 'en-US' }
        $script:Form.Enabled = $false
        $script:Form.Cursor = [System.Windows.Forms.Cursors]::WaitCursor
        try {
            foreach ($l in (Select-Layouts $ids)) {
                if ($Mode -eq 'Install') { Install-One $l $tag $script:ChkList.Checked }
                else { Uninstall-One $l }
            }
            if ($Mode -eq 'Install') {
                Write-Log ""
                Write-Log "Tayyor! Win+Space bilan layoutni tanlang."
                Write-Log "Ro'yxatda ko'rinmasa — tizimdan chiqib qayta kiring yoki 'Til sozlamalari'dan qo'shing."
            }
            else {
                Write-Log ""
                Write-Log "Olib tashlandi."
            }
        }
        catch {
            Write-Log "XATO: $($_.Exception.Message)"
        }
        finally {
            $script:Form.Cursor = [System.Windows.Forms.Cursors]::Default
            $script:Form.Enabled = $true
            & $script:RefreshStatus
        }
    }

    $script:BtnInstall.Add_Click({ & $script:RunAction 'Install' })
    $script:BtnRemove.Add_Click({ & $script:RunAction 'Uninstall' })
    $script:BtnSettings.Add_Click({ Start-Process 'ms-settings:regionlanguage' })
    $btnClose.Add_Click({ $script:Form.Close() })

    if ($script:OsArch -eq 'ARM64') {
        Write-Log "DIQQAT: ARM64 Windows aniqlandi — bu DLL'lar x64/x86 uchun, o'rnatish ishlamaydi."
    }
    & $script:RefreshStatus
    [void]$script:Form.ShowDialog()
}

# ───────────────────────────── Kirish nuqtasi ──────────────────────────────
try {
    switch ($Action) {
        'Gui' { Show-Gui }
        'Status' {
            foreach ($l in $script:Catalog) {
                $s = Get-Status $l
                $mark = if ($s.Installed) { "o'rnatilgan  [" + ($s.Klids -join ', ') + "]" } else { "o'rnatilmagan" }
                Write-Host ("{0,-6} {1,-26} {2}" -f $l.Id, $l.Text, $mark)
            }
        }
        'Install' {
            foreach ($l in (Select-Layouts $Layout)) { Install-One $l $Language (-not $NoLanguageList) }
            Write-Host "`nTayyor! Win+Space bilan layoutni tanlang (ko'rinmasa — tizimdan chiqib qayta kiring)."
        }
        'Uninstall' {
            foreach ($l in (Select-Layouts $Layout)) { Uninstall-One $l }
            Write-Host "`nOlib tashlandi."
        }
    }
}
catch {
    if ($Action -eq 'Gui') {
        Add-Type -AssemblyName System.Windows.Forms
        [void][System.Windows.Forms.MessageBox]::Show($_.Exception.Message, 'Xato')
    }
    else {
        Write-Host "XATO: $($_.Exception.Message)" -ForegroundColor Red
    }
    if ($Elevated -and $Action -ne 'Gui') { [void](Read-Host "Chiqish uchun Enter bosing") }
    exit 1
}
if ($Elevated -and $Action -ne 'Gui') { [void](Read-Host "Chiqish uchun Enter bosing") }
