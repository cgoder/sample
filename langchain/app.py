from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import AzureChatOpenAI
import os
from dotenv import load_dotenv


AI_TEMPERATURE=0
AI_MAX_TOKENS=2048

def load_azureLLM():
    os.environ["OPENAI_API_TYPE"] = os.environ.get('OPENAI_API_TYPE')
    os.environ["OPENAI_API_VERSION"] = os.environ.get('OPENAI_API_VERSION')
    os.environ["OPENAI_API_BASE"] = os.environ.get('OPENAI_API_BASE')
    os.environ["OPENAI_API_KEY"] = os.environ.get('OPENAI_API_KEY')
    DEPLOYMENT_NAME_CHAT = os.environ.get('DEPLOYMENT_NAME_CHAT')
    DEPLOYMENT_NAME_EMBEDDING = os.environ.get('DEPLOYMENT_NAME_EMBEDDING')
    
    chat = AzureChatOpenAI(
        deployment_name=DEPLOYMENT_NAME_CHAT,
        temperature=AI_TEMPERATURE,
        max_tokens=AI_MAX_TOKENS,
        )
    # 初始化向量模型
    embedding = OpenAIEmbeddings(deployment = DEPLOYMENT_NAME_EMBEDDING,chunk_size=1)
    
    return chat, embedding

from langchain import ConversationChain

def conversation():
    llm, embedding = load_azureLLM()
    conversation = ConversationChain(llm=llm, verbose=True)
    output = conversation.predict(input="Hi there!")
    print(output)

def main():
    load_dotenv()
    conversation()

if __name__ == "__main__":
    main()