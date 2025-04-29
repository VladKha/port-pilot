import os

from dotenv import load_dotenv
from smolagents import CodeAgent, VisitWebpageTool, GoogleSearchTool, PythonInterpreterTool, \
    FinalAnswerTool

from gradio_ui import GradioUI
from observability import setup_observability
from rate_limit_models import ExponentialBackoffOpenAIServerModel
from tools import calculate_distance, maps_search, get_shipping_estimate

load_dotenv()
setup_observability()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_model = 'gemini-2.0-flash'

search_tool = GoogleSearchTool(provider='serper') # DuckDuckGoSearchTool()


model = ExponentialBackoffOpenAIServerModel(gemini_model,
                                            api_base='https://generativelanguage.googleapis.com/v1beta/openai/',
                                            api_key=GEMINI_API_KEY,
                                            max_tokens=8096 * 2)
# model = HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct", max_tokens=8096)

agent = CodeAgent(
    model=model,
    tools=[search_tool,
        maps_search,
        VisitWebpageTool(),
        calculate_distance,
        get_shipping_estimate,
        PythonInterpreterTool(),
        FinalAnswerTool()],
    additional_authorized_imports=[
        "pandas",
        "json",
        "pandas",
        "numpy"],
    max_steps=20,
    planning_interval=4
)

# task = """
# Find all cities of Antler VC offices in Asia.
# Calculate the time and cost to transfer 1 container of apples to Apple Inc headquarters from each of the cities.
# """
#
# instruction = f"""
# You're an expert analyst. You make comprehensive reports after visiting many websites.
# Don't hesitate to search for many queries at once in a for loop.
# For each data point that you find, visit the source url to confirm numbers.
#
# {task}
# """
# detailed_report = agent.run(instruction)
# print(detailed_report)

GradioUI(agent).launch()
