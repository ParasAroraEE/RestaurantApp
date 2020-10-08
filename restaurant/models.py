# django imports
from django.db import models
from django.core import validators
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager  # django auth user model
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# python imports
import os
import datetime

# thrid party app imports
from phonenumber_field.modelfields import PhoneNumberField

STATUS_FIELD_CHOICES = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
    ('Expired', 'Expired'),
)

SEATING_STATUS_FIELD_CHOICES = (
    ('Booked', 'Booked'),
    ('Vacent', 'Vacent'),
)

DISCOUNT_TYPE_CHOICES = (
    ('Flat', 'Flat'),
    ('Percentage', 'Percentage'),
)

PAYMENT_FIELD_CHOICES = (
    ('Completed', 'Completed'),
    ('Pending', 'Pending'),
)

ORDER_FIELD_CHOICES = (
    ('Waiting', 'Waiting'),
    ('Acknowledged', 'Acknowledged'),
    ('Placed', 'Placed'),
    ('Cancelled', 'Cancelled'),
    ('Completed', 'Completed'),
    ('Pending', 'Pending'),
)


def image_upload_path(instance, filename):
    return os.path.join("images", filename)


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_supperuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="User Email", max_length=60, unique=True)
    username = models.CharField(verbose_name="User Name", max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="Date Joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last Login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_supperuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]
    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class MenuCategories(models.Model):
    name = models.CharField(verbose_name="Categorie Name", null=False, max_length=50,
                            help_text='Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.',
                            validators=[validators.RegexValidator(r'^[\w .@+-_]+$', 'Enter a valid name. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')])
    image = models.ImageField(upload_to=image_upload_path, verbose_name="Categories Image", null=True, blank=True)
    status = models.CharField(verbose_name="Satus", choices=STATUS_FIELD_CHOICES, default='Active', null=False, max_length=15)
    featured = models.BooleanField(verbose_name="Featured", null=False, default=False)
    created_at = models.DateTimeField(verbose_name="Date (created)", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Date (updated)", auto_now=True)

# Beverage, Starter, Breads, Salats, Sweets, Main Cource

    class Meta:
        db_table = "menu_categorie"
        verbose_name = "Menu Categorie"
        verbose_name_plural = "Menu Categories"

    def __str__(self):
        return self.name


class MenuSubCategories(models.Model):
    cateory = models.ForeignKey(MenuCategories, verbose_name="Categorie", related_name="subcategory", null=False, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Categorie Name", null=False, max_length=50,
                            help_text='Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.',
                            validators=[validators.RegexValidator(r'^[\w .@+-_]+$', 'Enter a valid name. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')])
    image = models.ImageField(upload_to=image_upload_path, verbose_name="Categories Image", null=True, blank=True)
    status = models.CharField(verbose_name="Satus", choices=STATUS_FIELD_CHOICES, default='Active', null=False, max_length=15)
    featured = models.BooleanField(verbose_name="Featured", null=False, default=False)
    created_at = models.DateTimeField(verbose_name="Date (created)", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Date (updated)", auto_now=True)

# veg, non veg

    class Meta:
        db_table = "sub_categorie"
        verbose_name = "Sub Categorie"
        verbose_name_plural = "Sub Categories"

    def __str__(self):
        return self.name


class Items(models.Model):
    name = models.CharField(verbose_name="Item Name", null=False, max_length=50,
                            help_text='Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.',
                            validators=[validators.RegexValidator(r'^[\w .@+-_]+$', 'Enter a valid name. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')])
    price = models.DecimalField(verbose_name="Item Price", decimal_places=2, max_digits=10)
    image = models.ImageField(upload_to=image_upload_path, verbose_name="Item Image", null=True, blank=True)
    sub_cateory = models.ForeignKey(MenuSubCategories, verbose_name="Sub Categorie", related_name="items", null=False, on_delete=models.CASCADE)
    status = models.CharField(verbose_name="Satus", choices=STATUS_FIELD_CHOICES, default='Active', null=False, max_length=15)
    featured = models.BooleanField(verbose_name="Featured", null=False, default=False)
    special = models.BooleanField(verbose_name="Special", null=False, default=False)
    created_at = models.DateTimeField(verbose_name="Date (created)", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Date (updated)", auto_now=True)

    class Meta:
        db_table = "item"
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return self.name


class Coupon(models.Model):
    code = models.CharField(verbose_name="Coupon Code", max_length=255, unique=True, null=False)
    description = models.TextField(default=None)
    discount_type = models.CharField(verbose_name="Discount Type", choices=DISCOUNT_TYPE_CHOICES, default='Flat', null=False, max_length=15)
    discount_value = models.DecimalField(verbose_name="Discount Value", decimal_places=2, max_digits=10, default=0)
    valid_from = models.DateField(verbose_name="Valid From",)
    valid_till = models.DateField(verbose_name="Valid Till",)
    status = models.CharField(verbose_name="Satus", choices=STATUS_FIELD_CHOICES, default='Active', null=False, max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code


class Tables(models.Model):
    table = models.CharField(verbose_name="Table Number", null=False, max_length=50,
                             help_text='Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.',
                             validators=[validators.RegexValidator(r'^[\w .@+-_]+$', 'Enter a valid name. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')])
    seating = models.PositiveIntegerField(verbose_name="Seating Capicity", null=True)
    image = models.ImageField(upload_to=image_upload_path, verbose_name="Categories Image", null=True, blank=True)
    status = models.CharField(verbose_name="Satus", choices=SEATING_STATUS_FIELD_CHOICES, default='Vacent', null=False, max_length=15)
    featured = models.BooleanField(verbose_name="Featured", null=False, default=False)
    created_at = models.DateTimeField(verbose_name="Date (created)", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Date (updated)", auto_now=True)

    class Meta:
        db_table = "table"
        verbose_name = "Table"
        verbose_name_plural = "Tables"

    def __str__(self):
        return '%s - (Seating %s)' % (self.table, str(self.seating))


class Orders(models.Model):
    order_number = models.CharField(verbose_name="Order Number", null=False, max_length=50,
                                    help_text='Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                    validators=[validators.RegexValidator(r'^[\w .@+-_]+$', 'Enter a valid name. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')])
    table_number = models.ForeignKey(Tables, verbose_name="Table Number", related_name="orders", null=False, default='no table', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, verbose_name="User", related_name="orders", blank=True, on_delete=models.SET_NULL)
    date = models.DateField(verbose_name="Order Date", default=datetime.date.today)
    bill_amount = models.DecimalField(verbose_name="Total Bill Amount", decimal_places=2, max_digits=10, null=True, blank=True)

    payment_status = models.CharField(verbose_name="Payment Satus", choices=PAYMENT_FIELD_CHOICES, default='Pending', null=False, max_length=15)
    order_status = models.CharField(verbose_name="Order Satus", choices=ORDER_FIELD_CHOICES, default='Pending', null=False, max_length=15)

    coupon = models.ForeignKey(Coupon, verbose_name="Coupon Code", related_name="orders", blank=True, null=True, on_delete=models.CASCADE)
    discount = models.IntegerField(default=0)
    discount_bill_amount = models.DecimalField(verbose_name="Bill After Discount", decimal_places=2, max_digits=10, null=True, blank=True)

    created_at = models.DateTimeField(verbose_name="Date (created)", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Date (updated)", auto_now=True)

    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ('-created_at',)

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        self.bill_amount = get_grand_total(self.id)

        try:

            if self.coupon.discount_type == 'Flat':
                self.discount = self.coupon.discount_value
                self.discount_bill_amount = self.bill_amount - self.coupon.discount_value
            elif self.coupon.discount_type == 'Percentage':
                self.discount = self.bill_amount * (self.coupon.discount_value / 100)
                self.discount_bill_amount = self.bill_amount - self.bill_amount * (self.coupon.discount_value / 100)
        except:
            self.bill_amount = get_grand_total(self.id)
            self.discount = 0
            self.discount_bill_amount = self.bill_amount - self.discount

        super(Orders, self).save(*args, **kwargs)

    # @property
    # def get_cart_total(self):
    #     orderitems = self.orderitem_set.all()
    #     total = sum(item.get_total for item in orderitems)
    #     return total


class OrderDetails(models.Model):
    order_number = models.ForeignKey(Orders, verbose_name="Order Number", related_name="orderdetails", null=False, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, verbose_name="Item", related_name="orderdetails", null=False, on_delete=models.CASCADE)
    food_qty = models.PositiveIntegerField(verbose_name="Item Qty", null=True)
    item_price = models.DecimalField(verbose_name="Item Price", decimal_places=2, max_digits=10)

    @property
    def get_total(self):
        total = self.item.price * self.food_qty
        return total

    class Meta:
        db_table = "order_detail"
        verbose_name = "Order Detail"
        verbose_name_plural = "Order Details"

    def save(self, *args, **kwargs):
        self.item_price = self.item.price
        super(OrderDetails, self).save(*args, **kwargs)


class CustomerPayments(models.Model):
    order = models.ForeignKey(Orders, verbose_name="Order Number", related_name="paymentdetails", null=False, on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Customer", related_name="paymentdetails", null=False, on_delete=models.CASCADE)
    bill = models.IntegerField(verbose_name="Bill Amount", validators=[MinValueValidator(0)])
    payment_id = models.CharField(verbose_name="Payment Id", max_length=255)
    payment_amount = models.IntegerField(verbose_name="Payment Amount")
    payment_status = models.CharField(verbose_name="Payment Status", max_length=50)
    payment_method = models.CharField(verbose_name="Payment Method", max_length=255)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = "customer_payment"
        verbose_name = "Customer Payment"
        verbose_name_plural = "Customer Payments"


def get_grand_total(order_number):
    """ Employee/Customer can view the grand total of an order """

    grand_total = OrderDetails.objects.select_related('item').filter(order_number_id=order_number)
    price_per_food = []
    for i in grand_total:
        d = {
            "qty": i.food_qty,
            "price": i.item.price
        }
        price_per_food.append(d["qty"] * d["price"])
    bill_amount = sum(price_per_food)
    return bill_amount


def get_table_status(table_number):

    table_status = Orders.objects.select_related('table_number').filter(payment_status='Pending')
    booked_tables = []
    for i in table_status:
        d = {
            "numbr": i.id,

        }
        booked_tables.append(d["numbr"])

    return booked_tables
