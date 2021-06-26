import os

if __name__ == "__main__":
    os.environ["FLASK_APP"] = "app.py"
    os.environ["FLASK_ENV"]="development"
    
    os.system('cmd /k "flask run"')

    
