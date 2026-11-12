import json

with open(r"C:\Users\vuasu\.gemini\antigravity\brain\6abc0cfc-ae3a-4837-a593-5fb8ab3f7be9\.system_generated\logs\transcript.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        obj = json.loads(line)
        idx = obj.get("step_index", 0)
        if 150 <= idx <= 180:
            print(f"=== Step {idx} ({obj.get('type')}) ===")
            if "content" in obj and obj["content"]:
                print("Content:", obj["content"][:300])
            if "thinking" in obj and obj["thinking"]:
                print("Thinking:", obj["thinking"][:300])
