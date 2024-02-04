import React, { useEffect, useState } from 'react'
import axiosInstance from '../api/api';
import Loader from '../components/Loader';
import MovieCard from '../components/MovieCard';
import AuthContext from '../context/AuthContext'
import { useContext } from 'react'
import './Recommender.css'

export default function Recommender() {
    const {authTokens} = useContext(AuthContext);

    const [movieData, setMovieData] = useState(null);
    const [loading, setLoading] = useState(true);


    async function recommendMovie() {
        setLoading(true);
        const response = await axiosInstance.get('/recommend-movie', {headers: {
            'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`
        }});
        console.log(response?.data);
        setMovieData(response?.data);
        setLoading(false);
    }

    useEffect(() => {
        recommendMovie();
    }, [])

   
  return (
    <div className='movie-page-container recommender-bg'>
        <div className='movie-container'>
            <div className='recommend-container'>
                <h1 className='title-with-line'>Get a Recommendation</h1>
                {loading && <div className='loading-wrapper'><Loader/></div>}
                {!loading && movieData && <div className='rec-movie-wrapper'>
                    <MovieCard movieTitle={movieData?.original_title}  averageRating={movieData?.rating?.avRating} movieID={movieData?.titleID} imageUrl={movieData?.titlePoster || "https://img.freepik.com/premium-vector/default-image-icon-vector-missing-picture-page-website-design-mobile-app-no-photo-available_87543-11093.jpg?w=2000"}/>
                    <button class="btn btn-primary" onClick={recommendMovie}><span>Recommend Again</span></button>
                    </div>
                }
                
            </div>
        </div>
    </div>
  )
}
