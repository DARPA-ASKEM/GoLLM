import argparse
import json
import logging
from openai import OpenAI
import os
import streamlit as st
from core.openai.react import OpenAIAgent, AgentExecutor, ReActManager
from core.openai.toolsets import ASKEMConfigDemo, AskHuman


def main():
    st.title("Uncharted LLM Demo")

    user_input = st.text_input("Type your message:")

    if user_input:
        agent = OpenAIAgent(api_key=os.getenv('OPENAI_API_KEY'),
                            toolset=AskHuman)
        executor = AgentExecutor(toolset=AskHuman)
        manager = ReActManager(agent=agent, executor=executor)
        response = manager.run(query=user_input)
        st.text_area("AI Response:", value=response, height=300)

if __name__ == '__main__':
    main()