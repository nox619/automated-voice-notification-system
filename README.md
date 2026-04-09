# Automated Voice Notification System

A backend voice notification system built using FreeSWITCH, Python, Zoiper, and SQLite.

This system automatically places SIP calls, converts text messages into voice notifications using TTS, supports batch notification workflows, retries failed calls, and logs delivery metadata into a database.

---

## Features

- Dynamic text-to-speech notifications using eSpeak
- Outbound SIP call origination via FreeSWITCH ESL
- RTP audio delivery to registered SIP clients
- Batch notifications using CSV input
- Automatic retry mechanism for failed recipients
- SQLite-based persistent logging
- Per-call status and retry attempt tracking

---

## Tech Stack

- Python
- FreeSWITCH
- SIP / RTP
- Zoiper
- SQLite
- eSpeak
- Git / GitHub

---

## Architecture

```text
Python Backend
    ↓
Generate TTS WAV
    ↓
FreeSWITCH ESL
    ↓
SIP Call Origination
    ↓
Zoiper / SIP Endpoint
    ↓
SQLite Logging
```

---

## Current Status

MVP completed with:

- dynamic TTS
- batch notifications
- retries
- database logging

Next phase:

- REST API using FastAPI
- Docker deployment
- call analytics dashboard
