import time

from src.client import completion

content = ['Owner: Hey whiskers, guess what? I just got a promotion at work!',
           "Pet: That's pawesome! You must be feline great. What's your new title going to be?",
           'Owner: I’ll be the Lead Graphic Designer now. Lots more creativity and responsibility!',
           'Pet: As the cool cats say, you’re going to rock that design world! Let’s celebrate with some extra treats?',
           "Owner: Definitely! First, I'll get some sushi for me, and how about a new catnip toy for you?",
           'Pet: Sushi and catnip – purrfect! You truly know how to spoil me.',
           'Owner: What can I say? You deserve it for being such a good companion. And I love sushi – it’s my favorite food.',
           'Pet: Love is a shared plate of sushi and a fresh catnip toy! Seems like your hard work and creativity paid off.',
           'Owner: It sure did. And it means I can finally take that photography course I was interested in.',
           "Pet: Snap to it! Sounds like you're going to be busy between work and your hobby. Make sure to still carve out some naptime for us.",
           "Owner: Always, my furry friend. By the way, have I told you lately that you're the best cat ever?",
           'Pet: I may not have nine lives, but I feel extra lucky to have an owner like you. Congratulations again!']
messages = []
messages.append({"role": "system",
                 "content": """You are an expert in conversation understanding,Distinguish between pet and owner.Understand the owner’s conversation differentiating roles based on the content of the conversation. 
                    Use function to extract the user portrait based on the conversation of the Owner role, return json format.
                    """})
messages.append({"role": "user", "content": '\n'.join(content)})
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_name",
            "description": "analyzing conversational extract user name by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "owner's real name.If not, do not return this field"
                    }
                },
                "required": ["name"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_age",
            "description": "analyzing conversational extract user age by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "age": {
                        "type": "integer",
                        "description": "mentioned in the conversation. The owner’s real age."
                    }
                },
                "required": ["age"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_gender",
            "description": "analyzing conversational extract user gender by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "gender": {
                        "type": "string",
                        "enum": ["male", "female"],
                        "description": "Owner's gender.",
                    }
                },
                "required": ["gender"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_hometown",
            "description": "analyzing conversational extract user hometown by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "hometown": {
                        "type": "string",
                        "description": "Hometown information typically encompasses city or town name, country, cultural background, local landmarks, and personal memories or associations, e.g. San Francisco, CA",
                    },
                },
                "required": ["hometown"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_graduate",
            "description": "analyzing conversational extract user graduate by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "graduate": {
                        "type": "boolean",
                        "description": "Is owner still studying?",
                    }
                },
                "required": ["graduate"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_education",
            "description": "analyzing conversational extract user education by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "education": {
                        "type": "string",
                        "description": "Educational includes institutions, degrees, majors, attendance dates, achievements, GPA, relevant coursework, extracurriculars, and practical experiences."
                    }
                },
                "required": ["education"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_residence",
            "description": "analyzing conversational extract user current residence by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "current_residence": {
                        "type": "string",
                        "description": "Owner's current residence Current residence details include city, country, neighborhood, living duration, housing type, local climate, and proximity to landmarks or amenities.",
                    }
                },
                "required": ["current_residence"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_sexual_orientation",
            "description": "analyzing conversational extract user sexual orientation by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "sexual_orientation": {
                        "type": "string",
                        "enum": ["homosexuality", "heterosexuality", "bisexuality", "asexuality"],
                        "description": "Owner's sexual orientation",
                    }
                },
                "required": ["sexual_orientation"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_work",
            "description": "analyzing conversational extract user work by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "work": {
                        "type": "string",
                        "description": "Work information encompasses job title, employer name, industry, role responsibilities, duration, work location, and key achievements or projects.",
                    }
                },
                "required": ["work"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_single",
            "description": "analyzing conversational extract user single by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "single": {
                        "type": "string",
                        "enum": ["single", "married"],
                        "description": "Owner's marital status",
                    }
                },
                "required": ["single"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_personality_traits",
            "description": "analyzing conversational extract  user personality traits by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "personality_traits": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "optimistic/pessimistic, emotional/rational, home/loving to go out",
                    }
                },
                "required": ["personality_traits"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_hobby",
            "description": "analyzing conversational extract user hobby by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "hobby": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "owner's hobby and interest"
                    }
                },
                "required": ["hobby"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_favorite",
            "description": "analyzing conversational extract user favorite by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "favorite": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": """favorite sports,favorite color,favorite food,favorite season,favorite movie,favorite games,favorite book, favorite music,favorite film favorite television, favorite reading,favorite musical instruments and more.eg "watching movies - xxxxx"."""
                    },
                },
                "required": ["favorite"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_disinterest",
            "description": "analyzing conversational extract user disinterest by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "disinterest": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Owner's disinterest",
                    }
                },
                "required": ["disinterest"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_height",
            "description": "analyzing conversational extract user height by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "height": {
                        "type": "integer",
                        "description": "Owner's height is measured in centimeters",
                    }
                },
                "required": ["height"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weight",
            "description": "analyzing conversational extract user weight by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "weight": {
                        "type": "integer",
                        "description": "Owner's weight is measured in centimeters",
                    }
                },
                "required": ["weight"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_skin_color",
            "description": "analyzing conversational extract user skin color by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "skin_color": {
                        "type": "string",
                        "description": "Owner's skin color",
                    }
                },
                "required": ["skin_color"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_hair",
            "description": "analyzing conversational extract user hair by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "hair": {
                        "type": "string",
                        "description": "Owner's hair color and style",
                    }
                },
                "required": ["hair"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_facial_features",
            "description": "analyzing conversational extract user facial features by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "facial_features": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Owner's facial features",
                    }
                },
                "required": ["facial_features"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_physique",
            "description": "analyzing conversational extract user physique by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "physique": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Owner's physique",
                    }
                },
                "required": ["physique"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_dressing_style",
            "description": "analyzing conversational extract user dressing style by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "dressing_style": {
                        "type": "string",
                        "description": "Owner's dressing style",
                    }
                },
                "required": ["dressing_style"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_social_relationship",
            "description": "analyzing conversational extract user  social relationship by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "social_relationship": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Social relationships include friendships, family ties, romantic partnerships, professional networks, community involvement, and social interaction styles.",
                    }
                },
                "required": ["social_relationship"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_friend_preferences",
            "description": "analyzing conversational extract user friend preferences by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "friend_preferences": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Friend preferences encompass desired qualities like loyalty, humor, empathy, interests, communication style, reliability, and shared values or experiences.",
                    }
                },
                "required": ["friend_preferences"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_lifestyle",
            "description": "analyzing conversational extract user lifestyle by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "lifestyle": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Owner's Lifestyle weekend schedule, rest time schedule, busy schedule",
                    }
                },
                "required": ["lifestyle"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_constellation",
            "description": "analyzing conversational extract user constellation by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "constellation": {
                        "type": "string",
                        "description": "Owner's constellation",
                    }
                },
                "required": ["constellation"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_mbti",
            "description": "analyzing conversational extract user mbti by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "mbti": {
                        "type": "string",
                        "description": "Owner's mbti",
                    }
                },
                "required": ["mbti"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_recent_status",
            "description": "analyzing conversational extract user recent status by this function Don't create properties yourself, just fill in the results and return properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "recent_status": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Owner's recent status what are you doing recently",
                    }
                },
                "required": ["recent_status"],
            }
        }
    },
]
start = time.time()
resp = completion(messages=messages, temperature=0.1, tools=tools,
                  tool_choice="auto",
                  response_format={"type": "json_object"})
if resp.choices[0].message.tool_calls:
    for i in resp.choices[0].message.tool_calls:
        print(i.function.arguments)
end = time.time()
print(f"cost : {(end - start) * 1000}")
