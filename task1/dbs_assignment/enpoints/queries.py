SELECT_VERSION = "SELECT version();"


def GET_POST_USERS_QUERY(post_id: int) -> str:
    return f"""
SELECT DISTINCT u.*
FROM users u
JOIN comments c ON u.id = c.userid
JOIN posts p ON c.postid = p.id
WHERE p.id = {post_id}
ORDER BY c.creationdate DESC
"""


def GET_USERS(user_id: int) -> str:
    return f"""
    WITH postsu AS (
        SELECT po.id
        FROM posts po
        WHERE po.owneruserid = {user_id}
        UNION
        SELECT c.postid
        FROM comments c
        JOIN posts po ON c.postid = po.id
        WHERE c.userid = {user_id}
    ),    
    commentsu AS (
        SELECT DISTINCT c.userid
        FROM comments c
        JOIN postsu p ON c.postid = p.id
    )
    SELECT u.*
    FROM users u
    JOIN commentsu c ON u.id = c.userid
    ORDER BY u.creationdate ASC;
    """


def GET_TAGS(tag: str):
    return f"""
WITH PostCounts AS (
    SELECT
        TRIM(to_char(post.creationdate, 'Day')) AS day_of_week,
        COUNT(DISTINCT post.id) AS total_posts
    FROM
        tags
    JOIN post_tags pt ON  tags.id = pt.tag_id
    JOIN posts post ON pt.post_id = post.id
    GROUP BY
        day_of_week
),
TaggedPostCounts AS (
    SELECT
        TRIM(to_char(p.creationdate, 'Day')) AS day_of_week,
        COUNT(DISTINCT p.id) AS tagged_posts
    FROM
        posts p
        JOIN post_tags pt ON p.id = pt.post_id
        JOIN tags t ON pt.tag_id = t.id
    WHERE
        t.tagname = '{tag}'
    GROUP BY
        day_of_week
)
SELECT
    pc.day_of_week,
    COALESCE(ROUND(((tpc.tagged_posts * 100.0) / pc.total_posts), 2), 0) AS percentage
FROM
    PostCounts pc
    LEFT JOIN TaggedPostCounts tpc ON pc.day_of_week = tpc.day_of_week
ORDER BY
    CASE pc.day_of_week
        WHEN 'Monday' THEN 1
        WHEN 'Tuesday' THEN 2
        WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4
        WHEN 'Friday' THEN 5
        WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END;
"""


def Duration(duration_m: int, limit: int):
    return f"""
    SELECT posts.id,posts.creationdate,posts.viewcount,posts.lasteditdate,posts.lastactivitydate,posts.title, 
    posts.closeddate,
     ROUND(EXTRACT(EPOCH FROM posts.closeddate - posts.creationdate) / 60, 2) AS duration
FROM posts 
WHERE closeddate IS NOT NULL AND EXTRACT(EPOCH FROM posts.closeddate - posts.creationdate) / 60 < {duration_m}
ORDER BY creationdate DESC
LIMIT {limit};
    """


def search_q(limit: int, query: str):
    return f""" 
SELECT p.id,p.creationdate,p.viewcount,p.lasteditdate,p.lastactivitydate,p.title,p.body,p.answercount,p.closeddate,
    (SELECT array_agg(t.tagname)
     FROM post_tags pt
     JOIN tags t ON pt.tag_id = t.id
     WHERE pt.post_id = p.id
     GROUP BY pt.post_id) AS tag_array
FROM posts p
WHERE unaccent(p.body) ILIKE unaccent('%{query}%') OR unaccent(p.title) ILIKE unaccent('%{query}%')
ORDER BY
    p.creationdate DESC
LIMIT
    {limit};
"""
