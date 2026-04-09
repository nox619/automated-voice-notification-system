# Automated Voice Notification System

A backend voice notification system built using FreeSWITCH, Python, Zoiper, and SQLite.

## Features
- Dynamic TTS voice notifications using eSpeak
- Outbound SIP call origination via FreeSWITCH ESL
- Batch notifications using CSV input
- Retry mechanism for failed calls
- SQLite-based call logging
- Per-call status and attempt tracking

## Stack
- Python
- FreeSWITCH
- SIP / RTP
- Zoiper
- SQLite
- eSpeak

## Workflow
Python → TTS → FreeSWITCH → SIP call → RTP audio → Logging

## Current Status
MVP completed with batch + retry support
