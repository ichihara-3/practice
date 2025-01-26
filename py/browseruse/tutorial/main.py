import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig

load_dotenv()

config = BrowserConfig(
    headless=False,
    disable_security=True,
    chrome_instance_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
)

browser = Browser(config)

async def main():
    agent = Agent(
        task=f"""
https://www.monotaro.com/ を開き、麺棒を検索してください。
検索結果の中で、評価が高く、予算1万円以内の麺棒を探してください。
その商品をカートに入れてください。
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        browser=browser,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
