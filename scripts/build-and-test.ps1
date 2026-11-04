# Run on the Windows agent (build step: NON-admin terminal)
pip install pyinstaller
pyinstaller -F quarantine-file.py
# copy dist\quarantine-file.exe to:
#   C:\Program Files (x86)\ossec-agent\active-response\bin\

# Same for Wazuh's remove-threat.py (download from Wazuh docs): pyinstaller -F remove-threat.py

# --- Test (admin PowerShell, lab only, Defender real-time protection off) ---
# Writes the standard EICAR antivirus test string (harmless) to the monitored folder.
# Get the string from https://www.eicar.org/download-anti-malware-testfile/
$eicar = '<paste EICAR standard test string here>'
Set-Content -Path "C:\Users\Admin\Downloads\Wazuh-Agent\eicar.com" -Value $eicar
