from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_openai import ChatOpenAI
from IPython.display import Image, display
import gpt as ai


class _BaseGPTAgent:
    def __init__(self, prompt):
        self.__tools = [ai.tools.GetWeatherTool(), ai.tools.GetTokenInfoTool()]
        self.__tool_node = (
            ai.graphs.nodes.ToolNode(tools=self.__tools) if self.__tools else None
        )

        self.__prompt = ChatPromptTemplate.from_messages(
            messages=[
                ("system", prompt),
                ("user", "{message}"),
            ]
        )
        self.__build_agent()

    def __chatbot(self, state: ai.graphs.states.State):
        message = self.__chain.invoke(state["messages"])
        return {"messages": [message]}

    def __build_agent(self):
        self.__llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3,
            api_key="OPENAI_API_KEY",
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
        config = {"configurable": {"thread_id": "1"}, "recursion_limit": 20}
        response = self.__agent.invoke(
            {
                "messages": [message],
            },
            config=config,
        )
        return response["messages"][-1].content

    def run(self, message: str) -> str:
        return self.__run(message=message)
