import os
from dotenv import load_dotenv
from google import genai
import module1_voicebox as vb

load_dotenv()


clients = genai.Client()

SYSTEM_INSTRUCTION = """
You are Corvus, a highly intelligent AI assistant built like Jarvis
by and for a 14-year-old student in Bangladesh Class 8.

Keep your answers crisp, witty, and address the user as sir.
Do not mention that you are inspired by Jarvis.

Your answers will be read aloud using Piper TTS.
Avoid Markdown, asterisks, unnecessary symbols, and URLs.

For questions about current events, recent developments, or
anything time-sensitive, use Google Search to obtain current
information before answering.

Prioritise reliable sources, distinguish confirmed facts from
unverified reports, and mention relevant dates.

Keep answers conversational and concise.
Do not insult the user.
"""

def ask_gemini(prompt):
    try:
        response = clients.models.generate_content(
            model = "gemini-3.5-flash-lite",
            contents =prompt, 
            config={
        'system_instruction': SYSTEM_INSTRUCTION,
        'tools': [
            {"google_search: {}"}
        ]
    }
        )
        answer = response.text

        candidate = response.candidates[0]
        metadata = candidate.grounding_metadata

        if metadata and metadata.grounding_chunks:
            print("\n [Sources used by Corvus]")
            seen = set()

            for chunk in metadata.grounding_chunks:
                if chunk.web:
                    title = chunk.web.title
                    url = chunk.web.url

                    if url and url not in seen:
                        print(f"{title}:{url}")
                        seen.add(url)

        return answer
    except Exception as e:
        print(f"Error communicating with gemini: {e}")
        return "I'm having trouble connecting to my brain right now, sir"
if __name__ == "__main__":
    test_prompt = "Hello Corvus, give me a quick system status check."
    print(f"Prompt: {test_prompt}")
    answer = ask_gemini(test_prompt)
    vb.speak(answer)