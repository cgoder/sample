import os
from dotenv import load_dotenv

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import AzureChatOpenAI
from langchain.llms import AzureOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
AI_TEMPERATURE=0
AI_MAX_TOKENS=2048
def load_azureLLM():
    os.environ["OPENAI_API_TYPE"] = os.environ.get('OPENAI_API_TYPE')
    os.environ["OPENAI_API_VERSION"] = os.environ.get('OPENAI_API_VERSION')
    os.environ["OPENAI_API_BASE"] = os.environ.get('OPENAI_API_BASE')
    os.environ["OPENAI_API_KEY"] = os.environ.get('OPENAI_API_KEY')
    DEPLOYMENT_NAME_CHAT = os.environ.get('DEPLOYMENT_NAME_CHAT')
    DEPLOYMENT_NAME_EMBEDDING = os.environ.get('DEPLOYMENT_NAME_EMBEDDING')
    # chat
    chat = AzureChatOpenAI(
        deployment_name=DEPLOYMENT_NAME_CHAT,
        temperature=AI_TEMPERATURE,
        max_tokens=AI_MAX_TOKENS,
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()],
        )
    # llm
    llm = AzureOpenAI(model_name="text-davinci-003")
    
    return chat, llm

### Conversation
from langchain import ConversationChain
def Conversation(chatLLM):
    conversation = ConversationChain(llm=chatLLM, verbose=True)
    res = conversation.predict(input="Hi there!")
    print(f"Conversation: {res}")

### ChatMessage
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
def ChatMessage(chatLLM):
    chatLLM([HumanMessage(content="Translate this sentence from English to French. I love programming.")])

    messages = [
    SystemMessage(content="You are a helpful assistant that translates English to French."),
    HumanMessage(content="Translate this sentence from English to French. I love programming.")
    ]
    chatLLM(messages)

    batch_messages = [
        [
            SystemMessage(content="You are a helpful assistant that translates English to French."),
            HumanMessage(content="Translate this sentence from English to French. I love programming.")
        ],
        [
            SystemMessage(content="You are a helpful assistant that translates English to French."),
            HumanMessage(content="Translate this sentence from English to French. I love artificial intelligence.")
        ],
    ]
    res = chatLLM.generate(batch_messages)
    print(f"\nchatMsg result: {res}")
    print(f"chatMsg useage: {res.llm_output['token_usage']}")

### ChatPromptTemplate & ChatChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain import LLMChain
def ChatPromptTempl(chatLLM):
    template = "You are a helpful assistant that translates {input_language} to {output_language}."
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # get a chat completion from the formatted messages
    res = chatLLM(chat_prompt.format_prompt(input_language="English", output_language="French", text="I love programming.").to_messages())
    print("\nchatTempl result: ",res)

    # get a chat chain 
    chain = LLMChain(llm=chatLLM, prompt=chat_prompt)
    res = chain.run(input_language="English", output_language="Chinese", text="I love programming.")
    print("\nchatChain result: ",res)


### ChatHistory
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
def ChatHistory(chatLLM):
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know."),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    memory = ConversationBufferMemory(return_messages=True)
    conversation = ConversationChain(memory=memory, prompt=prompt, llm=chatLLM)
    res = conversation.predict(input="Hi there!")
    print("\nconversation result: ",res)
    res = conversation.predict(input="I'm doing well! Just having a conversation with an AI.")
    print("\nconversation result: ",res)
    res = conversation.predict(input="Tell me about yourself.")
    print("\nconversation result: ",res)


### ChatAgent
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
def ChatAgent(llm):
    tools = load_tools(["serpapi", "llm-math"], llm=llm)
    # Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
    agent = initialize_agent(tools, llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    # Now let's test it out!
    res = agent.run("刘强东的妻子是谁？他们是什么时候结婚的？")
    print("\nchatAgent result: ",res)

### FewShot
def FewShot(chat):
    template="You are a helpful assistant that translates english to pirate."
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    # example_human = HumanMessagePromptTemplate.from_template("Hi")
    example_human = SystemMessagePromptTemplate.from_template("Hi", additional_kwargs={"name": "example_user"})
    # example_ai = AIMessagePromptTemplate.from_template("Argh me mateys")
    example_ai = SystemMessagePromptTemplate.from_template("Argh me mateys", additional_kwargs={"name": "example_assistant"})
    human_template="{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, example_human, example_ai, human_message_prompt])
    chain = LLMChain(llm=chat, prompt=chat_prompt)
    # get a chat completion from the formatted messages
    res = chain.run("I love programming.")
    print("\nFewShot result: ",res)

def main():
    load_dotenv()
    chat, llm = load_azureLLM()
    Conversation(chat)
    ChatMessage(chat)
    ChatPromptTempl(chat)
    ChatHistory(chat)
    FewShot(chat)

if __name__ == "__main__":
    main()