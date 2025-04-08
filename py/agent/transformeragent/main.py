import os

from dotenv import load_dotenv
from huggingface_hub import login
from transformers import Tool

load_dotenv()

login(os.environ.get("HUGGINGFACE_TOKEN"))



image_generation_tool = Tool.from_space(
    "black-forest-labs/FLUX.1-dev",
    name="image_generator",
    description="Generate an image from a prompt")

image_generation_tool("A sunny beach")