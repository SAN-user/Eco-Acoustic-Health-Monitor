import serial
import time
from datetime import datetime
from pathlib import Path

# ==============================
# ESP32 SERIAL CONFIGURATION
# ==============================

PORT = "COM7"
BAUD = 460800

# ==============================
# OUTPUT DIRECTORY
# ==============================

UPLOADS_DIR = Path(
    r"C:\Users\HP\Desktop\Eco-Acoustic\uploads"
)

# Create uploads folder if it doesn't exist
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Create a unique filename for every ESP32 recording
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT = UPLOADS_DIR / f"esp32_{timestamp}.wav"


# ==============================
# CONNECT TO ESP32
# ==============================

print("Connecting to ESP32...")

ser = serial.Serial(
    PORT,
    BAUD,
    timeout=5
)

time.sleep(2)

ser.reset_input_buffer()

print("Connected!")
print("Waiting for recording to finish...")
print()


# ==============================
# WAIT FOR ESP32 RECORDING
# ==============================

while True:

    line = ser.readline()

    if not line:
        print("Waiting...")
        continue

    text = line.decode(
        "ascii",
        errors="ignore"
    ).strip()

    print("ESP32:", text)

    if text == "READY_TO_TRANSFER":
        break


print()
print("Recording is ready!")
print("Requesting WAV transfer...")


# ==============================
# REQUEST FILE TRANSFER
# ==============================

ser.write(b"SEND\n")


# ==============================
# WAIT FOR ECO_START
# ==============================

while True:

    line = ser.readline()

    if not line:
        print("Waiting for transfer...")
        continue

    text = line.decode(
        "ascii",
        errors="ignore"
    ).strip()

    print("ESP32:", text)

    if text == "ECO_START":
        break

    if text == "ERROR_FILE":
        print("ERROR: recording.wav not found.")
        ser.close()
        raise SystemExit


# ==============================
# READ EXACT FILE SIZE
# ==============================

size_line = ser.readline()

file_size = int(
    size_line.decode("ascii").strip()
)

print()
print("========================================")
print("WAV FILE SIZE:", file_size, "bytes")
print("========================================")
print("Receiving binary audio...")
print()


# ==============================
# RECEIVE AUDIO DATA
# ==============================

received = 0

with open(OUTPUT, "wb") as f:

    while received < file_size:

        remaining = file_size - received

        chunk = ser.read(
            min(4096, remaining)
        )

        if not chunk:
            print()
            print("ERROR: Transfer stopped.")
            break

        f.write(chunk)

        received += len(chunk)

        percent = (
            received * 100 /
            file_size
        )

        print(
            f"\rReceived: "
            f"{received}/{file_size} "
            f"({percent:.1f}%)",
            end=""
        )


# ==============================
# CLOSE SERIAL CONNECTION
# ==============================

ser.close()

print()


# ==============================
# VERIFY TRANSFER
# ==============================

if received == file_size:

    print()
    print("========================================")
    print("       TRANSFER SUCCESSFUL! 🎉")
    print("========================================")
    print()

    print("File saved:")
    print(OUTPUT)

    print()
    print("Size:", received, "bytes")
    print()

    print("🎤 ESP32 audio is now on the PC!")
    print("📁 Ready for Streamlit detection.")

else:

    print()
    print("========================================")
    print("          TRANSFER FAILED")
    print("========================================")
    print()

    print("Received:", received)
    print("Expected:", file_size)