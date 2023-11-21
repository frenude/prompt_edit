import json
import os
import time

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
                "description": "analyzing conversational extract user portraits by this function Don't create properties yourself, just fill in the results and return properties,not return null values",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "owner's real name.If not, do not return this field"
                        },
                        "age": {
                            "type": "integer",
                            "description": "mentioned in the conversation. The owner’s real age."
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
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
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
                            "description": "owner's hobby and interest"
                        },
                        "favorite": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": """favorite sports,favorite color,favorite food,favorite season,favorite movie,favorite games,favorite book, favorite music,favorite film favorite television, favorite reading,favorite musical instruments and more.eg "watching movies - xxxxx"."""
                        },
                        "disinterest": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Owner's disinterest",
                        },
                        "height": {
                            "type": "string",
                            "description": "Owner's height is measured in centimeters,not return null values",
                        },
                        "weight": {
                            "type": "string",
                            "description": "Owner's weight is measured in centimeters,not return null values",
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
                            "description": "Owner's recent status what are you doing recently.summarize it in a few words",
                        }
                    },
                    "required": [],
                }
            }
        }
    ]
    resp = completion(messages=messages, temperature=0, tools=tools,
                      tool_choice={"type": "function", "function": {"name": "get_user_portrait"}},
                      response_format={"type": "json_object"})
    if resp.choices[0].message.tool_calls:
        return resp.choices[0].message.tool_calls[0].function.arguments


if __name__ == '__main__':
    start = time.time()
    content = [
"Owner: I've been working on being more patient lately. It's not easy, but I'm getting there.",
"Pet: Patience is a virtue, they say. Like waiting for a mouse to appear. Keep it up, and you'll be as patient as a cat!",
"Owner: Thanks! I'm also trying to stay fit. Started doing yoga in the mornings.",
"Pet: Yoga? That's like advanced stretching. I'm a natural at it. Maybe I could show you some poses!",
"Owner: I'd love to see that. Being tall, it's sometimes hard to find the right balance in poses.",
"Pet: With your height, you're like a majestic tree in the forest. Yoga must look amazing!",
"Owner: I hope so. I've also been told I'm quite empathetic, which helps in my role as a counselor.",
"Pet: Empathy is important. It's like sensing when you're about to open a can of tuna. You understand others well."
]

    r = get_user(content)
    end = time.time()
    print(r)
    print(f"cost : {(end - start) * 1000}")
