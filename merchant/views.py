from django.shortcuts import render
from django.http import HttpResponse
from faker import Faker
# Create your views here.
import requests
import random
import pandas as pd
import json
from merchant.serializes import ProductSerializer
from .models import *
fake = Faker(['en-IN'])

# Function to generate a fake product
def generate_fake_address():
    # product_name = fake.word()
    # image_url = fake.image_url()
    # description = fake.text()
    # price = round(random.uniform(10, 1000), 2)
    # category = fake.word()
    # subcategory = fake.word()

    # return {
    #     "name": product_name,
    #     "images": image_url,
    #     "description": description,
    #     "price": price,
    #     "category": category,
    #     "subcategory": subcategory,
    # }
    return {
        "street": fake.street_name(),
        "city"  :  fake.city(),
        "state"  : fake.state(),
        "zip_code":fake.postcode(),
   
    }




def home_page(request):
    products=Products.objects.all()
    json_data=ProductSerializer(products,many=True).data
    # json_dataa=json.dumps(json_data)#[1]["images"][0]["image_url"]
    categories=ProductCategory.objects.filter(id=1)
    print(categories.first().image.all().values())
    subcategories=SubCategory.objects.all().values()
    data={"product_list":json_data,"categories":categories,"subcategories":subcategories}
    # for i in json_data:
    #     for j in i["images"]:
    #         for k in json.loads(j["image_url"]):
    #             print(k,"=============")
    return  render(request,"index.html",data)


def homdddddde_page(request):
    '''       title,url,pid,formatted_url,brand,stock,f_assured,price,currency,original_price,discount,images,seller,seller_rating,return_policy,description,highlights,specifications,formatted_specifications,avg_rating,reviews_count,category,sub_category,sub_category_2,breadcrumbs,payment_options,uniq_id,scraped_at'''
    flipkart_csv=pd.read_csv("flipkart-fashion-products-dataset-QueryResult.csv")
    # print(flipkart_csv.loc[0])
    # flipkart_csv.dropna(subset=['images'])
    # x=flipkart_csv.loc[1].to_dict()
    # print(x)
    # for index,row in flipkart_csv.iterrows():
    products = flipkart_csv.iterrows()
    for index,product in products:
        print(index,"---------------",product['title'])
        
        CATEGORY = 'category'
        SUBCATEGORY = 'subcategory'
        PRODUCT = 'product'
        
        if (product['images']) and type(product['images'])==str:
            
            # try:            
            # print(product['images'])
            images_separator_by_pipe= product['images'][0]
            images_separator_by_pipe1= product['images'][1]
            # print(images_separator_by_pipe)
            try:
                obj= ProductImages.objects.get(image=product['category'])
            except ProductImages.DoesNotExist:
                obj=ProductImages()
                obj.image_type=CATEGORY
                obj.image=product['category']
                obj.image_url=images_separator_by_pipe
                obj.save()
                
            try:
                obj1= ProductImages.objects.get(image=product['sub_category'])
            except ProductImages.DoesNotExist:
                obj1=ProductImages()
                obj1.image_type=SUBCATEGORY
                obj1.image=product['sub_category']
                obj1.image_url=images_separator_by_pipe1
                obj1.save()
                
            try:
                obj2= ProductImages.objects.get(image=product['title'])
            except ProductImages.DoesNotExist:
                obj2=ProductImages()
                obj2.image_type=PRODUCT
                obj2.image=product['title']
                obj2.image_url=product['images']
                obj2.save()    
            
            
            
            
            try:
                catergory=ProductCategory.objects.get(category=product["category"])
            except ProductCategory.DoesNotExist:
                catergory=ProductCategory()
                catergory.category=product["category"]
                catergory.save()
                catergory.image.add(obj)
        
        
        
            try:
                sub_category=SubCategory.objects.get(name=product["sub_category"])
            except SubCategory.DoesNotExist:
                sub_category=SubCategory()
                sub_category.name=product["sub_category"]
                sub_category.save()
                sub_category.image.add(obj1)
            
            try:
                user_merchant=User.objects.get(name=product["seller"])
            except User.DoesNotExist:
                user_merchant=User()
                user_merchant.name=product["seller"]
                user_merchant.email=fake.email()
                user_merchant.mobile=fake.phone_number()
                user_merchant.username=fake.phone_number()
                user_merchant.save()
                
                
            try:
                address_obj=Address.objects.get(user=user_merchant)
            except Address.DoesNotExist:
                address=generate_fake_address()
                address_obj=Address()
                address_obj.city=address["city"]
                address_obj.state=address["state"]
                address_obj.street=address["street"]
                address_obj.zip_code=address["zip_code"]
                address_obj.user=user_merchant
                address_obj.save()
            
            try:
                merchant=Merchant.objects.get(user=user_merchant)
            except Merchant.DoesNotExist:
                merchant=Merchant()
                merchant.user=user_merchant
                merchant.save()
                merchant.addresses.add(address_obj)
                


        
            try:
                product_obj=Products.objects.get(name=product["title"])
            except Products.DoesNotExist:
                product_obj=Products()
                product_obj.name=product["title"]
                product_obj.seller=merchant
                product_obj.brand=product["brand"]
                product_obj.avg_rating=product["average_rating"]
                product_obj.price=product["actual_price"]
                product_obj.discounted_percent=random.randint(10,50) #int(product["discount"][:2])
                product_obj.original_price=product["selling_price"]
                product_obj.highlights=product["product_details"]
                product_obj.category=catergory
                product_obj.sub_category=sub_category
                product_obj.save()
                product_obj.images.add(obj2)
                
     
    
        # print("row", row['title'])
        
    return  render(request,"index.html",{"products":["x"]})