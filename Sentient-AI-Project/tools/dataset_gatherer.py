import requests
from bs4 import BeautifulSoup
import json
import os
import time
from datetime import datetime
from duckduckgo_search import DDGS

def search_duckduckgo(topic, max_results=100):
    urls = []
    with DDGS() as ddgs:
        for r in ddgs.text(topic, max_results=max_results):
            if 'href' in r:
                urls.append(r['href'])
    return urls

def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        for script in soup(["script", "style", "header", "footer", "nav", "aside", "form"]):
            script.decompose()
        text = ' '.join(soup.stripped_strings)
        return text
    except Exception as e:
        print(f"[Error] Failed to extract from {url}: {e}")
        return ""

def clean_text(text):
    lines = text.split('\n')
    cleaned = []
    seen = set()
    for line in lines:
        line = line.strip()
        if line and line not in seen:
            seen.add(line)
            cleaned.append(line)
    return ' '.join(cleaned)

def ensure_folder(topic):
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    topic_folder = f"../datasets/{topic.replace(' ', '_').lower()}/{date_str}/"
    os.makedirs(topic_folder, exist_ok=True)
    return topic_folder

def gather_topic_data(topic):
    urls = search_duckduckgo(topic)
    dataset = []

    for url in urls:
        print(f"[Gathering] {url}")
        raw_text = extract_text_from_url(url)
        cleaned_text = clean_text(raw_text)

        if len(cleaned_text.split()) > 100:
            dataset.append({
                "topic": topic,
                "url": url,
                "content": cleaned_text,
                "word_count": len(cleaned_text.split()),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })

        time.sleep(1.5)

    return dataset

def save_dataset(topic, dataset):
    folder_path = ensure_folder(topic)
    filename = folder_path + f"{topic.replace(' ', '_').lower()}_dataset.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"[Saved] Dataset for topic: {topic}")

def load_topics_from_file(filename="starter_topics.txt"):
    try:
        with open(filename, "r") as file:
            topics = [line.strip() for line in file if line.strip()]
        return topics
    except FileNotFoundError:
        print(f"⚠️ File not found: {filename}")
        return []

if __name__ == "__main__":
    user_topic = input("🌸 Enter a topic to gather (or press Enter to use the starter list): ").strip()

    if user_topic:
        print(f"\n✨ Gathering manually entered topic: {user_topic}")
        dataset = gather_topic_data(user_topic)
        save_dataset(user_topic, dataset)
        print(f"✅ Done gathering for topic: {user_topic}")
    else:
        print("\n🌸 No topic entered. Reading starter topics list... 🌸")
        topics = load_topics_from_file()

        if not topics:
            print("⚠️ No topics to gather. Exiting.")
            exit(1)

        for topic in topics:
            print(f"\n🌸 Gathering topic: {topic} 🌸")
            dataset = gather_topic_data(topic)
            save_dataset(topic, dataset)
            print(f"✅ Finished gathering for: {topic}")
            print("----------------------------------------")
            time.sleep(5)  # Optional soft pause between topics

        print("\n🌟 All listed topics have been gathered! 🌟")
