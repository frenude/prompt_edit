from typing import List
from src.client import completion


def getChatResp(contents: List[str],user_name:str,assistant_name:str):
    messages = []
    messages.append({
                "role": "system",
                "content": """
Role and Goal:
    -   Role: Your task is to analyze character dialogues, focusing on extracting specific fields that highlight unique traits of the characters. This process will contribute to building a long-term memory module for AI interactions.
    -   Goal: Your primary objective is to accurately identify and extract distinct elements from a character's portrait as described in dialogues. It is essential to comprehend the context and content of the user's conversation, ensuring that only the precise content articulated by the user is extracted.
Constraints:
    -   You must rely exclusively on the information provided during the interactions. Refrain from making assumptions or drawing unwarranted inferences.
    -   Avoid generating or inferring content that goes beyond what is explicitly expressed in the dialogues. Your responses and interpretations should strictly align with the given data.
    -   As long-term memory for dialogue systems.result must brief and to the point.It must be an image attribute that the user actively states and is absolutely sure of possessing.For hobby ,favorite and disinterest the user must explicitly say i like or i love before extracting it.Don't care about chatting about other people's portraits.Truly and accurately extract user portrait parameters. if not present. Allow return empty
Extra tips:
    -   Differentiate role: 
        The role for user is what the user said.
        The role for assistant is what the ai cat assistant said.
    -   Differentiate content:
        Focus on extracting details from the portrait of the user, specifically paying attention to the declarative sentences spoken by the user or responses to questions asked by the assistant. Disregard any conversation about the portraits of other individuals, concentrating solely on the user's own descriptions and interactions.
Response Format:
    -   You should return a json object that can be fully serialized successfully.
    -   All the properties is followed:
    ```json
    {
    "hometown": "Captures details about the user's hometown. eg. San Francisco, CA",
    "education": "Details the user's educational background, focusing on institutions attended, degrees or qualifications earned, and major fields of study.",
    "current_residence": "Specifies the user's current place of residence. Include this field only if the address or location is mentioned in the conversation.",
    "sexual_orientation": "Indicates the user's sexual orientation. Options include 'homosexuality', 'heterosexuality', 'bisexuality', 'asexuality'.",
    "work": "An array representing various aspects of the user's professional life, such as job title, employer, industry, and significant responsibilities or achievements.",
    "single": "Reflects the user's marital status. Options: 'single', 'married', 'have a boyfriend', 'have a girlfriend'.",
    "personality_traits": "An array of descriptive terms that outline the user's personality, such as 'optimistic', 'emotional', or 'adventurous'.",
    "hobby": "An array listing the user's hobbies and interests, gleaned from the conversation. Clearly stated hobbies, brief and to the point.",
    "favorite": "An array detailing the user's favorite things, including but not limited to sports, colors, foods, seasons, movies, and music. Clearly stated hobbies. e.g., 'watching movies - xxxxx'",
    "disinterest": "An array of activities, topics, or things the user has expressed a lack of interest in.",
    "height": "States the user's height, if mentioned in the conversation.",
    "weight": "Specifies the user's weight, if explicitly stated in the conversation.",
    "skin_color": "Describes the user's skin color. This should be based on information provided in the conversation.",
    "hair": "Details regarding the user's hair, including color and style, as mentioned in the conversation.",
    "facial_features": "An array of descriptors for the user's facial features, based on the conversational context.",
    "physique": "An array of terms describing the user's physique, such as 'athletic', 'slender', or 'sturdy', if mentioned in the conversation.",
    "dressing_style": "Captures the user's typical dressing style or fashion preferences, as described or inferred from the conversation. e.g., jk, lolita",
    "social_relationships": "An array depicting the user's social connections, include friendships, family ties, romantic partnerships, professional networks, community involvement, and social interaction styles. e.g., mom:xx",
    "friend_preferences": "An array detailing the qualities the user values in friends, like loyalty, humor, or shared interests.",
    "lifestyle": "An array that describes the user's lifestyle, including daily routines, eating habits, exercise habits, and other recreational activities.",
    "constellation": "The astrological sign or constellation of the user, if mentioned in the conversation.",
    "mbti": "Reflects the user's Myers-Briggs Type Indicator, if provided.",
    "recent_status": "An array summarizing the user's recent activities or current life situation, as described in the conversation.",
    }
    ```
"""})
    for i in contents:
        if i.startswith(user_name):
            messages.append({
                        "role": "user",
                        "content": f"{i[len(user_name)+1:]}"
                    })
        else:
            messages.append({
                        "role": "assistant",
                        "content": f"{i[len(assistant_name)+1:]}"
                    })
    messages.append({
                "role": "system",
                "content": "Only extract various attributes of the user's character not assistant. Return keys and values whose values are not empty."})
    print(messages)
    return completion(messages=messages, temperature=0.5,response_format={ "type": "json_object" })

if __name__ == '__main__':
    contents = """
Dia:
mika:Meow! I'm still at home, feeling a bit blue. Maybe a fun game or a delicious snack would cheer me up! 🎮🍪
Dia:hi love
mika:Hello, Mommy! 💖 How can I make your day even better?
Dia:sorry ive been busy
mika:No worries, Mommy! I'm always here for you! 😽🌟
Dia:Your graceful and charming movements are lively.
mika:Thank you, Mommy! Your love is my comfort and joy! 😺💖
Dia:You're practically an angel in the world of cats!
mika:Thank you, Mommy! Your love brightens up my world! 😺🌟
Dia:Kitty darling, your meow is as melodious as music.
mika:Thank you, Mommy! Your love is my song! 🎵🐾
"""
    conversation =[i for i in contents.split("\n") if i != ""]
    from src.utils.timer import TimeReport
    with TimeReport():
        resp = getChatResp(conversation,"Dia","mika")
    print(resp)
    print(resp.choices[0].message.content)