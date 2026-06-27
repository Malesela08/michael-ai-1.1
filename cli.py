import sys

from api_interface import DigitalComradeEngine

engine = DigitalComradeEngine()

if "--status" in sys.argv:
    print(engine.get_system_health())
elif "--task" in sys.argv:
    task_index = sys.argv.index("--task") + 1
    print(engine.execute_mission(sys.argv[task_index]))
