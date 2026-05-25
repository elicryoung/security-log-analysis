---
title: Security Log Analysis Portfolio
subtitle: Windows & Linux Security Event Investigation
author: Eli Young
project: 1 of 4
---

# Security Log Analysis  
## SOC Analyst Practical Investigation Portfolio

---

# Contents

1. Phase 1 — Environment Setup  
2. Phase 2 — Windows Event Log Fundamentals  
   - MSSQL Failed Authentication Analysis  
   - DACL & DCSync Rights Analysis  
   - IIS Webshell & Sysmon Investigation  
3. Phase 3 — Linux Authentication & SSH Analysis  

---

# Phase 1  
## Environment Setup

During Phase 1 of this project, I focused on building a structured and realistic environment for learning security log analysis. As this was my first hands-on cybersecurity project, the priority was not only learning how logs work, but also understanding how analysts organise investigations, document findings, and manage evidence in a professional workflow.

A dedicated working environment was created using Visual Studio Code on macOS, alongside extensions for:
- XML formatting
- large log viewing
- Markdown documentation

This significantly improved readability when working with verbose security telemetry and helped establish a cleaner investigative workflow from the beginning.

A structured project directory named `security-log-analysis` was then created, separating:
- Windows datasets
- Linux datasets
- analyst notes
- investigation write-ups
- documentation

This mirrored the type of organisation expected during real-world investigations and reinforced the importance of separating raw evidence from analysis material.


## Windows Security Datasets

Multiple Windows EVTX datasets were collected for investigation practice, including:

| Dataset | Investigation Theme |
|---|---|
| MSSQL Failed Logons | Authentication attacks |
| DCSync & ACL Abuse | Active Directory permission abuse |
| IIS Webshell & Sysmon | Post-exploitation process telemetry |

These datasets were chosen because they simulate realistic attack scenarios commonly investigated within SOC environments.


## Linux Security Datasets

Linux authentication datasets were also collected, including:
- raw authentication logs
- structured CSV variants
- parsed log templates

This provided an opportunity to compare:
- raw telemetry analysis
- structured security data
- detection-oriented log formatting

The raw logs were later used for command-line investigations using:
- `grep`
- `cut`
- `sort`
- `uniq`
- `awk`

while the structured datasets helped demonstrate how telemetry can be transformed into searchable security data.


## Documentation & Reporting Workflow

Initially, I created a reusable Markdown reporting template designed for:
- investigation objectives
- findings
- timeline reconstruction
- indicators of compromise
- final assessment summaries

However, as the project progressed, I realised a rigid reporting structure did not fit the way I was naturally learning and investigating.

Instead, I shifted towards maintaining large evolving Markdown investigation notes throughout each phase. This approach allowed me to:
- document thought processes in real time
- record investigative mistakes
- explain why certain commands were used
- track how understanding developed over time

In hindsight, this produced a much more authentic representation of the investigation process than a heavily templated report


## Version Control & Operational Practice

The project was connected to GitHub using Git on macOS, alongside the creation of a `.gitignore` file.

The raw log datasets themselves were intentionally excluded from the repository because they were publicly downloadable training datasets. However, if these had been genuine organisational logs, they would have been excluded entirely for security and privacy reasons.

This reinforced an important operational lesson:
security data should always be handled carefully, even within training environments.

---

## Outcome

By the end of Phase 1, the project environment included:
- organised Windows and Linux security datasets
- structured documentation workflows
- version-controlled investigation notes
- a repeatable analyst workspace
- portfolio-ready project foundations

Most importantly, this phase established the investigative workflow that would later be used throughout the Windows and Linux analysis sections.

---

# Phase 2  
# Windows Event Log Fundamentals

---

# Section 1  
## MSSQL Failed Authentication Analysis

### Dataset
`1.MSSQL_multiple_failed_logon_EventID_18456.evtx`



This investigation focused on analysing Microsoft SQL Server authentication failures within Windows Event Logs.

One of the first challenges encountered was understanding that Windows EVTX files are stored in a binary format rather than plain text. Because of this, the dataset could not be read directly inside Visual Studio Code and first needed to be converted into XML format using the `python-evtx` library within a Python virtual environment on macOS. To do this I made a simple `convert.py` file to change the formatting.

This provided an initial understanding of how Windows security telemetry is stored and processed.



## Initial Observations

After converting the dataset, one behavioural pattern became immediately obvious:

The logs contained repeated authentication failures targeting multiple administrator-style accounts.

Examples included:
- `sa`
- `root`
- `##MS_*`

The repeated targeting of privileged account names strongly suggested automated credential attacks rather than normal user behaviour.



## Indicators of Suspicious Behaviour

Several indicators pointed towards brute-force or credential enumeration activity:

| Observation | Why It Was Suspicious |
|---|---|
| Repeated Event ID 18456 | Continuous SQL authentication failures |
| Multiple usernames targeted | Credential enumeration behaviour |
| Millisecond-level timestamps | Automated execution |
| Single source IP repeated | Centralised attack source |

Source IP identified repeatedly:
`10.0.2.17`

The rapid timing between events suggested the authentication attempts were being executed programmatically rather than manually.



## Key Learning Points

This investigation introduced several foundational concepts:
- Windows Event Log structure
- authentication telemetry
- event correlation
- behavioural analysis
- recognising brute-force indicators

It also reinforced an important analytical principle:

- Individual events rarely matter on their own.  
- Patterns across events are what tell the story.

---

# Section 2  
## DACL & DCSync Rights Analysis

### Dataset
`2.DACL_DCSync_Right_Powerview_Add-DomainObjectAcl.evtx`



This dataset was significantly more difficult to analyse than the MSSQL authentication logs because the activity involved Active Directory permissions and object access rather than straightforward authentication failures.

Most of the investigation involved researching:
- unfamiliar operation codes
- LDAP attributes
- GUIDs
- Active Directory security descriptors

Unlike the previous dataset, suspicious activity was not immediately obvious from plain-English log messages.



## Event ID Analysis

To identify which events appeared most frequently, Linux command-line tools were used:

```bash
grep "<EventID" dcsync.xml | sort | uniq -c
```

This revealed repeated occurrences of:
- Event ID 4662
- Event ID 5136

These events became the primary focus of the investigation.



## User & Session Correlation

Further analysis identified repeated activity associated with the account:

```text
bob
```

and a repeated `SubjectLogonId`, indicating that many events were linked to the same authenticated session.

This introduced an important investigative concept:

> Logon IDs allow analysts to correlate related activity across multiple events.



## Active Directory Permission Abuse

One event in particular stood out:

```xml
<Data Name="SubjectUserName">bob</Data>
<Data Name="ObjectDN">DC=insecurebank,DC=local</Data>
<Data Name="AttributeLDAPDisplayName">nTSecurityDescriptor</Data>
```

This indicated that the account `bob` was modifying the `nTSecurityDescriptor` attribute on the Active Directory domain object itself.

After researching the associated GUIDs and permission values, it became clear the activity related to:
- DACL modification
- replication permissions
- potential DCSync preparation activity



## Investigation Challenges

This section highlighted how difficult Windows security events can initially appear.

Many important details were buried inside:
- XML fields
- operation codes
- GUID values
- security descriptor strings

A large portion of the investigation involved:
- researching Microsoft documentation
- validating field meanings
- understanding Active Directory terminology

Although slower, this process significantly improved understanding of:
- Windows object access auditing
- DACL modifications
- replication abuse
- Active Directory attack preparation

---

# Section 3  
## IIS Webshell & Sysmon Process Investigation

### Dataset
`3.LM_typical_IIS_webshell_sysmon_1_10_traces.evtx`



This investigation represented the first point in the project where the analysis felt like tracing actual attacker behaviour rather than simply reviewing logs.

The dataset contained Sysmon process telemetry, including:
- command lines
- parent-child process relationships
- execution chains
- process IDs
- session correlation

Unlike standard Windows Security logs, Sysmon provided significantly richer visibility into process activity.


## Investigative Approach

Rather than manually reading every event, the investigation became question-driven:

- Which processes executed?
- What spawned them?
- Do the process chains make sense?
- Are the events related through a shared Logon ID?
- Does the execution behaviour appear normal?

This represented a major shift in investigative thinking compared to earlier sections.


## Suspicious Process Activity

Several suspicious processes were identified:
- `cmd.exe`
- `net.exe`
- `net1.exe`

alongside the IIS worker process:
- `w3wp.exe`

Command-line analysis revealed:

```cmd
cmd.exe /c net user
```

This command performs Windows account enumeration.

The critical detail, however, was not the command itself — it was the parent process relationship.


## Process Chain Reconstruction

Using process correlation, the following execution chain was reconstructed:

```text
w3wp.exe
 └── cmd.exe
      └── net.exe
           └── net1.exe
```

This strongly suggested:
- webshell activity
- remote command execution
- attacker reconnaissance behaviour

because IIS web server processes should not normally spawn command shells.


## Key Learning Outcome

This section became one of the most important learning milestones in the project because it introduced:
- process tree reconstruction
- parent-child process analysis
- command execution telemetry
- attacker behavioural analysis
- session correlation using Logon IDs

More importantly, it marked the point where investigations became less about identifying Event IDs and more about reconstructing attacker behaviour from telemetry.

---

# Phase 3  
# Linux SSH Brute Force & Authentication Analysis


This phase focused on analysing Linux authentication logs and identifying SSH brute-force behaviour through command-line investigation techniques.

By this stage of the project, Linux log analysis had started becoming far more intuitive. Earlier investigations relied heavily on broad searches and manual scrolling. During this phase, the analysis became much more structured and investigative in nature.


## SSH Authentication Failure Analysis

The investigation began by identifying failed authentication attempts:

```bash
grep -i "authentication failure" Linux_2k.log
```

After extracting remote host values and summarising results, several repeated attacker IP addresses became obvious.

One host stood out immediately:

```text
150.183.249.110
```

with approximately:

```text
80 failed authentication attempts
```

This strongly suggested automated brute-force activity.


## Behavioural Indicators

Several characteristics pointed towards malicious SSH activity:

| Indicator | Observation |
|---|---|
| Rapid timestamps | Attempts occurring every second |
| Repeated usernames | `root` targeted continuously |
| Increasing SSH process IDs | Rapid daemon spawning |
| Multiple source IPs | Distributed brute-force behaviour |

The repeated targeting of:
- `root`
- administrative accounts
- predictable usernames

matched common SSH attack behaviour frequently observed on internet-facing systems.


## Timeline Correlation

The attack activity also appeared in waves.

After one sequence of failed attempts ended, another sequence began from a different source IP roughly 30 minutes later.

This pattern suggested:
- automated scanning infrastructure
- distributed attack sources
- repeated credential attacks over time


## Investigating Successful Access

The investigation later shifted from asking:

> “Are there failed logins?”

to:

> “Did any of these attempts actually succeed?”

Successful session analysis revealed:
- predictable maintenance-style activity
- repetitive automated sessions
- no successful access linked to the suspicious attacker IPs

This distinction became an important analytical lesson:

> Suspicious activity does not automatically mean compromise.


## Workflow Development

One of the most noticeable improvements during this phase was investigative workflow maturity.

Instead of manually reading logs, investigations became focused on:
- extracting fields
- reducing noise
- counting occurrences
- validating hypotheses
- correlating timelines
- distinguishing malicious from legitimate behaviour

The command line stopped feeling like a collection of random tools and started becoming a method for answering investigative questions systematically.

---

# Overall Reflection

This project marked the first time I had worked directly with raw security telemetry across both Windows and Linux systems.

At the beginning, security logs appeared overwhelming and largely unreadable. Over time, the investigation process became significantly more structured and analytical. Eventually leading to me being able to very quickly type out linux commands to be able to effectively and efficiently see patterns and recognise security threats.

The biggest improvement was not memorising Event IDs or Linux commands. 
It was learning how to think like an analyst:
- asking investigative questions
- identifying patterns
- reconstructing timelines
- validating suspicious behaviour
- distinguishing signal from noise

By the end of the project, I was able to:
- analyse Windows and Linux authentication telemetry
- reconstruct process execution chains
- identify brute-force indicators
- investigate Active Directory permission abuse
- correlate related events across sessions
- use Linux command-line tooling for practical log investigations

Most importantly, this project transformed security logs from unreadable data into behavioural evidence that could be interpreted and investigated systematically.

---

*Project completed as part of practical SOC analyst preparation and foundational security operations training.*