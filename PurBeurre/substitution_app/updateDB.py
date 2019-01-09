#!/usr/bin/env python3
from .models import ProductsA 
    
    
class Update_database():
    """

    """  
    def clean_db(self):
        """
            Queries the API with filters such as the natural score
            to find substitutes in the same product category of the user's request.
        """
        products = ProductsA.objects.all()
        if products:
            products.delete()
        else:
            print("empty base !")
    
    def request(self):

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
            return response.status_code


    def clean_substitution_products_in_openfoodfact_api(self, apiquery):
        """
            Analyze the response of the API to keep only the useful information.
        """
        results = []
        products = {}
        count = apiquery["count"]
        if count > 0:
            items = apiquery["products"]

            for item in items:
                try:
                    products["product_name"] = item["product_name_fr"]
                    products["code"] = item["code"]
                    products["nutrition_grade_fr"] = item["nutrition_grade_fr"]
                    products["categories_hierarchy"] = [categorie for categorie in \
                                    item["categories_hierarchy"] if categorie[0:2] == 'fr']
                    products["categories"] = item["categories"]
                    products["image_small_url"] = item["image_small_url"]

                    if len(products["categories"]) > 0:
                        results.append(products.copy())

                except KeyError:
                    pass
     
            if len(results) > 0:
                return results
            else:
                raise Http404

