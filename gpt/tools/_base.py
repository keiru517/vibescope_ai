import requests
import os
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

        print("GROK AI TOOL is called")
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
                "Authorization": f"Bearer {os.getenv('GROK_API_KEY')}",
            },
            json=data,
        )

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error {response.status_code}: {response.text}"  # Handle errors


class CoinMarketCapAPIInput(BaseModel):
    api_label: str = Field(description="API label to get data from CoinMarketCap API")


class CoinMarketCapAPITool(BaseTool):
    """
    The CoinMarketCapAPITool is a tool to get cryptocurrency data from CoinMarketCap API.

    Attributes:
        name: The name of the tool.
        description: The description of the tool and how to use it.
        args_schema: The schema for the arguments required by the tool.
        return_direct: Whether the results should be returned directly.
        api_map: The map of API endpoints to get data from.
    """

    # api_map: List of API endpoints to get data from.

    name: str = "CoinMarketCapAPITool"
    description: str = f"""
    Tool to get data from CoinMarketCap API.

    How to use this tool:
    - There is only one required input to trigger this tool.
        api_label: Required argument, representing the API endpoint to get data from CoinMarketCap API.
    """
    args_schema: Type[BaseModel] = CoinMarketCapAPIInput
    return_direct: bool = True
    api_map: dict = None

    def __init__(self, api_map: dict):
        #     # def __init__(self):
        super(CoinMarketCapAPITool, self).__init__()

        self.api_map = api_map

    def _run(self, api_label: str) -> str:
        """Use this tool."""
        print(f"Triggered API: {self.api_map[api_label]}")
        print("COIN MARKET CAP API TOOL is called", api_label)
        # base_url = "https://pro-api.coinmarketcap.com/"
        # url = f"{base_url}{self.api_map[api_label]}"
        # print("url", url)
        # return "cool"
        # response = requests.get(
        #     url=url,
        #     headers={"X-CMC_PRO_API_KEY": os.getenv("CMC_API_KEY")},
        # )
        # print("Response", response.json())
        # return response.json()


class TokenBallanceInput(BaseModel):
    wallet_address: str = Field(description="Wallet address to get data from")


class GetTokenBallanceTool(BaseTool):
    """
    The GetTokenBallanceTool is a tool to get the balance of a token in a wallet address.

    Attributes:
        name: The name of the tool.
        description: The description of the tool and how to use it.
        args_schema: The schema for the arguments required by the tool.
        return_direct: Whether the results should be returned directly.
    """

    name: str = "GetTokenBallanceTool"
    description: str = """
    Tool to get the balance of a token in a wallet address.

    How to use this tool:
    - There is only one required input to trigger this tool.
        wallet_address: Required argument, representing the wallet address to get the balance of the token.
    """
    args_schema: Type[BaseModel] = TokenBallanceInput
    return_direct: bool = True

    def _run(self, wallet_address: str) -> str:
        """Use this tool."""
        print("GetTokenBallanceTool is called", wallet_address)

        url = f"https://eth-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_API_KEY')}"

        payload = {
            "jsonrpc": "2.0",
            "method": "alchemy_getTokenBalances",
            "params": [wallet_address, "erc20"],
            "id": "42",
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=payload, headers=headers)
        print("Response:", response.json())
        return response.json()
