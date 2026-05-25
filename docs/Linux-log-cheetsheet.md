# Understanding Linux Log Structure

While working through the Linux authentication logs, I realised that I was beginning to recognise suspicious patterns without fully understanding how Linux log entries were actually structured. Since the same fields and formats kept appearing throughout the investigations, I decided to properly break down how Linux logs are organised and which parts are most important during analysis.

One thing I noticed early on is that Linux logs are much less structured than Windows XML logs. Instead of neatly separated fields, most Linux logs are plain text entries written in a standard format.

A typical log entry looked like this:

```text id="y9v0ms"
Jul 10 16:01:43 combo sshd(pam_unix)[30530]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=150.183.249.110 user=root
```

At first this looked chaotic, but after breaking it down piece by piece, it became much easier to understand.

---

# Linux Log Structure Breakdown

## Timestamp

Example:

```text id="wd9d7h"
Jul 10 16:01:43
```

The timestamp tells you when the event occurred.

This became one of the most important parts of Linux log analysis because investigations often depend on reconstructing timelines and identifying sequences of activity.

During the brute-force investigation, I used timestamps to identify:
- rapid login attempts
- attack waves
- repeated behaviour patterns
- simultaneous events

One thing I noticed is that Linux timestamps are usually less precise than Windows logs because they often only record to the nearest second.

---

## Hostname

Example:

```text id="2mg0x8"
combo
```

This identifies the Linux system where the event occurred.

In enterprise environments, this becomes important because logs are often collected centrally from many systems.

The hostname helps analysts identify:
- which server was targeted
- where suspicious activity occurred
- how events relate across systems

---

## Service / Process Name

Example:

```text id="kwd6s7"
sshd
```

This tells you which service generated the log entry.

Examples I encountered:
- sshd
- su
- login
- pam_unix

This became one of the fastest ways to identify what type of activity was happening.

For example:
- `sshd` → SSH authentication activity
- `su` → user switching / privilege escalation
- `login` → interactive logins
- `pam_unix` → authentication module activity

---

## Authentication Module

Example:

```text id="g5o6xk"
pam_unix
```

`pam_unix` refers to the Linux PAM (Pluggable Authentication Module) system.

I learned that PAM handles authentication and session management in Linux systems.

This means many authentication-related events will appear through PAM modules.

Examples include:
- authentication failures
- session openings
- privilege escalation
- account switching

---

## Process ID (PID)

Example:

```text id="v0n5hc"
[30530]
```

This is the process ID of the service handling the event.

During the SSH brute-force investigation, I noticed the PIDs increased rapidly during attack bursts:

```text id="3g5kt9"
[30530]
[30532]
[30534]
[30535]
```

This helped me understand that the SSH daemon was spawning many authentication processes quickly, which strongly suggested automated activity.

PIDs can help:
- track process sequences
- correlate related activity
- identify process spawning behaviour

---

## Event Message

Example:

```text id="9kzv8u"
authentication failure
```

This describes what actually happened.

Examples I encountered:
- authentication failure
- session opened
- session closed

This became one of the most useful parts of the logs because it directly described the activity being performed.

---

# Authentication Fields

After the event message, Linux logs often contain additional key-value fields.

These became extremely important during investigations.

---

## uid / euid

Example:

```text id="0tq4xk"
uid=0 euid=0
```

These refer to:
- real user ID
- effective user ID

I learned that:
- `0` = root

This means the process was running with root privileges.

This becomes important during privilege escalation investigations because attackers often attempt to gain root-level access.

---

## tty

Example:

```text id="r3b2jq"
tty=NODEVssh
```

This refers to the terminal or session type associated with the event.

`NODEVssh` appeared frequently in SSH authentication logs.

While I did not rely heavily on this field during investigations, it helped identify that the activity was occurring through SSH sessions rather than local console access.

---

## ruser

Example:

```text id="1xq3wh"
ruser=
```

This field refers to the remote username initiating the authentication request.

In many of the brute-force attempts, this field was blank.

---

## rhost

Example:

```text id="2p1u9s"
rhost=150.183.249.110
```

This became one of the highest-value fields during Linux investigations.

`rhost` identifies the remote host or IP address attempting access.

During the SSH brute-force investigation, I used this field extensively to:
- identify attackers
- count repeated login attempts
- identify attack sources
- correlate attack waves

I eventually used Linux command pipelines to extract and count these values:

```bash
grep -i "authentication failure" Linux_2k.log | grep -o 'rhost=[^ ]*' | cut -d= -f2 | sort | uniq -c | sort -nr | head
```

This helped me quickly identify the most aggressive attacking hosts.

---

## user

Example:

```text id="6qz0m7"
user=root
```

This field identifies the target account involved in the authentication attempt.

One thing I noticed quickly was that attackers repeatedly targeted predictable usernames such as:
- root
- test
- admin

This helped me understand why privileged accounts are such common targets during brute-force attacks.

---

# Session Activity

Another important type of Linux authentication event involved session management.

Example:

```text id="s7r2zt"
session opened for user test by (uid=509)
```

This indicates that authentication succeeded and a session was successfully created.

This became extremely important because investigations are not only about identifying failed attempts — they are also about determining whether attackers successfully gained access.

During analysis, I searched for:
- `session opened`
- `accepted`

to determine whether suspicious authentication attempts succeeded.

---

# Understanding Linux Investigation Workflow

One of the biggest things I learned during this side investigation was that Linux log analysis is heavily focused on:
- filtering
- extracting
- counting
- correlating
- reducing noise

Unlike Windows XML logs, Linux logs are much less structured, so analysts rely heavily on command-line tools to transform raw logs into something easier to investigate.

As the project progressed, I started naturally thinking in terms of:
- extracting fields
- identifying repeated patterns
- correlating timestamps
- separating normal behaviour from suspicious behaviour

rather than simply searching for keywords.

---

# Key Takeaways

The biggest thing I learned from this side investigation was that Linux logs initially look overwhelming because everything is written as plain text rather than structured XML. Once I understood the meaning of the common fields though, the logs became much easier to interpret.

The fields that became most useful during investigations were:
- timestamp
- service name
- process ID
- authentication result
- rhost
- user
- session activity

Understanding these fields made it much easier to:
- identify brute-force attacks
- investigate SSH activity
- recognise privilege escalation behaviour
- reconstruct authentication timelines
- separate normal system behaviour from suspicious activity

This side investigation helped me feel much more confident reading raw Linux authentication logs because I finally understood what the individual parts of each event were actually telling me.