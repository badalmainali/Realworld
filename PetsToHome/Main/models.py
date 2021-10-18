from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Admin(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=50)
    image=models.ImageField(upload_to="admins")
    mobile=models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    full_name=models.CharField(max_length=200)
    address=models.CharField(max_length=200, null=True)
    joined_on= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Category(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True)

    def __str__(self):
        return self.title

class Pets(models.Model):

    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="static/images")
    marked_price=models.PositiveIntegerField()
    selling_price=models.PositiveIntegerField()
    description=models.TextField()
    return_policy=models.CharField(max_length=300)

    view_count=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Cart(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    total=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: "+str(self.id)

class CartProduct(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE)
    pets=models.ForeignKey(Pets, on_delete=models.CASCADE)
    rate=models.PositiveIntegerField()
    quantity=models.PositiveIntegerField()
    subtotal=models.PositiveIntegerField()

    def __str__(self):
        return "Cart: " + str(self.cart.id)

ORDER_STATUS=(
    ("Order Received","Order Received"),
    ("Order Processing","Order Processing"),
    ("Moved for deliver","Moved for deliver"),
    ("Order Completed","Order Completed"),
    ("Order Cancelled","Order Cancelled"),

)
METHOD=(
    ("Cash On Delivery","Cash On Delivery"),
    ("QR Scanner","QR Scanner"),
    ("Esewa","Esewa"),
)
class Order(models.Model):
    cart=models.OneToOneField(Cart,on_delete=models.CASCADE)
    ordered_by=models.CharField(max_length=200)
    shipping_address=models.CharField(max_length=200)
    mobile=models.CharField(max_length=10)
    email=models.EmailField(null=True)
    subtotal=models.PositiveIntegerField()
    discount=models.PositiveIntegerField()
    total=models.PositiveIntegerField()
    order_status=models.CharField(max_length=50,choices=ORDER_STATUS)
    payment_method=models.CharField(max_length=20,choices=METHOD,default="Cash On Delivery")
    payment_completed=models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return "Order: " +str(self.id)