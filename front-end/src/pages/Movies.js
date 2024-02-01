import React, { useEffect, useState } from 'react'
import './Movies.css'
import MovieCard from '../components/MovieCard'
import MandalorianImage from '../assets/images/mandalorian.jpg'
import TopGunImage from '../assets/images/topgun.jpg'
import InterstellarImage from '../assets/images/interstellar.jpg'
import BatmanImage from '../assets/images/poster-2.jpg'
import OppenheimerImage from '../assets/images/oppenheimer.jpg'
import Preloader from '../components/Preloader'
import axiosInstance from '../api/api'

export default function Movies() {

    const [genre, setGenre] = useState("");
    const [titles, setTitles] = useState(null);
    const [loading, setLoading] = useState(true);
    const [page, setPage] = useState(1);

    async function loadTitles() {
        const response = await axiosInstance.get(`/get-movies?page=${page}&genre=${genre}`);

        setTitles(response?.data);
        setLoading(false);
    }

    useEffect( () => {
        loadTitles();
    }, [])


  if (loading) return <Preloader />


  return (
    <div className='page-container'>
        <hr/>
        <div className='movies-container'>
 
            {titles && titles.map((title) => {
              return <MovieCard 
                key={title.titleID} 
                movieID={title.titleID} 
                movieTitle={title.original_title} 
                averageRating={title.rating.avRating} 
                imageUrl={title?.titlePoster}/>
            })}

        </div>
    </div>
  )
}
