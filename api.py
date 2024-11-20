import os
from dotenv import load_dotenv, find_dotenv
load_dotenv()

from flask import Flask, request, jsonify, make_response
from llama_index.core.indices import loading
import os

## llama-index
from llama_index.core import SimpleDirectoryReader

from llama_index.core.node_parser import SentenceWindowNodeParser

from llama_index.core.indices.postprocessor import MetadataReplacementPostProcessor
from llama_index.core.node_parser import SentenceWindowNodeParser
from llama_index.core import Settings

from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding

from llama_index.core.indices.postprocessor import SentenceTransformerRerank
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core import load_index_from_storage

api_key = os.getenv("azure_openai_key")
azure_endpoint = "https://ssayjc.openai.azure.com/"
api_version = "2024-08-01-preview"

app = Flask(__name__)


## RAG functions
def load_documents():
    # logger.info('Loading all the documents')
    return SimpleDirectoryReader(
        input_dir = f"rag_data/"
    ).load_data()

def load_embed():
    return AzureOpenAIEmbedding(
        model="text-embedding-ada-002",
        deployment_name="ssayjc-ada-002",
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        api_version=api_version,
    )

def load_model():
    return AzureOpenAI(
        model="gpt-35-turbo-16k",
        engine = "ssayjc-gpt35-turbo-16k", ## swap to "ssayjc-gpt-4o"
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        api_version=api_version,
    )

Settings.llm = load_model()
Settings.embed_model = load_embed()

# create the sentence window node parser w/ default settings
node_parser = SentenceWindowNodeParser.from_defaults(
    window_size=3,
    window_metadata_key="window",
    original_text_metadata_key="original_text",
)
Settings.node_parser = node_parser
documents = load_documents()

## Saves to a index store directory
if not os.path.exists("sentence_index"):
    sentence_index = VectorStoreIndex.from_documents(documents)
    sentence_index.storage_context.persist(persist_dir="sentence_index")
    
else:
    sentence_index = load_index_from_storage(
        StorageContext.from_defaults(persist_dir="sentence_index")
    )

# define postprocessors
postproc = MetadataReplacementPostProcessor(target_metadata_key="window")
rerank = SentenceTransformerRerank(
    top_n=2, model=f"BAAI/bge-reranker-base"
)

sentence_window_engine = sentence_index.as_query_engine(
    similarity_top_k=6, node_postprocessors=[postproc, rerank]
)

@app.route("/rag_completion", methods=['POST'])
def rag_completion():
    data = request.get_json()
    prompt = data['prompt']
    response = sentence_window_engine.query(prompt)
    response_dict = {
        'response': str(response)
    }
    sources = {}
    for i, source_node in enumerate(response.source_nodes):
        sources[f"source_{i}"] = source_node.text

    return jsonify(
        {
            **response_dict,
            **sources
        }
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8089, debug=True)