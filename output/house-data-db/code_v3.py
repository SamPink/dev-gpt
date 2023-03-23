def get_lat_lng(postcode: str):
    import requests
    try:
        response = requests.get(f'http://api.postcodes.io/postcodes/{postcode}').json()
        if response['status'] == 200:
            lat, lng = response['result']['latitude'], response['result']['longitude']
            return lat, lng
    except:
        return (None, None)  # Fix here