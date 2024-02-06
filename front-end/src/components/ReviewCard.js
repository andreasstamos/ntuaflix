import React from 'react'
import './ReviewCard.css'
import { Link } from 'react-router-dom'
import StarBorderIcon from '@mui/icons-material/StarBorder';
import StarIcon from '@mui/icons-material/Star';
import { AiFillLike, AiFillDislike } from "react-icons/ai";
import axiosInstance from '../api/api';
import AuthContext from '../context/AuthContext'
import { useContext, useEffect, useState } from 'react'


export default function ReviewCard({id, username, title, stars, text, likes, dislikes, date, fetchReviews}) {

    const { user } = useContext(AuthContext);
    const { authTokens } = useContext(AuthContext);

    const starIcons = [];
    for (let i = 0; i < 5; ++i) {
        if (i < stars) {
            starIcons.push(<StarIcon key={i} />);
        } else {
            starIcons.push(<StarBorderIcon key={i} />);
        }
    }

    // const [updatedLikes, setUpdatedLikes] = useState(likes);
    // const [updatedDislikes, setUpdatedDislikes] = useState(dislikes);


    const handleReaction = async(type) => {
        try {
            const response = await axiosInstance.post(`/reviews/${id}/${user.user_id}?like=${type}` ,null,{
                headers: {
                  'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`,
                },
              });
              if (response.status===200){
                // console.log("successfully reacted");
                fetchReviews();
                // if (type) {
                    // setUpdatedLikes(prevLikes => prevLikes + 1);
                    // setUpdatedDislikes(prevDislikes => prevDislikes - 1);
                // } else {
                    // setUpdatedDislikes(prevDislikes => prevDislikes + 1);
                    // setUpdatedLikes(prevLikes => prevLikes - 1);
                // }
            }
        }
        catch(error){
            console.log(error);
        } 
    }


    return (
        <div className='review-card'>
        <div className='user-info'>
            <div className='user-avatar'/>
            <span className='user-name'>{username}</span>
            <span className="date">{date}</span>
        </div>
        <span className='movie-title'>{title}</span>
        <div className="review-stars">
                {starIcons.map((icon, index) => (
                    <span key={index}>{icon}</span>
                ))}
            </div>
        <p className="review-text">
            "{text}"
        </p>
        <div className="review-actions">
            {/* <span>Likes:{updatedLikes}  </span> */}
            <span>Likes:{likes}  </span>
            <button className="like-button"onClick={()=>handleReaction(true)}><AiFillLike /></button>
            {/* <span>Dislikes:{updatedDislikes}  </span> */}
            <span>Dislikes:{dislikes}  </span>
            <button className="dislike-button"onClick={()=>handleReaction(false)}><AiFillDislike /></button>
        </div>
    </div>
    )
}