# SmartNichoir Project
**SmartCities 2025-2026**

---

## Project Overview
The **SmartNichoir** aims to create a connected and intelligent birdhouse that monitors bird activity at **low cost** while achieving **long battery life**.  
The system uses an ESP32 camera module, a Raspberry Pi backend, and a web interface to store and visualize captured images.

**Key Features:**
- Cost under €50  
- Battery autonomy between 6 months and 1 year  
- Optional solar panel for extended autonomy  
- PIR motion detection  
- IR camera for night monitoring  
- Image storage and visualization via Raspberry Pi + Web Server  
- Communication using MQTT  

---

## Technical Components

### Hardware
- **Microcontroller:** ESP32-D0WDQ6-V3  
- **Camera:** OV3660, 3MP, DFOV 66.5°, up to 2048×1536 resolution  
- **Memory:** 8 MB PSRAM  
- **Indicators:** Status LED + RESET button  
- **Power Management:**  
  - Ultra‑low power design  
  - Integrated RTC (BM8563) for timed wake-ups  
  - Sleep current as low as 2 μA  
- **Connectivity:** Wi-Fi, USB debugging, HY2.0-4P external port  

### Software
- **ESP32:** TimerCAM library for image capture  
  - https://github.com/m5stack/TimerCamarduino/tree/master  
- **Raspberry Pi:**  
  - Python MQTT listener storing photos + metadata in MariaDB  
  - Flask web server to serve gallery and battery information  
- **Web Interface:**  
  - Gallery for viewing captured images  
  - Battery status display  

---

## Operation Modes

### Standby Mode
The ESP32 wakes once per day to send the battery level over MQTT if no activity is detected.

### Presence Mode
When the PIR sensor detects movement, a picture is captured with IR lighting and sent via MQTT with the battery level.

---

## Project Directories

The repository contains the following folders:

- [**stm32/**](stm32/) – ESP32 TimerCAM firmware, PIR detection, IR LED control  
- [**raspberry/**](raspberry/) – Raspberry Pi MQTT receiver, MariaDB storage, Flask web server  
- [**web/**](web/) – HTML/CSS/JS interface, image gallery, battery visualizations  

---

## Objectives
- Detect and record activity inside the SmartNichoir  
- Reduce energy consumption to maximize battery life  
- Store photos and metadata in a structured database  
- Display collected information through a clean and accessible web interface  
- Respect modularity to support future improvements (e.g. solar power)

---

## References
- TimerCAM Library:  
  https://github.com/m5stack/TimerCamarduino/tree/master

  ---

## Made by Team CBB/12

[![Team Logo]

