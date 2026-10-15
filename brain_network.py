"""
Michael AI: Biologically-Inspired Split-Brain Nervous System
Integrating physical vehicle (CAN bus) and property (RTSP/Relay) nerves.
"""
import logging
from corpus_callosum import CorpusCallosumBridge, MCPRouter, ToolRegistry

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("MichaelAI-NervousSystem")

class PeripheralNervousSystem:
    """
    The Right Brain & Peripheral Nerves: Gathers raw data from physical sensors 
    (Automotive CAN bus, property RTSP cameras, perimeter GPIO relays).
    """
    def __init__(self, tool_registry: ToolRegistry, corpus_bridge: CorpusCallosumBridge):
        self.registry = tool_registry
        self.bridge = corpus_bridge
        logger.info("👁️ [Perceptual Cortex] Peripheral Nervous System initialized & wired.")

    def sense_environment(self, environment_type: str):
        """Fires sensory nerve impulses based on whether Michael AI is deployed in the Car or House."""
        if environment_type == "car":
            logger.info("🚗 [Vehicle Nerves] Polling automotive CAN bus & ECU telemetry...")
            sensory_data = {
                "can_bus": self.registry.get_tool("can_bus"),
                "ignition_status": {"state": "active", "voltage": 12.6},
                "motion_vector": {"speed": 0.0, "heading": "stationary"}
            }
        elif environment_type == "house":
            logger.info("🏠 [Property Nerves] Polling perimeter cameras & GPIO relays...")
            sensory_data = {
                "camera_feed": self.registry.get_tool("camera"),
                "gate_sensor": {"status": "closed", "lock": "secure"},
                "motion_detector": {"zone_1": "clear", "zone_2": "clear"}
            }
        else:
            sensory_data = {"sensor": self.registry.get_tool("default")}

        # Transmit nerve impulse across the Corpus Callosum
        signal_transmission = self.bridge.route_message(
            source_domain=f"PeripheralNerves_{environment_type.upper()}",
            target_domain="AnalyticalCortex",
            payload={"environment": environment_type, "nerve_signals": sensory_data}
        )
        return signal_transmission

class AnalyticalCortex:
    """
    The Left Brain: Processes incoming nerve impulses, evaluates threats using logic/StackQL, 
    and fires motor reflex commands back to the hardware.
    """
    def __init__(self, mcp_router: MCPRouter):
        self.router = mcp_router
        logger.info("🧠 [Analytical Cortex] Left brain nerve center active.")

    def process_impulses_and_reflexes(self, transmission: dict):
        logger.info("🧠 [Analytical Cortex] Processing nerve impulses through cognitive stack...")
        
        # 1. Run StackQL/MCP analytical evaluation
        evaluation = self.router.execute_query("analytical_cognition_bridge", transmission)
        
        # 2. Determine motor reflex response (e.g., lock doors, flash lights, sound alarm)
        env = transmission.get("data", {}).get("environment", "unknown")
        if env == "car":
            reflex_action = {"motor_command": "maintain_monitoring", "fuel_pump_relay": "armed"}
        else:
            reflex_action = {"motor_command": "perimeter_secure", "floodlights": "off"}

        return {
            "cognitive_evaluation": evaluation,
            "motor_reflex": reflex_action,
            "neural_status": "fully_synchronized"
        }

class MasterNervousSystem:
    """Unites the entire hardware-to-brain neural architecture."""
    def __init__(self):
        logger.info("⚡ [Neural Core] Bootstrapping Michael AI Master Nervous System...")
        self.corpus_callosum = CorpusCallosumBridge()
        self.mcp_router = MCPRouter()
        self.tool_registry = ToolRegistry()

        self.left_brain = AnalyticalCortex(self.mcp_router)
        self.right_brain = PeripheralNervousSystem(self.tool_registry, self.corpus_callosum)

    def execute_neural_reflex_cycle(self, environment: str = "car"):
        logger.info(f"=== Starting Neural Reflex Cycle [Deployment: {environment.upper()}] ===")
        
        # Step 1: Right Brain perceives via physical car/house nerves
        transmission = self.right_brain.sense_environment(environment)
        
        # Step 2: Left Brain analyzes and fires motor reflexes
        response = self.left_brain.process_impulses_and_reflexes(transmission)
        
        logger.info(f"✅ Neural Reflex Cycle Complete: {response}")

if __name__ == "__main__":
    # Test vehicle nerve integration (Car / Anti-Hijack mode)
    system = MasterNervousSystem()
    system.execute_neural_reflex_cycle("car")
    
    print("\n" + "="*50 + "\n")
    
    # Test property nerve integration (House / Estate mode)
    system.execute_neural_reflex_cycle("house")
