import json

from backend.analyzer import analyze_text


text = """
Rahul met Arjun at Park Street.
Arjun transferred ₹50,000 to Vikram.
Vikram owns vehicle WB02AB1234.
Vikram contacted Sameer.
Sameer met Rahul.
Arjun works for TechNova Solutions.
Sameer contacted Arjun.
Vikram transferred ₹20,000 to Rahul.
"""


result = analyze_text(text)

print(json.dumps(result, indent=2, ensure_ascii=False))