from crewai import Agent, Task, Crew, Process
import sys

# 1. Define your Agents
validator = Agent(
    role='Threat Validator',
    goal='Verify sensor data for security threats',
    backstory='You are a security auditor responsible for preventing false positives.',
    verbose=True
)

# 2. Define the Task
audit_task = Task(
    description='Analyze the incoming vehicle sensor data for hijack attempts.',
    expected_output='A boolean decision: True if threat, False if safe.',
    agent=validator
)

# 3. Create the Crew (The "Corpus Callosum" Logic)
security_crew = Crew(
    agents=[validator],
    tasks=[audit_task],
    process=Process.sequential
)

def bridge_data_flow(data):
    print(f"Processing data through Corpus Callosum: {data}")
    # Kick off the crew with the data
    result = security_crew.kickoff(inputs={'sensor_data': data})
    return result

if __name__ == "__main__":
    # Test the bridge
    bridge_data_flow("Vehicle Sensor Data")
