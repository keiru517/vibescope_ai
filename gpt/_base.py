import os
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_openai import ChatOpenAI
from IPython.display import Image, display
import gpt as ai


class _BaseGPTAgent:
    def __init__(self, prompt):
        api_map = {
            "cryptocurrency_listings_latest": "/v1/cryptocurrency/listings/latest",
            "cryptocurrency_listings_historical": "/v1/cryptocurrency/listings/historical",
            "cryptocurrency_quotes_latest": "/v2/cryptocurrency/quotes/latest",
            "cryptocurrency_quotes_historical": "/v2/cryptocurrency/quotes/historical",
            "cryptocurrency_market_pairs_latest": "/v2/cryptocurrency/market-pairs/latest",
            "cryptocurrency_ohlcv_latest": "/v2/cryptocurrency/ohlcv/latest",
            "cryptocurrency_ohlcv_historical": "/v2/cryptocurrency/ohlcv/historical",
            "cryptocurrency_price_performance_stats": "/v2/cryptocurrency/price-performance-stats/latest",
            "cryptocurrency_categories": "/v1/cryptocurrency/categories",
            "cryptocurrency_category": "/v1/cryptocurrency/category",
            "cryptocurrency_airdrops": "/v1/cryptocurrency/airdrops",
            "cryptocurrency_airdrop": "/v1/cryptocurrency/airdrop",
            "cryptocurrency_trending_latest": "/v1/cryptocurrency/trending/latest",
            "cryptocurrency_trending_most_visited": "/v1/cryptocurrency/trending/most-visited",
            "cryptocurrency_trending_gainers_losers": "/v1/cryptocurrency/trending/gainers-losers",
            # Global metrics endpoints
            "global_metrics_quotes_latest": "/v1/global-metrics/quotes/latest",
            "global_metrics_quotes_historical": "/v1/global-metrics/quotes/historical",
            # Content endpoints
            "content_latest": "/v1/content/latest",
            "content_posts_top": "/v1/content/posts/top",
            "content_posts_latest": "/v1/content/posts/latest",
            "content_posts_comments": "/v1/content/posts/comments",
        }
        self.__tools = [
            ai.tools.GetTokenInfoTool(),
            # ai.tools.CoinMarketCapAPITool(api_map=api_map),
            # ai.tools.CoinMarketCapAPITool(),
            ai.tools.GetTokenBallanceTool(),
        ]
        self.__tool_node = (
            ai.graphs.nodes.ToolNode(tools=self.__tools) if self.__tools else None
        )
        api_map_str = "\n".join([f"{k}: {v}" for k, v in api_map.items()])
        system_prompt = f"""
        You are a helpful assistant that can help with the following tasks:
        {prompt}

        """
        # Here are the API endpoints for the cryptocurrency data:
        # {api_map_str}
        self.__prompt = ChatPromptTemplate.from_messages(
            messages=[
                ("system", system_prompt),
                ("user", "{message}"),
            ]
        )

        self.__build_agent()

    def __chatbot(self, state: ai.graphs.states.State):
        message = self.__chain.invoke(state["messages"])
        return {"messages": [message]}

    def __build_agent(self):
        self.__llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        if self.__tools:
            self.__llm = self.__llm.bind_tools(self.__tools)
            print("Bined tools")

        self.__chain = self.__prompt | self.__llm

        self.__graph_builder = ai.graphs.StateGraph(state_schema=ai.graphs.states.State)
        self.__graph_builder.add_node("chatbot", self.__chatbot)
        if self.__tool_node:
            self.__graph_builder.add_node("tools", self.__tool_node)
            print("Tool node is added")
        self.__graph_builder.set_entry_point("chatbot")
        self.__graph_builder.set_finish_point("chatbot")
        if self.__tool_node:
            self.__graph_builder.add_conditional_edges(
                "chatbot", ai.graphs.nodes.tools_condition
            )
            self.__graph_builder.add_edge("tools", "chatbot")

        self.__agent = self.__graph_builder.compile()
        # display(Image(self.__agent.get_graph().draw_mermaid_png()))
        # graph_data = self.__agent.get_graph().draw_mermaid_png()
        # with open("graph.png", "wb") as f:
        #     f.write(graph_data)

    def __run(self, message: str) -> str:
        # try:
        config = {"configurable": {"thread_id": "1"}, "recursion_limit": 20}
        response = self.__agent.invoke(
            {
                "messages": [message],
            },
            config=config,
        )
        return {"answer": response["messages"][-1].content, "status": 200}
        # except Exception as e:
        #     return {"answer": str(e), "status": 500}

    def run(self, message: str) -> str:
        return self.__run(message=message)
