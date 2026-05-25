# PROJECT 1: Security Event Log Analysis

---
Find my analysis and write ups in the docs folder
---

## Project Overview

| Attribute | Details |
|-----------|---------|
| **Difficulty** | Beginner |
| **Time Estimate** | 1 week (2-4 hours/day, ~15-20 hours total) |
| **When to Build** | Week 1 - Start immediately alongside Network+ study |
| **Prerequisites** | None - designed for absolute beginners |

**What You'll Build:** A collection of analyzed Windows and Linux security logs with documented findings, pattern recognition notes, and a personal reference guide for common security events.

**Why This Matters:** Log analysis is 60-70% of a SOC analyst's daily work. Before touching any fancy tools, you need to understand what you're looking at. This project builds the foundational skill of reading and interpreting raw security data.

---

## Tech Stack (All Free, Mac-Compatible)

| Tool | Purpose | Installation |
|------|---------|--------------|
| **Terminal** | Built into Mac - primary interface | Already installed |
| **grep, awk, sed** | Text processing and log parsing | Already installed on Mac |
| **VS Code** | Viewing and annotating log files | Download from code.visualstudio.com |
| **Sample Log Files** | Practice material | Downloaded from security datasets |
| **Obsidian or Notes** | Documentation and pattern notes | Your choice |

**No virtual machines needed for this project** - you're analyzing static log files on your Mac.

---

## Learning Objectives

### Technical Skills
- Read and interpret Windows Event Log format (XML-based)
- Read and interpret Linux syslog format
- Use command-line tools (grep, awk, cut) to filter and search logs
- Identify timestamps, event IDs, source systems, and user accounts in logs
- Correlate related events across time

### Security Concepts
- Windows Event ID categories (logon, logoff, privilege use, process creation)
- Linux authentication logs (auth.log, secure)
- Common attack indicators in logs (brute force, privilege escalation, lateral movement)
- The difference between noise and signal in security logs
- Baseline understanding - what "normal" looks like

### Interview Ammunition
- "I can read raw Windows and Linux security logs without relying on SIEM queries"
- "I understand the key Event IDs that indicate potential compromise"
- "I've documented analysis of brute force attacks, privilege escalation, and suspicious logon patterns"
- Demonstrate understanding of WHAT logs contain and WHY specific events matter

---

## Build Phases

### Phase 1: Environment Setup (Day 1, ~2 hours)
- Install VS Code with log viewing extensions
- Download sample Windows Event Logs (EVTX format)
- Download sample Linux logs (auth.log, syslog samples)
- Set up a folder structure for organising findings
- Create your documentation template

### Phase 2: Windows Event Log Fundamentals (Days 2-3, ~6 hours)
- Learn Windows Event Log structure (XML format, key fields)
- Study the critical Event IDs every SOC analyst must know
- Analyze sample logs for authentication events (4624, 4625, 4634)
- Analyse sample logs for privilege use (4672, 4673)
- Analyse sample logs for process creation (4688)
- Document patterns and create your reference sheet

### Phase 3: Linux Log Fundamentals (Days 4-5, ~6 hours)
- Learn syslog format and structure
- Understand auth.log and secure log contents
- Analyse sample Linux authentication logs
- Look for SSH brute force patterns
- Look for sudo abuse and privilege escalation indicators
- Compare Linux and Windows logging approaches

### Phase 4: Pattern Recognition & Correlation (Days 6-7, ~6 hours)
- Work through scenario-based log samples (CTF-style)
- Practice identifying attack patterns across multiple log entries
- Create timeline reconstructions from log data
- Build your personal "cheat sheet" of suspicious patterns
- Complete portfolio documentation

---

## Key Challenges & Learning Moments

### What Will Be Hard
- **Information overload**: Security logs are verbose. You'll see thousands of entries and need to find the 5 that matter.
- **Understanding context**: Event ID 4624 (successful logon) isn't suspicious alone - but 500 of them in 1 minute from different usernames is.
- **Timestamp correlation**: Piecing together a story from events scattered across time requires patience.

### What's Important to Understand
- **Logs tell stories**: Your job is to reconstruct what happened, when, and by whom
- **False positives are normal**: Most alerts and suspicious-looking entries are benign. Learning to filter noise is the skill.
- **Event IDs are your vocabulary**: Memorising key Event IDs is like learning words in a language - you need them to communicate
- **Context matters more than content**: A single event means nothing without understanding what came before and after

---

## Deliverables (For Your Portfolio)

1. **Windows Event ID Reference Guide** (Markdown or PDF)
   - Top 20 Event IDs for security monitoring
   - What each ID means in plain English
   - When each ID becomes suspicious (with examples)

2. **Linux Log Analysis Reference Guide** (Markdown or PDF)
   - Key log files and their purposes
   - Common attack patterns in auth.log
   - Useful grep/awk commands for log analysis

3. **3 Completed Log Analysis Write-ups**
   - Each should be 1-2 pages
   - Include: timeline, findings, indicators of compromise
   - Format like a real SOC analyst report

4. **Command Line Cheat Sheet**
   - Your personal collection of useful log parsing commands
   - Tested on real log samples

5. **GitHub Repository** (optional but recommended)
   - Upload your reference guides and write-ups
   - Demonstrates documentation skills to employers

---

## Learning Resources

### Read BEFORE Starting
- Microsoft Docs: "Windows Security Log Events" (just the overview)
- SANS: "Windows Event Log Reference" poster (free download)
- Linux man pages for syslog (man syslog)

### Use DURING the Project
- Ultimate Windows Security: ultimatewindowssecurity.com/securitylog/encyclopedia
- SANS Event ID Quick Reference Cards
- Your certification study materials (Network+ touches on logging basics)

### Sample Log Sources
- Mordor Project: github.com/OTRF/mordor (attack simulation datasets)
- EVTX-ATTACK-SAMPLES: github.com/sbousseaden/EVTX-ATTACK-SAMPLES
- SecRepo: secrepo.com (security data samples)

---

## Common Pitfalls

| Pitfall | Why It Happens | How to Avoid |
|---------|---------------|--------------|
| Trying to memorise every Event ID | There are thousands | Focus on top 20-30 security-relevant IDs |
| Getting lost in the data | Logs are overwhelming | Always start with a specific question to answer |
| Skipping the "boring" logs | Normal activity seems pointless | Understanding normal is how you spot abnormal |
| Not documenting as you go | Seems faster to just analyse | You WILL forget what you found - write it down immediately |
| Using only GUI tools | Feels easier | Command line skills are expected in interviews |

---

## Self-Assessment Questions

Before moving to Project 2, you should be able to answer these:

### Windows Events
1. What Event ID indicates a successful logon? What about a failed logon?
2. What's the difference between Logon Type 2 and Logon Type 10?
3. How would you identify a brute force attack in Windows Security logs?
4. What Event ID shows when a user was added to a privileged group?
5. Why is Event ID 4688 (process creation) valuable for threat hunting?

### Linux Logs
1. What file contains SSH authentication attempts on most Linux systems?
2. What does a successful SSH login look like in auth.log?
3. How would you grep for all failed SSH attempts?
4. What's the difference between su and sudo, and how do they log differently?
5. How would you identify a brute force SSH attack in the logs?

### General Skills
1. Given a log file, can you reconstruct a timeline of events?
2. Can you explain the difference between a log and an alert?
3. What makes an event "suspicious" vs just "unusual"?

---

## Claude Context Instructions

**Copy everything below this line into a new Claude chat when starting this project:**

---

CONTEXT FOR CLAUDE - PROJECT 1: SECURITY EVENT LOG ANALYSIS

I'm working on Project 1 of my SOC Analyst preparation - Security Event Log Analysis. This is my first project and I have ZERO prior security or networking knowledge.

MY SITUATION:
- Just finished CS Master's but learned nothing practical about security
- Starting from absolute zero with logs, security events, and analysis
- Working on a Mac
- Have 2-4 hours per day for this project
- Goal: Complete in 1 week

WHAT I'M BUILDING:
- Windows Event ID reference guide
- Linux log analysis reference guide  
- 3 completed log analysis write-ups
- Command line cheat sheet for log parsing

MY LEARNING PHILOSOPHY:
- I want to understand WHY, not just copy commands
- If I'm stuck, point me to documentation and ask diagnostic questions
- Don't give me walls of text - break things into digestible chunks
- Challenge me with questions to test understanding
- Treat me like a junior analyst learning the ropes

TOOLS I HAVE:
- Mac Terminal (grep, awk, sed, etc.)
- VS Code
- Sample log files (I'll download as needed)

WHERE I AM IN THE PROJECT:
[UPDATE THIS AS YOU PROGRESS]
- [ ] Phase 1: Environment Setup
- [ ] Phase 2: Windows Event Log Fundamentals  
- [ ] Phase 3: Linux Log Fundamentals
- [ ] Phase 4: Pattern Recognition & Correlation

CURRENT PHASE: [Tell Claude which phase you're on]

Please help me work through this project step by step. Start by confirming you understand my context, then guide me through my current phase.

---

## Progress Checklist

### Phase 1: Environment Setup
- [ ] VS Code installed with log viewing extensions
- [ ] Folder structure created for project
- [ ] Windows sample logs downloaded (at least 2 EVTX files)
- [ ] Linux sample logs downloaded (auth.log samples)
- [ ] Documentation template created

### Phase 2: Windows Event Log Fundamentals
- [ ] Understand Windows Event Log XML structure
- [ ] Know the 5 most critical security Event IDs
- [ ] Know the 10 additional important Event IDs
- [ ] Analysed authentication events in sample logs
- [ ] Analysed privilege use events in sample logs
- [ ] Analysed process creation events in sample logs
- [ ] Created Windows Event ID reference guide

### Phase 3: Linux Log Fundamentals
- [ ] Understand syslog format
- [ ] Know which files contain authentication logs
- [ ] Analysed SSH authentication patterns
- [ ] Identified brute force indicators
- [ ] Identified privilege escalation indicators
- [ ] Created Linux log reference guide

### Phase 4: Pattern Recognition & Correlation
- [ ] Completed at least 3 scenario-based analyses
- [ ] Created timeline reconstruction from logs
- [ ] Built personal "suspicious patterns" cheat sheet
- [ ] Wrote up 3 analysis reports for portfolio
- [ ] Answered all self-assessment questions correctly

---

**Project Complete When:** All checklist items done, all self-assessment questions answered correctly, and 3 portfolio-ready analysis write-ups created.

**Next Project:** Project 2 - Basic Network Traffic Analysis
