import React from 'react'
import './ReviewCard.css'
import { Link } from 'react-router-dom'
import StarBorderIcon from '@mui/icons-material/StarBorder';

export default function ReviewCard({user_id, title_id, stars, text, likes, dislikes, date}) {

    return (
        <div className='review-card'>
        <div className='user-info'>
            <div className='user-avatar'/>
            <span className='user-name'>{user_id}</span>
            <span className="date">{date}</span>
        </div>
        <span className='movie-title'>{title_id}</span>
        <p className="review-text">
            "{text}"
        </p>
        <div className="review-actions">
            <span>Likes:{likes}</span>
            <button className="like-button">Like</button>
            <span>Dislikes:{dislikes}</span>
            <button className="dislike-button">Dislike</button>
        </div>
    </div>
    )
}