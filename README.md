# Security Log Analysis (Project 1)

# Phase 1 — Environment Setup

During Phase 1 of this project, I focused on building a structured environment for learning and analysing security logs in a way that reflects real SOC analyst workflows. Since this is my first hands-on cybersecurity project, the emphasis was on understanding how analysts organise evidence, document findings, and prepare datasets before beginning active investigation work.

I configured Visual Studio Code as my primary workspace and installed extensions for log viewing, XML formatting, and Markdown documentation. This provided a cleaner workflow for reading large log files and maintaining organised investigation notes throughout the project.

To keep the project structured, I created a dedicated working directory named `security-log-analysis` with separate folders for Windows logs, Linux logs, documentation, and analyst notes. This helped establish good operational habits early, particularly the practice of separating raw evidence from analysis material.

I then collected multiple Windows Event Log datasets in EVTX format, including:
- Microsoft SQL Server failed logon activity
- Active Directory DCSync and ACL abuse activity
- IIS webshell and Sysmon process telemetry

These datasets were selected because they represent realistic authentication, privilege escalation, and post-exploitation scenarios commonly investigated in SOC environments.

For Linux analysis practice, I downloaded a raw authentication log dataset alongside structured CSV variants of the same data. The raw logs will later be used for manual investigation and command-line parsing exercises, while the structured datasets provide insight into how security telemetry can be transformed for detection engineering and analysis workflows.

To support future investigations and portfolio work, I also created a reusable Markdown reporting template containing sections for:
- Investigation objectives
- Key findings
- Timeline reconstruction
- Indicators of compromise
- Final assessment notes

Finally, I connected the project to a GitHub repository using Git on macOS and configured a `.gitignore` file to prevent raw security logs from being publicly uploaded. This reinforced the importance of handling security data responsibly while still maintaining version-controlled documentation and analysis notes.

By the end of Phase 1, I had successfully prepared a complete working environment with realistic Windows and Linux security datasets, an organised documentation workflow, and a portfolio-ready project structure prepared for deeper log analysis in later phases.