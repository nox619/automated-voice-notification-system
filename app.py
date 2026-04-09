from fastapi import FastAPI
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
        "success" if "+OK" in response else "failed",
        1
    ))

    conn.commit()
    conn.close()
    s.close()

    return response


@app.post("/notify")
def notify(extension: str, message: str):
    response = make_call(extension, message)

    return {
        "extension": extension,
        "response": response
    }
