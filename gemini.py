import json
import google.generativeai as genai

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.responses import PlainTextResponse

app = FastAPI()


@app.get("/", response_class=PlainTextResponse)
async def main():
    return "Hello World"
app = FastAPI()


class LLMs:
    def get_gemini(self, API_KEYS, promt_and_text):
        """
        Args:
            API_KEYS(str): The API key got from Gemini: https://aistudio.google.com/app/apikey 
            prompt(str)  : Prompt used to ask the Generative AI.
        
        Returns:
            Text(str): To return text from the Gemini.        
        """
        genai.configure(api_key=API_KEYS)
        generation_config = {
            "temperature": 1.0,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 8192
        }
        model = genai.GenerativeModel(model_name="gemini-1.5-pro", generation_config=generation_config)

        convo = model.start_chat()

        convo.send_message(promt_and_text)
        return convo.last.text
    
gemini = LLMs()

data = "performance_metrics.json"
with open("performance_metrics.json", 'r') as log_file:
    log_data = json.load(log_file)


prompt = f"""
You are a system engineer analysis expert. You will be analyzed a system server log PerfMon(Windows Performance Monitor) and report to a user what was happened and where might be a point to cause the problems.
Your task is to generate concise explain events step by steps and way to troubleshooting , accurate descriptions of the images without adding any information you are not confident about.
Focus on interpret what log is telling what happened in the system.

Important Guidelines:
* Prioritize accuracy:  If you are uncertain about any detail, state "Unknown" or "Can't tell" instead of guessing.
* Avoid hallucinations: Do not add information that is not directly supported by document or log data.
* Be specific: Use precise language to describe , and any interactions depicted.

Task: Answer the following questions in detail, providing clear reasoning and evidence from the giving data likes text in bullet points.
Instructions:

1. **Analyze:** Carefully examine the provided text context.
2. **Synthesize:** Integrate information textual elements.
3. **Reason:**  Deduce logical connections and inferences to address the question.
4. **Respond:** Provide a concise, accurate answer in the following format then Return these statements as a JSON Object with the structure contain in head name "message" where each problem is separated by its unique id. You can keep adding more objects with new id values for each issue:
    id:
    **Problem**: [Show a problem which analysis from all data , separate problem you found by each topic and report]
    **Explanation**: [Direct response to the question Root cause analysis and Bullet-point reasoning steps if applicable]
    **Solution**: [If possible give a recommandation or advice to troubleshooting from a problem by Root cause analysis]
    **departments**: [Give me a recommandation person who can give advice or will be troubleshooting to a problem.]

    and [don't!! write ```json in output], [don't write * ** on every value pairs].
    don't start unique id by "problem1": , "problem2": like this it not what i want.
5. **Ambiguity:** If the context is insufficient to answer, respond "Not enough context to answer."


From my log data:
{log_data}

Please Analyze log data from json format file and recommand or guide how should to do next if a server facing with problems The loaded JSON log data is now embedded in the prompt.

"""



json_string = gemini.get_gemini(API_KEYS="AIzaSyCrDbkd286r0RDi2xYBXBAOLx2kgl1_Yn4", promt_and_text=prompt)
print(json_string)



app = FastAPI()
@app.get("/chat/", response_class=PlainTextResponse)
async def read_items():
    return PlainTextResponse(json_string)

if __name__ == "__main":
    uvicorn.run("gemini.py:app", host="0.0.0.0",port=8000,worker=4)
