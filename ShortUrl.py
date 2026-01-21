import requests


def shorten_url(long_url):
    api_url = "https://tinyurl.com/api-create.php"
    params = {'url': long_url}
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Error shortening URL")


# Example usage
long_url = "https://www.flipkart.com/motorola-g45-5g-brilliant-blue-128-gb/p/itmc45105311348e?pid=MOBH3YKQT2HEAPAM&lid=LSTMOBH3YKQT2HEAPAMDCRVSS&marketplace=FLIPKART&q=motorola+phones+under+15000&store=tyy%2F4io&srno=s_1_4&otracker=search&otracker1=search&fm=organic&iid=c4a608a4-ba51-47cb-8bd5-d88d029b6da1.MOBH3YKQT2HEAPAM.SEARCH&ppt=hp&ppn=homepage&ssid=loani49wkg0000001759067508078&qH=c6ea71c598495f6d"
short_url = shorten_url(long_url)
print("Short URL:", short_url)