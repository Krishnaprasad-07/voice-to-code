# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# import json
# import requests
# import os
# import re

# LLAMA_API_URL = "http://localhost:11434/api/generate"
# CODE_STORAGE_PATH = "generated_code/"

# if not os.path.exists(CODE_STORAGE_PATH):
#     os.makedirs(CODE_STORAGE_PATH)

# last_generated_code = ""

# @login_required
# def voice2code(request):
#     global last_generated_code
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             command = data.get("command", "").strip().lower()
#             print(f"Received command: {command}")  

#             if not command:
#                 return JsonResponse({"error": "No command received"}, status=400)

#             # Handle add new line command
#             add_line_match = re.match(r"add a new line after line (\d+)", command)
#             if add_line_match:
#                 line_number = int(add_line_match.group(1))

#                 code_lines = last_generated_code.split("\n")
#                 if 1 <= line_number <= len(code_lines):
#                     code_lines.insert(line_number, "")  # Insert blank line
#                     last_generated_code = "\n".join(code_lines)
#                     return JsonResponse({"generated_code": last_generated_code})

#                 return JsonResponse({"error": "Invalid line number"}, status=400)

#             # Handle delete command
#             delete_match = re.match(r"delete (\d+)[a-z]{2} line", command)
#             if delete_match:
#                 line_number = int(delete_match.group(1))  

#                 code_lines = last_generated_code.split("\n")
#                 if 1 <= line_number <= len(code_lines):
#                     del code_lines[line_number - 1]
#                     last_generated_code = "\n".join(code_lines)
#                     return JsonResponse({"generated_code": last_generated_code})

#                 return JsonResponse({"error": "Invalid line number"}, status=400)

#             # Handle edit command
#             edit_match = re.match(r"edit (\d+)[a-z]{2} line as (.+)", command)
#             if edit_match:
#                 line_number = int(edit_match.group(1))  
#                 new_text = edit_match.group(2)  

#                 code_lines = last_generated_code.split("\n")
#                 if 1 <= line_number <= len(code_lines):
#                     code_lines[line_number - 1] = new_text
#                     last_generated_code = "\n".join(code_lines)
#                     return JsonResponse({"generated_code": last_generated_code})

#                 return JsonResponse({"error": "Invalid line number"}, status=400)

#             # Handle save command
#             if command == "save":
#                 return save_code(request)

#             # Prepare prompt for Llama API
#             prompt = f"Write only the Python function to:\n\n{command}\n\nDo not include any explanations, just return the function code."

#             payload = {
#                 "model": "llama3",
#                 "prompt": prompt,
#                 "max_tokens": 150,
#                 "temperature": 0.2,
#                 "stream": False
#             }
#             headers = {"Content-Type": "application/json"}

#             # Make request to Ollama API
#             response = requests.post(LLAMA_API_URL, headers=headers, json=payload)
#             if response.status_code != 200:
#                 return JsonResponse({"error": "Failed to generate code", "details": response.text}, status=response.status_code)

#             # Extract generated Python code
#             response_data = response.json()
#             generated_code = response_data.get("response", "").strip()

#             # Remove unnecessary markdown
#             generated_code = clean_code_output(generated_code)

#             # Store last generated code
#             last_generated_code = generated_code

#             return JsonResponse({"generated_code": last_generated_code})

#         except Exception as e:
#             return JsonResponse({"error": "Error processing request", "details": str(e)}, status=500)

#     return render(request, 'chats.html')


# def clean_code_output(code):
#     """ Remove unnecessary markdown from Llama responses """
#     if code.startswith("```python"):
#         code = code.replace("```python", "").strip()
#     if code.endswith("```"):
#         code = code.replace("```", "").strip()
#     return code


# @login_required
# def save_code(request):
#     """ Save the last generated code to a file """
#     global last_generated_code
#     try:
#         # Remove line numbers before saving
#         code_without_line_numbers = "\n".join(line.split(": ", 1)[-1] for line in last_generated_code.split("\n") if ": " in line)

#         file_path = os.path.join(CODE_STORAGE_PATH, "generated_script.py")
#         with open(file_path, "w") as f:
#             f.write(code_without_line_numbers)
#         return JsonResponse({"success": True, "file_path": file_path})
#     except Exception as e:
#         return JsonResponse({"error": "Failed to save file", "details": str(e)}, status=500)







from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import requests
import os
import re

LLAMA_API_URL = "http://localhost:11434/api/generate"
CODE_STORAGE_PATH = "generated_code/"

if not os.path.exists(CODE_STORAGE_PATH):
    os.makedirs(CODE_STORAGE_PATH)

last_generated_code = ""

@login_required
def voice2code(request):
    global last_generated_code
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            command = data.get("command", "").strip().lower()
            print(f"Received command: {command}")  

            if not command:
                return JsonResponse({"error": "No command received"}, status=400)

            # Handle insert new line of code
            insert_match = re.match(r"insert the code in line (\d+) \"(.+)\"", command)
            if insert_match:
                line_number = int(insert_match.group(1))
                new_code = insert_match.group(2)

                code_lines = last_generated_code.split("\n")
                if 1 <= line_number <= len(code_lines) + 1:
                    code_lines.insert(line_number - 1, new_code)
                    last_generated_code = "\n".join(code_lines)
                    return JsonResponse({"generated_code": last_generated_code})

                return JsonResponse({"error": "Invalid line number"}, status=400)

            # Handle add new line command
            add_line_match = re.match(r"add a new line after line (\d+)", command)
            if add_line_match:
                line_number = int(add_line_match.group(1))

                code_lines = last_generated_code.split("\n")
                if 1 <= line_number <= len(code_lines):
                    code_lines.insert(line_number, "")  # Insert blank line
                    last_generated_code = "\n".join(code_lines)
                    return JsonResponse({"generated_code": last_generated_code})

                return JsonResponse({"error": "Invalid line number"}, status=400)

            # Handle delete command
            delete_match = re.match(r"delete (\d+)[a-z]{2} line", command)
            if delete_match:
                line_number = int(delete_match.group(1))

                code_lines = last_generated_code.split("\n")
                if 1 <= line_number <= len(code_lines):
                    del code_lines[line_number - 1]
                    last_generated_code = "\n".join(code_lines)
                    return JsonResponse({"generated_code": last_generated_code})

                return JsonResponse({"error": "Invalid line number"}, status=400)

            # Handle edit command
            edit_match = re.match(r"edit (\d+)[a-z]{2} line as (.+)", command)
            if edit_match:
                line_number = int(edit_match.group(1))
                new_text = edit_match.group(2)

                code_lines = last_generated_code.split("\n")
                if 1 <= line_number <= len(code_lines):
                    code_lines[line_number - 1] = new_text
                    last_generated_code = "\n".join(code_lines)
                    return JsonResponse({"generated_code": last_generated_code})

                return JsonResponse({"error": "Invalid line number"}, status=400)

            # Handle save command
            if command == "save":
                return save_code(request)

            # Prepare prompt for Llama API
            prompt = f"Write only the Python function to:\n\n{command}\n\nDo not include any explanations, just return the function code."

            payload = {
                "model": "llama3.2",
                "prompt": prompt,
                "max_tokens": 150,
                "temperature": 0.2,
                "stream": False
            }
            headers = {"Content-Type": "application/json"}

            response = requests.post(LLAMA_API_URL, headers=headers, json=payload)
            if response.status_code != 200:
                return JsonResponse({"error": "Failed to generate code", "details": response.text}, status=response.status_code)

            response_data = response.json()
            generated_code = response_data.get("response", "").strip()

            generated_code = clean_code_output(generated_code)
            last_generated_code = generated_code

            return JsonResponse({"generated_code": last_generated_code})

        except Exception as e:
            return JsonResponse({"error": "Error processing request", "details": str(e)}, status=500)

    return render(request, 'chats.html')


def clean_code_output(code):
    if code.startswith("```python"):
        code = code.replace("```python", "").strip()
    if code.endswith("```"):
        code = code.replace("```", "").strip()
    return code


@login_required
def save_code(request):
    global last_generated_code
    try:
        file_path = os.path.join(CODE_STORAGE_PATH, "generated_script.py")
        with open(file_path, "w") as f:
            f.write(last_generated_code)
        return JsonResponse({"success": True, "file_path": file_path})
    except Exception as e:
        return JsonResponse({"error": "Failed to save file", "details": str(e)}, status=500)





# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# import speech_recognition as sr
# import requests
# import json

# # Local LLaMA API URL
# LLAMA_API_URL = "http://localhost:11501/v1/completions"

# @login_required
# def voice2code(request):
#     print("Request Method:", request.method)
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             command = data.get("command", "")
#             print("Received Command:", command)

#             if not command:
#                 return JsonResponse({"error": "No command received"}, status=400)

#             prompt = f"Convert this command into a Python program:\n\n'{command}'\n\nPython Code:\n"
#             print("Generated Prompt:", prompt)

#             payload = {
#                 "model": "llama3.2",
#                 "prompt": prompt,
#                 "max_tokens": 150,
#                 "temperature": 0.2
#             }
#             print("Payload to LLaMA:", payload)

#             headers = {"Content-Type": "application/json"}
#             response = requests.post(LLAMA_API_URL, headers=headers, data=json.dumps(payload))
#             print("LLaMA API Response:", response)

#             response_data = response.json()
#             print("Response Data:", response_data)

#             generated_code = response_data.get("choices", [{}])[0].get("text", "").strip()
#             print("Generated Code:", generated_code)

#             return JsonResponse({"generated_code": generated_code})
#         except Exception as e:
#             print("Error processing request:", e)
#             return JsonResponse({"error": "Error processing request"}, status=500)
    
#     return render(request, 'code.html')