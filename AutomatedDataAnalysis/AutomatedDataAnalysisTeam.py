!pip install crewai_tools > /dev/null

import os
os.environ["CREWAI_NO_WIDGETS"] = "1"
os.environ["SERPER_API_KEY"] = "YOUR_API_KEY"
os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"
os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"

import yaml
files = {
    'agents': "agents.yaml",
    'tasks': "tasks.yaml"
}

configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)

agents_config = configs['agents']
tasks_config = configs['tasks']

from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

data_collector = Agent(
    config=agents_config['data_collector'],
    tools=[SerperDevTool()]

)

data_analyst = Agent(
    config=agents_config['data_analyst']
)

topic = "Recent Gold Rate Trends"
collect_data_task = Task(
    config=tasks_config['collect_data_task'].format(topic=topic),
    agent=data_collector
)

analyze_data_task = Task(
    config=tasks_config['analyze_data_task'],
    agent=data_analyst,
    context=[collect_data_task]
)

data_analysis_crew = Crew(
    agents=[data_collector, data_analyst],
    tasks=[collect_data_task, analyze_data_task],
    process=Process.sequential,
    verbose=True
)

result=data_analysis_crew.kickoff()

with open("GoldRateAnalysis.txt", "w") as f:
    f.write(result.raw)

with open("GoldRateAnalysis.txt", "r") as f:
    print(f.read())
