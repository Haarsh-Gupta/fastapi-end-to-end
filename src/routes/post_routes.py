from fastapi import APIRouter, Depends , status, HTTPException
from ..db.database import engine , get_db
from sqlalchemy.orm import Session 
from ..models import post_model
from ..schema.post_schema import Post , PostBase , PostUpdate
from ..utils.auth import get_current_user
from ..models.user_model import User

router = APIRouter(prefix="/post")

@router.get("/")
def get_all(db : Session = Depends(get_db)):
    # cursor.execute('Select * from "Posts"')
    # posts = cursor.fetchall()
    # print(posts)

    posts = db.query(post_model.Post).all()
    return {"data" : posts} 

@router.post("/")
def create_post(post : PostBase , db : Session = Depends(get_db) , current_user : User = Depends(get_current_user)):
    # # pron of sql injection
    # cursor.execute(f"insert into posts (title , content , published) values({post.title} , {post.content} , {post.published})")

    # cursor.execute('Insert into "Posts" (title , content , published) Values (%s, %s, %s) returning *' , (post.title , post.content , post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    user = current_user

    user_post = post.model_dump()
    new_post = post_model.Post(owner_id = user.id , **user_post)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}

@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int , current_user : User = Depends(get_current_user) , db : Session = Depends(get_db)):
    # cursor.execute('delete from "Posts" where id = %s returning * '  ,(str(id)))

    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(post_model.Post).filter(post_model.Post.id == id)


    if post_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} doesn't exist"
        )

    post_query.delete(synchronize_session=False)
    db.commit()


@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: PostUpdate , db : Session = Depends(get_db) , current_user : dict = Depends(get_current_user)):
    # cursor.execute(
    #     'UPDATE "Posts" '
    #     'SET title = %s, content = %s, published = %s '
    #     'WHERE id = %s RETURNING *',
    #     (post.title, post.content, post.published, id)
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()


    #if no data return error
    update_data = post.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided for update"
        )

    post_query = db.query(post_model.Post).filter(post_model.Post.id == id)
    curr_post = post_query.first()

    if curr_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist"
        )
    
    post_query.update(
        post.model_dump(exclude_unset=True),
        synchronize_session=False
    )

    db.commit()
    db.refresh(curr_post)

    return curr_post