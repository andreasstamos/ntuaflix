import React, { useEffect, useState } from 'react'
import './Recommender.css'
import axiosInstance from '../api/api';
import Loader from '../components/Loader';
import MovieCard from '../components/MovieCard';
import { Link, useParams } from 'react-router-dom';

export default function Recommender() {

    const [movieData, setMovieData] = useState(null);
    const [loading, setLoading] = useState(true);


    async function recommendMovie() {
        setLoading(true);
        const response = await axiosInstance.get('/recommend-movie');
        console.log(response?.data);
        setMovieData(response?.data);
        setLoading(false);
    }

    useEffect(() => {
        recommendMovie();
    }, [])

   
  return (
    <div className='movie-page-container' style={{background: `linear-gradient(to right, rgba(0, 0, 0, 0.52), rgba(0, 0, 0, 0.52)), url(https://i.redd.it/ugg6a3ka5qi91.jpg)`}}>
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
