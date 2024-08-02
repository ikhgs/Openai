from flask import Flask, jsonify, request, g
import replicate

app = Flask(__name__)

@app.before_request
def before_request():
    g.title = "❤️🍸Bruno API🍷🍸"

@app.route('/', methods=['GET'])
def get_fizz_buzz_sql():
    try:
        ask = request.args.get('ask', default="Write fizz buzz in SQL")

        input = {
            "prompt": ask,
            "temperature": 0.2,
            "stop_sequences": "",
            "presence_penalty": 1.15,
            "frequency_penalty": 0.2
        }

        result = []
        for event in replicate.stream(
            "snowflake/snowflake-arctic-instruct",
            input=input
        ):
            if event:  # Vérifier que l'événement n'est pas None
                result.append(str(event))  # S'assurer que l'événement est une chaîne de caractères

        return jsonify({"title": g.title, "output": ''.join(result)})

    except Exception as e:
        # Afficher l'erreur dans la console pour le débogage
        print(f"Erreur: {e}")
        return jsonify({"title": g.title, "error": "Une erreur s'est produite."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
      
