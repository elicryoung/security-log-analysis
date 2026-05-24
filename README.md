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

# Phase 2

## Section 1: MSSQL Failed Authentication Log Analysis

For the first part of Phase 2, I analysed a Windows EVTX log file containing Microsoft SQL Server authentication failures. Since this was my first time working directly with Windows event logs, the initial challenge was simply understanding how Windows stores and structures logging data compared to standard text-based Linux logs.

The dataset analysed was:

1.MSSQL_multiple_failed_logon_EventID_18456.evtx

One of the first things I learned was that Windows EVTX files are stored in a binary format rather than plain text. Because of this, the file could not be opened directly inside VS Code. To make the data readable, I converted the EVTX file into XML format using the python-evtx library inside a Python virtual environment on macOS. This gave me my first practical experience handling Windows security telemetry outside of a SIEM platform.

During analysis, what immediately stood out to me was how repetitive the authentication failures were. Almost every event contained the same Event ID (18456), which represents a failed SQL Server login attempt, but the usernames being targeted kept changing rapidly between events.

Some of the usernames observed included:
- sa
- root
- multiple SQL-related accounts beginning with ##MS_

The repeated targeting of administrator-style accounts was one of the first indicators that the activity was likely not normal user behaviour. Accounts such as sa and root are commonly targeted during brute force attacks because they are high-privilege accounts that attackers expect to exist on systems.

Another thing that stood out was the timing of the events. Many authentication attempts occurred within milliseconds of each other, all originating from the same client IP address:

10.0.2.17

This timing pattern was important because it strongly suggested the activity was automated or scripted rather than a human manually attempting passwords. The log data showed a rapid sequence of failed login attempts against multiple accounts in an extremely short time window, which is consistent with brute force or credential enumeration behaviour.

As I continued reading through the events, I started understanding that log analysis is less about reading individual entries and more about identifying behavioural patterns across many entries. A single failed login attempt is usually not suspicious on its own, but repeated failures targeting multiple accounts from the same source system becomes much more significant when viewed as a sequence of activity.

This analysis also helped me better understand the structure of Windows event logs. I became familiar with the distinction between the System section, which contains metadata such as timestamps and Event IDs, and the EventData section, which contains the actual investigation details such as usernames, failure reasons, and client IP addresses.

Some of the most useful fields during analysis were:
- Event ID
- Timestamp
- Username
- Failure reason
- Source client IP
- Host system

By the end of this section, I was able to:
- Convert binary EVTX logs into readable XML
- Identify SQL Server authentication failure events
- Recognise indicators of automated login activity
- Understand how repeated failed logons can indicate brute force behaviour
- Extract useful investigation details from Windows event data

This was my first hands-on experience analysing Windows authentication telemetry, and it gave me a much clearer understanding of how analysts use event logs to reconstruct suspicious activity and identify behavioural patterns within large volumes of security data.

