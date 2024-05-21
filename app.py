#########################
from bottle import default_app, get, post, response, run, static_file, template, request,delete, put, redirect
import git
import x
import bcrypt
import json
import credentials
import uuid
import time
import random



##############################
@get("/app.css")
def _():
    return static_file("app.css", ".")


##############################
@get("/<file_name>.js")
def _(file_name):
    return static_file(file_name+".js", ".")

##############################
@get("/test")
def _():
    return [{"name":"one"}]



##############################
@get("/images/<item_splash_image>")
def _(item_splash_image):
    return static_file(item_splash_image, "images")

 
@post('/secret_url_for_git_hook')
def git_update():
  repo = git.Repo('./mysite')
  origin = repo.remotes.origin
  repo.create_head('main', origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
  origin.pull()
  return ""
# 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

# https://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@github.com/TobiasRoland123/mysite.git
 
 
##############################
@get("/")
def _():
    try:
        db = x.db()
        # q = db.execute("SELECT * FROM items ORDER BY item_created_at LIMIT 0, ?", (x.ITEMS_PER_PAGE,))
        q = db.execute("SELECT * FROM items_images INNER JOIN items ON items_images.item_fk  = items.item_pk LIMIT 0, ?", (x.ITEMS_PER_PAGE,))
        
        # return "x"
        rows = q.fetchall()

        items = x.group_images(rows)



        # q_images = db.execute("SELECT * FROM items_images ORDER BY image_created_at ")
        # images = q_images.fetchall()
        print(items)
        is_logged = False

        try:
            x.validate_user_logged()
            is_logged =True
        except:
            pass
        return template("index.html", items=items,  mapbox_token=credentials.mapbox_token, is_logged=is_logged)
    except Exception as ex:
        print(ex)
        return ex
    finally:
        if "db" in locals(): db.close()


##############################
@get("/items/page/<page_number>")
def _(page_number):
    try:

        is_logged = False

        try:
            user = x.validate_user_logged()
            is_logged =True
        except:
            pass

        db = x.db()
        next_page = int(page_number) + 1
        offset = (int(page_number) - 1) * x.ITEMS_PER_PAGE
        if is_logged:
            if user['user_role'] == "admin":
                q = db.execute(f""" SELECT * FROM items_images 
                                    INNER JOIN items ON items_images.item_fk  = items.item_pk  
                                    ORDER BY item_created_at 
                                    LIMIT ? OFFSET {offset}
                            """, (x.ITEMS_PER_PAGE,))
            elif user['user_role'] == "partner":
                q = db.execute(f"""SELECT * FROM items_images 
                                    INNER JOIN items ON items_images.item_fk  = items.item_pk
                                    WHERE item_owner_fk = ?
                                    ORDER BY item_created_at 
                                    LIMIT ? OFFSET {offset}
                            """, (user['user_pk'],x.ITEMS_PER_PAGE,))
        else:
            q = db.execute(f"""     SELECT * FROM items_images 
                                    INNER JOIN items ON items_images.item_fk  = items.item_pk  
                                    ORDER BY item_created_at 
                                    LIMIT ? OFFSET {offset}
                            """, (x.ITEMS_PER_PAGE,))
        rows = q.fetchall()

        print("################################# morew btn pressed rows:")
        print(rows)
        

        items = x.group_images(rows)        

        html = ""
        for item in items: 
            html += template("_item", item=item, is_logged=is_logged)
        btn_more = template("__btn_more", page_number=next_page)
        if len(items) < x.ITEMS_PER_PAGE: 
            btn_more = ""
        return f"""
        <template mix-target="#items" mix-bottom>
            {html}
        </template>
        <template mix-target="#more" mix-replace>
            {btn_more}
        </template>
        <template mix-function="test">{json.dumps(items)}</template>
        """
    except Exception as ex:
        print(ex)
        return "ups..."
    finally:
        if "db" in locals(): db.close()

##############################
@get("/login")
def _():
    x.no_cache()
    return template("login.html")


##############################
@get("/profile")
def _():
    try:
        x.no_cache()
        user = x.validate_user_logged()
        db=x.db()

        if user['user_role'] == 'partner':
            try:
                q = db.execute("""SELECT * FROM items_images 
                               INNER JOIN items ON items_images.item_fk  = items.item_pk 
                               WHERE item_owner_fk = ? 
                               ORDER BY item_created_at """, 
                               (user['user_pk'],))
                rows = q.fetchall()


                print("rows: *************************")
                print(rows)




                items = x.group_images(rows)


               

                print("items:  #########################################")
                print(items)
                profile_template = template("profile_partner.html", is_logged=True,user=user, items=items, role=user['user_role'])
            except Exception as ex:
                print("############   error in fetching partner items   ****************:")
                print(ex)
        elif user['user_role'] == 'admin':
            try:
                q = db.execute(f""" SELECT * FROM items_images 
                                    INNER JOIN items ON items_images.item_fk  = items.item_pk  
                                    ORDER BY item_created_at 
                                    
                            """)              
                rows = q.fetchall()

                items = x.group_images(rows)
                profile_template = template("profile_admin.html", is_logged=True,user=user, items=items, role=user['user_role'])
            except Exception as ex:
                print("############   error in fetching admin items   ****************:")
                print(ex)
        else:
            profile_template = template("profile_customer.html", is_logged=True,user=user , role='customer')




        
      

        return profile_template
        
    except Exception as ex:
        print(ex)
        response.status = 303 
        response.set_header('Location', '/login')
        return


##############################
@post("/toogle_item_block")
def _():
    try:
        item_id = request.forms.get("item_id", '')
        return f"""
        <template mix-target="[id='{item_id}']" mix-replace>

            <form id="{item_id}">

            <input name="item_id" type="text" value="{item_id}" class="hidden">
             <button
            mix-data="[id='{item_id}']"
            mix-post="/toogle_item_unblock"
             >
            Unblock
        </button>

        </form>
        </template>
        """
    except Exception as ex:
        pass
    finally:
        if "db" in locals(): db.close()

##############################
@post("/toogle_item_unblock")
def _():
    try:
        item_id = request.forms.get("item_id", '')
        return f"""
        <template mix-target="[id='{item_id}']" mix-replace>

         <form id="{item_id}">
            <input name="item_id" type="text" value="{item_id}" class="hidden">
        <button
            mix-data="[id='{item_id}']"
            mix-post="/toogle_item_block"
        >
           Block
        </button>
         </form>
        </template>
        """
    except Exception as ex:
        pass
    finally:
        if "db" in locals(): db.close()


##############################
@get("/logout")
def _():
    response.delete_cookie("user")
    response.status = 303
    response.set_header("Location", "/login")
   

##############################
@get("/api")
def _():
    return x.test()


##############################
##############################
@get("/signup")
def _():
    try:

      

        return template("signup.html")
    except Exception as ex:
        print(f"########## {ex} ***************")


##############################
@get("/all-users")
def _():
    try:

        db = x.db()  # Replace x.db with the actual function or method that returns a database connection object
        users = db.execute("SELECT * FROM users").fetchall()
        return template("all_users.html", users=users)
    except Exception as ex:
        print(ex)



##############################
@delete("/delete-all-but-admin")
def _():
    try:
        db = x.db()
        q = db.execute("DELETE FROM users WHERE user_username != 'johndoe'")
        db.commit()
        return "x"
    except Exception as ex:
        print(ex)
    finally:
        if "db" in locals: db.close



##############################
@post("/signup")
def _():
    try:

        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        user_confirm_password = x.validate_user_confirm_password()
        user_username = x.validate_user_username()
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()
        user_role = x.validate_user_role()
        user_pk = str(uuid.uuid4().hex)
        user_created_at = int(time.time())
        

        # # this makes user_password into a byte string
        password = user_password.encode() 
    
        # # Adding the salt to password
        salt = bcrypt.gensalt()
        # # Hashing the password
        hashed = bcrypt.hashpw(password, salt)
        # # printing the salt
        print("Salt :")
        print(salt)
        
        # # printing the hashed
        print("Hashed")
        print(hashed)    



        try:
            db = x.db()
            q = db.execute("INSERT INTO users (user_pk, user_username, user_first_name, user_last_name, user_email,user_password, user_role, user_created_at, user_updated_at, user_is_verified, user_blocked_at,user_deleted_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)", (user_pk, user_username, user_first_name, user_last_name, user_email, hashed, user_role, user_created_at, "0", "0", "0","0"))
            db.commit()
            
            x.send_verification_email('samueltobiasrolanduyet@gmail.com', user_email, user_pk)
        except Exception as ex:
            print(ex)
        finally:
            if "db" in locals(): db.close()
        



        return f"""
        <template mix-target="[id='frm_signup']" mix-replace>

            <div>
                <h1 class="text-2xl font-bold">A mail has been sent to {user_email}</h1>
                <p>Check email in order to verify account</p>
            </div>

         
        </template>
        """
    except Exception as ex:
        try:
            print(ex)
            response.status = ex.args[1]
            return f"""
            <template mix-target="#toast">
                <div mix-ttl="3000" class="error">
                    {ex.args[0]}
                </div>
            </template>
            """
        except Exception as ex:
            print(ex)
            response.status = 500
            return f"""
            <template mix-target="#toast">
                <div mix-ttl="3000" class="error">
                   System under maintainance
                </div>
            </template>
            """
    finally:
        if "db" in locals(): db.close()


##############################
@get("/activate-user/<id>")
def _(id):
    try:
        db = x.db()
        q = db.execute("UPDATE users SET user_is_verified = 1 WHERE user_pk = ?", (id,))
        user_first_name = db.execute("SELECT user_first_name FROM users WHERE user_pk = ?", (id,)).fetchone()["user_first_name"]
        db.commit()

        print(f"################################  {user_first_name}   #####################################")
        
        # return f"Activated user with ID: {id}"
        return template("activate_user.html", user_first_name=user_first_name) 
    
    except Exception as ex:
        return f"Failed to activate user with ID: {id}"
        print("activate user get went wrong #########################",ex)
    finally:
        if "db" in locals(): db.close()

##############################
# @post("/activate_user_with_key/<id>")
# def _(id):
#     try:
#         db = x.db()
#         q = db.execute("UPDATE users SET user_is_verified = 1 WHERE user_pk = ?", (id,))
#         db.commit()



#         return (f"{id}", 200)
#     except Exception as ex:
#         raise Exception("***** user could not be activated *****", 400)
#         print(ex)
    



##############################
@post("/login")
def _():
    try:
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        db = x.db()
        q = db.execute("SELECT * FROM users WHERE user_email = ? LIMIT 1", (user_email,))
        user = q.fetchone()
        if not user: raise Exception("user not found", 400)

        print(f"########### user: ")
        print(f"  {user} ************")
        if not user["user_is_verified"] == 1: raise Exception("user not verified", 400)

        if not user["user_deleted_at"] == 0: raise Exception("user doesn't exist", 400)
        if not user["user_blocked_at"] == 0: raise Exception("user is blocked", 400)
        
        try:
            if not  bcrypt.checkpw(user_password.encode(), user["user_password"].encode()): raise Exception("Invalid credentials", 400)
        except Exception as ex:
            if not  bcrypt.checkpw(user_password.encode(), user["user_password"]): raise Exception("Invalid credentials", 400)
        user.pop("user_password") # Do not put the user's password in the cookie
        print(user)
        try:
            import production
            is_cookie_https = True
        except:
            is_cookie_https = False        
        response.set_cookie("user", user, secret=x.COOKIE_SECRET, httponly=True, secure=is_cookie_https)
        frm_login = template("__frm_login")

        return f"""
        <template mix-target="frm_login" mix-replace>
            {frm_login}
        </template>
        <template mix-redirect="/profile">
        </template>
        """
    except Exception as ex:
        try:
            print(ex)
            response.status = ex.args[1]
            return f"""
            <template mix-target="#toast">
                <div mix-ttl="3000" class="error">
                    {ex.args[0]}
                </div>
            </template>
            """
        except Exception as ex:
            print(ex)
            response.status = 500
            return f"""
            <template mix-target="#toast">
                <div mix-ttl="3000" class="error">
                   System under maintainance
                </div>
            </template>
            """
        

    finally:
        if "db" in locals(): db.close()


##############################
@put("/edit-user")
def _():
    try:
        user = x.validate_user_logged()


        user_email = x.validate_user_email()
        user_username = x.validate_user_username()
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()
        user_updated_at = int(time.time())

        db = x.db()

        q = db.execute("UPDATE users SET user_email =?, user_username = ?, user_first_name = ?, user_last_name = ?, user_updated_at = ? WHERE user_pk = ?", ( user_email,user_username, user_first_name, user_last_name, user_updated_at, user["user_pk"]))
        db.commit()        



        updated_user = {**user, "user_email": user_email, "user_username": user_username, "user_first_name": user_first_name, "user_last_name": user_last_name, "user_updated_at": user_updated_at}

        print("############### updated_user: ", updated_user)
        print(updated_user)

        try:
            is_cookie_https = True
        except:
            is_cookie_https = False        
        response.set_cookie("user", updated_user, secret=x.COOKIE_SECRET, httponly=True, secure=is_cookie_https)


       
        redirect(request.url)

        
        
    except Exception as ex:    
        print(ex)
    finally:
        if "db" in locals(): db.close()



##############################
@get("/forgot-password")
def _():
    try:
        return template("forgot_password.html")
    except Exception as ex:
        print(ex)


##############################
@post("/send-reset-password-email")
def _():
    try:
        user_email = x.validate_user_email()

        db = x.db()
        q = db.execute("SELECT * FROM users WHERE user_email = ? LIMIT 1", (user_email,))
        user = q.fetchone()

        x.send_reset_password_email("samueltobiasrolanduyet@gmail.com", user_email, user["user_pk"])



        return f"{user}"
    except Exception as ex:
        print(ex)
    finally:
        if "db" in locals(): db.close()

##############################
@get("/change-password/<id>")
def _(id):
    try:
        # db = x.db()
        # q = db.execute("SELECT * FROM users WHERE user_pk = ? LIMIT 1", (id,))
        # user = q.fetchone()


        return template("change_password.html", id=id)
    except Exception as ex:
        print(ex)

    finally:
        if "db" in locals(): db.close()


##############################
@put("/change-password/<id>")
def _(id):
    try:
        
        user_password = x.validate_user_password()
        user_confirm_password = x.validate_user_confirm_password()
  
            

        updated_at = int(time.time())

        # # this makes user_password into a byte string
        password = user_password.encode() 
    
        # # Adding the salt to password
        salt = bcrypt.gensalt()
        # # Hashing the password
        hashed = bcrypt.hashpw(password, salt)
        # # printing the salt
        print("Salt :")
        print(salt)
        
        # # printing the hashed
        print("Hashed")
        print(hashed)    


        db = x.db()

        q = db.execute("UPDATE users SET user_password = ?, user_updated_at = ? WHERE user_pk = ?", ( hashed, updated_at,id))
        db.commit()    


        get_user_query = db.execute("SELECT * FROM users WHERE user_pk = ?", (id,))   
        user = get_user_query.fetchone()

        return f"""

            <template mix-target="#frm_change_password" mix-replace>
            <div>
                <h1 class="text-2xl font-bold"> {user['user_first_name']}  </h1>
                <p>your password has been changed</p>
                <a class="text-blue-600 underline" href="/login"> Click here to login </a>
            </div>
             </template>

            """
    except Exception as ex:
        try:
            print(ex)
            response.status = ex.args[1]
            return f"""
            <template mix-target="#toast">
                <div mix-ttl="3000" class="error">
                    {ex.args[0]}
                </div>
            </template>
            """
        except Exception as ex:
            print(ex)
            response.status = 500
            return f"""
            <template mix-target="#toast">
                <div mix-ttl="3000" class="error">
                   System under maintainance
                </div>
            </template>
            """
    finally:
        if "db" in locals(): db.close()


##############################
@get("/delete-user")
def _():
    try:
        user = x.validate_user_logged()
       

        return template("delete_user.html")
    except Exception as ex:
        print(ex)
        response.status = 303 
        response.set_header('Location', '/login')
    finally:
        pass



##############################
@post("/delete-user")
def _():
    try:
        user = x.validate_user_logged()
        user_password = x.validate_user_password()

        db = x.db()
        q = db.execute("SELECT * FROM users WHERE user_email = ? LIMIT 1", (user['user_email'],))
        logged_user = q.fetchone()
        


        
        print(f"######################## user_password: {user_password}")
        print(f"######################## logged_user_password: {logged_user['user_password']}")

        

        try:
            if not  bcrypt.checkpw(user_password.encode(), logged_user["user_password"].encode()): raise Exception("Invalid credentials", 400)
        except Exception as ex:
            if not  bcrypt.checkpw(user_password.encode(), logged_user["user_password"]): raise Exception("Invalid credentials", 400)
       

      
        db.execute("UPDATE users SET user_deleted_at = ? WHERE user_pk = ?", (int(time.time()), user["user_pk"]))
        db.commit()

        x.send_user_deleted_email("samueltobiasrolanduyet@gmail.com", logged_user['user_email'])

        response.delete_cookie("user")

        return """


                <template mix-target="#frm_confirm_delete_user" mix-replace>
                    <h1>User has been deleted</h1>
                </template>

            """
    except Exception as ex:
        print(ex)
        response.status = 303 
        response.set_header('Location', '/login')
    finally:
        if "db" in locals(): db.close()


############################################################
@post("/check-email")
def _():
    try:
        email = x.validate_user_email()

        return email
        
    except Exception as ex:
        print(ex)
        return f"""

            <template mix-target="#message">
                <div>
                    Please enter a valid email
                </div>
            </template>
    
        """

#####################################

@post("/create_property")
def _():
    try:
        item_pk = uuid.uuid4().hex
        item_name = x.validate_item_name()
        item_lat = random.uniform(55.615, 55.727)
        item_lon = random.uniform(12.451, 12.650)
        item_stars = 5
        item_price_per_night  = x.validate_item_price()
        item_created_at = 1
        item_updated_at = 0
        item_owner_fk = "01ad74495a114c28b80fd73be024aa7d"


        db = x.db()

            # Images
        item_images = x.validate_item_images()


        


           # Process each image, rename it, save it, and store just the filename in the database
        for index, image in enumerate(item_images, start=1):
            image_pk =  uuid.uuid4().hex
            filename = f"{item_pk}_{index}.{image.filename.split('.')[-1]}"
            path = f"images/{filename}"
            image.save(path)  # Save the image with the new filename

            # Insert the image filename into the item_images table (without path)
            db.execute("INSERT INTO items_images (image_pk,image_url,item_fk, image_created_at) VALUES (?,?, ?,?)", (image_pk,filename,item_pk, 0))
            db.commit()

        print("##############***********w**'##################")
        print(item_images)
        q = db.execute("INSERT INTO items (item_pk, item_name, item_lat, item_lon, item_stars, item_price_per_night, item_created_at, item_updated_at, item_owner_fk) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
               (item_pk, item_name, item_lat, item_lon, item_stars, item_price_per_night, item_created_at, item_updated_at, item_owner_fk))
        db.commit()
            
        redirect(request.url)
    except Exception as ex:
        try:
            print(ex)
            response.status = ex.args[1]
            return f"""
            <template mix-target="#toast">
                <div mix-ttl="3000" class="error">
                    {ex.args[0]}
                </div>
            </template>
            """
        except Exception as ex:
            print(ex)
            response.status = 500
            return f"""
            <template mix-target="#toast">
                <div mix-ttl="3000" class="error">
                   System under maintainance
                </div>
            </template>
            """
    finally:
        if "db" in locals(): db.close()


########################################################
@put("/edit_item/<item_pk>")
def _(item_pk):

    try:
        user = x.validate_user_logged()

        
        db = x.db()
        
        if user['user_role'] == "admin":
            pass
        elif user['user_role'] =='partner':
            x.validate_user_has_rights(user, item_pk)
        else:
            raise Exception("User does not have the right to edit this property")
        
        # Fetch existing images from the database
        old_images = db.execute("SELECT image_url FROM items_images WHERE item_fk = ?", (item_pk,)).fetchall()

        if 1 <= len(old_images) <= 5:
            item_new_images = x.validate_item_images_no_image_ok()
        else:
            item_new_images = x.validate_item_images()
        item_name = x.validate_item_name()
        item_price = x.validate_item_price()
       
        item_updated_at = int(time.time())

      

         # Update item details
        db.execute("""
            UPDATE items
            SET item_name = ?, item_price_per_night = ?, item_updated_at = ?
            WHERE item_pk = ?
        """, (item_name, item_price, item_updated_at, item_pk))
        db.commit()

        return item_pk
    except Exception as ex:
        print("#############################################edit item")
        print(ex)
    finally:
        if "db" in locals(): db.close()

##############################
try:
    import production

    application = default_app()
except:
    run(host="0.0.0.0", port=80, debug=True, reloader=True, interval=0)