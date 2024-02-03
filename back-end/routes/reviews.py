from typing import Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, Delete, Update, exc
from sqlalchemy.orm import Session
from database import get_db
from datetime import date
from pydantic import BaseModel
from utils import CSVResponse, FormatType
from fastapi.responses import JSONResponse

from models import Review, ReviewReactions, Title
from schemas import TitleObject, TqueryObject, GqueryObject
from utils import authorize_user, token_dependency

router = APIRouter()

db_dependency = Annotated[Session,Depends(get_db)]

#maybe change some rtuern values to this object later...
class ReviewObj(BaseModel):
    title: str
    user_name: str
    stars: int
    text: str
    likes: int
    dislikes: int
    uploaded: date
    
#----------> REVIEWS NAV <----------------

@router.get("/reviews")
async def view_reviews(
    db: db_dependency,
    from_user: int = Query(None, description="user_filter"),
    for_title: str = Query(None, description="title_filter"),
    format: FormatType = FormatType.json):
    db_ans = []
    if from_user:
        search_user_reviews = db.query(Review).filter(Review.user_id==from_user).all()
        if search_user_reviews: db_ans.append(search_user_reviews)
    if for_title:
        search_title_review = db.query(Review).filter(Review.title_id==for_title).all()
        if search_title_review: db_ans.append(search_title_review)
    if db_ans == []:
        if (from_user and for_title):
            raise HTTPException(status_code=400, detail=f"No reviews found by user {from_user} and title {for_title}") 
        elif (from_user and not for_title):
            raise HTTPException(status_code=400, detail=f"No reviews found by user {from_user}")  
        elif (for_title and not from_user):
            raise HTTPException(status_code=400, detail=f"No reviews found for title {for_title}")   
        else:
            raise HTTPException(status_code=400, detail=f"No reviews made yet!") 
    if format==FormatType.csv: pass
    return db_ans 

@router.get("/myreviews/{user_id}")
@authorize_user
async def view_my_reviews(
    user_id: int,
    session_id: token_dependency,
    db: db_dependency,
    format: FormatType = FormatType.json):
    my_revs = db.query(Review).filter(Review.user_id==user_id).all()
    if my_revs==[]:
        raise HTTPException(status_code=204, detail=f"You haven't made any reviews yet")
    else:
        return my_revs
    
@router.post("/myreviews/{user_id}/add")
@authorize_user
async def add_review(
    user_id: int,
    session_id: token_dependency,
    movie_title: str,
    text: str or None,
    stars: int,
    db: db_dependency):
    db_movie = db.query(Title).filter(Title.original_title==movie_title).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail=f"Title not found")
    else:
        title_id = db_movie.tconst
        try :
            db_review = Review(user_id=user_id,title_id=title_id,stars=stars,likes=0,dislikes=0,text=text)
            db.add(db_review)
            db.commit()

            return JSONResponse(content={"message": "Your Review was uploaded!"}, status_code=200)
        except exc.IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail='Unable to upload review!')
 
        
        
@router.post("/myreviews/{user_id}/remove")  
@authorize_user
async def remove_review(review_id: int, db: db_dependency, user_id: int, session_id: token_dependency):
    db_review = db.query(Review).filter(Review.review_id==review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail=f"Review {review_id} doesn't exist")
    else:
        # remove related to likes and dislikes 
        db.delete(ReviewReactions).where(ReviewReactions.review_id==review_id)
        db.delete(Review).where(review_id==review_id)
        db.commit()
        

@router.post("/reviews/{review_id}")
async def react(session_id: token_dependency, review_id: int, like: bool, db: db_dependency):
    db_review = db.query(Review).filter(Review.id==review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail=f"Review not found")
    
    db_reaction = db.query(ReviewReactions).filter(and_(ReviewReactions.review_id==review_id),ReviewReactions.user_id==session_id).first()
    #neither like nor dislike yet
    if not db_reaction:
        user_reaction = ReviewReactions(user_id=session_id,review_id=review_id,type=like)
        db.add(user_reaction)
        db.commit()
        if type: #increase likes in Reviews here
            db_review.likes+=1
        else: #decrease likes in Reviews here
            db_review.dislikes-=1
            db.commit()
             
    else: 
        if db_reaction.type == type: 
            raise HTTPException(status_code=400, detail=f"Reaction is up to date")
        else : 
            db_reaction.type=type
            db.commit()
            if type: #increase likes, decrease dislikes in Reviews here
                db_review.likes+=1
                db_review.dislikes-=1
            else: #decrease likes, increase dislikes in Reviews here
                db_review.likes-=1
                db_review.dislikes+=1
            db.commit()

