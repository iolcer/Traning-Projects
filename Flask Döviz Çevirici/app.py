from flask import Flask, render_template,request
import requests

url = "http://data.fixer.io/api/latest?access_key=2f2f94cb9e515c51e4744513264567a0"

app = Flask(__name__)
@app.route("/",methods = ["GET","POST"])
def index():
    if request.method == "POST":
        firstCurrency = request.form.get("firstCurrency")
        secondCurrency = request.form.get("secondCurrency")

        amount = request.form.get("amount")
        response = requests.get(url)
        
        infos = response.json()
        
        Currency1 = infos["rates"][firstCurrency]
        Currency2 = infos["rates"][secondCurrency]

        result = (Currency2 / Currency1) * float(amount)

        currencyInfo = dict()

        currencyInfo["firstCurrency"] = firstCurrency
        currencyInfo["secondCurrency"] = secondCurrency
        currencyInfo["amount"] = amount
        currencyInfo["result"] = result

        return render_template ("index.html",info = currencyInfo)

    else:
        return render_template ("index.html")
    
if __name__ == "__main__":
    app.run(debug=True)

