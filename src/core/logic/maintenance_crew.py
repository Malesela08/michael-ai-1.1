from crewai import Agent, Crew, Task

cleaner = Agent(
    role="System Cleaner",
    goal="Clean stale signals and repair inconsistent state",
    backstory="A maintenance specialist focused on keeping the system operational and clean.",
)

auditor = Agent(
    role="System Auditor",
    goal="Review system signal integrity and flag maintenance issues",
    backstory="A careful auditor that checks for latent system problems detectably from the blackbox logs.",
)

clean_task = Task(
    description="Review the current signal trail and clean any stale or duplicated records.",
    agent=cleaner,
    expected_output="A concise report of cleanup actions taken.",
)

audit_task = Task(
    description="Audit the blackbox log to identify any suspicious or unsafe signals.",
    agent=auditor,
    expected_output="A concise assessment of the system's integrity.",
)

maintenance_crew = Crew(agents=[cleaner, auditor], tasks=[clean_task, audit_task])
