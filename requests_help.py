from pathlib import Path
import requests
import json

default_cache_folder = "get_requests_cache"

def html_request_with_cache(url: str,
                            print_process: bool=False,
                            bypass_cache: bool=False,
                            cache_folder:
                            str=default_cache_folder,
                            **kwargs)->bytes:
                              
    '''This function performs get requests to fetch the html data of the given url.
    It also stores the fetch ftml data in a subdirectory ("get_requests_cache" by default).
    Subsequent get requests of the same website are taken from the cache instead of doing a new get request.
    
    url(string):
    - Takes string of target URL

    print_process(bool)(default=False):
    - This flag prints this functions processes to the console

    bypass_cache(bool)(default=False):
    - This flag allowes skipping the cache to make a new request every time

    cache_folder(string)(default="get_requests_cache"):
    - Allows user to change the name of the cache directory

    Return Value(bytes):
    - Returns html content in bytes (can be use in beautiful soup module)

    Requirements:
    - requests library (pip install requests)
    '''

    if bypass_cache:
        if print_process:
            print(f"Trying to fetch from '{url}' without using cache.")

        no_cache_request = requests.get(url=url, **kwargs)

        if no_cache_request.status_code != 200:
            raise Exception(f"Request failed. HTTP error code: {no_cache_request.status_code}")
        
        if print_process:
            print(f"Success. Returning html content of '{url}'")
        
        return no_cache_request.content
    
    module_path = Path(__file__).parent

    cache_path = module_path.joinpath(cache_folder)

    tracking_file = "cache_tracking.json" 

    tracking_file_path = cache_path.joinpath(tracking_file)

    if not cache_path.exists():
        cache_path.mkdir()

        if print_process:
            print(f"'{cache_folder}' did not exist, so it has been created in '{module_path.name}' directory.")

    if not tracking_file_path.exists():
        tracking_file_path.write_text("{}")

        if print_process:
            print(f"'{tracking_file}' did not exist, so it has been created in '{cache_path.name}' directory.")

    with open(tracking_file_path, "r") as file:
        cache_registry = json.load(file)

    if print_process:
        print("Cache registry loaded Successfully.")
    
    if not url in cache_registry.keys():
        if print_process:
            print(f"'{url}' not found in cache.")
            print("Trying to fetch website.")

        request = requests.get(url=url, **kwargs)

        if request.status_code != 200:
            raise Exception(f"Request failed. HTTP error code: {request.status_code}")
        
        cache_registry[url] = f"cache{len(cache_registry)+1}.html"

        cache_path.joinpath(cache_registry.get(url)).write_bytes(request.content)

        with open(tracking_file_path, "w") as file:
            json.dump(cache_registry, file)

        if print_process:
            print(f"New cache file from get request created and stored in '{cache_registry.get(url)}'.")
    
    else:
        if print_process:
            print(f"'{url}' found in cache as '{cache_registry.get(url)}'.")

    if print_process:
        print(f"Returning html content from '{cache_registry.get(url)}'")

    return open(cache_path.joinpath(cache_registry.get(url)),"rb")
 

def api_call_with_cache(url:str,
                        params:dict=None,
                        headers:dict=None,
                        print_process: bool=False,
                        bypass_cache: bool=False,
                        cache_folder: str=default_cache_folder,
                        **kwargs)->dict:
    
    '''Function makes a get request call to an api. is the same call has already been made with the same parameters. Cached data is loaded instead. This can reduce the use of limited API calls during testing.
    
    You can eventually bypass the cache set the 'bypass_cache' flag to True.

    url(string):
    - Takes string of target URL

    params(dict[str,any])(default=None):
    - contains the api call parameters in a dictionary

    headers(dict[str,any])(default=None):
    - contains the api call headers in a dictionary

    print_process(bool)(default=False):
    - This flag prints this functions processes to the console

    bypass_cache(bool)(default=False):
    - This flag allowes skipping the cache to make a new request every time

    cache_folder(string)(default="get_requests_cache"):
    - Allows user to change the name of the cache directory

    Return Value(dict):
    - Returns the API response as a python dictionary.

    Requirements:
    - requests library (pip install requests)

    '''

    if bypass_cache:
        if print_process:
            print(f"Trying to fetch api data from '{url}' without using cache.")

        no_cache_response = requests.get(url=url, params=params, headers=headers,**kwargs)

        if no_cache_response.status_code != 200:
            raise Exception(f"Request failed. HTTP error code: {no_cache_response.status_code}")
        
        if print_process:
            print(f"Success. Returning API data of '{url}'")
        
        return no_cache_response.json()
    
    module_path = Path(__file__).parent

    cache_path = module_path.joinpath(cache_folder)

    cache_file = "api_cache.json" 

    cache_file_path = cache_path.joinpath(cache_file)

    if not cache_path.exists():
        cache_path.mkdir()

        if print_process:
            print(f"'{cache_folder}' did not exist, so it has been created in '{module_path.name}' directory.")

    if not cache_file_path.exists():
        cache_file_path.write_text("{}")

        if print_process:
            print(f"'{cache_file}' did not exist, so it has been created in '{cache_path.name}' directory.")

    with open(cache_file_path, "r") as file:
        api_cache = json.load(file)

    if print_process:
        print("API cache loaded Successfully.")
        print("Generating key of API call.")

    api_cache_key = url

    if params:
        api_cache_key = api_cache_key + "&p:"

        for key, value in sorted(params.items(), key=lambda x: x[0]):
            api_cache_key = api_cache_key + key + str(value)


    if headers:
        api_cache_key = api_cache_key + "&h:"

        for key, value in sorted(headers.items(), key=lambda x: x[0]):
            api_cache_key = api_cache_key + key + str(value)
                                                      
    if print_process:
        print("Key of API call generated.")
        print("Comparing key with cache entries.")

    if api_cache_key in api_cache.keys():
        if print_process:
            print("API call found in cache.")
            print(f"Returning cache entry from {url}.")

        return api_cache.get(api_cache_key)
    
    if print_process:
            print("API call not found in cache.")
            print(f"Trying to fetch api data from '{url}'.")

    response = requests.get(url=url, params=params, headers=headers, **kwargs)

    if response.status_code != 200:
        raise Exception(f"Request failed. HTTP error code: {response.status_code}")
    
    if print_process:
            print("API call successful.")
            print("Caching API call data.")
    
    api_data = response.json()

    api_cache[api_cache_key] = api_data

    with open(cache_file_path, "w") as file:
        json.dump(api_cache, file)

    if print_process:
            print(f"API call successful. Returning data from '{url}'.")

    return api_data
