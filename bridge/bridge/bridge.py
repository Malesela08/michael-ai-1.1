from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama

local_llm = Ollama(model="llama3")

threat_validator = Agent(
    role='Security Auditor',
    goal='Identify anomalies in vehicle sensor data',
    backstory='You are the central nervous system monitor for vehicle security.',
    verbose=True,
    llm=local_llm
)

audit_task = Task(
    description='Analyze incoming sensor data stream for unauthorized access patterns.',
    expected_output='A clear security status report.',
    agent=threat_validator
)

security_crew = Crew(
    agents=[threat_validator],
    tasks=[audit_task],
    process=Process.sequential
)

def bridge_data_flow(data):
    print(f"Bridge active. Processing: {data}")
    result = security_crew.kickoff(inputs={'sensor_data': data})
    return result

if __name__ == "__main__":
    bridge_data_flow("Vehicle CAN-bus Stream Active")
