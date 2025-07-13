import os
import json

def browse_datasets(base_folder="../datasets/"):
    for topic_folder in sorted(os.listdir(base_folder)):
        topic_path = os.path.join(base_folder, topic_folder)
        if os.path.isdir(topic_path):
            print(f"\n🌸 Topic: {topic_folder.replace('_', ' ').title()} 🌸")
            for date_folder in sorted(os.listdir(topic_path)):
                date_path = os.path.join(topic_path, date_folder)
                if os.path.isdir(date_path):
                    for filename in os.listdir(date_path):
                        if filename.endswith(".json"):
                            file_path = os.path.join(date_path, filename)
                            with open(file_path, "r", encoding="utf-8") as f:
                                dataset = json.load(f)
                                print(f"\n🗓️ Date: {date_folder}")
                                for i, entry in enumerate(dataset, start=1):
                                    print(f"\n{i}. 🔹 Source: {entry['url']}")
                                    print(f"   🔸 Word count: {entry['word_count']}")
                                    print(f"   🔸 Preview: {entry['content'][:250]}...")  # Show first 250 characters

if __name__ == "__main__":
    browse_datasets()
