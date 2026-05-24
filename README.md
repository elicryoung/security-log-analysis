# Security Log Analysis (Project 1)

# Phase 1 — Environment Setup

During Phase 1 of this project, I focused on building a structured environment for learning and analysing security logs in a way that reflects real SOC analyst workflows. Since this is my first hands-on cybersecurity project, the emphasis was on understanding how analysts organise evidence, document findings, and prepare datasets before beginning active investigation work.

I configured Visual Studio Code as my primary workspace and installed extensions for log viewing, XML formatting, and Markdown documentation. This provided a much cleaner workflow for reading large log files and maintaining organised investigation notes throughout the project.

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
**AFTERTHOUGHT**
I completely disregarded this in the end and decided to just have a big markdown cell of my findings, as I went along i realised that the template was pretty useless as I didn't really know what i was getting myself in for and noting my findings after each phase/section depending on what i did in each of them was easier and more showing of the work I was doing.

Finally, I connected the project to a GitHub repository using Git on macOS and configured a `.gitignore`. I decided to not add the raw logs in this because i was able to download them for testing purposes, and if anyone wants to do this project they also could just search for th files online, however I must stress if these were real logs I would have added them to the git ignore. This reinforces the importance of handling security data responsibly while still maintaining version-controlled documentation and analysis notes.

By the end of Phase 1, I had prepared a complete working environment with realistic Windows and Linux security datasets, an organised documentation workflow, and a portfolio-ready project structure prepared for deeper log analysis in later phases.

# Phase 2

## Section 1: MSSQL Failed Authentication Log Analysis

For the first part of Phase 2, I analysed a Windows EVTX log file containing Microsoft SQL Server authentication failures. Since this was my first time working directly with Windows event logs, the initial challenge was simply understanding how Windows stores and structures logging data.

The dataset analysed was:

1.MSSQL_multiple_failed_logon_EventID_18456.evtx

One of the first things I learned was that Windows EVTX files are stored in a binary format rather than plain text. Because of this, the file could not be opened directly inside VS Code. To make the data readable, I converted the EVTX file into XML format using the python-evtx library inside a Python virtual environment on macOS. This gave me my first practical experience handling Windows security telemetry.

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

## Section 2: DACL and DCSync Rights Analysis

This dataset was a lot harder to understand than the first Windows log I analysed because there was far less plain-English information inside the events. Instead of obvious failed logins, this log was focused on Active Directory object access and permission changes, so most of the investigation involved trying to figure out what the different fields and operation values actually meant.

The dataset analysed was:

2.DACL_DCSync_Right_Powerview_Add-DomainObjectAcl.evtx

After converting the EVTX file into XML format, I quickly realised manually scrolling through the logs was not practical because there was too much data and many of the events looked almost identical at first glance. This was the point where I started relying much more on Linux commands to filter the logs and identify patterns.

The first thing I wanted to understand was which Event IDs appeared most often, so I used:

bash grep "<EventID" dcsync.xml | sort | uniq -c 

This command searches for every Event ID in the file, sorts the output, and counts how many times each unique Event ID appears.

The output was:

text 1  <EventID Qualifiers="">1102</EventID> 9  <EventID Qualifiers="">4662</EventID> 18 <EventID Qualifiers="">5136</EventID> 

From this, I decided to focus mostly on Event IDs 4662 and 5136 because they appeared much more frequently than the others.

I then started looking at usernames inside the logs using:

bash grep -i "SubjectUserName" dcsync.xml | sort | uniq -c 

which returned:

text 27 <Data Name="SubjectUserName">bob</Data> 1  <SubjectUserName>bob</SubjectUserName> 

At that point it became obvious that most of the activity in the dataset was connected to the user bob.

I also checked the Logon IDs using:

bash grep -i "SubjectLogonId" dcsync.xml | sort | uniq -c 

which returned:

text 27 <Data Name="SubjectLogonId">0x00000000040f2719</Data> 1  <SubjectLogonId>0x00000000008d7099</SubjectLogonId> 

I had no idea what a SubjectLogonId was initially, so I ended up Googling it and reading Microsoft documentation. After researching it, I learned that it acts like a session identifier that can be used to correlate related activity together. Since the same Logon ID kept appearing, it suggested that most of the actions were tied to the same authenticated session.

I then looked at the operation types with:

bash grep -i "OperationType" dcsync.xml | sort | uniq -c 

which gave:

text 9 <Data Name="OperationType">%%14674</Data> 9 <Data Name="OperationType">%%14675</Data> 9 <Data Name="OperationType">Object Access</Data> 

Again, I had to Google what %%14674 and %%14675 actually meant because Windows logs contain a lot of operation codes that are not immediately readable. This part of the investigation honestly slowed me down quite a bit because almost every unfamiliar field required more research before I understood its importance.

One of the events that stood out most during the investigation was:

xml <Data Name="SubjectUserName">bob</Data> <Data Name="ObjectDN">DC=insecurebank,DC=local</Data> <Data Name="AttributeLDAPDisplayName">nTSecurityDescriptor</Data> <Data Name="OperationType">%%14675</Data> 

This event stood out because it showed the account bob modifying the nTSecurityDescriptor attribute on the Active Directory domain object itself.

At first, the massive AttributeValue field looked completely unreadable because it was filled with GUIDs, permissions, and security descriptor strings. I ended up researching several of the GUID values individually to try and understand what permissions were being modified.

This was also where I started coming across references to DCSync-related permissions and replication rights. Once I understood that nTSecurityDescriptor relates to Active Directory security permissions, the overall purpose of the dataset became much clearer.

The investigation appeared to simulate:
- Active Directory permission modification
- DACL changes
- replication-related permission changes
- possible DCSync preparation activity

One thing I found difficult during this investigation was how overwhelming Windows security events can look initially. A lot of the important information is buried inside very long XML fields, GUIDs, and operation codes, so understanding the logs involved a lot of Googling, reading documentation, and slowly piecing together what the events actually meant.

This section also felt like the point where I started becoming more comfortable using Linux command-line tools for investigations instead of manually reading logs line by line. Using grep, sort, uniq, and wc made it much easier to identify repeated usernames, repeated session IDs, and repeated operation types across the dataset.

If this were a real investigation, the next thing I would want to investigate would be exactly which permissions were added or removed from the domain object and whether the account bob was authorised to make those changes.

Overall, this dataset was much harder than the first authentication log analysis, but it gave me a much better understanding of how Active Directory permission abuse and DCSync-related activity can appear inside Windows event logs.