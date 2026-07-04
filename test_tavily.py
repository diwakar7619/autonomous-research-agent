from services.tavily_service import search_web

results = search_web("Latest AI news")

print(f"Results Found: {len(results)}")

for result in results:
    print("-" * 80)
    print("Title :", result.get("title"))
    print("URL   :", result.get("url"))
    print("Score :", result.get("score"))
