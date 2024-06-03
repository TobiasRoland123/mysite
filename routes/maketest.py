from bottle import get


@get("/make-test")
def _():
    try:
        return "x"
    except Exception as ex:
        print(ex)
    finally:
        pass
