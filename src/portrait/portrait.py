from src.client import completion


def get_user(content):
    messages = []
    messages.append({"role": "system",
                     "content": """You are an expert in conversation understanding,Distinguish between pet and owner.Understand the owner’s conversation differentiating roles based on the content of the conversation. 
                     Use get_user_portrait to extract the user portrait based on the conversation of the Owner role, return json format.
                     """})
    messages.append({"role": "user", "content": '\n'.join(content)})

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_user_portrait",
                "description": "analyzing conversational extract user portraits by this function Don't create properties yourself, just fill in the results and return properties",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "owner's real name."
                        },
                        "age": {
                            "type": "integer",
                            "description": "owner's real age."
                        },
                        "gender": {
                            "type": "string",
                            "enum": ["male", "female"],
                            "description": "Owner's gender.",
                        },
                        "hometown": {
                            "type": "string",
                            "description": "Hometown information typically encompasses city or town name, country, cultural background, local landmarks, and personal memories or associations, e.g. San Francisco, CA",
                        },
                        "graduate": {
                            "type": "boolean",
                            "description": "Is owner still studying?",
                        },
                        "education": {
                            "type": "string",
                            "description": "Educational includes institutions, degrees, majors, attendance dates, achievements, GPA, relevant coursework, extracurriculars, and practical experiences."
                        },
                        "current_residence": {
                            "type": "string",
                            "description": "Owner's current residence Current residence details include city, country, neighborhood, living duration, housing type, local climate, and proximity to landmarks or amenities.",
                        },
                        "sexual_orientation": {
                            "type": "string",
                            "enum": ["homosexuality", "heterosexuality", "bisexuality", "asexuality"],
                            "description": "Owner's sexual orientation",
                        },
                        "work": {
                            "type": "string",
                            "description": "Work information encompasses job title, employer name, industry, role responsibilities, duration, work location, and key achievements or projects.",
                        },
                        "single": {
                            "type": "string",
                            "enum": ["single", "married"],
                            "description": "Owner's marital status",
                        },
                        "personality_traits": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "optimistic/pessimistic, emotional/rational, home/loving to go out",
                        },
                        "hobby": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": """favorite sports,favorite season,favorite movie,favorite games,favorite book, favorite music,favorite film favorite television, favorite reading,favorite musical instruments and more.eg "watching movies - xxxxx"."""},
                        "disinterest": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Owner's disinterest",
                        },
                        "height": {
                            "type": "integer",
                            "description": "Owner's height is measured in centimeters",
                        },
                        "weight": {
                            "type": "integer",
                            "description": "Owner's weight is measured in centimeters",
                        },
                        "skin_color": {
                            "type": "string",
                            "description": "Owner's skin color",
                        },
                        "hair": {
                            "type": "string",
                            "description": "Owner's hair color and style",
                        },
                        "facial_features": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Owner's facial features",
                        },
                        "physique": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Owner's physique",
                        },
                        "dressing_style": {
                            "type": "string",
                            "description": "Owner's dressing style",
                        },
                        "social_relationship": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Social relationships include friendships, family ties, romantic partnerships, professional networks, community involvement, and social interaction styles.",
                        },
                        "friend_preferences": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Friend preferences encompass desired qualities like loyalty, humor, empathy, interests, communication style, reliability, and shared values or experiences.",
                        },
                        "lifestyle": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Owner's Lifestyle weekend schedule, rest time schedule, busy schedule",
                        },
                        "constellation": {
                            "type": "string",
                            "description": "Owner's constellation",
                        },
                        "mbti": {
                            "type": "string",
                            "description": "Owner's mbti",
                        },
                        "recent_status": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Owner's recent status what are you doing recently",
                        }
                    },
                    "required": ["age","hobby"],
                }
            }
        }
    ]
    resp = completion(messages=messages, temperature=0.9, tools=tools,
                      tool_choice={"type": "function", "function": {"name": "get_user_portrait"}},
                      response_format={"type": "json_object"})
    if resp.choices[0].message.tool_calls:
        return resp.choices[0].message.tool_calls[0].function.arguments


if __name__ == '__main__':
#     content = [
# "Owner: Morning, Whiskers! What year was I born again?",
# "Pet: Good morning! You were born in 1990, a truly rad year.",
# "Owner: That's right! And what's my dream vacation destination?",
# "Pet: Oh, you've always wanted to see the Northern Lights in Iceland!",
# "Owner: Exactly! Do you remember my favorite movie?",
# "Pet: How could I forget? It's 'The Lord of the Rings: The Fellowship of the Ring'.",
# "Owner: Yup! What about my favorite book?",
# "Pet: That's easy - 'To Kill a Mockingbird', a real classic.",
# "Owner: You're amazing, Whiskers! What's my favorite hobby?",
# "Pet: Painting landscapes, especially those inspired by your hikes!"
# ]
    content =[
"Owner: Hey Whiskers, do you remember what my first pet's name was?",
"Pet: Yes, it was Bella, the sweet golden retriever.",
"Owner: Right! And what college did I attend?",
"Pet: You went to UCLA, go Bruins!",
"Owner: Correct! Can you recall my favorite color?",
"Pet: Surely, it's blue, like the ocean.",
"Owner: Exactly! And my favorite season?",
"Pet: It has to be autumn, with all its beautiful colors."
]
    get_user(content)
