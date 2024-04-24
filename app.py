#########################
from bottle import default_app, get, post, response, run, static_file, template, request
import git
import x
import bcrypt
import json
import credentials


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
try:
  import production
  application = default_app()
except Exception as ex:
  print("Running local server")
  run(host="127.0.0.1", port=80, debug=True, reloader=True)