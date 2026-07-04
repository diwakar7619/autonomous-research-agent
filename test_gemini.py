from services.tavily_service import search_web
from services.gemini_service import summarize_results

results = search_web("Latest AI news")

summary = summarize_results(results)

print(summary)
