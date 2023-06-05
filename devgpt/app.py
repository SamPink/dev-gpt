import devgpt.prompts.config as config
from devgpt import GPT4

# Create a GPT4 instance
gpt4 = GPT4(config.OPENAI_API_KEY)

task = """
build me an app collects as much data as possible on each house,

I want to start with the floor plan, picttures and location.

using this build a model for each house.

also get proces for houses that have recently sold.

base code: 
def rightmove_scraper():
    url = "https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E1440&propertyTypes=&maxDaysSinceAdded=3&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    for property_div in soup.find_all("div", class_="propertyCard"):
        try:
            price = property_div.find("div", class_="propertyCard-priceValue").string.strip()
        except AttributeError:
            price = "N/A"

        try:
            address = property_div.find("span", class_="propertyCard-address").string.strip()
        except AttributeError:
            address = "N/A"

        print(f"Rightmove - Price: {price}, Address: {address}")
        
"""

gpt4.start_project(task)

# Prompt the user to add more messages until they enter "quit" or "exit"
while True:
    message_text = input("Enter a new message (or type 'quit' to exit): ")
    if message_text.lower() in ["quit", "exit"]:
        break

    gpt4.update_project(message_text)