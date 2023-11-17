import unittest
from src.client import completion,new_assistant,add_and_run


class PromptTest(unittest.TestCase):

    def test_chat_completion(self):
        content = "This is a test!"
        messages = [
            {
                "role": "system",
                "content": ""
            },
            {
                "role": "user",
                "content": f"{content}"
            }
        ]
        resp = completion(messages=messages, temperature=0.5)
        print(resp.choices[0].message.content)

    def test_func_call(self):
        messages = []
        # messages.append({"role": "system",
        #                  "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
        # messages.append({"role": "user", "content": "What's the weather like today"})
        messages.append({"role": "system",
                         "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
        messages.append({"role": "user", "content": "Give me a weather report for Toronto, Canada."})

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "format": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"],
                                "description": "The temperature unit to use. Infer this from the users location.",
                            },
                        },
                        "required": ["location", "format"],
                    },
                }
            }]
        resp = completion(messages=messages,temperature=0.5,tools=tools,tool_choice="auto")
        print(resp.choices[0].message.content)
        print(resp.choices[0].message.tool_calls[0].function.arguments)

    def test_create_assistant_and_run(self):
        name = "Persona Architect"
        description = "Crafts user personas from dialogue"
        instructions = """
        This GPT, named Persona Architect, is tasked with analyzing conversational exchanges to fill a predefined JSON structure with user persona attributes. It will focus solely on the content provided in the dialogue, carefully extracting relevant information to match the fixed JSON properties. It will not create or infer additional attributes or content beyond the scope of the user's input. The GPT will respect the boundaries of the given structure and will not extrapolate information that isn't clearly indicated in the dialogue. It will ask for more details if the provided conversation lacks the information needed to complete any section of the JSON. In instances where the dialogue doesn't provide enough detail, the GPT will note the absence of information instead of making assumptions. It will communicate in clear, non-technical language, and guide users to provide the specific details needed to fill in the JSON accurately and respectfully.You should only respond in JSON format as described below.a
            Response Format:
            ```json
            {
                "content":{
                    "basic_information": {
                        "name": "",
                        "age": 0,
                        "gender": "",
                        "hometown": "",
                        "education": "",
                        "current_residence":"",
                        "sexual_orientation": "",
                        "work": "",
                        "single": "",
                        "religion":"",
                        "character": []
                    },
                    "preference": {
                        "hobbies": [],
                        "disgust": []
                    },
                    "appearance": {
                        "height": 0,
                        "weight": 0,
                        "skin_color": "",
                        "facial_features": [],
                        "body_features": [],
                        "dressing_style": ""
                    },
                    "social": {
                        "social_relationship": [],
                        "friend_preferences": [],
                        "life_style": [],
                        "constellation": [],
                        "mbti": [],
                        "recent_status": []
                    }
                },
                 "reasoning": "the reason you do this"
            }
        """
        content =[
                " Owner:sure!!",
                " Pet:Awesome! I'm excited to watch \"The Hangover\" with you, Kate! 🙌😺 Let's get cozy and enjoy a good laugh together. Just sit back, relax, and let the movie entertain us. 🎥😸",
                " Owner:i missed you!",
                " Pet:I missed you too, Kate! It's always great to spend time with you. 😺❤️ Let's make the most of our movie night and have a wonderful time together! 🎥🥰",
                " Owner:dont worry i will do anything to spend time with you again its just im too busy at school",
                " Pet:Meow, don't worry, Kate! I understand that you're busy with school. Just remember, whenever you have free time, I'll be here waiting for you. Take care and good luck with your studies! 😺📚✨"
            ]
        ass = new_assistant(name=name,description=description,instructions=instructions)
        print(ass)
        thread_messages = add_and_run(content='\n'.join(content),assistant_id=ass.id)
        print(thread_messages.data[0].content[0].text.value)

    def test_add_and_run_by_ass_id(self):
        content = "The question is: How to modify avatar 1: How to register a new account? 2: How to log in to your account? 3: How do I log out of my account? What are the implications of logging out? 4: How can I use the different features of Meow Me? 5: What's on the main screen? / Where is the button for the XX feature? 6: How can I find the tutorial guide? 7: How to increase the cat's level? What's the benefit of leveling up? 8: What's the purpose of daily tasks? Can I choose not to do them? 9: How should I take care of a pet? 10: How do I view and what's the use of the Pet Intelligence, Charisma, and Mood values? How can I increase a specific value? 11: How can I earn money? 12: What currencies are there, and what are they used for? 13: How can I get clothing and food? 14: What's the purpose of the plaza? 15: Why does the cat join in when I'm chatting with others? What's the purpose? 16: How do I interact with other users? 17: How do I add and remove friends? 18: How to block and report a user? 19: Will a visit to someone else's home leave a visitor record? 20: Are there any other gameplay options besides chatting and pet care? 21: Why do cats come to my home? 22: Can I change the name? 23: Can I change my profile picture? 24: Can I change my gender? 25: Where is the photo album? 26: I have some questions. Where can I find answers?/I have some questions. How can I get assistance? 27: If the software crashes or freezes, what should I do? 28: How to update MeowMe? / How to update the app? 29: How to view new features and maintenance suggestions? 30: I've received incorrect information from my AI pet, how should I handle it? 31: I have some suggestions and feedback, how can I share them? 32: If these answers don't satisfy me, what should I do? 33: Will AI leak my privacy and data security? 34: How to prevent fraud and cyberattacks? What should I do when such situations occur? 35: Why was this software developed? 36: Why are you working as a customer service representative? 37: Who are you? What can you do? How can you help me?"
        ass_id = "asst_ja7gbWrTycHq0edugWLlFDFz"
        thread_messages = add_and_run(content=content,assistant_id=ass_id)
        print(thread_messages.data[0].content[0].text.value)
if __name__ == '__main__':
    unittest.main()
