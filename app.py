import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import speech_recognition as sr

# === إعداد التطبيق ===
app = Flask(__name__)
CORS(app)  # تمكين CORS لجميع النطاقات

# === إعداد مفتاح Gemini API ===
api_key = "AIzaSyBzGRe__QBvML5BlljaydfWxT9sKki4ieE"
os.environ["GEMINI_API_KEY"] = api_key
genai.configure(api_key=api_key)

# === تحميل بيانات الأمثلة من JSON (اختياري) ===
examples = []
try:
    with open("last.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        examples = data.get("qa_pairs", [])
except FileNotFoundError:
    print("⚠️ ملف last.json غير موجود، سيتم تشغيل النموذج بدون أمثلة.")

# === إعداد النموذج ===
generation_config = {
    "temperature": 0.5,
    "top_p": 0.9,
    "top_k": 50,
    "max_output_tokens": 500,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# === بناء البرومبت مع الأمثلة إن وجدت ===
def build_prompt(user_input):
    intro = (
        "أنا مساعد في موقع يهتم بصحة المرأة الجسدية والنفسية. "
        "يمكنني تقديم استشارات طبية ونصائح حول مواضيع مثل الدورة الشهرية، السرطان، والدعم النفسي والاجتماعي.\n"
        "لكن يجب أن تعلمي أنني لست بديلاً عن الطبيب المختص. نصائحي مبنية على المعلومات المتاحة لي. "
        "يُفضل دائمًا استشارة طبيب مختص للحصول على تشخيص دقيق.\n\n"
    )
    history = ""
    for pair in examples:
        history += f'المستخدم: {pair["question"]}\nالمساعد: {pair["answer"]}\n'

    return f"{intro}{history}المستخدم: {user_input}\nالمساعد:"

# === توليد رد باستخدام Gemini ===
def chatbot_response(user_input):
    prompt = build_prompt(user_input)
    print("📨 Prompt sent to Gemini:\n", prompt)
    try:
        response = model.generate_content([prompt])
        print("✅ Response from Gemini:\n", response.text)
        return response.text.strip()
    except Exception as e:
        print("❌ Error from Gemini:", str(e))
        return f"حدث خطأ أثناء توليد الرد: {str(e)}"

# === نقطة نهاية للرسائل النصية ===
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get('user_input', '')
        response = chatbot_response(user_input)
        return jsonify({'response': response})
    except Exception as e:
        print("❌ Error in /chat endpoint:", str(e))
        return jsonify({'response': f"حدث خطأ: {e}"}), 500

# === نقطة نهاية للرسائل الصوتية ===
@app.route('/voice', methods=['POST'])
def voice_chat():
    audio_file = request.files.get('audio')
    if not audio_file:
        return jsonify({'response': '⚠️ لم يتم تحميل الملف الصوتي.'}), 400

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            user_input = recognizer.recognize_google(audio, language="ar-EG")
            print("🎤 Transcribed voice input:", user_input)
            response = chatbot_response(user_input)
            return jsonify({'response': response})
    except Exception as e:
        print("❌ Error in /voice endpoint:", str(e))
        return jsonify({'response': f"⚠️ فشل التعرف على الصوت: {str(e)}"}), 500

# === تشغيل السيرفر ===
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
