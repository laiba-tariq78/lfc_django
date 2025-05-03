from django.db import models

# Create your models here.


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    #products default is product_set
    
    #collection = models.ForeignKey('Collection', on_delete=models.PROTECT)  #pass as string if classis defined below
class Collection(models.Model):
    title= models.CharField(max_length=255)
    is_featured = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')  #circlular dependency prdocut depends on collection and vice versa


class Product(models.Model):
    sku =models.CharField(max_length=255, primary_key=True) #if not using default primary key 
    title= models.CharField(max_length=255)
    description = models.TextField()
    price =models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField()
    last_update =models.DateTimeField(auto_now=True)
    collection =models.ForeignKey(Collection, on_delete=models.PROTECT)  #pass as string if classis defined below
    promotions = models.ManyToManyField(Promotion, related_name='products')  #many to many relationship with Promotion model default product_set
                                      
class Customer(models.Model):
    MEMBERSHIP_BASIC='B'
    MEMBERSHIP_GOLD='G'
    MEMBERSHIP_SILVER='S'

    MEMBERSHIP_CHOICES=[
        (MEMBERSHIP_BASIC,'Basic'),
        (MEMBERSHIP_GOLD,'Gold'),
        (MEMBERSHIP_SILVER,'Silver')
    ]
    fisrt_name =models.CharField(max_length=255)
    last_name =models.CharField(max_length=255)
    email =models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date=models.DateField(null=True)
    membership =models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_SILVER)

class Order(models.Model):
    PENDING='P'
    COMPLETED='C'
    FAILED='F'
    PAYMENT_STATUS_CHOICES=[
        (PENDING,'Pending'),
        (COMPLETED,'Complete'),
        (FAILED,'Failed')
    ]
    placed_at =models.DateTimeField(auto_now_add=True)  
    payment_status =models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class Address(models.Model):   
    street = models.CharField(max_length=255)   
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    #customer = models.OneToOneField(Customer, on_delete=models.CASCADE,primary_key=True)  #one to one relationship
    #customer = models.ManyToManyField(Customer)  #many to many relationship
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  #one to many  


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2) 



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)     