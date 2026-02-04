from fastapi import APIRouter, Depends , status, HTTPException
from ..db.database import get_db
from sqlalchemy.orm import Session 
from ..models.vote_model import Vote
from ..schema.vote_schema import VoteRequest
from ..utils.auth import get_current_user
from ..models.user_model import User
from ..models import post_model
from typing import List , Optional, Literal
from sqlalchemy import func

from typing import Literal

def vote_to_post(
    post_id: int,
    vote_type: Literal[1, -1],
    db: Session,
    current_user: User
):
    user_id = current_user.id

    post = db.query(post_model.Post).filter(post_model.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} does not exist"
        )

    vote_query = db.query(Vote).filter(
        Vote.post_id == post_id,
        Vote.user_id == user_id
    )

    curr_vote = vote_query.first()

    if curr_vote:
        vote_query.update(
            {"vote": vote_type},
            synchronize_session=False
        )
    else:
        new_vote = Vote(
            post_id=post_id,
            user_id=user_id,
            vote=vote_type
        )
        db.add(new_vote)

    db.commit()
    return {"status": "success"}

router = APIRouter(prefix="/vote")

@router.post("/upvote/{post_id}")
def upvote_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return vote_to_post(post_id, 1, db, current_user)


@router.post("/downvote/{post_id}")
def downvote_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return vote_to_post(post_id, -1, db, current_user)


@router.delete("/remove/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_vote(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = (
        db.query(Vote)
        .filter(
            Vote.post_id == post_id,
            Vote.user_id == current_user.id
        )
        .delete(synchronize_session=False)
    )

    if deleted == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vote does not exist"
        )

    db.commit()
