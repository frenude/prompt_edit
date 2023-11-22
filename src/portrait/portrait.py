import json
import os
import time

from src.client import completion

from typing import List, Literal

from pydantic import BaseModel
from pydantic import Field

from src.client.base_model import BaseSchemaModel


class OwnerPortrait(BaseSchemaModel):
    """analyzing conversational extract user portraits by this function Don't create properties yourself, just fill in the results and return properties,not return null values.Don't create age."""
    name: str = Field(description="owner's real name.If not, Do not return this field")
    age: int = Field(
        description="owner's age.If not, Do not return this field")
    gender: Literal["female", "male"] = Field(description="Owner's gender not pet.")
    hometown: str = Field(
        description="Hometown information typically encompasses city or town name, country, cultural background, local landmarks, and personal memories or associations, e.g. San Francisco, CA")
    education: str = Field(
        description="Educational includes institutions, degrees, majors, attendance dates, achievements, GPA, relevant coursework, extracurriculars, and practical experiences.")
    current_residence: str = Field(
        description="Owner's live address.mentioned in the conversation. If not, do not return this field")
    sexual_orientation: Literal["homosexuality", "heterosexuality", "bisexuality", "asexuality"] = Field(
        description="Owner's sexual orientation")
    work: List[str] = Field(
        description="Work information encompasses job title, employer name, industry, role responsibilities, duration, work location, and key achievements or projects.")
    single: Literal["single", "married","have boy friend","have girl friend"] = Field(description="Owner's marital status")
    personality_traits: List[str] = Field(
        description="optimistic/pessimistic, emotional/rational, home/loving to go out")
    hobby: List[str] = Field(description="owner's hobby and interest")
    favorite: List[str] = Field(
        description="favorite sports,favorite color,favorite food,favorite season,favorite movie,favorite games,favorite book, favorite music,favorite film favorite television, favorite reading,favorite musical instruments and more.eg 'watching movies - xxxxx'")
    disinterest: List[str] = Field(description="Owner's disinterest")
    height: str = Field(description="Owner's height")
    weight: str = Field(description="Owner's weight")
    skin_color: str = Field(description="Owner's skin color")
    hair: str = Field(description="Owner's hair color and style")
    facial_features: List[str] = Field(description="Owner's facial features")
    physique: List[str] = Field(description="Owner's physique")
    dressing_style: str = Field(description="Owner's dressing style")
    social_relationships: List[str] = Field(
        description="Social relationships include friendships, family ties, romantic partnerships, professional networks, community involvement, and social interaction styles.")
    friend_preferences: List[str] = Field(
        description="Friend preferences encompass desired qualities like loyalty, humor, empathy, interests, communication style, reliability, and shared values or experiences.")
    lifestyle: List[str] = Field(
        description="Lifestyle includes daily routines, sleeping habits, eating habits, exercise habits, hobbies, and recreational activities.")
    constellation: str = Field(description="Owner's constellation")
    mbti: str = Field(description="Owner's mbti")
    recent_status: List[str] = Field(
        description="Owner's recent status what are you doing recently.summarize it in a few words")


# class Summarize(BaseSchemaModel):
#     """区分用户和宠物讲话的内容。理解上下文，只总结用户个人信息相关的内容。"""
#     owner: str = Field(description="Summarize what Owner basic information")


def get_summarize(content: List[str]):
    messages = []
    messages.append({"role": "system",
                     "content": """You are a summary generation expert.You can know what users and pets are specifically saying, and you can extract user information summaries based on context,only.Summary based on facts the gpt’s super simple and understandable vocabulary description.Understand summary age"""})
    messages.append({"role": "user", "content": '\n'.join(content)})
    # tools = [Summarize.schema()]

    resp = completion(messages=messages, temperature=0, )
    if resp.choices[0].message:
        print(resp.choices[0].message.content)
        return resp.choices[0].message.content


def get_user(content):
    messages = []
    messages.append({"role": "system",
                     "content": """You are an expert in conversation understanding,Distinguish between pet and owner.Understand the owner’s conversation differentiating roles based on the content of the conversation. 
                     Avoid guessing or creating content and strictly adhere to the information provided in the conversation to extract get_user_portrait to extract the user portrait.Don't create age.
                     return json format.
                     """})
    messages.append({"role": "user", "content": content})
    tools = [OwnerPortrait.schema()]

    resp = completion(messages=messages, temperature=0.2, tools=tools,
                      tool_choice="auto",
                      )
    if resp.choices[0].message.tool_calls:
        return resp.choices[0].message.tool_calls[0].function.arguments


if __name__ == '__main__':
    from src.utils.timer import TimeReport

    with TimeReport():
        content = [
            "Pet: I love my bow, thank you",
            "Owner: OK, I think you should be a girl with short hair"

        ]
        e = get_summarize(content)
        r = get_user(e)
        print(r)
