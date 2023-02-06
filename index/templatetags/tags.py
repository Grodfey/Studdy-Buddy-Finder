from django import template
register = template.Library()


# Define a custom django template for concatentating strings together without shooting myself in the foot
# Possible alternatives to creating this custom template tag were either to use add or stringformat...
# Both of which weren't great options as _:
# - add will attempt to cast supplied arguments to int() types and then sum them up
# and...
# - stringformat is better suited for operations that involve 1 or 2 variables of which one argument is a str()/int()/etc. literal
#   on top of that stringformat also has a formatting system similar to printf in C or Python, yet omits using % in the beginning
#   and there are no examples demonstration how you you want to supply two variables arguments to stringformat as arguments
# 
# Which leaves us with no real good choice, but to write our own custom tenmplate tags
# Documentation
# - https://docs.djangoproject.com/en/4.1/ref/templates/builtins/
# - https://docs.djangoproject.com/en/4.1/howto/custom-template-tags/#a-quick-overview
# - https://docs.djangoproject.com/en/4.1/ref/templates/api/
# 
# - https://docs.djangoproject.com/en/4.1/topics/templates/#django.template.backends.django.DjangoTemplates
# 
# - https://django-book.readthedocs.io/en/latest/chapter09.html
#
# - https://www.geeksforgeeks.org/how-to-create-custom-template-tags-in-django/
# - https://stackoverflow.com/a/70981469
# 
# - https://stackoverflow.com/a/61980796 (concat is based on this code, but simplified a few items)
# - https://stackoverflow.com/questions/13223633/override-existing-django-template-tags
# 
# - https://stackoverflow.com/questions/1070398/how-to-set-a-value-of-a-variable-inside-a-template-code

register.simple_tag(
    lambda *args, sep=' ':
        sep.join(map(str, args)),
    name='concat')
