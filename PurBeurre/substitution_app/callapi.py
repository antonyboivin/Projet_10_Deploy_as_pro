#!/usr/bin/env python3
import requests
import json


def request_the_openfoodfact_api(query):
    """
    This method will allow the construction of the url of the openfoodfact API
    and return the response of the query.
    """

    url = 'https://fr.openfoodfacts.org/cgi/search.pl'
    # Determinations of the build parameters of the query.
    payload = {
        'search_terms' : query,
        'search_simple' : 1,
        'action' : 'process',
        'json' : '1',
        'page_size' : 100,
        'page' : '1'
    }
    # Built of the query
    try:
        response = requests.get(url, params=payload)
        requests.get(url, params=payload).raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as err:
        return response.status_code


def clean_the_openfoodfact_api_request(response):
    """
    The API returns a response in json format with information that will not be needed.
    This method will therefore select the useful elements only,
    and return the answer of the request in the form of a list containing dictionaries.
    """

    results = []
    products = {}
    count = response["count"]
    if count > 0:
        items = response["products"]

        for item in items:
            try:
                products["product_name_fr"] = item["product_name_fr"]
                products["code"]  = item["code"]
                products["nutrition_grade_fr"] = item["nutrition_grade_fr"]
                products["categories_hierarchy"] = [categorie for categorie in item["categories_hierarchy"] if categorie[0:2] == 'fr']
                products["categories"] = item["categories"]
                products["image_small_url"] = item["image_small_url"]
               

                if len(products["categories"]) > 0 and len(products["categories_hierarchy"]) > 0: # 
                    results.append(products.copy())
                    
            except KeyError:
                pass
                
        return results
   
    else:
        """
        [{'product_name_fr': '', 'code': '', 'nutrition_grade_fr': '', 'categories_hierarchy': '',
         'categories': '', 'image_small_url': ''}
        """
        results = [{'product_name_fr': 'Désolé, le produit demandé est introuvable', 'code': '0', 'nutrition_grade_fr': '', 'categories_hierarchy': '',
         'categories': '', 'image_small_url': ''}]
        return results


def barcode_request_the_openfoodfact_api(barcode):
    """
    This method will allow the construction of the url of the openfoodfact API
    and return the response of the query.
    https://world.openfoodfacts.org/api/v0/product/737628064502.json
    """

    url = 'https://world.openfoodfacts.org/api/v0/product/' + str(barcode) + '.json'

    try:
        response = requests.get(url)
        requests.get(url).raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as err:
        return response.status_code


def barcode_clean_the_oppenfoodfact_api_request(response):

    results = []
    products = {}

    items = response["product"]


    try:
        products["product_name_fr"] = items["product_name_fr"]
        products["code"]  = items["code"]
        products["nutrition_grade_fr"] = items["nutrition_grade_fr"]
        products["categories_hierarchy"] = [categorie for categorie in items["categories_hierarchy"] if categorie[0:2] == 'fr']
        #products["categories_hierarchy"] = [categorie for categorie in items["categories_hierarchy"]]
        products["categories"] = items["categories"]
        products["image_small_url"] = items["image_small_url"]
        

        if len(products["categories"]) > 0 and len(products["categories_hierarchy"]) > 0: #  
            results.append(products.copy())
            results = results[0]

            
    except KeyError:
        pass

    return results


def request_for_substitution_products_in_openfoodfact_api(apiquery):
    """
            # Third criteria
        'tagtype_2' : 'categories',
        'tag_contains_2' : 'contains',
        'tag_2' : apiquery["categories_hierarchy"][0:-1],
    
         # Additives = without
        'additives' : 'without',
        # Oil palm = without
        'ingredients_from_palm_oil' : 'without',
        'ingredients_that_may_be_from_palm_oil' : 'without',
        'ingredients_from_or_that_may_be_from_palm_oil' : 'without',    
    
    """

    url = 'https://fr.openfoodfacts.org/cgi/search.pl'
    # Determinations of the build parameters of the query.
    payload = {
        'action' : 'process',
        'search_terms' : apiquery["categories_hierarchy"][0][3:],
        # First criteria
        'tagtype_0' : 'nutrition_grades',
        'tag_contains_0':'contains',
        'tag_0' : 'a',
        # Third criteria
        'tagtype_1' : 'nutrition_grades',
        'tag_contains_1':'contains',
        'tag_1' : 'b',



        'sort_by' : 'unique_scans_n',
        'json' : '1',
        'page_size' : 100,
        'page' : '1'
    }

    # Built of the query
    try:
        response = requests.get(url, params=payload)
        requests.get(url, params=payload).raise_for_status()
        #return response.json()
        return(response.json())

    except requests.exceptions.HTTPError as err:
        print("Message d'erreur 404, pas de chance !")


def clean_substitution_products_in_openfoodfact_api(apiquery):
    results = []
    products = {}
    count = apiquery["count"]
    if count > 0:
        items = apiquery["products"]

        for item in items:
            try:
                products["product_name_fr"] = item["product_name_fr"]
                products["code"]  = item["code"]
                products["nutrition_grade_fr"] = item["nutrition_grade_fr"]
                products["categories_hierarchy"] = [categorie for categorie in item["categories_hierarchy"] if categorie[0:2] == 'fr']
                products["categories"] = item["categories"]
                products["image_small_url"] = item["image_small_url"]
               

                if len(products["categories"]) > 0: #  and len(products["categories_hierarchy"]) > 0
                    results.append(products.copy())
                    
            except KeyError:
                pass
                
        return results
   
    else:
        """
        [{'product_name_fr': '', 'code': '', 'nutrition_grade_fr': '', 'categories_hierarchy': '',
         'categories': '', 'image_small_url': ''}
        """
        results = [{'product_name_fr': 'Désolé, le produit demandé est introuvable', 'code': '0', 'nutrition_grade_fr': '', 'categories_hierarchy': '',
         'categories': '', 'image_small_url': ''}]
        return results
