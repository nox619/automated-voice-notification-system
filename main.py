import socket
import subprocess
import time
import sqlite3
import csv
from datetime import datetime

HOST = "127.0.0.1"
PORT = 8021
PASSWORD = "ClueCon"

MESSAGE = "Hello Hassaan, this is a batch notification test"
AUDIO_FILE = "/tmp/notification.wav"
DB_FILE = "calls.db"

recipients = []

with open("recipients.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        recipients.append({
            "extension": row["extension"],
            "message": row["message"]
        })


def log_call(cursor, extension, message, timestamp, duration, response, attempt):
    status = "success" if "+OK" in response else "failed"

    cursor.execute("""
    INSERT INTO call_logs (
        extension,
        message,
        timestamp,
        duration,
        response,
        status,
        attempt
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        extension,
        message,
        timestamp,
        duration,
        response,
        status,
        attempt
    ))


def call_extension(extension):
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

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    s.close()

    return start_time.isoformat(), duration, response


# Generate TTS once
subprocess.run(
    ["espeak", "-w", AUDIO_FILE, MESSAGE],
    check=True
)

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

MAX_RETRIES = 3
RETRY_DELAY = 5

for recipient in recipients:
    ext = recipient["extension"]
    MESSAGE = recipient["message"]

    subprocess.run(
        ["espeak", "-w", AUDIO_FILE, MESSAGE],
        check=True
    )

    success = False
    attempt = 1

    while attempt <= MAX_RETRIES and not success:
        timestamp, duration, response = call_extension(ext)

        print(response)

        log_call(
            cursor,
            ext,
            MESSAGE,
            timestamp,
            duration,
            response,
            attempt
        )

        conn.commit()

        if "+OK" in response:
            success = True
            print(f"{ext} successful")
        else:
            print(f"{ext} failed, attempt {attempt}")
            attempt += 1
            time.sleep(RETRY_DELAY)