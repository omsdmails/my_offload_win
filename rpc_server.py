# rpc_server.py

from flask import Flask, request, jsonify
import smart_tasks  # ✅ غيّرنا من your_tasks إلى الاسم الحقيقي لملف المهام
import logging

# إعداد تسجيل الأحداث في ملف
logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify(status="ok")

@app.route("/run", methods=["POST"])
def run():
    try:
        data = request.get_json()
        func_name = data.get("func")
        args = data.get("args", [])
        kwargs = data.get("kwargs", {})

        fn = getattr(smart_tasks, func_name, None)
        if not fn:
            logging.warning(f"❌ لم يتم العثور على الدالة: {func_name}")
            return jsonify(error="Function not found"), 404

        logging.info(f"⚙️ تنفيذ الدالة: {func_name} من جهاز آخر")
        result = fn(*args, **kwargs)
        return jsonify(result=result)

    except Exception as e:
        logging.error(f"🔥 خطأ أثناء تنفيذ المهمة: {str(e)}")
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    # ✅ تأكد أن هذا المنفذ 7520 أو اللي خصصته مفتوح في الجدار الناري
    app.run(host="0.0.0.0", port=7520)

