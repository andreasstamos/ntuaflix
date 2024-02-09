import React from 'react'
import './Reviews.css'
import AuthContext from '../context/AuthContext'
import { useContext, useEffect, useState } from 'react'
import axiosInstance from '../api/api'
import { Link } from 'react-router-dom';
import ReviewCard from '../components/ReviewCard';
import { useLocation } from 'react-router-dom';


export default function Reviews() {
  const { pathname } = useLocation();

    const { user } = useContext(AuthContext);
    const { authTokens } = useContext(AuthContext);

    const [userOnly, setUserOnly] = useState(false);
    const [reviews, setReviews] = useState([]);


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


    useEffect(() => {    
        fetchReviews();
      }, [user?.user_id, authTokens, userOnly]);

      useEffect(() => {
        window.scrollTo(0, 0);
      }, [pathname]);

    return (
        <div className='theme'>
            <nav className='reviews-navbar'>
                <Link to={'/reviews/'} onClick={ () => setUserOnly(false) }>All Reviews</Link>
                <Link to={'/reviews/'} onClick={ () => setUserOnly(true)}>My Reviews</Link>
                <Link to={'/makereview/'}>Make Review</Link>
            </nav>
            <div>
              {reviews && reviews.map((review) => {
              return <ReviewCard
                key={review.id}
                id = {review.id}
                username={review.username}
                title={review.title}
                stars={review.stars}
                likes={review.likes}
                dislikes = {review.dislikes}
                text = {review.text}
                date = {review.uploaded}
                fetchReviews = {fetchReviews}
              />
        })}
            </div>
        </div>
    )
}