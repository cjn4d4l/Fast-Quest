from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

class Question (BaseModel):
    question: str = Field(description="Question to be generated based on the topic")
    correct_answer: str = Field(description="The correct answer of the generated question")

class QuestionList (BaseModel):
    questions: list[Question] = Field(description="The List of questions generated with the respective answers")

client = genai.Client()

def generate_question (topic: str, count: int):
    try:
        prompt = f"""
            Generate {count} questions based on the topic {topic}, then provide the correct answers to each questions
        """
        
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema_": QuestionList.model_json_schema()
            },
        )
        
        question = QuestionList.model_validate_json(interaction.output_text)
        return question
    except Exception:
        return None