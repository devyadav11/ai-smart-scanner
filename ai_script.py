#!/data/data/com.termux/files/usr/bin/python
import sys
import os

# Set the path to the smart_agent directory
agent_path = "/data/data/com.termux/files/home/project1/smart_agent"
sys.path.append(agent_path)

from main import agent

if __name__ == "__main__":
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        agent(prompt)
    else:
        print("Usage: ai \"scan document\"")
