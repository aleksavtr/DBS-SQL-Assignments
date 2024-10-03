from fastapi import APIRouter, HTTPException
from .queries import *
from dbs_assignment.database import database
from .schemas.Root import Root, Item
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


@router.get("/v1/status")
async def get_status():
    query = SELECT_VERSION
    result = await database.fetch_one(query)
    version_info = result[0]
    return {"version": version_info}


@router.get("/v2/posts/{post_id}/users", response_model=Root)
async def get_post_users(post_id: int):
    query = GET_POST_USERS_QUERY(post_id)
    result = await database.fetch_all(query)
    if not result:
        raise HTTPException(status_code=404, detail=f"Post with ID {post_id} not found")

    modified_users = []
    for user in result:
        user_dict = dict(user)

        if 'creationdate' in user_dict and user_dict['creationdate']:
            user_dict['creationdate'] = to_utc_isoformat(user_dict['creationdate'])

        if 'lastaccessdate' in user_dict and user_dict['lastaccessdate']:
            user_dict['lastaccessdate'] = to_utc_isoformat(user_dict['lastaccessdate'])
        modified_users.append(user_dict)

    items = [Item(**user) for user in modified_users]
    return Root(items=items)


@router.get("/v2/users/{user_id}/friends")
async def get_status(user_id: int):
    query = GET_USERS(user_id)
    result = await database.fetch_all(query)
    if not result:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    modified_users = []
    for user in result:
        user_dict = dict(user)
        if 'creationdate' in user_dict and user_dict['creationdate']:
            user_dict['creationdate'] = to_utc_isoformat2(user_dict['creationdate'])
        if 'lastaccessdate' in user_dict and user_dict['lastaccessdate']:
            user_dict['lastaccessdate'] = to_utc_isoformat2(user_dict['lastaccessdate'])
        modified_users.append(user_dict)

    json_result = {"items": modified_users}
    return json_result


@router.get("/v2/tags/{tagname}/stats")
async def get_status(tagname: str):
    query = GET_TAGS(tagname)
    result = await database.fetch_all(query)
    if not result:
        raise HTTPException(status_code=404, detail=f"Tag {tagname} not found")
    stats_result = {}

    for item in result:
        day = item['day_of_week'].lower()
        percentage = item['percentage']
        stats_result[day] = percentage
    json_result = {"result": stats_result}

    return json_result


# 4 endpoint
# @router.get("/v2/posts/")
# async def get_status(duration: int, limit: int):
#     query = Duration(duration, limit)
#     result = await database.fetch_all(query)
#     if not result:
#         raise HTTPException(status_code=404, detail=f"Not found")
#     modified = []
#     for user in result:
#         posts_dict = dict(user)  # Convert Record to dictionary
#         # Format 'creationdate' if present
#         if 'creationdate' in posts_dict and posts_dict['creationdate']:
#             posts_dict['creationdate'] = to_utc_isoformat(posts_dict['creationdate'])
#         # Format 'lastaccessdate' if present
#         if 'lastactivitydate' in posts_dict and posts_dict['lastactivitydate']:
#             posts_dict['lastactivitydate'] = to_utc_isoformat(posts_dict['lastactivitydate'])
#         modified.append(posts_dict)
#
#     json_result = {"items": modified}
#
#     return json_result
#
#
# @router.get("/v2/posts")
# async def get_status(limit: int, query: str):
#     query = search_q(limit, query)
#     result = await database.fetch_all(query)
#     if not result:
#         raise HTTPException(status_code=404, detail=f"Not found")
#     json_result = {"items": result}
#
#     return json_result

@router.get("/v2/posts")
async def get_posts(limit: int, query: Optional[str] = None, duration: Optional[int] = None):
    json_result = []
    if query is not None:
        sql_query = search_q(limit, query)
    elif duration is not None:
        sql_query = Duration(duration, limit)
    else:
        raise HTTPException(status_code=400, detail="Must provide either query or duration")

    result = await database.fetch_all(sql_query)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")

    if query is not None:
        posts = {}
        for row in result:
            post_id = row['id']
            if post_id not in posts:
                posts[post_id] = {
                    "id": row['id'],
                    "creationdate": to_utc_isoformat2(row['creationdate']),
                    "viewcount": row['viewcount'],
                    "lasteditdate": to_utc_isoformat2(row['lasteditdate']) if row['lasteditdate'] else None,
                    "lastactivitydate": to_utc_isoformat2(row['lastactivitydate']),
                    "title": row['title'],
                    "body": row['body'],
                    "answercount": row['answercount'],
                    "closeddate": to_utc_isoformat2(row['closeddate']) if row['closeddate'] else None,
                    "tags": row['tag_array']
                }

        json_result = {"items": list(posts.values())}
    elif duration is not None:
        modified = []
        for post in result:
            posts_dict = dict(post)
            if 'closeddate' in posts_dict and posts_dict['closeddate']:
                posts_dict['closeddate'] = to_utc_isoformat2(posts_dict['closeddate'])
            if 'creationdate' in posts_dict and posts_dict['creationdate']:
                posts_dict['creationdate'] = to_utc_isoformat2(posts_dict['creationdate'])
            if 'lastactivitydate' in posts_dict and posts_dict['lastactivitydate']:
                posts_dict['lastactivitydate'] = to_utc_isoformat2(posts_dict['lastactivitydate'])
            if 'lasteditdate' in posts_dict and posts_dict['lasteditdate']:
                posts_dict['lasteditdate'] = to_utc_isoformat2(posts_dict['lasteditdate'])
            modified.append(posts_dict)
        json_result = {"items": modified}

    return json_result
