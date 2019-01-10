#!/usr/bin/env python3
from .models import ProductsA
import json
import requests
    
    
class Update_database():
    """
        This class manages the updated part of the application.
        It will allow the application database to stay up-to-date with a Cron job.
    """  
    def clean_db(self):
        """
            Before updating the database, it is fully cleaned.
        """
        products = ProductsA.objects.all()
        if products:
            products.delete()

    def request_openfoofact_API(self, page='1', page_size='1000'):

        url = 'https://fr.openfoodfacts.org/cgi/search.pl'
        # Determinations of the build parameters of the query.
        payload = {
            'action' : 'process',
            # First criteria
            'tagtype_0' : 'nutrition_grades',
            'tag_contains_0':'contains',
            'tag_0' : 'a',
            # Third criteria
            'tagtype_1' : 'origins',
            'tag_contains_1':'contains',
            'tag_1' : 'France',

            'additives' : 'without',
            'ingredients_from_palm_oil' : 'without',
            'ingredients_that_may_be_from_palm_oil' : 'without',
            'ingredients_from_or_that_may_be_from_palm_oil' : 'without',
            'ingredients_from_or_that_may_be_from_palm_oil' : 'without',

            'sort_by' : 'unique_scans_n',
            'json' : '1',
            'page_size' : page_size,
            'page' : page
        }

        # Built of the query
        try:
            response = requests.get(url, params=payload).json()
            requests.get(url, params=payload).raise_for_status()
            return(response)
        except requests.exceptions.HTTPError as err:
            return response.status_code

    def pages_number_determination(self, response):
        """
            This method will ask the API to determine how much product page
            involves searching for healthy products.
        """
        products_number = int(response["count"])
        page_size = int(response["page_size"])
        page_number = int((products_number // page_size)+1)

        return(page_number)

    def clean_updated_products(self, response):
        """
            Analyze the response of the API to keep only the useful information.
        """
        results = []
        products = {}
        count = response["count"]
        if count > 0:
            items = response["products"]

            for item in items:
                try:
                    products["product_name"] = item["product_name_fr"]
                    products["code"] = item["code"]
                    products["url"] = item["url"]
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

    def save_updated_products(self, clean_response):
        """
            This method saves the cleaned data in the database.
        """
        for products in clean_response:
            products_save = ProductsA.objects.create(
                code=products['code'],
                url=products['url'],
                product_name=products['product_name'],
                nutrition_grade_fr=products['nutrition_grade_fr'],
                main_category=products['categories_hierarchy'],
                main_category_fr=products['categories_hierarchy'],
                image_small_url=products['image_small_url']
            )


    def request_updated_products(self, response, page_number):
            # Requete l'API page par page en fonction du nombre de page.
            # Nettoie la réponse de requete.
            # Enregistre les produits dans la base de données.
        page = 1
        while page <= page_number:
            self.clean_db()
            response = self.request_openfoofact_API(page, page_size='1000')
            clean_response = self.clean_updated_products(response)
            self.save_updated_products(clean_response)
            print(response['page'])
            print(clean_response[1])
            page += 1
      


