import requests
import re
import json

AMAZON_DOMAINS = {
    'US': 'www.amazon.com',
    'GB': 'www.amazon.co.uk',
    'CA': 'www.amazon.ca',
    'DE': 'www.amazon.de',
    'FR': 'www.amazon.fr',
    'IT': 'www.amazon.it',
    'ES': 'www.amazon.es',
    'AU': 'www.amazon.com.au',
    'JP': 'www.amazon.co.jp',
    'IN': 'www.amazon.in',
}

TRACKING_IDS = {
    'US': 'your-us-affiliate-id',
    'GB': 'your-uk-affiliate-id',
    'CA': 'your-canada-affiliate-id',
    'DE': 'your-germany-affiliate-id',
    'FR': 'your-france-affiliate-id',
    'IT': 'your-italy-affiliate-id',
    'ES': 'your-spain-affiliate-id',
    'AU': 'your-australia-affiliate-id',
    'JP': 'your-japan-affiliate-id',
    'IN': 'lightappssk-21',
}

def get_country_code():
    try:
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        return data['country']
    except:
        return 'US'  # default to US if there's an error getting the country code

def is_product_available(asin, domain):
    response = requests.get(f'https://{domain}/dp/{asin}')
    return response.status_code == 200

def convert_amazon_link(link):
    country_code = get_country_code()
    domain = AMAZON_DOMAINS.get(country_code)
    tracking_id = TRACKING_IDS.get(country_code)
    if domain and tracking_id:
        asin_match = re.search('/dp/(\w{10})', link)
        if asin_match:
            asin = asin_match.group(1)
            if is_product_available(asin, domain):
                return f'https://{domain}/dp/{asin}/?tag={tracking_id}'
        # If product is not available on this domain, redirect to search results page
        search_term_match = re.search('keywords=([^&]*)', link)
        if search_term_match:
            search_term = search_term_match.group(1)
        else:
            search_term = ''
        return f'https://{domain}/s?k={search_term}&tag={tracking_id}'
    return link



# Example usage

main_link = 'https://www.amazon.com/Beelink-4-4GHz%EF%BC%8CAMD-Graphics%EF%BC%8C16G-BT5-2%EF%BC%8CThree-60hz%EF%BC%8COffice/dp/B0BVFTM5MF?crid=2107MARPER3GD&keywords=ryzen+mini+pc&qid=1681128815&sprefix=ryzen+mini+%2Caps%2C365&sr=8-2-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFNMjBKMUFIN0xWRFAmZW5jcnlwdGVkSWQ9QTA0ODkzODIzSEVRVUZFWUZNSFpBJmVuY3J5cHRlZEFkSWQ9QTA3NTczMzUzNEEzVVVJQ1JYQUlFJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ%3D%3D&linkCode=ll1&tag=ranjan099-20&linkId=39760fe9ae2a379fac216585013aa38e&language=en_US&ref_=as_li_ss_tl'

link = main_link
converted_link = convert_amazon_link(link)
print(converted_link)
