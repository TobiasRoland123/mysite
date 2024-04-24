#########################
from bottle import default_app, get, post, response, run, static_file, template, request
import git
import x

 
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
  return " after test removed icecream"
 
##############################
try:
  import production
  application = default_app()
except Exception as ex:
  print("Running local server")
  run(host="127.0.0.1", port=80, debug=True, reloader=True)