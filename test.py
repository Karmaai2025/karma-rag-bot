import google.generativeai as genai

genai.configure(api_key="AIzaSyA_5lIT4kc-Ni5OoS44HmVQvuDT8bRBJTA")
models = genai.list_models()
for m in models:
    print(m.name)