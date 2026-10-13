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
- Captures one frame from a local image/video file or configured online camera
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
- Optional local environment settings from `.env`; copy `.env.example` and
  adjust `CAMERA_SOURCE` for your device, file, or authorized camera stream.
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
cp .env.example .env
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

Use `--camera-source` to select a local device, image/video file, or authorized
camera stream for a camera request. `--all-nodes` displays the registered node
status; it does not activate unavailable services or hardware.

```bash
python main.py --camera-source path/to/video.mp4 "Check the South perimeter"
python main.py --all-nodes
```

The application loads `.env` settings when the vision module starts. The
example sets `HEADLESS=true` and `CAMERA_SOURCE=0` (webcam device index zero).
You can set `CAMERA_SOURCE` to a local image/video file or an authorized online
stream instead; numeric values are treated as camera device indexes.
`CAMERA_RTSP_URL` remains supported for existing RTSP configurations. Do not
commit camera credentials or `.env` files.

```bash
CAMERA_SOURCE='rtsp://camera-host:554/stream' python main.py "Check the North zone perimeter"
```

The current camera path is headless and keeps operational messages visible.
`MICHAEL_AI_MODE=STEALTH` and `SILENT_DISPATCH=true` are not supported; camera
capture and any configured dispatch must remain apparent in the application
logs. The CLI does not provide a `--stealth` option. No GUI preview is
implemented.

For RTSP configurations using the legacy variable:

```bash
export CAMERA_SOURCE=''
export CAMERA_RTSP_URL='rtsp://camera-host:554/stream'
python main.py "Check the North zone perimeter"
```

Use the same perimeter route with an offline local video or image:

```bash
export CAMERA_SOURCE='path/to/video.mp4'
python main.py "Check the South zone perimeter"
```

You can also pass a source directly to the vision agent or route:

```bash
python -c "from vision_agent import VisionAgent; print(VisionAgent().analyze_frame('path/to/image.jpg'))"
python -c "from main import create_hub; print(create_hub().route_intent('Check perimeter', context={'source': 'path/to/video.mp4'}))"
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
