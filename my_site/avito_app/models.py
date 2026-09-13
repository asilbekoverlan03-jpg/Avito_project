import phonenumber_field
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField



User_STATUS =(
   ('simple','simple'),
   ('bronze','bronze'),
   ('silver','silver'),
   ('gold','gold')
)
class Category(models.Model):
   category_name = models.CharField(max_length=30, unique=True)
   category_image = models.ImageField(upload_to='category_images')


   def __str__(self):
       return self.category_name

class UserProfile(AbstractUser):
   age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18), MaxValueValidator(70)],
                                          null=True,blank=True)
   phone_number = PhoneNumberField(default='+996')
   avatar = models.ImageField(upload_to='profile_images/', null=True, blank=True)
   status = models.CharField(max_length=10, choices=User_STATUS, default='simple')
   data_registered = models.DateField(auto_now_add=True)


class SubCategory(models.Model):
      category =models.ForeignKey(Category, on_delete=models.CASCADE,related_name='sub_category')
      sub_category_name = models.CharField(max_length=30, unique=True)
      sub_category_image = models.ImageField(upload_to='sub_category_images/', null=True, blank=True)

      def __str__(self):
         return f'{self.category.category_name}-{self.sub_category_name}'

class Product(models.Model):
   subcategory =models.ForeignKey(SubCategory,on_delete=models.CASCADE,related_name='sub_product')
   product_name = models.CharField(max_length=200)
   description = models.TextField(null=True,blank=True)
   price =models.DecimalField(max_digits=10, decimal_places=2)
   article = models.PositiveBigIntegerField(unique=True)
   product_type = models.BooleanField(default=False)
   created_date = models.DateField(auto_now_add=True)

   def __str__(self):
      return f'{self.subcategory.sub_category_name}-{self.product_name}'

   def get_avg_rating(self):
      ratings =self.product_review.all()
      if ratings.exists():
         return round(sum([i.rating for i in ratings]) / ratings.count(), 1)
      return 0


   def get_count_rating(self):
      return self.product_review.count()



class ProductImage(models.Model):
   product =models.ForeignKey(Product,on_delete=models.CASCADE, related_name='product_img')
   product_image = models.ImageField(upload_to='product_images/', null=True, blank=True)




class Review(models.Model):
   user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
   product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='product_review')
   review_image = models.ImageField(upload_to='review_images/',null=True,blank=True)
   comment = models.TextField(null=True, blank=True)
   rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
   created_time = models.DateTimeField(auto_now_add=True)


   def __str__(self):
       return f'{self.user.first_name}-comment'


class Cart(models.Model):
   user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

   def get_total_price(self):
      return sum([i.get_total_price() for i in self.item.all()])

class CartItem(models.Model):
   cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='item')
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   quantity = models.PositiveSmallIntegerField(default=1)

   def get_total_price(self):
      return self.quantity * self.product.price

class Favorite(models.Model):
   user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

class FavoriteItem(models.Model):
   favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE, related_name='favorite_item')
   product = models.ForeignKey(Product, on_delete=models.CASCADE)



