import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# Set up Chrome options (if needed)
chrome_options = webdriver.ChromeOptions()
# Add any desired options to chrome_options here

# Specify the path to the ChromeDriver executable
driver_path = r"C:\chromedriver-win64\chromedriver.exe"
# Update with the actual path to chromedriver.exe

# Create a ChromeDriver service
chrome_service = Service(executable_path=driver_path)

# Use the ChromeDriver service to create a WebDriver instance
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Make a request to the website
url = "https://premiumpension.com/our-branch-offices/"
driver.get(url)

# Wait for the page to load (you may need to adjust the wait time)
# Example: wait for up to 10 seconds for elements to appear
driver.implicitly_wait(10)

# Get the page source after waiting
page_source = driver.page_source

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

# Find all office blocks
office_blocks = soup.find_all("div", class_="col-sm")

# Initialize a list to store dictionaries for each block
office_data = []

# Loop through the office blocks
for office_block in office_blocks:
    h5_tag = office_block.find("h5")
    if h5_tag:
        state = h5_tag.get_text(strip=True)
    else:
        state = "N/A"

    b_tag = office_block.find("b")
    if b_tag:
        personnel_name = b_tag.get_text(strip=True)
    else:
        personnel_name = "N/A"

    a_tag = office_block.find("a", href=True)
    if a_tag:
        email = a_tag["href"].replace("mailto:", "")
    else:
        email = "N/A"

    p_tag = office_block.find("p")
    if p_tag:
        br_tags = p_tag.find_all("br")
        if len(br_tags) > 1:
            phone = br_tags[1].next_sibling.strip()
        else:
            phone = "N/A"
    else:
        phone = "N/A"

    address_tag = office_block.find("address")
    if address_tag:
        address = address_tag.get_text(strip=True)
    else:
        address = "N/A"

    # Create a dictionary for this block's data
    block_data = {
        "Organization Name": "Premium Pension Limited",
        "State": state,
        "Personnel": personnel_name,
        "Email": email,
        "Phone": phone,
        "Tel": "N/A",
        "Address": address
    }

    # Append the dictionary to the list
    office_data.append(block_data)

    # Print the extracted data for debugging
    print(f"State: {state}")
    print(f"Personnel: {personnel_name}")
    print(f"Email: {email}")
    print(f"Phone: {phone}")
    print(f"Tel: N/A")
    print(f"Address: {address}")
    print("-" * 40)  # Separator between records

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(office_data)

# Save the data to a CSV file
df.to_csv("premiumpension_data.csv", index=False)

# Close the Chrome WebDriver
driver.quit()

# Print a message to indicate that the data has been saved
print("Data has been saved to premiumpension_data.csv")
