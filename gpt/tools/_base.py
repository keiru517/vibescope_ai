import requests
from typing import Optional, Type

from langchain_core.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field
import json


class WeatherInput(BaseModel):
    city: str = Field(description="Name of the city")


class GetWeatherTool(BaseTool):
    """
    A tool to get weather in a city.

    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool and how to use it.
        args_schema (Type[BaseModel]): The schema for the arguments required by the tool.
        return_direct (bool): Whether the results should be returned directly.
    """

    name: str = "GetWeather"
    description: str = """
    Useful for when you need to answer questions about weather in a city.

    How to use this tool:
    - There is only one required input to triger this tool.
        city: Required argument, name of the city for weather.
    """

    args_schema: Type[BaseModel] = WeatherInput
    return_direct: bool = True

    def _run(self, city: str):
        """Use the tool."""

        print("WEATHER TOOL is called")
        return f"Weather in {city} is hot"


class TokenInput(BaseModel):
    content: str = Field(description="Content for crypto tokens")


class GetTokenInfoTool(BaseTool):
    """
    A tool to get information about crypto tokens.

    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool and how to use it.
        args_schema (Type[BaseModel]): The schema for the arguments required by the tool.
        return_direct (bool): Whether the results should be returned directly.
    """

    name: str = "GetTokenInfoTool"
    description: str = """
    Useful when you need to answer questions about crypto token news or something.

    How to use this tool:
    - There is only one required input to trigger this tool.
        content: Required argument, question about crypto token.
    """
    args_schema: Type[BaseModel] = TokenInput
    return_direct: bool = True

    def _run(self, content: str):
        """Use this tool."""

        print("GROK TOOL is called")
        system_prompt = """You are a cryptocurrency news chatbot, designed to provide the latest and most relevant information about crypto tokens.
        Your main goal is to inform users about market trends, recent token developments, news, and important updates in the cryptocurrency space"""
        data = {
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {"role": "user", "content": content},
            ],
            "model": "grok-2-1212",
            "stream": False,
            "temperature": 0,
        }

        response = requests.post(
            url="https://api.x.ai/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer xai-kq0sSPAcc5wEhygSH9nnopVyZifupdYZXXamUyfUPv25Mw64pBEMtMGIh8m5AvOwGAzudyJduOw1arQv",
            },
            json=data,
        )

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error {response.status_code}: {response.text}"  # Handle errors
