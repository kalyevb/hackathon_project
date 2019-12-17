from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
	name = models.CharField(max_length=50, blank=False, null=False)
	subscriber = models.ManyToManyField(User, blank=True, related_name='sub_cat')



	def __str__(self):
		return self.name


	# def get_absolute_url(self):
	# 	return reverse('category_detail', kwargs={'pk':self.pk})

# class Subscriber(models.Model):
# 	subscriber = models.ForeignKey(User, blank=True, related_name='subscriber', on_delete=models.CASCADE)
# 	category = models.ForeignKey(Category, blank=True, related_name='category_subscriber', on_delete=models.CASCADE)



class Tag(models.Model):
	title = models.CharField(max_length=50)


	def __str__(self):
		return self.title


class Event(models.Model):
	title = models.CharField(max_length=250, blank=False, null=False)
	desecription = models.TextField()
	date =  models.DateField(null=True, blank=True)
	adress = models.CharField(max_length=250, blank=True, null=False)
	price = models.CharField(max_length=50)
	category = models.ForeignKey(Category, related_name="categoryes", on_delete=models.CASCADE)
	tags  = models.ManyToManyField(Tag, blank=True, related_name='events')
	foto = models.ImageField(upload_to='')
	favorites = models.ManyToManyField(User, blank=True, related_name='favorites')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('event_detail', kwargs={'pk':self.pk})



class Comment(models.Model):
	user = models.ForeignKey(User, related_name="users", on_delete=models.CASCADE)
	text = models.CharField(max_length=500, blank=False, null=False)
	created_on = models.DateTimeField(auto_now_add=True)
	event = models.ForeignKey(Event, related_name="events", on_delete=models.CASCADE)
	active = models.BooleanField(default=False)


	class Meta:
		ordering = ['created_on']

	def __str__(self):
		return self.text


from django.dispatch import receiver
from django.db.models.signals import post_save


# @receiver(post_save, sender=Event)
# def send_m(sender, instance, created, **kwargs):
#     if created:
#     	category = instance.category.id
#     	user = User
#     	email = user.email
#     	subscribers = User.objects.filter(sub_cat=category)
#     	# filter_email = subscribers.filter(email=subscribers)
#     	# subscribers = subscribers
#     	print('**************************************')
#     	print(subscribers)
#     	print('**************************************')
#     	print(category)
#     	print('**************************************')
#     	print(user)
#     	print('**************************************')