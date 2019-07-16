#  Simple html webscraper template made for newegg.ca. Writes scraped data into a microsoft excel doc.
#  Was made fairly quickly to compare cpu prices between AMD and Intel during a store sale. Resulting in
#  not being as robust as it should be. However, scaling this script should be easy and I'll come back to it
#  when I have time.

#  Written By: Rusty
#  Written In: Python 3.7

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import smtplib

my_url = 'https://www.newegg.ca/p/pl?N=100007670%2050001028&PageSize=96'

# Opening connection, and downloading the webpage
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html Parsing
page_soup = soup(page_html, "html.parser")
# Grabs each product container
containers = page_soup.findAll("div", {"class": "item-container"})
# Keeps track of number of products
product_id = 0

# Open CSV
file = "products.csv"
f = open(file, "w")
# Name headers for columns in csv
headers = "Brand, Product Name, Price, Shipping \n"
# Write the headers
f.write(headers)

# Loop through and find all wanted data on items
for container in containers:
    product_id += 1
    try:
        brand_container = container.find("a", {"class": "item-brand"})
        brand = brand_container.find("img")['title']
    except:
        brand = "N/A"

    try:
        name_container = container.find("a", {"class": "item-title"})
        product_name = name_container.text
    except:
        product_name = "N/A"

    try:
        price_container = container.find("li", {"class": "price-current"})
        pc = price_container.find("strong").text
        pc2 = price_container.find("sup").text
        price = pc + pc2
    except:
        price = "N/A"

    try:
        shippping_container = container.find("li", {"class": "price-ship"})
        shipping = shippping_container.text.strip()
    except:
        shipping = "N/A"


    print("Item #: " + str(product_id))
    print("Brand: " + brand)
    print("Product Name: " + product_name.replace(",","|"))
    print("Price: " + price)
    print("Shipping: " + shipping)
    print("\n")
    # Write to csv. Replaces any ',' in name and prices to '|' avoiding accidental new lines in csv 
    f.write(brand + "," + product_name.replace(",", "|") + "," + price.replace(",", "") + "," + shipping + "\n")

# Close CSV
f.close()
print("TOTAL ITEMS CHECKED: %s/%s" %(product_id, len(containers)) )

print("Prepping email to be sent...")
try:
    # 587 default port
    server = smtplib.SMTP("smtp.gmail.com",587)
    # Establishes mail server connection and identifies itself
    server.ehlo()
    # Start encryption using TLS Protocol **NOTE: SSL is deprecated
    server.starttls()
except:
    print("ERROR: Unable to start mail server using TLS Protocol.")

# Decided to use a local text file to store user and bot credentials in the format
# Bot user creds -> name@gmail.com:password -> stored in UserAuth.txt
# Client creds -> name:client@gmail.com -> stored in MailList.txt
# **NOTE** Storing user information in plain text like this is a horrible fucking idea!
# This was made quickly so storing info on a local file is still better than leaving it in
# the script in plain text.
# If I come back to this script I'll add a some encrypt/ decrypt functions for security 

# Get bot email accounts login credentials
AuthFile = open(r"C:\Users\wongr\Documents\GitHub\Python_Scraper\UserAuth.txt", "r")
user_creds = AuthFile.readlines()
for user in user_creds:
    user_creds_cleaned = user.strip().split(':')
    # Get User ID and Pass
    user_id, user_pass = user_creds_cleaned
AuthFile.close()

# Get clients in mail list credentials
MailList = open(r"C:\Users\wongr\Documents\GitHub\Python_Scraper\MailList.txt", "r")
client_creds = MailList.readlines()
for client in client_creds:
    client_creds_cleaned = client.strip().split(':')
    # Get Client ID and Email
    client_id, client_email = client_creds_cleaned
MailList.close()

# Send email
try:
    server.login(user_id, user_pass)
    # Format Email
    to = client_email
    subject = "Test Email Subject"
    description = "OwO this is a short exerpt of the email"
    body = """
    UwU here is the email body %s! 
    """ % (client_id)

    msg = f"Subject: {subject}\n{description}\n{body}"

    # Sends email to client
    server.sendmail(user_id, to, msg)
    # Close mail server connection
    server.quit()
    print("Email sent successfully!")

except:
    print("ERROR: Invalid Bot Credentials.")
