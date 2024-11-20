docker build -t llm-guardrails-chat:latest .
docker tag  llm-guardrails-chat abpzzareg.azurecr.io/llm-guardrails-chat
docker push abpzzareg.azurecr.io/llm-guardrails-chat
## redeploy app
kubectl apply -f guardrail_app.yaml
kubectl rollout restart deployment guardrail-chat -n llm-guardrail