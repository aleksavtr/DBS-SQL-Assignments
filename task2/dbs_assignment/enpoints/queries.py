def first(user_id: int) -> str:
    return f"""
    SELECT
    p.id AS id_p,
    p.title AS title_p,
    p.creationdate AS created_at_p,
    b.id AS id_b,
    b.name AS title_b,
    b.date AS created_at
FROM
    users u
JOIN
    posts p ON u.id = p.owneruserid
JOIN
    badges b ON u.id = b.userid
WHERE
    p.creationdate < b.date
    AND u.id = {user_id}
    AND p.creationdate = (
        SELECT MAX(p2.creationdate)
        FROM posts p2
        WHERE p2.owneruserid = u.id AND p2.creationdate < b.date
    )
    AND b.date = (
        SELECT MIN(b2.date)
        FROM badges b2
        WHERE b2.userid = u.id AND b2.date > p.creationdate
    )
    AND b.id = (
        SELECT b3.id
        FROM badges b3
        WHERE b3.userid = u.id AND b3.date = (
            SELECT MIN(b4.date)
            FROM badges b4
            WHERE b4.userid = u.id AND b4.date > p.creationdate
        )
        ORDER BY b3.id ASC
        LIMIT 1
    )
ORDER BY
    p.creationdate ASC, b.date ASC;
    """


def second(tag: str, count: int):
    query = """
SELECT
  sub.postid,
  sub.title,
  sub.displayname,
  sub.text,
  sub.post_creationdate,
  sub.comment_creationdate,
  sub.diff,
  SUM(sub.diff) OVER (PARTITION BY sub.postid ORDER BY sub.comment_creationdate) / NULLIF(COUNT(sub.text) OVER (PARTITION BY sub.postid ORDER BY sub.comment_creationdate), 0) AS avg_diff
FROM (
  SELECT
    post_w_tag.title,
    comments.text,
    post_w_tag.creationdate AS post_creationdate,
    comments.creationdate AS comment_creationdate,
    user_c.displayname,
    comments.postid,
    comments.creationdate - COALESCE(LAG(comments.creationdate) OVER (PARTITION BY comments.postid ORDER BY comments.creationdate), post_w_tag.creationdate) AS diff
  FROM comments
  JOIN (
    SELECT p.id, p.title, u.displayname, p.creationdate
    FROM posts p
    JOIN users u ON u.id = p.owneruserid
    JOIN post_tags pt ON p.id = pt.post_id
    JOIN tags t ON t.id = pt.tag_id
    WHERE t.tagname = :tag
      AND p.id IN (
        SELECT c.postid
        FROM comments c
        GROUP BY c.postid
        HAVING COUNT(c.id) > :count
      )
  ) AS post_w_tag ON comments.postid = post_w_tag.id
  LEFT JOIN users user_c ON comments.userid = user_c.id
) AS sub
ORDER BY sub.postid, sub.comment_creationdate;

    """
    return query, {"tag": tag, "count": count}


def third(tagname: str, position: int, limit: int):
    query = """
        SELECT c.id,u.displayname,p.body,c.text, c.score
        FROM comments c
        JOIN public.posts p ON c.postid = p.id
        JOIN public.post_tags pt ON p.id = pt.post_id
        JOIN public.tags t ON t.id = pt.tag_id
        JOIN public.users u ON u.id = c.userid
        WHERE t.tagname = :tagname
        AND (
            SELECT COUNT(*)
            FROM comments c2
            WHERE c2.postid = p.id AND c2.creationdate <= c.creationdate
        ) = :position
        GROUP BY p.id, p.creationdate, c.creationdate, c.text, c.id, u.displayname, c.score
        ORDER BY p.creationdate, c.creationdate
        LIMIT :limit;
        """
    return query, {"tagname": tagname, "position": position, "limit": limit}


def fourth(postid: int, limit: int):
    query = """
SELECT u.displayname, p.body, p.creationdate, child.creationdate AS child_creationdate, child.body AS child_body, child.displayname AS child_displayname
FROM posts p
LEFT JOIN users u on u.id = p.owneruserid
LEFT JOIN (
    SELECT po.body, po.parentid, po.creationdate, u.displayname
    FROM posts po
    LEFT JOIN users u on u.id = po.owneruserid
    WHERE po.parentid = :postid
    ORDER BY po.creationdate ASC
    LIMIT :limit-1
) AS child ON p.id = child.parentid
WHERE p.id = :postid
LIMIT :limit;
    """
    return query, {"postid": postid, "limit": limit}
