from flask import Flask, request, jsonify
from flask_cors import CORS
from your_tasks import multiply_task  # دالة مربوطة بـ @offload

app = Flask(__name__)
CORS(app)

@app.route('/multiply', methods=['POST'])
def multiply():
    try:
        data = request.get_json()
        a = data.get("a", 0)
        b = data.get("b", 0)
        result_dict = multiply_task(a, b)  # دالة offload
        return jsonify({"result": result_dict["result"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # هذا العنوان يسمح بالاستماع على IP خارجي لتلقي الاتصالات من الإنترنت
    app.run(host="0.0.0.0", port=7520)


