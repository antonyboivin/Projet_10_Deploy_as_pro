from django.db import models


class ProductsA(models.Model):
    code = models.BigIntegerField(primary_key=True)
    url = models.CharField(max_length=250)
    product_name = models.CharField(max_length=250)
    nutrition_grade_fr = models.CharField(max_length=1)
    main_category = models.CharField(max_length=250)
    main_category_fr = models.CharField(max_length=250)
    image_small_url = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'products_A'