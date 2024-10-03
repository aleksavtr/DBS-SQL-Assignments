from fastapi import APIRouter
from .queries import *
from dbs_assignment.database import database
from datetime import datetime
from typing import Optional

router = APIRouter()


def to_utc_isoformat(dt: datetime) -> str:
    milliseconds = f"{dt.microsecond / 1000000:.2f}".split(".")[1]
    formatted_date = dt.strftime(f"%Y-%m-%dT%H:%M:%S.{milliseconds}") + "+00:00"
    return formatted_date


def to_utc_isoformat2(dt: datetime) -> str:
    milliseconds = f"{dt.microsecond / 1000000:.3f}".split(".")[1]
    formatted_date = dt.strftime(f"%Y-%m-%dT%H:%M:%S.{milliseconds}") + "+00"
    return formatted_date


@router.get("/v3/users/{user_id}/badge_history")
async def get_badges(user_id: int):
    query = first(user_id)
    result = await database.fetch_all(query)
    transformed_items = []
    position_counter = 1
    for item in result:
        created_at_p = to_utc_isoformat2(item["created_at_p"])
        created_at_b = to_utc_isoformat2(item["created_at"])
        post = {
            "id": item["id_p"],
            "title": item["title_p"],
            "type": "post",
            "created_at": created_at_p,
            "position": position_counter
        }
        transformed_items.append(post)

        badge = {
            "id": item["id_b"],
            "title": item["title_b"],
            "type": "badge",
            "created_at": created_at_b,
            "position": position_counter
        }
        transformed_items.append(badge)

        position_counter += 1

    result2 = {"items": transformed_items}
    return result2


def format_time_diff(time_diff):
    total_seconds = time_diff.total_seconds()
    days = total_seconds // (24 * 3600)
    remaining_seconds = total_seconds % (24 * 3600)
    hours = remaining_seconds // 3600
    remaining_seconds %= 3600
    minutes = remaining_seconds // 60
    remaining_seconds %= 60
    seconds = remaining_seconds
    if days == 1:
        days_str = "1 day"
    elif days == 0:
        return f"{int(hours):02d}:{int(minutes):02d}:{seconds:06.3f}"
    else:
        days_str = f"{int(days)} days"
    time_str = f"{int(hours):02d}:{int(minutes):02d}:{seconds:06.3f}"
    return f"{days_str} {time_str}"


@router.get("/v3/tags/{tag}/comments")
async def get_comm(tag: str, count: Optional[int] = None):
    query, values = second(tag, count)
    result = await database.fetch_all(query, values)
    transformed_items = []
    for item in result:
        comm = {
            "post_id": item["postid"],
            "title": item["title"],
            "displayname": item["displayname"],
            "text": item["text"],
            "post_created_at": to_utc_isoformat2(item["post_creationdate"]),
            "created_at": to_utc_isoformat2(item["comment_creationdate"]),
            "diff": format_time_diff(item["diff"]),
            "avg": format_time_diff(item["avg_diff"])
        }
        transformed_items.append(comm)
    return {"items": transformed_items}


@router.get("/v3/tags/{tagname}/comments/{position}")
async def get_comments_by_tag_position(tagname: str, position: int, limit: Optional[int] = None):
    query, values = third(tagname, position, limit)
    result = await database.fetch_all(query, values)
    transformed_items = []
    for item in result:
        post = {
            "id": item["id"],
            "displayname": item["displayname"],
            "body": item["body"],
            "text": item["text"],
            "score": item["score"],
            "position": position
        }
        transformed_items.append(post)
    return {"items": transformed_items}


@router.get("/v3/posts/{postid}")
async def get_badges(postid: int, limit: int):
    query, values = fourth(postid, limit)
    result1 = await database.fetch_all(query, values)
    transformed_items = []
    for item in result1:
        created_at_p = to_utc_isoformat2(item["creationdate"])
        post = {
            "displayname": item["displayname"],
            "body": item["body"],
            "created_at": created_at_p,
        }
        transformed_items.append(post)
        if item["child_displayname"] and item["child_body"] and item["child_creationdate"]:
            created_at_c = to_utc_isoformat2(item["child_creationdate"])
            child_post = {
                "displayname": item["child_displayname"],
                "body": item["child_body"],
                "created_at": created_at_c,
            }
            transformed_items.append(child_post)
    return {"items": transformed_items}
