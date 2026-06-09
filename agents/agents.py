from pyexpat import model
from langchain_core.messages.block_translators import google_genai
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools.tools import (search_web,scrape_url)
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)


# Search Agent

def build_search_agent():
    return create_agent(
        model=llm,
        tools=[search_web]
    )

# Scrape Agent

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )

# Writter Chain

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise, factual research report writer. Use bullet points. No fluff."),
    ("human", """Write a report on this topic based on the topic below:
    
    Topic:
    {topic}
    
    Research gathered:
    {research}

    Structure the report as:
    - Introduction
    - Key findings (minimum 3 well explained points)
    - Conclusion
    - Sources (list all the urls found in the research)

    Be detailed, factual and proffesional
    """)
])

writer_chain = writer_prompt | llm | StrOutputParser()

# Critic chain

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a strict research critic. Your job is to review a report and identify weaknesses.
    Check for:
    - unsupported claims
    - weak evidence
    - lack of sources
    - poor structure
    - unclear explanations

    Be harsh but fair. Return bulleted list of issues.
    """),
    ("human", """
    Report to critique:
    {report}

    Respond in this exact format:

    Score: X/10

    Strengths:
    - ...
    - ...

    Areas to Improve:
    - ...
    - ...

    One line verdict:
    ...""")
])

critic_chain = critic_prompt | llm | StrOutputParser()