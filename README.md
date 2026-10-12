# Michael AI — Sovereign Edge Prototype

Michael AI is an offline-first edge prototype for deterministic tool routing,
camera-frame capture, and local image processing.

> **Prototype scope:** The repository contains a 13-pillar status registry, but
> that does not mean all 13 services are implemented or connected. The current
> hub registers a water-meter placeholder and a local vision handler. Water
> data is unavailable until a provider is configured. Vision can capture a frame
> and calculate brightness, but YOLO detection and gait profiling are not
> implemented. MCP-style local tools are registered; remote MCP server
> connections are not configured. No security decision should be based on this
> prototype's output.

## Current capabilities

- Routes water-meter, perimeter/camera, CAN/ECU/vehicle, and RF/spectrum
  keywords deterministically.
- Reports unavailable providers as unavailable rather than inventing sensor
  readings or claiming a system is secure.
- Captures one frame from a local image, video source, or configured camera
  stream and calculates mean grayscale brightness.
- Returns the current pillar registry for agent/status queries.
- Uses a local Ollama model as a fallback for prompts that do not match a
  deterministic route.

## Requirements

- Python 3.10 or newer.
- The Python packages in `requirements.txt`.
- Ollama with the configured `llama3.2` model for prompts that use the LLM
  fallback. The deterministic water/camera/CAN/RF routes do not require Ollama.
- A camera stream or local image/video file for frame capture. Camera hardware
  is optional.

The project requirements include packages used by other repository components
and may take time or additional system resources to install.

## Install

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Configure and run

Set `CAMERA_RTSP_URL` to a camera stream if you want the perimeter route to
attempt a frame capture. Do not commit camera credentials or `.env` files.

```bash
export CAMERA_RTSP_URL='rtsp://camera-host:554/stream'
python main.py "Check the North zone perimeter"
```

To try frame processing with a local file, call the vision API from Python:

```bash
python -c "from vision_agent import VisionAgent; print(VisionAgent().analyze_frame('path/to/image.jpg'))"
```

Other examples:

```bash
python main.py "Check the water meter"
python main.py "Check vehicle CAN bus status"
python main.py "Check RF spectrum for jamming"
python main.py "Show all agent status"
```

The water, CAN, and RF integrations are not configured by default, so their
results report unavailable. The status command reports registry/configuration
state, not live health checks for connected hardware.

## Test

```bash
python -m pytest -q
```

The Ollama integration test is skipped when its local service or configured
model is not available.