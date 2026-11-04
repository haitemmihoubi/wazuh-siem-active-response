# wazuh-siem-active-response
Automated threat detection and response with Wazuh: FIM, custom rules, VirusTotal integration, MTTR benchmarking

Automated Threat Detection & Active Response with Wazuh
An end-to-end, open-source detection and response pipeline built on Wazuh 4.12. File Integrity Monitoring (FIM) on a Windows 10 endpoint detects a malicious file, the Wazuh Manager's rule engine decides, and an Active Response script removes the file automatically, with no human in the loop.
> Course project for CS595 (M.S. Cybersecurity). Built and tested in an isolated lab on native OS installs (no VMs) for realistic timings.
Goal
Reduce Mean Time to Respond (MTTR): the time between creation of a malicious file and its neutralization, for organizations without a dedicated SOC.
Architecture
Node	OS	Role
Wazuh Manager	Ubuntu 22.04 LTS	Wazuh Server (rule engine, alert dispatch), Indexer (OpenSearch), Dashboard
Wazuh Agent	Windows 10	FIM on a "Sensitive Folder", forwards events over TLS, runs active-response scripts
```
 Detection                 Decision                  Response
 Windows 10 Agent  ──►  Wazuh Manager rule match ──►  Active-response script
 (FIM, real-time,        (custom XML rules,           executed on the agent
  TLS to manager)         severity >= threshold)       (file deleted)
```
Threat model: the adversary already has initial access to the endpoint. The Manager is the trust anchor; the Agent is a managed, not inherently trusted, entity. All Manager-Agent traffic is TLS-encrypted.
Two response configurations compared
Custom rules + local script (`scripts/quarantine-file.py`): rules match on file creation and name patterns; a small Python script (compiled with PyInstaller) deletes matching files locally.
Custom rules + VirusTotal integration: Wazuh's `virustotal` integration looks up file hashes; confirmed-malicious results trigger Wazuh's `remove-threat` active-response script.
Results
Test: EICAR test file delivered via a simulated phishing page and written into the monitored folder. MTTR = file creation to file deletion, taken from syscheck and active-response records in the dashboard.
Response method	MTTR	Notes
Custom rule + local script	< 1 s	Fast, local, but name/pattern-based so less accurate
Manual (Windows GUI delete)	~5 s	Doesn't scale across many endpoints
VirusTotal integration	5 - 9 s	Hash reputation lookup over API adds latency but is more accurate
See `docs/results.md` for methodology and screenshots.
Repository layout
```
configs/manager/ossec.conf.snippet.xml   Manager: VirusTotal integration + active-response blocks
configs/agent/ossec.conf.fim.xml         Agent: FIM (syscheck) configuration
rules/local\_rules.xml                    Custom detection rules (/var/ossec/etc/rules/)
scripts/quarantine-file.py               Local active-response script (build to .exe)
scripts/build-and-test.ps1               PyInstaller build + EICAR test commands
docs/                                    Setup guide, results, limitations, screenshots
```
Setup (summary)
Full steps in `docs/setup.md`.
Install Wazuh all-in-one on Ubuntu 22.04: `curl -sO https://packages.wazuh.com/4.12/wazuh-install.sh \&\& sudo bash ./wazuh-install.sh -a`
Register the Windows agent (dashboard: Deploy new agent), set the Manager IP, start `WazuhSvc`.
Add the FIM config to the agent, the rules and ossec.conf snippets to the manager, and restart both.
Build and place the response executables in `C:\\Program Files (x86)\\ossec-agent\\active-response\\bin\\`.
Limitations
Detection is only as good as the rule-set; events with no matching decoder or rule trigger nothing.
The agent is a single point of failure: if an attacker stops it, the Manager is blind to that host.
Lab-only, single endpoint, EICAR only. No false-positive or multi-endpoint testing yet.
VirusTotal free tier is rate-limited (4 req/min, 500/day) and not for production use.
Future work
Anomaly detection with ML beyond static rules; multi-endpoint scalability and false-positive testing; agent tamper protection / heartbeat alerting.
Ethics & safety
EICAR is a harmless industry-standard AV test string. Everything was run in an isolated lab I own. Do not run this against systems you don't have authorization to test. Defender real-time protection was disabled only on the lab endpoint for the test.
Credits
`remove-threat` is Wazuh's script from the official documentation (Copyright Wazuh Inc.), used unmodified. Not included in this repo.
