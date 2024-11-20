docker build -t llm-guardrails-chatbot-api:latest -f Dockerfile_api .
docker tag  llm-guardrails-chatbot-api abpzzareg.azurecr.io/llm-guardrails-chatbot-api:latest
docker push abpzzareg.azurecr.io/llm-guardrails-chatbot-api:latest
## redeploy app
kubectl apply -f api.yaml
kubectl rollout restart deployment chatbot-api -n llm-guardrail