# Project Todo List (please move all finished items to the end.) 

## Project Related: (please start with small & easy tasks)

[+] Delete post

[+] Add title, last_modified_date to the Post model

[+] We should use a short markdown tutorial as the default value for the new post page.

[+] On the display_posts page, the needed css file is import by hard coding.  We need to change it to static file loading. (django_bootstrap_markdown could give some hints).

[+] Build user profile for each user. Not sure if we can directly change the django.contrib.auth.models.User model.  If we cannot, simple add another model which contains a foreign key to User.

[+] Add a topic/category to each post, give users different permission based on the topic/user group.

[+] Need a way to browse all posts page by page, sorted by last_modified_date.  Show only titles, user may click in to see the content of the post.

[+] After reading the Django document, I realized user login/register should be handled by the project, not any single app.  We should move the corresponding part to the project folder or a separate app.  I am not sure which way is better, but the project folder might be easier to work with.

## General Knowledge:

[+] Understand function `reverse()` and its role in `HttpResponseRedirect( reverse(...) )`.

[+] I noticed in some packages, the urls.py file contains multiple patterns, (a `forum_patterns` followed by a `topic_patterns` followed by a `url_patterns`).  How does this work?

