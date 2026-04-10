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
AUDIO_FILE = "/tmp/notification.wav"
DB_FILE = "calls.db"


class NotifyRequest(BaseModel):
    extension: str
    message: str


def make_call(extension: str, message: str):
    subprocess.run(
        ["espeak", "-w", AUDIO_FILE, message],
        check=True
    )

    start_time = datetime.now()

    s = socket.socket()
    s.connect((HOST, PORT))
    s.recv(4096)

    s.send(f"auth {PASSWORD}\n\n".encode())
    s.recv(4096)

    command = (
        f"api originate user/{extension} "
        f"&playback({AUDIO_FILE})\n\n"
    )

    s.send(command.encode())
    time.sleep(1)

    response = s.recv(4096).decode()

    duration = (datetime.now() - start_time).total_seconds()

    conn = sqlite3.connect(DB_FILE)
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