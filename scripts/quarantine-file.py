"""Local active-response script (section 4.2).
Deletes files matching known-bad patterns from the monitored folder.
Build: pyinstaller -F quarantine-file.py  (run as a NON-admin user)
Lab use only. Hard-coded paths are for the test environment.
"""
import os
import glob

file_patterns = [
    r'C:\Users\Admin\Downloads\Wazuh-Agent\*.exe',
    r'C:\Users\Admin\Downloads\Wazuh-Agent\*.bat',
    r'C:\Users\Admin\Downloads\Wazuh-Agent\*.com',
    r'C:\Users\Admin\Downloads\Wazuh-Agent\eicar.*',
]

for pattern in file_patterns:
    # glob.glob finds all pathnames matching the pattern
    for file in glob.glob(pattern):
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except OSError as e:
            print(f"Error deleting {file}: {e}")
