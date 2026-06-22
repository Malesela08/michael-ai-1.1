from crewai import Agent, Task, Crew

cleaner = Agent(
    role='Software Cleaner',
    goal='Identify and clean deprecated code or syntax errors',
    backstory='An expert in legacy software maintenance and code optimization.'
)

auditor = Agent(
    role='System Auditor',
    goal='Review all logic signals for security compliance',
    backstory='A rigorous auditor focused on system integrity and anti-hijack protocols.'
)

clean_task = Task(
    description='Review and clean the current codebase.',
    agent=cleaner,
    expected_output='A clean, refactored version of the codebase with comments on improvements made.'
)

audit_task = Task(
    description='Audit the latest signal logs for potential risks.',
    agent=auditor,
    expected_output='A formal security report summarizing any anomalies found in the blackbox.log.'
)

maintenance_crew = Crew(agents=[cleaner, auditor], tasks=[clean_task, audit_task])
