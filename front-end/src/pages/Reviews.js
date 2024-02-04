import React from 'react'
import './Reviews.css'
import AuthContext from '../context/AuthContext'
import { useContext, useEffect, useState } from 'react'
import NotRegistered from './NotRegistered';
import axiosInstance from '../api/api'
import { Link } from 'react-router-dom';
import ReviewCard from '../components/ReviewCard';

export default function Reviews() {

    const { user } = useContext(AuthContext);
    const { authTokens } = useContext(AuthContext);

    const [userOnly, setUserOnly] = useState(false);
    const [reviews, setReviews] = useState([]);

    useEffect(() => {
        const fetchReviews = async () => {
        setReviews([])
          try {
            let endpoint = '/reviews';
            if (userOnly) {
              endpoint = `/myreviews/${user.user_id}`;
            }
    
            const response = await axiosInstance.get(endpoint, {
              headers: {
                'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`,
              },
            });
    
            if (response.status === 200) {
              setReviews(response?.data);
              console.log(reviews);
            }
          } catch (error) {
            console.error('Error fetching reviews:', error);
          }
        };
    
        fetchReviews();
      }, [user?.user_id, authTokens, userOnly]);

    return (
        <div className='theme'>
            <nav className='reviews-navbar'>
                <Link to={'/reviews/'} onClick={ () =>  setUserOnly(false) }> All Reviews </Link>
                <Link to={'/reviews/'} onClick={ () => setUserOnly(true)}> My Reviews </Link>
                <Link to={'/makereview/'}> Make Review </Link>
            </nav>
            <div>
            {reviews && reviews.map((review) => {
            return <ReviewCard
            key={review.id} 
            user_id={review.user_id} 
            title_id={review.title_id} 
            stars={review.stars} 
            likes={review.likes}
            dislikes = {review.dislikes}
            text = {review.text}
            date = {review.date}/>
        })}
            </div>
        </div>
    )
}