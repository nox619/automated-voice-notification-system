# Automated Voice Notification System

A production-style backend voice notification system built using **FastAPI, FreeSWITCH, Python, Zoiper, SQLite, and Docker**.

This system automatically places SIP calls, converts dynamic text messages into voice notifications using TTS, supports batch notification workflows with retry handling, records calls, and logs delivery metadata into a persistent database.

---

## Features

- Dynamic text-to-speech notifications using **eSpeak**
- Outbound SIP call origination via **FreeSWITCH ESL**
- RTP audio delivery to registered SIP clients
- Batch notifications using **REST API**
- Automatic retry mechanism for failed recipients
- **SQLite-based persistent logging**
- Per-call status and retry attempt tracking
- **Call recording support**
- **Dockerized FastAPI backend**
- Persistent shared volume support for audio + database

---

## Tech Stack

- Python
- FastAPI
- FreeSWITCH
- SIP / RTP
- Zoiper
- SQLite
- eSpeak
- Docker
- Git / GitHub

---

## Architecture

```text
FastAPI Backend (Docker)
        ↓
Generate TTS WAV
        ↓
Shared Audio Volume
        ↓
FreeSWITCH ESL Socket
        ↓
SIP Call Origination
        ↓
Zoiper / SIP Endpoint
        ↓
SQLite Logging + Recordings
```


## API Endpoints
Send single notification
POST /notify

Example payload:

{
  "extension": "1001",
  "message": "Hello, this is a voice notification"
}


Send batch notifications
POST /notify-batch
View logs
GET /logs
Current Status

✅ MVP completed with:

dynamic TTS
batch notifications
retries
database logging
call recording
FastAPI REST API
Docker deployment
Future Improvements
scheduled notifications
analytics dashboard
async task queue
cloud deployment
