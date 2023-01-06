# SquashBug.xyz


A ticket system to help you track, collaborate,  and destroy bugs.

The ticket system was built with Django utilizing a MVC design architecture. The system enables collaboration and task management by allowing many accounts to work together on each ticket. All tickets have a severity rating, date, author, as well as comments and attached files. The ticket dashboard enables sorting, pagination, and stats with ticket distribution graphs. New tickets are created with a form and can be edited. The project also includes an admin dashboard, and is mobile responsive.

Django Apps:

1.  MySite - Default
2.  Bugs - urls, views, models, for ticket system.
3.  Users - models and views for users.

# Live: https://squashbug.xyz/

#### Install:

```bash
git clone https://github.com/nealmick/SquashBug
cd SquashBug
pip install -r requirements.txt
python3 manage.py runserver
```

<img src="https://i.imgur.com/3ven2Y1.png" width="600" height="500" />

