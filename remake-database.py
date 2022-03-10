import os
if os.path.exists("db.sqlite3"):
    os.remove("db.sqlite3")
message = os.popen("python manage.py makemigrations crescendo_app")
print(message.read())
message = os.popen("python manage.py migrate")
print(message.read())
message = os.popen("python population_script.py")
print(message.read())
print("Success")