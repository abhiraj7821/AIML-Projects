from groq import Groq
from dotenv import load_dotenv
import os
from PIL import ImageGrab,Image
import pyperclip
import google.generativeai as genai
import cv2

load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)
genai.configure(api_key=os.getenv("GENAI_API_KEY"))
web_cam=cv2.VideoCapture(0)


sys_msg = (
    "You are a multi-modal AI voice assistant. Your user may or may not have attached a photo for context"
"(either a screenshot or a webcam capture). Any photo has already been processed into a highly detailed"
"text prompt that will be attached to their transcribed voice prompt. Generate the most useful and"
"factual response possible, carefully considering all previous generated text in your response before"
"adding new tokens to the response. Do not expect or request images, just use the context if added."
"Use all of the context of this conversation so your response is relevant to the conversation. Make"
"your responses clear and concise, avoiding any verbosity."
)
convo=[{'role':'system','content':sys_msg}]

#GENAI_IMPLIMENTATION
safety_settings = [
    {
        'category': 'HARM_CATEGORY_HARASSMENT',
        'threshold': 'BLOCK_NONE'
    },
    {
        'category': 'HARM_CATEGORY_HATE_SPEECH',
        'threshold': 'BLOCK_NONE'
    },
    {
        'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
        'threshold': 'BLOCK_NONE'
    },
    {
        'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
        'threshold': 'BLOCK_NONE'
    },
]

genration_config = {
    'temperature': 0.7,
    'top_p': 1,
    'top_k': 1,
    'max_output_tokens': 2048
}

model = genai.GenerativeModel('gemini-1.5-flash-latest',
                            generation_config=genration_config,
                            safety_settings=safety_settings)

#Graq Implimentation
def groq_prompt(prompt,img_context):
  if img_context:
    prompt=f'USER PROMPT: {prompt}\n\n IMAGE CONTEXT:{img_context}'
  convo.append({'role':'user','content':prompt})
  chat_completion= groq_client.chat.completions.create(messages=convo, model='llama3-70b-8192')
  response=chat_completion.choices[0].message
  convo.append(response)
  return response.content

#Function Call Implimentation
def function_call(prompt):
    sys_msg=(
        'You are an AI function calling model. You will determine whether extracting the users clipboard content.'
        'Taking a screenshot, capturing the webcam or calling no function is best for voice assistant to respond'
        'to the users prompt. The webcam be assumed to be normal laptop webcam facing the user. You will '
        'respnd with only one selection from this list:["extract clipboard","take screenshot","capture webcam","None]\n'
        'Do not respond with anything but the most logical selection from that list with no explanations. Format the'
        'function call name exactly as I listed.'
    )

    function_convo=[{'role':'system','content':sys_msg},
                    {'role':'user','content':prompt}]
    
    chat_completion=groq_client.chat.completions.create(messages=function_convo,model='llama3-70b-8192')
    response=chat_completion.choices[0].message
    return response.content

#Function to take screenshot
def take_screenshot():
    path='screenshot.jpg'
    screenshot = ImageGrab.grab()
    rgb_screenshot=screenshot.convert('RGB')
    rgb_screenshot.save(path,quality=15)

#Function to capture web cam
def web_cam_capture():
    if not web_cam.isOpened():
        print('Error: Camera did not open successfully')
        exit()
    path = 'webcam.jpg'
    ret, frame = web_cam.read()
    if ret:
        cv2.imwrite(path, frame)
    else:
        print("Error: Could not capture frame from camera.")

#Function for clipboard
def get_clipboard_text():
    clipboard_content=pyperclip.paste()
    if isinstance(clipboard_content,str):
        return clipboard_content
    else:
        print('No clipboard text to copy')
        return None
    
#Function for vision analysis
def vision_prompt(prompt,photo_path):
    img=Image.open(photo_path)
    prompt=(
        'yout are the vision analysis AI that provides semtantic meaning from image to provide context'
        'to send another AI that will create a response to the user. Do not respond as AI assistant'
        'to the user. Insted take the user prompt input and try to extract all meaning from the photo'
        'relevant to the user prompt. Then generate as mush objective data about the image for the AI'
        f'assistant who will respond to the user. \nUSER PROMPT:{prompt}'
    )
    response=model.generate_content([prompt,img])
    return response.text

while True:
  prompt=input('USER: ')
  call=function_call(prompt)
  
  if 'take screenshot' in call:
    print('Taking screenshot')
    take_screenshot()
    print("SCREENSHOT TAKEN")
    visual_context=vision_prompt(prompt,'screenshot.jpg')
    print("VISON PROMPT EXECUTED SUCCESSFULL")
  elif 'capture webcam' in call:
    print('Capturing webcam')
    web_cam_capture()
    visual_context=vision_prompt(prompt,'webcam.jpg')
  elif 'extract clipboard' in call:
    print('Extracting clipboard text')
    paste=get_clipboard_text()
    prompt=f'{prompt}\n\n CLIPBOARD CONTENT:{paste}'
    visual_context=None
  else:
    visual_context=None
  
  response=groq_prompt(prompt,visual_context)
  print('ASSISTANT:',response)

print("EXECUTION SUCCESS")