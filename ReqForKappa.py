import requests
import difflib
from bs4 import BeautifulSoup

def format_wiki_link(quest_name):
    base = "https://escapefromtarkov.fandom.com/wiki/"
    return base + quest_name.replace(" ", "_")

# Load the Quests page once
def load_quests():
    url = "https://escapefromtarkov.fandom.com/wiki/Quests"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    required_quests = {}
    for table in soup.select("table.wikitable"):
        for row in table.select("tr"):
            cells = row.find_all(['td', 'th'])
            if cells:
                quest_link = cells[0].find("a")
                if quest_link:
                    href = quest_link.get("href", "")
                    if href.startswith("/wiki/") and not any(x in href for x in ["Category:", "File:", "Template:"]):
                        quest_name = quest_link.get_text(strip=True)
                        kappa_cell = cells[-1].get_text(strip=True).lower()
                        kappa_required = kappa_cell == 'yes'
                        required_quests[quest_name.lower()] = (kappa_required, quest_name)
    return required_quests

# Main function to check quest
def check_kappa_requirement(user_input, quest_data):
    user_input = user_input.strip().lower()

    if user_input in quest_data:
        is_required, original_name = quest_data[user_input]
        return {
            "status": "found",
            "exact": True,
            "required": is_required,
            "quest_name": original_name,
            "link": format_wiki_link(original_name)
        }

    # Substring or fuzzy matches
    matches = [name for name in quest_data if user_input in name]
    if not matches:
        matches = difflib.get_close_matches(user_input, list(quest_data.keys()), n=5, cutoff=0.6)

    if matches:
        suggestions = [quest_data[m][1] for m in matches]
        return {
            "status": "multiple",
            "matches": suggestions
        }

    return {
        "status": "not_found"
    }