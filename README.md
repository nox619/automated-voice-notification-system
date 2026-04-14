
# Automated Voice Notification System

A production-style voice automation and SIP routing system built using **FastAPI, Docker, Kamailio, FreeSWITCH, Python, Zoiper, SQLite, and eSpeak**.

The system automatically places outbound SIP calls, converts dynamic text messages into voice notifications using TTS, routes SIP signaling through Kamailio, handles media playback and recordings using FreeSWITCH, and stores call metadata in SQLite.

---

## Features

- Dynamic text-to-speech notifications using **eSpeak**
- **Kamailio-based SIP proxy and signaling routing**
- Outbound SIP call origination via **FreeSWITCH ESL**
- RTP audio delivery to registered SIP clients
- Batch notifications using REST API
- Automatic retry mechanism for failed recipients
- SQLite-based persistent logging
- Per-call status and retry attempt tracking
- Call recording support
- Dockerized FastAPI backend

---

## Tech Stack

- Python
- FastAPI
- Docker
- Kamailio
- FreeSWITCH
- SIP / RTP
- Zoiper
- SQLite
- eSpeak
- Git / GitHub

---

## Architecture

```text
FastAPI Backend (Docker)
        ↓
ESL Socket Control
        ↓
FreeSWITCH (Media / RTP / Recording)
        ↑
Kamailio (SIP Proxy / Routing)
        ↑
Zoiper / SIP Client
        ↓
SQLite Logging + Recordings

## API Endpoints
Send single notification
POST /notify


Example payload:
```text
{
  "extension": "1001",
  "message": "Hello, this is a voice notification"
}
```

Send batch notifications
POST /notify-batch
View logs
GET /logs


## Setup & Configuration

### FreeSWITCH

The internal SIP profile port was updated to avoid conflict with Kamailio.

```text
internal_sip_port = 5070
```

This allows Kamailio to listen on the default SIP port `5060` and forward SIP signaling to FreeSWITCH on `5070`.

---

### Kamailio

Kamailio is configured as a SIP proxy layer in front of FreeSWITCH.

It forwards SIP registration and call signaling requests to FreeSWITCH:

```cfg
if (is_method("REGISTER")) {
    $du = "sip:192.168.1.5:5070";
    t_relay();
    exit;
}

if (is_method("INVITE|ACK|BYE|CANCEL|OPTIONS")) {
    $du = "sip:192.168.1.5:5070";
    t_relay();
    exit;
}
```

This creates the signaling flow:

```text
Zoiper → Kamailio :5060 → FreeSWITCH :5070
```

---

### Run FastAPI Backend

```bash
sudo docker run --network host \
-v ~/voicebot/shared:/app/shared \
-v ~/voicebot/calls.db:/app/calls.db \
voicebot-api
```


## Current Status

✅ MVP completed with:

- dynamic TTS
- batch notifications
- retries
- database logging
- call recording
- FastAPI REST API
- Docker deployment
- Kamailio SIP routing

## Future Improvements
- scheduled notifications
- analytics dashboard
- async task queue
- cloud deployment
