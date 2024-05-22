import pathlib
from io import BytesIO
# import sys
# sys.path.insert(0, str(pathlib.Path(__file__).parent.resolve())+"/bottle")
from bottle import request, response, template
import re
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

ITEMS_PER_PAGE = 2
COOKIE_SECRET = "41ebeca46f3b-4d77-a8e2-554659075C6319a2fbfb-9a2D-4fb6-Afcad32abb26a5e0"


##############################
def dict_factory(cursor, row):
    col_names = [col[0] for col in cursor.description]
    return {key: value for key, value in zip(col_names, row)}

##############################

def db():
    db = sqlite3.connect(str(pathlib.Path(__file__).parent.resolve())+"/company.db")  
    db.row_factory = dict_factory
    return db


##############################
def no_cache():
    response.add_header("Cache-Control", "no-cache, no-store, must-revalidate")
    response.add_header("Pragma", "no-cache")
    response.add_header("Expires", 0)    



##############################

def group_images(rows):
    # Group images by item_pk
    items = {}


    print("************* rows in x.group_images ****************")
    print(rows)
    for row in rows:
        item_pk = row['item_pk']
        if item_pk not in items:
            items[item_pk] = {
                'item_pk': row['item_pk'],
                'item_name': row['item_name'],
                'item_price_per_night': row['item_price_per_night'],
                'item_lat': row['item_lat'],
                'item_lon': row['item_lon'],
                'item_stars': row['item_stars'],
                'item_created_at': row['item_created_at'],
                'item_updated_at': row['item_updated_at'],
                'item_images': []
                            }
        if row['image_url']:
            items[item_pk]['item_images'].append(row['image_url'])

    items = list(items.values())
    return items


##############################
def validate_user_logged():
    user = request.get_cookie("user", secret=COOKIE_SECRET)
    if user is None: raise Exception("user must login", 400)
    return user


##############################

def validate_logged():
    # Prevent logged pages from caching
    response.add_header("Cache-Control", "no-cache, no-store, must-revalidate")
    response.add_header("Pragma", "no-cache")
    response.add_header("Expires", "0")  
    user_id = request.get_cookie("id", secret = COOKIE_SECRET_KEY)
    if not user_id: raise Exception("***** user not logged *****", 400)
    return user_id



##############################

def validate_user_has_rights_by_item_pk(user, item_pk):
    database = db()
    q = database.execute("SELECT * FROM items WHERE item_pk = ?", (item_pk,))
    item = q.fetchone()

    if user['user_role'] != 'admin':    
        if user['user_pk'] == item['item_owner_fk']:
            return True
        else:
            raise Exception("You do not have the rights to do that", 400)
    else:
        return True





##############################
def send_verification_email(from_email, to_email, verification_id):
    try:

        

        message = MIMEMultipart()
        message["To"] = from_email
        message["From"] = to_email
        message["Subject"] = 'Testing my email to verify'

        try:
            import production
            base_url = "https://samueltobias4343.eu.pythonanywhere.com"
        except:
            base_url =   "http://localhost"


    
        email_body= f""" 

                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8" />
                            <meta
                            name="viewport"
                            content="width=device-width, initial-scale=1.0"
                            />
                            <title>Verification Email</title>
                        </head>
                        <body>
                            <h1>You need to verify your account</h1>
                            <a href="{base_url}/activate-user/{verification_id}">Activate user </a>
                        </body>
                        </html>

             """
 
        messageText = MIMEText(email_body, 'html')
        message.attach(messageText)
 
        email = from_email
        password = 'sxakvggwacukkdmk'
 
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo('Gmail')
        server.starttls()
        server.login(email,password)
        from_email = from_email
        to_email  = to_email
        server.sendmail(from_email,to_email,message.as_string())
 
        server.quit()
    except Exception as ex:
        print(ex)
        return "error"
    


##############################
def send_reset_password_email(from_email, to_email, verification_id):
    try:

        

        message = MIMEMultipart()
        message["To"] = from_email
        message["From"] = to_email
        message["Subject"] = 'Reset password'

        try:
            import production
            base_url = "https://samueltobias4343.eu.pythonanywhere.com"
        except:
            base_url =   "http://localhost"


    
        email_body= f""" 

                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8" />
                            <meta
                            name="viewport"
                            content="width=device-width, initial-scale=1.0"
                            />
                            <title>Reset Password</title>
                        </head>
                        <body>
                            <h1>Click the link below to reset your password</h1>
                            <a href="{base_url}/change-password/{verification_id}">change password </a>
                        </body>
                        </html>

             """
 
        messageText = MIMEText(email_body, 'html')
        message.attach(messageText)
 
        email = from_email
        password = 'sxakvggwacukkdmk'
 
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo('Gmail')
        server.starttls()
        server.login(email,password)
        from_email = from_email
        to_email  = to_email
        server.sendmail(from_email,to_email,message.as_string())
 
        server.quit()
    except Exception as ex:
        print(ex)
        return "error"
    


##############################
def send_user_deleted_email(from_email, to_email):
    try:
        message = MIMEMultipart()
        message["To"] = from_email
        message["From"] = to_email
        message["Subject"] = 'Your account is deleted'

        try:
            import production
            base_url = "https://samueltobias4343.eu.pythonanywhere.com"
        except:
            base_url =   "http://localhost"


    
        email_body= f""" 

                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8" />
                            <meta
                            name="viewport"
                            content="width=device-width, initial-scale=1.0"
                            />
                            <title>Reset Password</title>
                        </head>
                        <body>
                            <h1>Your Account has been deleted</h1>
                           
                        </body>
                        </html>

             """
 
        messageText = MIMEText(email_body, 'html')
        message.attach(messageText)
 
        email = from_email
        password = 'sxakvggwacukkdmk'
 
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo('Gmail')
        server.starttls()
        server.login(email,password)
        from_email = from_email
        to_email  = to_email
        server.sendmail(from_email,to_email,message.as_string())
 
        server.quit()
    except Exception as ex:
        print(ex)
        return "error"

##############################

USER_ID_LEN = 32
USER_ID_REGEX = "^[a-f0-9]{32}$"

def validate_user_id():
	error = f"user_id invalid"
	user_id = request.forms.get("user_id", "").strip()      
	if not re.match(USER_ID_REGEX, user_id): raise Exception(error, 400)
	return user_id


##############################

EMAIL_MAX = 100
EMAIL_REGEX = "^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"

def validate_user_email():
    error = f"email invalid"
    user_email = request.forms.get("user_email", "").strip()
    if not re.match(EMAIL_REGEX, user_email): raise Exception(error, 400)
    return user_email

##############################

USER_USERNAME_MIN = 2
USER_USERNAME_MAX = 20
USER_USERNAME_REGEX = "^[a-zA-Z\s]{2,20}$"

def validate_user_username():
    error = f"username {USER_USERNAME_MIN} to {USER_USERNAME_MAX} lowercase english letters"
    user_username = request.forms.get("user_username", "").strip()
    if not re.match(USER_USERNAME_REGEX, user_username): raise Exception(error, 400)
    return user_username

##############################

USER_NAME_MIN = 2
USER_NAME_MAX = 20

def validate_user_first_name():
    error = f"name {USER_NAME_MIN} to {USER_NAME_MAX} characters"
    user_first_name = request.forms.get("user_first_name", "").strip()
    if not re.match(USER_USERNAME_REGEX, user_first_name): raise Exception(error, 400)
    return user_first_name

##############################

LAST_NAME_MIN = 2
LAST_NAME_MAX = 20

def validate_user_last_name():
  error = f"last_name {LAST_NAME_MIN} to {LAST_NAME_MAX} characters"
  user_last_name = request.forms.get("user_last_name").strip()
  if not re.match(USER_USERNAME_REGEX, user_last_name): raise Exception(error, 400)
  return user_last_name

##############################

USER_PASSWORD_MIN = 6
USER_PASSWORD_MAX = 50
USER_PASSWORD_REGEX = "^.{6,50}$"

def validate_user_password():
    error = f"password {USER_PASSWORD_MIN} to {USER_PASSWORD_MAX} characters"
    user_password = request.forms.get("user_password", "").strip()

    print(f"############# {user_password}   ################# ")
    if not re.match(USER_PASSWORD_REGEX, user_password): raise Exception(error, 400)

    return user_password

##############################
CUSTOMER_ROLE = "customer"
PARTNER_ROLE = "partner"

def validate_user_role():
    user_role = request.forms.get("user_role", "").strip()
    error = f"The role ###{user_role}### is neither {CUSTOMER_ROLE} or {PARTNER_ROLE}"
    if user_role != CUSTOMER_ROLE and user_role != PARTNER_ROLE:
        raise Exception(error, 400)
    return user_role

##############################

def validate_user_confirm_password():
  error = f"password and confirm_password do not match"
  user_password = request.forms.get("user_password", "").strip()
  user_confirm_password = request.forms.get("user_confirm_password", "").strip()
  if user_password != user_confirm_password: raise Exception(error, 400)
  return user_confirm_password

##############################


##############################

ITEM_NAME_MIN = 2
ITEM_NAME_MAX = 20
ITEM_NAME_REGEX = "^[a-zA-Z\s]{2,20}$"

def validate_item_name():


    error = f"name {ITEM_NAME_MIN} to {ITEM_NAME_MAX} lowercase english letters"
    item_name = request.forms.get("item_name", "").strip()
  
    if not re.match(ITEM_NAME_REGEX, item_name): raise Exception(error, 400)
    return item_name




##############################

ITEM_PRICE_MIN = 0
ITEM_PRICE_MAX = 20000
ITEM_PRICE_REGEX =  "^\d{1,8}(\.\d{1,2})?$" 

def validate_item_price():


    error = f"price needs to be bwtween {ITEM_NAME_MIN} and {ITEM_NAME_MAX} "
    item_price_per_night = request.forms.get("item_price_per_night", "").strip()
    if not re.match(ITEM_PRICE_REGEX, item_price_per_night): raise Exception(error, 400)
    return item_price_per_night


############################## TODO: Fix this, we need to validate the image size and number of images
ITEM_IMAGES_MIN = 1
ITEM_IMAGES_MAX = 5
ITEM_IMAGE_MAX_SIZE = 1024 * 1024 * 5 # 5MB


def validate_item_images():
    try:
        item_splash_images = request.files.getall("item_splash_images")

        print(item_splash_images)
        for image in item_splash_images:
            if pathlib.Path(image.filename).suffix.lower() == "":
                raise Exception("No image file added", 400)

            # Read the file into memory and check its size
            file_in_memory = BytesIO(image.file.read())
            if len(file_in_memory.getvalue()) > ITEM_IMAGE_MAX_SIZE:
                raise Exception("Image size exceeds the maximum allowed size of 5MB", 400)

            # Don't forget to go back to the start of the file if it's going to be read again later
            image.file.seek(0)

        if len(item_splash_images) == 0 or len(item_splash_images) < ITEM_IMAGES_MIN or len(item_splash_images) > ITEM_IMAGES_MAX:
            raise Exception(f"Invalid number of images, must be between {ITEM_IMAGES_MIN} and {ITEM_IMAGES_MAX}", 400)

        allowed_extensions = ['.png', '.jpg','.jpeg', '.webp']
        for image in item_splash_images:
            if not pathlib.Path(image.filename).suffix.lower() in allowed_extensions:
                raise Exception("Invalid image extension", 400)
            
        
        return item_splash_images
    except Exception as ex:
        print(ex)

    


##############################

ITEM_IMAGES_MIN = 0
ITEM_IMAGES_MAX = 5
ITEM_IMAGE_MAX_SIZE = 1024 * 1024 * 5 # 5MB


def validate_item_images_no_image_ok():
    item_splash_images = request.files.getall("item_splash_images")
        
    print("#################  no_image_ok  ###############################")
    print(item_splash_images)
    print("length of item_splash_images:", len(item_splash_images))
    for image in item_splash_images:
        if pathlib.Path(image.filename).suffix.lower() == "":
            return "no-image"


    if len(item_splash_images) == 0 or len(item_splash_images) < ITEM_IMAGES_MIN or len(item_splash_images) > ITEM_IMAGES_MAX:
        raise Exception(f"Invalid number of images, must be between {ITEM_IMAGES_MIN} and {ITEM_IMAGES_MAX}", 400)

    allowed_extensions = ['.png', '.jpg','.jpeg', '.webp']
    for image in item_splash_images:
        if not pathlib.Path(image.filename).suffix.lower() in allowed_extensions:
            raise Exception("Invalid image extension", 400)


    return item_splash_images



