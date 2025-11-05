from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph, CompiledGraph
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, RemoveMessage
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.checkpoint.mongodb.aio import AsyncMongoDBSaver
from src.utils import vectorStore, llm, mongodbClient, responsePrompt, summarizeMessagePrompt


class messagesState (MessagesState):
    summary: str

class RetriverError (Exception):
    pass

class LLMCallError (Exception):
    pass

class DB_Error (Exception):
    pass

async def retrieve (query: str) -> str:
    """
    This is a tool call to retieve relevant contents fromn the vectors document

    Args:
        query: A string of the query

    Returns:
        A string of the serialized retrieval
    """
    #print (query)
    try:
        doc = await vectorStore.amax_marginal_relevance_search(query, k=5, fetch_k=20)
    except Exception as e:
        raise RetriverError (f"Error why retrieving context {e}.") from e
    else:
        doc_content = "\n\n".join(f"Source: {d.metadata["source"]}, title: {d.metadata['title']}, page: {d.metadata['page_label']} \nContent: {d.page_content}" for d in doc)

        return doc_content

async def summarize_conversation (state: messagesState) -> messagesState:
    """
        This Function summarizes the conversation to minimize the token input to the LLM
    """

    summary = state.get('summary', '')
    messages = state['messages']

    if len(messages) > 10:
        if summary:
            summary_message = summary
        else:
            summary_message = "No summary of the conversation so far"

        msg = (
            "Taking into account the previous summary:\n"
            "{summary}\n\n"
            "Summarize the following conversation\n"
            "{conversation}"
        )

        msg = msg.format (summary=summary_message, conversation=messages)
        try:
            response = await llm.ainvoke ([SystemMessage(content=summarizeMessagePrompt)] + [HumanMessage(content=msg)])
        except Exception as e:
            raise LLMCallError (f"Error why making LLM call {e}") from e

        else:
            delete_messages = [RemoveMessage(id=m.id) for m in state['messages'][:-2]]
            return {'summary': response.content, 'messages':delete_messages}
    else:
        return state

async def llm_call (state: messagesState) -> messagesState:
    try:
        response = await llm_with_tool.ainvoke ([SystemMessage(content=responsePrompt)] + state['messages'])
    except Exception as e:
            raise LLMCallError (f"Error why making LLM call {e}") from e
    else:
        return {'messages': response}

async def RAG () -> CompiledStateGraph:
    builder = StateGraph (MessagesState)
    builder.add_node ("LLM", llm_call)
    builder.add_node ("tools", ToolNode(tools))
    builder.add_node ('summarize conversation', summarize_conversation)

    builder.add_edge (START, 'summarize conversation')
    builder.add_edge ('summarize conversation', "LLM")
    builder.add_conditional_edges ("LLM", tools_condition)
    builder.add_edge ("tools", "LLM")

    try:
        memorydb = AsyncMongoDBSaver (client=mongodbClient, db_name="RAG_Memory", checkpoint_collection_name="RAG_Chat_memory")
    except Exception as e:
        raise DB_Error (f"Error connecting to db {e}") from e
    else:
        graph = builder.compile (checkpointer=memorydb)
        return graph

async def getResponse (query:str, thread_id:str) -> str:
    msg = HumanMessage (content=query)
    config = {'configurable': {'thread_id': thread_id}}
    try:
        response = await graphAgent.ainvoke (input={'messages': [msg]}, config=config)
    except:
        raise
    else:
        return response['messages'][-1].content

async def streamResponse (query:str, thread_id:str):
    node_to_stream = "LLM"
    msg = HumanMessage (content=query)
    config = {'configurable': {'thread_id': thread_id}}
    try:
        async for event in graphAgent.astream_events (input={'messages': [msg]}, config=config, version='v2'):
            if event ['event'] == 'on_chat_model_stream' and event['metadata'].get('langgraph_node', '') == node_to_stream:
                chunk = event['data']['chunk'].content
                if chunk:
                    print (chunk, end='', flush=True)
                    yield chunk.encode ('utf-8')
    except:
        yield "---Error Occured---"

async def init_graph ():
    global graphAgent
    try:
        graphAgent = await RAG ()
    except:
        raise
    return None



tools = [retrieve]
llm_with_tool = llm.bind_tools (tools)

graphAgent = None

