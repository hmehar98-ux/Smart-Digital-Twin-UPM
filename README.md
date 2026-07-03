# Smart Digital Twin Framework for Ultra-Precision Machining

A Digital Twin framework developed for **real-time monitoring of an ultra-precision machining laboratory**, integrating Industrial IoT (IIoT), MQTT communication, machine learning, and interactive 3D visualization.

---

## Overview

This project was developed as part of my **M.Tech research at IIT Bombay**.

The framework continuously acquires machining and environmental data from multiple sensors, transmits them through an MQTT-based IIoT architecture, stores historical information in Supabase, and visualizes the laboratory using a 3D Digital Twin.

The objective is to provide a scalable monitoring framework for Industry 4.0 manufacturing environments supporting predictive maintenance and intelligent decision-making.

---

## Features

- Real-time Digital Twin visualization
- MQTT-based communication
- Multi-sensor data acquisition
- Environmental monitoring
- Machine condition monitoring
- Historical trend visualization
- Interactive PySide6 dashboard
- PyVista-based 3D laboratory model
- Supabase cloud database integration
- Machine learning ready architecture

---

## Technologies Used

- Python
- PySide6
- PyVista
- MQTT
- Supabase
- ESP32
- Arduino
- NI DAQ
- NumPy
- Pandas
- PyQtGraph

---

## System Architecture

```text
Sensors
   │
   ▼
ESP32 / Arduino / NI DAQ
   │
   ▼
MQTT Broker
   │
   ▼
Python Backend
   │
   ├──────────────► Supabase Database
   │
   ▼
Digital Twin Dashboard
   │
   ▼
Real-Time Monitoring
```

---

## Dashboard Modules

- Machine Dashboard
- Environment Monitoring
- UPS Monitoring
- Dehumidifier Monitoring
- Machine Condition Monitoring
- Historical Trends

---

## Repository Structure

```
Smart-Digital-Twin-UPM/

├── assets/
├── twin/
├── ui/
├── main.py
├── README.md
└── .gitignore
```

---

## Future Improvements

- OPC UA integration
- CNC machine connectivity
- AI-based predictive maintenance
- Digital Thread implementation
- Cloud deployment
- Multi-machine monitoring

---

## Author

**Hitesh Mehar**

M.Tech Manufacturing Engineering

Indian Institute of Technology Bombay

GitHub: https://github.com/hmehar98-ux