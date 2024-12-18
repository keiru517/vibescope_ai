from gpt import _BaseGPTAgent

agent = _BaseGPTAgent("The system runs on the collection of tools")
while True:
    message = input("Question: ")
    response = agent.run(message)
    print("Answer:", response)
