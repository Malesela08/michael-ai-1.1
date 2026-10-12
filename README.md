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
- Stores locally submitted forensic payloads as JSON records with SHA-256
  checksums. Records are **not encrypted or tamper-proof**; do not store secrets
  or rely on this as a legally defensible evidence chain.
- Simulates relay state requests in memory only. The relay handler is not
  connected to ignition, gate, siren, or other physical hardware.
- Registers the forensic vault, relay simulation, and CAN telemetry simulation
  as agent handlers and local hub tools. The CAN handler does not read a bus;
  its metrics are unavailable until a real interface is implemented.
- Returns the current pillar registry for agent/status queries.
- Uses a local llamafile server as the text-generation fallback for prompts
  that do not match a deterministic route.

## Requirements

- Python 3.10 or newer.
- The Python packages in `requirements.txt`.
- The llamafile runner at `bin/llamafile` and a GGUF model at
  `models/model.gguf`, started separately for text-generation fallback. These
  large runtime artifacts are local and are not tracked in Git.
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

Start the local llamafile server:

```bash
./bin/llamafile -m ./models/model.gguf -b 127.0.0.1 --port 8080
```

Then run Michael AI in another terminal. By default it requests
`http://127.0.0.1:8080/v1`. `LLAMAFILE_BASE_URL` can select another loopback
address only; non-local endpoints are rejected to keep text generation on the
edge runtime. Set `LLAMAFILE_MODEL` to override the model label if required.

```bash
python main.py "Give me a tactical summary"
```

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
