import module1_voicebox as vb
import module2_geminibridge as gb


def ask_corvus(prompt):
    answer = gb.ask_gemini(prompt)
    vb.speak(answer)

ask_corvus("I have just started you up, greet me in your style")
while True:

    user_speech = vb.listen_and_recognize()
    if user_speech:
        if "go back to sleep" in user_speech:
            vb.speak("Going back to sleep, sir.")
            break
        ask_corvus(user_speech)
    else:
        pass
    
    