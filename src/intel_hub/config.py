"""Central configuration for collectors and generators."""

from __future__ import annotations

import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
REPORTS_DIR = ROOT_DIR / "reports"

USER_AGENT = os.getenv(
    "INTEL_HUB_USER_AGENT",
    "physical-ai-intelligence-hub/1.0 (+https://github.com/)",
)

REQUEST_TIMEOUT_SECONDS = int(os.getenv("INTEL_HUB_TIMEOUT", "30"))
MAX_ITEMS_PER_SOURCE = int(os.getenv("INTEL_HUB_MAX_ITEMS_PER_SOURCE", "12"))
MAX_STORED_ITEMS = int(os.getenv("INTEL_HUB_MAX_STORED_ITEMS", "100"))

AI_NEWS_FEEDS = {
    "OpenAI": "https://openai.com/news/rss.xml",
    "Anthropic": "https://www.anthropic.com/news/rss.xml",
    "Google DeepMind": "https://deepmind.google/discover/blog/rss.xml",
    "Meta AI": "https://ai.meta.com/blog/rss/",
    "Microsoft AI": "https://blogs.microsoft.com/ai/feed/",
    "NVIDIA AI": "https://blogs.nvidia.com/blog/category/deep-learning/feed/",
    "Hugging Face": "https://huggingface.co/blog/feed.xml",
}

ROBOTICS_NEWS_FEEDS = {
    "IEEE Spectrum Robotics": "https://spectrum.ieee.org/feeds/topic/robotics.rss",
    "The Robot Report": "https://www.therobotreport.com/feed/",
    "Robotics Business Review": "https://www.roboticsbusinessreview.com/feed/",
    "NVIDIA Robotics": "https://blogs.nvidia.com/blog/category/robotics/feed/",
}

PHYSICAL_AI_COMPANIES = [
    "Physical Intelligence",
    "Figure AI",
    "Skild AI",
    "Agility Robotics",
    "Apptronik",
    "Boston Dynamics",
    "Unitree",
    "NVIDIA Robotics",
    "LeRobot",
]

PAPER_KEYWORDS = [
    "physical ai",
    "embodied ai",
    "robotics",
    "vision language action",
    "vla",
    "world model",
    "foundation model",
    "humanoid robot",
    "robot learning",
    "robotics transformer",
    "multimodal robotics",
]

HUGGINGFACE_KEYWORDS = [
    "robot",
    "vla",
    "world model",
    "embodied",
    "physical ai",
    "navigation",
    "policy",
    "robotics",
]

GITHUB_TOPICS = [
    "physical-ai",
    "robotics",
    "embodied-ai",
    "vla",
    "world-model",
    "humanoid",
    "robot-learning",
    "lerobot",
    "robot-foundation-model",
]

JOB_KEYWORDS = [
    "robotics engineer",
    "robot learning",
    "physical ai",
    "embodied ai",
    "foundation model",
    "vla",
    "world model",
    "humanoid",
]

JOB_COMPANIES = {
    "Figure AI": {"greenhouse": "figureai"},
    "Agility Robotics": {"greenhouse": "agilityrobotics"},
    "Apptronik": {"lever": "apptronik"},
    "Boston Dynamics": {"greenhouse": "bostondynamics"},
    "Skild AI": {"lever": "skildai"},
}

