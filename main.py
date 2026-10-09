import sys
import json
from corpus_callosum import CorpusCallosum
from camera_tool import check_live_camera_stream

def query_water_meter(**kwargs):
    """Retrieves municipal utility water meter data and reading status."""
    return {"meter_id": "WM-8842", "last_reading": "142.5 KL", "status": "submitted_successfully"}

def scan_perimeter_camera(rtsp_url: str = "rtsp://admin:password@192.168.1.100:554/stream1", **kwargs):
    """Scans physical security zones and live camera stream status across the property."""
    # If a zone was passed by the LLM, we can include it in our check or pass it along
    return check_live_camera_stream(rtsp_url)

def main():
    print("Initializing Michael AI - Sovereign Core...")
    bridge = CorpusCallosum(model="llama3.2")

    bridge.register_mcp_tool(
        name="check_water_meter",
        description="Retrieves municipal utility water meter data and reading status.",
        handler=query_water_meter
    )
    bridge.register_mcp_tool(
        name="check_perimeter",
        description="Scans physical security zones and live camera stream status across the property.",
        handler=scan_perimeter_camera
    )

    prompt = sys.argv[1] if len(sys.argv) > 1 else "Check the water meter status for the household."
    print(f"\n[Dispatching Agent Prompt]: '{prompt}'")
    result = bridge.route_intent(prompt)
    print("\n[Execution Result]:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
