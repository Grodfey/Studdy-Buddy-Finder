# To ensure that templatetags is treated as a Python package
"""
Files:
- filters.py: define custom template filters like stringformat
- tags.py: define custom template tags url

Custom tag types:
- simple_tag:       override for simple data processing
- inclusion_tag:    override to render processed data using a custom template
- assignment_tag:   override to set variable data in context after processing data
"""

# {% with uid=user.username nom=user.first_name|add:' '|add:user.last_name|stringformat:"s %()" %}
# user-search.html, line 53

# {{nom}} @ {{uid}}
# user-search.html, line 55

# <button name="user_data" type="submit" class="btn btn-success" value="{{nom}} @ {{uid}}">
# user-search.html, line 56

# {% endwith %}
# user-search.html, line 60