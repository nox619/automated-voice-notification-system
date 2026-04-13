from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import socket
import time
import sqlite3
from datetime import datetime

app = FastAPI()

HOST = "127.0.0.1"
PORT = 8021
PASSWORD = "ClueCon"
AUDIO_FILE = "/app/shared/notification.wav"
DB_FILE = "calls.db"


class NotifyRequest(BaseModel):
    extension: str
    message: str


class BatchRecipient(BaseModel):
    extension: str
    message: str


class BatchNotifyRequest(BaseModel):
    recipients: list[BatchRecipient]


def make_call(extension: str, message: str):
    # Generate TTS audio
    subprocess.run(
        ["espeak", "-w", AUDIO_FILE, message],
        check=True
    )

    print("AUDIO FILE GENERATED AT:", AUDIO_FILE)

    start_time = datetime.now()

    # Recording file path
    record_file = (
        f"/home/hassaan/voicebot/recordings/"
        f"{extension}_{int(time.time())}.wav"
    )

    s = socket.socket()
    s.connect((HOST, PORT))

    banner = s.recv(4096).decode()
    print("BANNER:", banner)

    s.sendall(f"auth {PASSWORD}\n\n".encode())

    auth_response = s.recv(4096).decode()
    print("AUTH:", auth_response)

    if "+OK accepted" not in auth_response:
        raise Exception(f"ESL auth failed: {auth_response}")

    # Originate call + playback
    command = (
        f"api originate user/{extension} "
        f"&playback(/home/hassaan/voicebot/shared/notification.wav)\n\n"
    )
    print("COMMAND:", command)
    s.sendall(command.encode())
    time.sleep(1)

    response = s.recv(4096).decode()

    # Extract UUID
    uuid = None
    if "+OK" in response:
        uuid = response.split("+OK")[-1].strip()

    # Start recording if call originated
    if uuid:
        record_command = (
            f"api uuid_record {uuid} start {record_file}\n\n"
        )
        s.send(record_command.encode())
        time.sleep(1)

    duration = (datetime.now() - start_time).total_seconds()

    # Save log
    DB_FILE = "/app/calls.db"
    cursor = conn.cursor()

    status = "success" if "+OK" in response else "failed"

    cursor.execute("""
    INSERT INTO call_logs (
        extension, message, timestamp, duration, response, status, attempt
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        extension,
        message,
        start_time.isoformat(),
        duration,
        response,
        status,
        1
    ))

    conn.commit()
    conn.close()
    s.close()

    return response, status


@app.post("/notify")
def notify(payload: NotifyRequest):
    response, status = make_call(
        payload.extension,
        payload.message
    )

    return {
        "extension": payload.extension,
        "status": status,
        "response": response
    }


@app.get("/logs")
def get_logs():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, extension, message, timestamp, duration, status, attempt
    FROM call_logs
    ORDER BY id DESC
    LIMIT 20
    """)

    rows = cursor.fetchall()
    conn.close()

    logs = []

    for row in rows:
        logs.append({
            "id": row[0],
            "extension": row[1],
            "message": row[2],
            "timestamp": row[3],
            "duration": row[4],
            "status": row[5],
            "attempt": row[6]
        })

    return {"logs": logs}


@app.post("/notify-batch")
def notify_batch(payload: BatchNotifyRequest):
    results = []

    for recipient in payload.recipients:
        response, status = make_call(
            recipient.extension,
            recipient.message
        )

        results.append({
            "extension": recipient.extension,
            "status": status,
            "response": response
        })

    return {
        "total": len(results),
        "results": results
    }