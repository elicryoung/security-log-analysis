# side_quest.md

## Understanding Windows Event Log Structure

While working through the Windows EVTX datasets, I realised I was recognising patterns in the logs without fully understanding what all of the Windows event fields actually meant. Since the same fields kept appearing in every event, I decided to take some time to properly break down the structure of a Windows event log and understand which fields actually matter during investigations.

One thing I learned quickly is that Windows events are generally split into two main sections:

- System
- EventData

The System section contains metadata about the event itself, while the EventData section contains the actual investigation details.

---

# System Section Breakdown

## Provider

Example:

xml <Provider Name="Microsoft-Windows-Sysmon"> 

The provider tells you which service or application generated the event.

Examples I encountered during the project:
- Microsoft-Windows-Security-Auditing
- Microsoft-Windows-Sysmon
- MSSQLSERVER

This matters because different providers generate completely different types of telemetry.

For example:
- Security-Auditing logs authentication and security activity
- Sysmon logs detailed process and system activity
- MSSQLSERVER logs SQL Server events

---

## EventID

Example:

xml <EventID>1</EventID> 

This is one of the most important fields in Windows logging because it tells you what type of activity occurred.

Examples I encountered:
- 18456 → SQL Server failed login
- 4662 → Object access
- 5136 → Directory object modified
- 1 (Sysmon) → Process creation

Most Windows investigations start with identifying the Event ID first.

---

## Version

Example:

xml <Version>5</Version> 

The version refers to the schema version of the event.

From what I researched, this is mostly used for compatibility and tooling rather than investigations. I did not find it very useful during analysis.

---

## Level

Example:

xml <Level>4</Level> 

The level represents the severity or importance of the event.

Common values:
- 1 → Critical
- 2 → Error
- 3 → Warning
- 4 → Informational

Most Sysmon logs I encountered used Level 4 because they are informational telemetry rather than system errors.

---

## Task

Example:

xml <Task>1</Task> 

The task field categorises the type of operation internally.

For Sysmon logs, Task 1 was associated with process creation events.

I found that Event IDs were generally much more useful than Task values during investigations.

---

## Opcode

Example:

xml <Opcode>0</Opcode> 

From my research, Opcode describes the type or state of the operation.

I did not use this field much during analysis because it did not add much context to the investigations I was performing.

---

## Keywords

Example:

xml <Keywords>0x8000000000000000</Keywords> 

Keywords appear to be internal Microsoft categorisation flags used for filtering and indexing events.

I mostly ignored this field during investigations because it was not very useful from a practical SOC analysis perspective.

---

## TimeCreated

Example:

xml <TimeCreated SystemTime="2019-05-24 01:33:53.112486+00:00"> 

This is one of the most important fields in any investigation because it tells you exactly when the event occurred.

This becomes critical when reconstructing attack timelines.

---

## EventRecordID

Example:

xml <EventRecordID>1044</EventRecordID> 

This acts like the log entry number for the event.

It can help:
- order events chronologically
- identify missing events
- track investigation sequences

---

## Channel

Example:

xml <Channel>Microsoft-Windows-Sysmon/Operational</Channel> 

The channel shows which Windows log source stored the event.

Examples I encountered:
- Security
- Application
- System
- Microsoft-Windows-Sysmon/Operational

This helps identify where the telemetry originated from.

---

## Computer

Example:

xml <Computer>IEWIN7</Computer> 

This identifies the host machine where the activity occurred.

This becomes especially important in enterprise investigations involving multiple systems.

---

# EventData Section Breakdown

The EventData section is where most of the actual investigation happens.

This section contains:
- usernames
- process names
- command lines
- IP addresses
- parent processes
- file paths
- permissions
- security context information

---

## Image

Example:

xml <Data Name="Image">C:\Windows\System32\cmd.exe</Data> 

This tells you which executable was launched.

This is one of the highest-value fields during process investigations.

---

## CommandLine

Example:

xml <Data Name="CommandLine">"c:\windows\system32\cmd.exe" /c net user</Data> 

The command line shows exactly what command was executed.

This field is extremely important because it reveals attacker behaviour rather than just process names.

For example:
- whoami
- net user
- ipconfig
- PowerShell commands

can all indicate reconnaissance activity.

---

## User

Example:

xml <Data Name="User">IIS APPPOOL\DefaultAppPool</Data> 

This shows which account or security context executed the process.

In one of the Sysmon events I analysed, the IIS application pool account was launching cmd.exe, which immediately stood out as suspicious.

---

## ParentImage

Example:

xml <Data Name="ParentImage">C:\Windows\System32\inetsrv\w3wp.exe</Data> 

This field shows which process launched the child process.

This introduced me to one of the most important SOC concepts:

text Parent Process → Child Process 

Example:

text w3wp.exe → cmd.exe 

This is suspicious because a web server process normally should not be spawning command shells.

This can indicate:
- webshell activity
- remote code execution
- attacker-controlled commands

---

# Key Takeaways

The biggest thing I learned from this side investigation was that Windows logs initially look much more complicated than they actually are. A lot of the metadata fields are useful for context, but most investigations eventually focus on a smaller number of important fields such as:
- EventID
- TimeCreated
- Image
- CommandLine
- User
- ParentImage
- Computer

Once I understood the purpose of these fields, reading Windows logs became much less overwhelming and much easier to follow during investigations.