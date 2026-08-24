# CDN Simulator

A beginner-friendly, Python-based simulator explaining how a Content Delivery Network (CDN) uses geographic routing and edge caching to serve content faster.

## What this project does
This project simulates a miniature internet topology. Instead of hitting the main database (Origin) directly, the Client asks a Router for data. The Router calculates the user's GPS coordinates against available Edge servers (CDNs) and routes the request to the closest one. The CDN caches the result, making subsequent requests incredibly fast.

## Architecture

                    ┌──────────────────┐
                    │   ORIGIN SERVER  │
                    │      :8000       │
                    └────────┬─────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
      ┌───────▼────────┐            ┌───────▼────────┐
      │ BANGALORE CDN  │            │ NORTH INDIA CDN│
      │    :8001       │            │     :8002      │
      └───────▲────────┘            └───────▲────────┘
              │                             │
              └──────────────┬──────────────┘
                             │
                     ┌───────▼───────┐
                     │    CLIENT     │
                     │ Geo-location  │
                     └───────────────┘

## Features
- **Geographic Routing**: Uses the Haversine formula to route traffic based on minimal physical distance.
- **Independent Caching**: Separate in-memory caches for each edge node to demonstrate localization.
- **Latency Simulation**: Artificially delayed responses explicitly demonstrate Cache HITs vs MISSes.
- **Interactive CLI**: Easily hop between Indian cities to watch routing changes.

## Technology Stack
- **Python 3.10+**
- **FastAPI** (Web Server)
- **Uvicorn** (ASGI Server)
- **Requests** (HTTP Client)

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
