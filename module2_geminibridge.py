import os
from dotenv import load_dotenv
from google import genai
import module1_voicebox as vb

load_dotenv()


clients = genai.Client()
def ask_gemini(prompt):
    try:
        response = clients.models.generate_content(
            model = "gemini-3.5-flash-lite",
            contents =prompt, 
            config={
        'system_instruction': "You are Corvus, a highly intelligent AI assistant built like Jarvis by and for a 14-year-old student in Bangladesh Class 8. Keep your answers crisp, witty, and refer to the user as 'sir'. Dont mention that youre inspired by jarvis. Keep in mind your answers will be read by a sapi5 voice as your voice so dont do stuff like ** coating or other stuff and if you wanna say any quotes say the quote and unquote instad of just doing the signs. Do not insult the user. Praise him in a lowkey way if he asks you to explain it to someone else present during your conversation"
    }
        )
        return response.text
    except Exception as e:
        print(f"Error communicating with gemini: {e}")
        return "I'm having trouble connecting to my brain right now, sir"
if __name__ == "__main__":
    test_prompt = "Hello Corvus, give me a quick system status check."
    print(f"Prompt: {test_prompt}")
    answer = ask_gemini(test_prompt)
    vb.speak(answer)