import os
from dotenv import load_dotenv

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import AzureChatOpenAI
from langchain.llms import AzureOpenAI
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
        )
    # llm
    llm = AzureOpenAI(model_name="text-davinci-003")
    
    return chat, llm

### Conversation
from langchain import ConversationChain
def Conversation(chatLLM):
    conversation = ConversationChain(llm=chatLLM, verbose=True)
    res = conversation.predict(input="Hi there!")
    print("Conversation: ", res)

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
    print("\nchatMsg result: ",res)
    print("chatMsg useage: ",res.llm_output['token_usage'])

### ChatPromptTemplate & ChatChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
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

def main():
    load_dotenv()
    chat, llm = load_azureLLM()
    Conversation(chat)
    ChatMessage(chat)
    ChatPromptTempl(chat)
    ChatHistory(chat)
    ChatAgent(chat,llm)

if __name__ == "__main__":
    main()