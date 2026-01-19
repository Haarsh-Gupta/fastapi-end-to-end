from fastapi import FastAPI, HTTPException , Security , status, Response
from .models.post_model import Post
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI() 


try:
    conn = psycopg2.connect(host= "localhost", database= "FastApi" ,user="postgres", password="system@2002",
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Connected to the Database")
except Exception as error :
    print("Database Connection Failed")
    print("Error => " , error)


@app.get("/")
def home():
    return {"data" : "fucked_life"}

@app.get("/posts")
def get_all():
    cursor.execute('Select * from "Posts"')
    posts = cursor.fetchall()
    print(posts)
    return {"data" : posts} 

@app.post("/posts" , status_code=status.HTTP_201_CREATED)
def create_post(post : Post):
    cursor.execute('Insert into "Posts" (title , content , published) Values (%s, %s, %s) returning *' , (post.title , post.content , post.published))


    # # pron of sql injection
    # cursor.execute(f"insert into posts (title , content , published) values({post.title} , {post.content} , {post.published})")


    new_post = cursor.fetchone()
    conn.commit()

    return {"data" : new_post}

@app.get("/posts/{id}")
def get_post(id : int):
    cursor.execute('select * from "Posts" where id = %s' , (str(id)))
    curr_post = cursor.fetchone()
    print("testing the get by id route")

    return {"data" : curr_post}


@app.delete("/posts/{id}")
def delete_post(id : int):
    cursor.execute('delete from "Posts" where id = %s returning * '  ,(str(id)))

    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with user id {id} doesn't exist")
    print(deleted_post)
    return Response(status_code= status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    cursor.execute(
        'UPDATE "Posts" '
        'SET title = %s, content = %s, published = %s '
        'WHERE id = %s RETURNING *',
        (post.title, post.content, post.published, id)
    )
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist"
        )

    return {"data": updated_post}

    