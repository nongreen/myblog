# myblog

A blog system based on `python 3.9.13` and `Django 4.0.5`

# Main features:
- Articles, Categories(add, delete, edit)
- Complete support of Comments: adding, deleting, editing, replying (under developing)
- Custom User model, simplified user registration
# Installation:
- Clone this repository
- Install dependencies via pip `pip install -rU requirements.txt`
- Setup database in `myblog/settings.py`
- Do makemigrations
- Do sqlmigrate for any app (accounts, blog, comments)
- Do migrate
- Run server
