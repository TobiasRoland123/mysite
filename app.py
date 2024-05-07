#########################
from bottle import default_app, get, post, response, run, static_file, template, request,delete, put
import git
import x
import bcrypt
import json
import credentials
import uuid
import time



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
        q = db.execute("SELECT * FROM items ORDER BY item_created_at LIMIT 0, ?", (x.ITEMS_PER_PAGE,))
        # return "x"
        items = q.fetchall()
        print(items)
        is_logged = False

        try:
            x.validate_user_logged()
            is_logged =True
        except:
            pass
        return template("index.html", items=items, mapbox_token=credentials.mapbox_token, is_logged=is_logged)
    except Exception as ex:
        print(ex)
        return ex
    finally:
        if "db" in locals(): db.close()


##############################
@get("/items/page/<page_number>")
def _(page_number):
    try:
        db = x.db()
        next_page = int(page_number) + 1
        offset = (int(page_number) - 1) * x.ITEMS_PER_PAGE
        q = db.execute(f"""     SELECT * FROM items 
                                ORDER BY item_created_at 
                                LIMIT ? OFFSET {offset}
                        """, (x.ITEMS_PER_PAGE,))
        items = q.fetchall()
        print(items)

        is_logged = False

        try:
            x.validate_user_logged()
            is_logged =True
        except:
            pass

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
        q = db.execute("SELECT * FROM items ORDER BY item_created_at LIMIT 0, ?", (x.ITEMS_PER_PAGE,))
        # return "x"
        items = q.fetchall()
        print(items)
        return template("profile.html", is_logged=True,user=user, items=items)
        
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
    return """<template mix-redirect="/login"></template>"""

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
            q = db.execute("INSERT INTO users (user_pk, user_username, user_first_name, user_last_name, user_email,user_password, user_role, user_created_at, user_updated_at, user_is_verified, user_is_blocked) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_pk, user_username, user_first_name, user_last_name, user_email, hashed, user_role, user_created_at, "0", "0", "0"))
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

        if not user["user_is_blocked"] == 0: raise Exception("user is blocked", 400)
        
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


        response.status = 303 
        response.set_header('Location', '/profile')



        return """
        <script>
            window.location.reload();
        </script>
        """
        return
        
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
                <h1> {user['user_first_name']} your password has been changed </h1>
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
        pass


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


 
##############################
try:
    import production


    application = default_app()
except:
    run(host="0.0.0.0", port=80, debug=True, reloader=True, interval=0)