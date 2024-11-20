# Banking RAG Chatbot Demo
---

This repository contains assets for a customer service chatbot for a bank. The chatbot is designed to answer queries on the bank's products and services.

The chatbot is implemented as a streamlit frontend, which calls an API from a product known as SAS Intelligent Decisioning. This product implements prompt guardrails on top of the RAG application (which is implemented using llama-index and Azure OpenAI), such as if the customer is submitting sensitive and personal information, or if the customer is expressing frustration which prompts the LLM to be more understanding and helpful in its responses.

The repository contains files for the streamlit application, and the actual RAG endpoint. Currently I am working on a version where the prompt guardrails are implemented in the actual streamlit application itself.

## Demo Recording

TBD

## File Contents & Setup

You will need your own Azure OpenAI key, or alternative LLM provider if you want to use this code.

For the streamlit app:
* Build the Docker container by running the bash script, build_and_push_container_guardrail.sh
* Originally this container is pushed to a container registry and deployed to K8s - if you are running locally, comment out every line except the first in build_and_push_container_guardrail.sh and run the container locally on port 8501.

For the RAG endpoint:
* Build the Docker container by running the bash script, build_and_push_container_api.sh
* Again, if running locally - comment out every line except the first and run the container locally on 8089.

There are additional scripts for reference:
* score_rag_chatbot.py = example Python score code to call the RAG endpoint
* prompt_catalog_cba.csv = example table containing system prompts for user with application