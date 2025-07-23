from typing import TypedDict, Annotated, Any
from dotenv import load_dotenv
from time import sleep
from rich.console import Console
from rich.markdown import Markdown

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command

from langsmith import traceable

# load all environment variables
load_dotenv(override=True)
console = Console()


class State(TypedDict):
    messages: Annotated[list, add_messages]


@tool
def get_stock_price(symbol: str) -> float:
    """return latest stock price for stock symbol"""
    return {
        "MSFT": 200.3,
        "AAPL": 100.4,
        "AMZN": 150.0,
        "RIL": 87.6,
    }.get(symbol, 0.0)


@tool
def buy_stock(symbol: str, quantity: int) -> str:
    """buy stock with given symbol and quantity"""
    stock_price = get_stock_price(symbol)
    total_price = stock_price * quantity
    # here I'd like to ask the human to approve the "buy" before proceeding
    console.print(
        f"""[red]
        You are about to buy {quantity} shares of {symbol} at {stock_price:.2f}/share 
        for a total of {total_price:.2f}.[/red]"""
    )
    # at this point, control goes out of graph to caller
    user_response = interrupt("")

    if user_response.strip().lower() == "yes":
        return f"You bought {quantity} shares of {symbol} (at {stock_price:.2f}/share) for {total_price:.2f}."
    else:
        return f"Buying of {quantity} shares of {symbol} was cancelled."


tools = [get_stock_price, buy_stock]

# instantiate your llm & bind with tools
llm = init_chat_model("google_genai:gemini-2.5-flash", temperature=0.0)
llm_with_tools = llm.bind_tools(tools)
memory = MemorySaver()


def chatbot(state: State) -> State:
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# build our graph
builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode(tools))
# build edges: START -> chatbot -> END
builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition)
# loop back to chatbot from tools node
builder.add_edge("tools", "chatbot")
builder.add_edge("chatbot", END)
graph = builder.compile(checkpointer=memory)


@traceable
def run_chatbot(prompt: str, config=None) -> dict[str, Any] | Any:
    message = {"role": "user", "content": prompt}
    if config is not None:
        response = graph.invoke({"messages": [message]}, config=config)
    else:
        response = graph.invoke({"messages": [message]})

    return response


# set config for memory
config = {"configurable": {"thread_id": "abc@123"}}

# Step 1: check price of AMZN stock
prompt: str = "What is the latest price for AMZN stock? Return just the price."
response = run_chatbot(prompt, config)
stock_price = response["messages"][-1].content
console.print(f"Current price of AMZN is {stock_price} per share", style="cyan")
# deliberate call to prevent rate limit errors
sleep(1)

# Step 2: buy the stock
prompt: str = "Buy 25 stock of AMZN"
# this invoke will result in call to the "buy_stock" tool
response = graph.invoke(
    {"messages": [{"role": "user", "content": prompt}]},
    config=config,
)
# we have an "interrupt()" call in the "buy_stock" tool function, which
# immediately quits the tool & returns control to here
# we ask user if he/she wants to proceed
console.print("[red]Do you want to proceed (yes/no)?[/red]  ", end="")
user_response = input()
# user_response is passed back to the point where "interrupt" was called
# in the "buy_stock" tool - the Command(...) call passes back the response
# we get from user as a "return value" from the "interrupt(...)" call
response = graph.invoke(Command(resume=user_response), config=config)
# this is then the response returned from the "buy_stock" tool
console.print(response["messages"][-1].content, style="cyan")
# deliberate call to prevent rate limit errors
sleep(1)
