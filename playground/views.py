from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, Collection, OrderItem, Order, Customer, Promotion 
from tags.models import Tag, TagItem 
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Value, Func, CharField, IntegerField, DecimalField, DateTimeField, BooleanField, JSONField, TextField, FloatField
from django.db.models import JSONBAgg, ArrayAgg, StringAgg, IntegerField, FloatField, DateTimeField, BooleanField, TextField, CharField, Value, Func, ExpressionWrapper, F, Q
from django.db.models import OuterRef, Subquery, Exists, Prefetch, Count, Sum, Avg, Min, Max, Case, When
from django.db.models.functions import Concat, Cast, Coalesce, Length, Lower, Upper, Round, ExtractYear, ExtractMonth, ExtractDay, ExtractWeekDay, ExtractHour, ExtractMinute, ExtractSecond, ExtractDate, ExtractTime
from django.db.models import Prefetch, Subquery, OuterRef, Exists, Count, Sum, Avg, Min, Max, Case, When, BooleanField, IntegerChoices, FloatChoices
from django.db import transaction, connection
# Create your views here.


def calculate():
    return 1


def say_hello(request):
    Collection.objects.create(title='Collection 1')
    Collection.objects.create(title='Collection 2')
    Product.objects.create(title='Product 1', price=100, description='Product 1 description', inventory=10, collection_id=1)
    Product.objects.create(title='Product 2', price=200, description='Product 2 description', inventory=20, collection_id=1) 
    Product.objects.create(title='Product 2', price=200, description='Product 2 description', inventory=10, collection_id=2)
    Product.objects.create(title='Product 3', price=300, description='Product 3 description', inventory=10, collection_id=1)
    Product.objects.create(title='Product 4', price=400, description='Product 4 description', inventory=10, collection_id=1)
    Product.objects.create(title='Product 5', price=500, description='Product 5 description', inventory=10, collection_id=1)
    Product.objects.create(title='Product 6', price=600, description='Product 6 description', inventory=10,collection_id=2)
    Product.objects.create(title='Product 7', price=700, description='Product 7 description', inventory=10, collection_id=1)
    Product.objects.create(title='Product 8', price=800, description='Product 8 description', inventory=10, collection_id=1)
    Product.objects.create(title='Product 9', price=900, description='Product 9 description', inventory=10, collection_id=2)
    query_set = Product.objects.all()
    try:
        query_set_id = Product.objects.get(id=1)
        query_set_price = Product.objects.filter(price__gt=100).first()
        query_set_price = Product.objects.filter(price__gt__range=(10, 30)).first()
        query_set_price = Product.objects.filter(price__lt=100).first()
        query_set_price = Product.objects.filter(price__lte=100).first()
        query_set_price_exists = Product.objects.filter(price__gte = 100).exists()
        query_set_title_contain = Product.objects.filter(title__icontains='coffe') #icontain case insensitive else contains exact match
        query_set_title_startswith = Product.objects.filter(title__startswith='coffe') #icontain case insensitive else contains exact match
        query_set_title_endswith = Product.objects.filter(title__endswith='coffe') #icontain case insensitive else contains exact match
        query_set_title_exact = Product.objects.filter(title__exact='coffe') #icontain case insensitive else contains exact match
        query_set_description_exact = Product.objects.filter(description__isnull='True') 
        query_set_description_exact = Product.objects.filter(last_update__year=2021)
        query_set_description_exact = Product.objects.filter(last_update__month=1) 
        query_set_description_exact = Product.objects.filter(last_update__day=1)
        query_set_description_exact = Product.objects.filter(last_update__week=1)
        query_set_description_exact = Product.objects.filter(last_update__week_day=1) #1-7
        query_set_description_exact = Product.objects.filter(last_update__hour=1)
        query_set_description_exact = Product.objects.filter(last_update__minute=1)
        query_set_description_exact = Product.objects.filter(last_update__second=1)
        query_set_description_exact = Product.objects.filter(last_update__date=1)
        query_set_description_exact = Product.objects.filter(last_update__time=1)
        query_set_price_multile_filter = Product.objects.filter(price__lte=100, inventory__lt=20).first()
        query_set_price_multile_filter = Product.objects.filter(price__lte=100).filter(inventory__lt=20).first()
        query_set_price_multile_filter2 = Product.objects.filter(Q(price__lte=100) | ~Q(inventory__lt=20)).first() #multiple and can pass to filter without q operator but for OR Q operatpr is used negate can be used with Q operator
        query_set_price_multile_filter3 = Product.objects.filter(inventory = F('price') ).first() #F operator is used to compare two fields in the same model
        query_set_price_multile_filter4 = Product.objects.filter(inventory = F('collection__id') ).first()
        query_set_price_multile_filter5 = Product.objects.order_by('price', '-title').reverse() #descending price ascending title
        query_set_price_multile_filter6 = Product.objects.order_by('price', '-title').distinct() #distinct is used to get unique values
        #3ways for fetching first value
        product1 = Product.objects.order_by('price', '-title').distinct('price')[0] #distinct is used to get unique values based on price
        product2 = Product.objects.latest('price')
        product3 = Product.objects.earliest('price')
        #limit
        query_set = Product.objects.all()[:5] #limit 5 records
        query_set = Product.objects.all()[5:10] #limit 5 records from 5 to 10 limit 5 offset 5
        query_set = Product.objects.all()[5:] #limit 5 records from 5 to end limit 5 offset 5
        #seelecting fields to query
        query_set = Product.objects.values('title', 'price', 'colection__title') #selecting fields to query using __ access relative fields will return dictionary
        query_set = Product.objects.values_list('title', 'price') #selecting fields to query will return tuple
        query_set = Product.objects.values_list('title', 'price', flat=True) #selecting fields to query will return list of values
        #select product that has been sorted and ordered(order class) by price and title
        query_set = Product.objects.order_by('price', 'title').values('title', 'price', 'collection__title') #selecting fields to query using __ access relative fields will return dictionary
        #select product that has been placed as ordered(order class) and sort them by  title
        #get value from orderItem product_id
        query_set = Product.objects.filter(id__in = OrderItem.objects.values('product_id').distinct()).order_by('title') #selecting fields to query using __ access relative fields will return dictionary
        query_set = OrderItem.objects.values('product_id').distinct()
        
        
        #deffring fields select specfic fields to query alot of extra necessary quruies 
        query_set = OrderItem.objects.only('product_id')
        query_set = OrderItem.objects.defer('product_id') #defer is used to exclude fields from the query
        query_set = OrderItem.objects.defer('product_id', 'order_id') #defer is used to exclude fields from the query

        #select related fields using prefetch related and select related
        #select_related(1)
        #prefetch_related(n)
        query_set = Product.objects.prefetch_related('promotion').order_by('title') #prefetch related is used to select related fields using prefetch related and select related
        query_set = Product.objects.select_related('collection').order_by('title')  #inner join
        #prefetch related is used to select related fields using prefetch related and select related
        #in template if you'll do product->collection with all() method too costly and time take so select only related collection
        query_set = Product.objects.prefetch_related('promotion').select_related('collection').all() # 2 quries 1 for collection and 1 for promotion

        #get last 5 orders with customer details, product and items
        query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5] #select related is used to select related fields using prefetch related and select related
        
        #aggregate functions
        #return dictionary oth methods with or without dictionary key otherwise price__count price__sum etc
        query_set = Product.objects.aggregate(sum=Sum('price'), avg= Avg('price'), min=Min('price'), max=Max('price'), count=Count('id')) #aggregate functions with dictornary key
        query_set = Product.objects.aggregate(Sum('price'), Avg('price'), Min('price'), Max('price'), Count('id')) #aggregate functions without dictornary key

        #annotate is used to add new field to the query set
        #query_set = Product.objects.annotate(is_new = True) #wrong syntax
        query_set = Product.objects.annotate(is_new = Value(True)) #right syntax
        query_set = Product.objects.annotate(is_new =F('id')+1) #right syntax
        query_set = Product.objects.annotate(is_new = Case(When(price__gt=100, then=True), default=False, output_field=BooleanField())) #annotate is used to add new field to the query set with case when statement
        query_set = Product.objects.annotate(is_new = Case(When(price__gt=100, then=True), default=False, output_field=BooleanField())).order_by('is_new') #annotate is used to add new field to the query set with case when statement and order by is_new
        #can't pass boolen value to annotate

        #database functions
        query_set = Product.objects.annotate(price_rounded = Round('price', 2)) 
        #concat first_name and last name to full_name using func and F
        query_set = Customer.objects.annotate(full_name = Concat('first_name', Value(' '), 'last_name', output_field=CharField())) #concat first_name and last name to full_name
        query_set = Customer.objects.annotate(full_name = Concat('first_name', Value(' '), 'last_name', output_field=CharField())).order_by('full_name') #concat first_name and last name to full_name and order by full_name
        #using func and F convert first_name and last name to full_name 
        query_set = Customer.objects.annotate(full_name = Func('first_name', Value(' '), 'last_name', output_field=CharField(), function='CONCAT')).order_by('full_name')

        #group functions
        #query_set = Customer.objects.annotate(Count('order_set')) #altough order set is related field still givign error
        query_set = Customer.objects.annotate(order_count = Count('order')).order_by('order_count') #group by order count

        #example of expression wrapper
        query_set = Product.objects.annotate(price_with_tax = ExpressionWrapper(F('price') * 1.2, output_field=DecimalField())) #expression wrapper is used to add new field to the query set with expression wrapper
        query_set = Product.objects.annotate(price_with_tax = ExpressionWrapper(F('price') * 1.2, output_field=DecimalField())).order_by('price_with_tax') #expression wrapper is used to add new field to the query set with expression wrapper and order by price_with_tax

        #wrong example if  expression wrapper not used
        #query_set = Product.objects.annotate(price_with_tax = F('price') * 1.2) #wrong example if  expression wrapper not used

        
    except ObjectDoesNotExist:
        pass   
    # for single object based on where clause give doesnpt exist error if condition doesnt match
    # query_set = Product.objects.filter(price__gt=100) #for multiple objects based on where clause
    count = Product.objects.count()
    # query_set.filter.order_by('price')
    # for product in query_set:
    #     print(product.title, product.price, product.description)
    list(query_set)
    list(query_set) # for 2nd time to get data from cache only 1 query
    
    
    
    #if first 0 then list then 2 quries if dont stricture code properly caching disturbs

    query_set[0] 
    list(query_set)

    return render(request, 'hello.html' , {'name': 'Laiba', 'products':query_set})



def content_Types(request):
    content_type = ContentType.objects.get_for_model(Product) #get content type for product model
    content_type = ContentType.objects.get_for_model(OrderItem) #get content type for order item model
    TagItem.objects.create(tag_id=1, content_type=content_type, object_id=1) #create tagged item for product model
    TagItem.objects.create(tag_id=2, content_type=content_type, object_id=2) #create tagged item for order item model

    query_set = TagItem.objects.filter(content_type=content_type) #filter tagged item for product model
    query_set =  TagItem.objects.filter(content_type=content_type, object_id=1).select_related('tag') #filter tagged item for product model with object id 1
   

    #custom manager
    query_set =  TagItem.objects.get_tags_for(Product, 1) #get tags for product model with object id 1



def object_crud(request):  
    #with this method variable names updated automatically here if we update in collection model
    #BUT NOT HERE XXXXXXXXXcollection = Collection(title='Collection 1') #create collection object but not 
    collection = Collection()
    collection.title = 'Collection 1'
    collection.featured_product = Product(id=1) #set featured product to product with id 1
    #collection.featured_product_id = 1 #set featured product to product with id 1
    collection.save() #save collection object to database


    #update collection object
    collection = Collection.objects.get(id=1) #get collection object with id 1
    collection.title = 'Collection 2' #update collection object title   
    collection.featured_product = Product(id=2) #update featured product to product with id 2
    collection.save() #save collection object to database


    # FILTER IS NESSARY OTHERWISE IT WILL UPDATE ALL COLLECTIONS
    collection.objects.update(title='Collection 3') #update collection object title using update method
    collection.objects.filter(id=1).update(title='Collection 4') #update collection object title using update method with filter


    #delete collection object
    collection = Collection.objects.get(id=1) #get collection object with id 1
    collection.delete() #delete collection object from database


    collection = Collection.objects.get(id__gt=1).delete() #delete collection object with id greater than 1


#@transaction.atomic() use decorator to create a transaction block
def transations(request):  
   #all changes hsould be saved together if failed roll back all
   #transaction.atomic() is used to create a transaction block
   #transaction.set_autocommit(False) is used to disable autocommit mode
   #transaction.commit() is used to commit the transaction
   #transaction.rollback() is used to rollback the transaction
    #transaction.savepoint() is used to create a savepoint in the transaction

    with transaction.atomic(): #create a transaction block
        try:
            #create order object with customer id 1 and payment status P
            order = Order.objects.create(customer_id=1, payment_status='P') #create order object with customer id 1 and payment status P
            OrderItem.objects.create(order_id=order, product_id=-1) 
            # product id -1 will throw error 
        except Exception as e:
            transaction.rollback()

def raw_quries(request):
    #for complex quries use raw quries
    #raw quries are not recommended to use in django

    query_set = Product.objects.raw('SELECT * FROM store_product') #execute raw sql quiry to get all products from store_product table

    connection = connection.cursor() #create a cursor object to execute raw sql quiry
    connection.execute('SELECT * FROM store_product') #execute raw sql quiry to get all products from store_product table


    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM store_product')
        cursor.callproc('sp_get_products', [1, 2, 'a']) #call stored procedure to get products with id 1 and 2
        cursor.execute('SELECT * FROM store_product WHERE id = %s', [1])
        rows = cursor.fetchall()

    return render(request, 'hello.html' , {'name': 'Laiba', 'products':query_set})