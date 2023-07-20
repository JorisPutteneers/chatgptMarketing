
import subprocess
import json
import requests
import re

API_KEY = "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"
url = "https://www.villasinfrankrijk.be/vakantieverblijven/gite-menerolle/"
example = '''Ontsnap naar het paradijs in Le Grand Coutiou! 🌞✨Droom je van een adembenemend vakantieverblijf in het prachtige Frankrijk? Zoek niet verder! 🌿🍷
Geniet van het luxueuze comfort van Le Grand Coutiou, omgeven door weelderige natuur en rustige sereniteit. 🌱
💦 Neem een verfrissende duik in het schitterende privézwembad 🍽️ Ervaar de heerlijke Franse keuken en geniet van sfeervolle diners op het terras met een adembenemend 
🗺️ Maak prachtige wandelingen, ontdek pittoreske stadjes zoals Poitiers en proef van de rijke cultuur die Frankrijk te bieden heeft
Wacht niet langer, boek vandaag nog jouw droomvakantie in Le Grand Coutiou! ✨'''




def get_og_description(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            pattern = r'<meta property="og:description" content="([^"]*)"'
            matches = re.findall(pattern, response.text)
            if matches:
                return matches[0]
            else:
                return "No <meta property=\"og:description\"> tag found."
        else:
            return f"Error: Status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


content = f"zeg iets over dit vakantiehuis. max 100 woorden, en gebruik soms een enoji. met dit als content: {get_og_description(url)}.  '{example}'"


def getContent():
    curl_content = """curl -s https://www.villasinfrankrijk.be/vakantieverblijven/le-bonheur-bb-suite-cognac/ | grep -o '<meta property="og:description" content="[^"]*"' | sed 's/<meta property="og:description" content="//' | sed 's/"$//'"""
    try:
        content = subprocess.run(curl_content, capture_output=True, text=True)
        response_json = json.loads(content.stdout)
        return response_json
    except subprocess.CalledProcessError as e:
        print("Error executing the curl command:", e)
        return None


def call_openai_api(API_KEY, content):
    curl_cmd = [
        "curl",
        "https://api.openai.com/v1/chat/completions",
        "-H",
        "Content-Type: application/json",
        "-H",
        f"Authorization: Bearer {API_KEY}",  # Replace "YOUR_API_KEY" with your actual API key
        "-d",
        json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": content}],
            "temperature": 0.7
        })
    ]

    try:
        result = subprocess.run(curl_cmd, capture_output=True, text=True)
        response_json = json.loads(result.stdout)
        return response_json
    except subprocess.CalledProcessError as e:
        print("Error executing the curl command:", e)
        return None

if __name__ == "__main__":
    response = call_openai_api(API_KEY, content)

    if response:
        print(json.dumps(response, indent=2))
