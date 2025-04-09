import google.generativeai as genai

genai.configure(api_key="AIzaSyBx6oGMYzAklMwWQuEm0RKGXAWAWHaauTk")

models = genai.list_models()
for m in models:
    print(m.name, "—", m.supported_generation_methods)
