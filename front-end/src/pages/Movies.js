import React, { useState } from 'react'
import './Movies.css'
import MovieCard from '../components/MovieCard'
import MandalorianImage from '../assets/images/mandalorian.jpg'
import TopGunImage from '../assets/images/topgun.jpg'
import InterstellarImage from '../assets/images/interstellar.jpg'
import BatmanImage from '../assets/images/poster-2.jpg'
import OppenheimerImage from '../assets/images/oppenheimer.jpg'

export default function Movies() {

    const [genre, setGenre] = useState("");

    async function handleChange(e) {
        setGenre(e.target.value)
    }
  return (
    <div className='page-container'>
        <hr/>
        <div className='movies-container'>
                    <MovieCard MovieImage={MandalorianImage}/>
                    <MovieCard MovieImage={TopGunImage}/>
                    <MovieCard MovieImage={InterstellarImage}/>
                    <MovieCard MovieImage={BatmanImage}/>
                    <MovieCard MovieImage={OppenheimerImage}/>
                    <MovieCard MovieImage={BatmanImage}/>
                    <MovieCard MovieImage={OppenheimerImage}/>
                    <MovieCard MovieImage={BatmanImage}/>
                    <MovieCard MovieImage={InterstellarImage}/>
                    <MovieCard MovieImage={MandalorianImage}/>

                    <MovieCard MovieImage={MandalorianImage}/>
                    <MovieCard MovieImage={TopGunImage}/>
                    <MovieCard MovieImage={InterstellarImage}/>
                    <MovieCard MovieImage={BatmanImage}/>
                    <MovieCard MovieImage={OppenheimerImage}/>
                    <MovieCard MovieImage={BatmanImage}/>
                    <MovieCard MovieImage={OppenheimerImage}/>
                    <MovieCard MovieImage={BatmanImage}/>
                    <MovieCard MovieImage={InterstellarImage}/>
                    <MovieCard MovieImage={MandalorianImage}/>


                    <MovieCard MovieImage={MandalorianImage}/>
                    <MovieCard MovieImage={TopGunImage}/>
                    <MovieCard MovieImage={InterstellarImage}/>
                    <MovieCard MovieImage={BatmanImage}/>
                    <MovieCard MovieImage={OppenheimerImage}/>
                    <MovieCard MovieImage={BatmanImage}/>
                    <MovieCard MovieImage={OppenheimerImage}/>
                    <MovieCard MovieImage={BatmanImage}/>
                    <MovieCard MovieImage={InterstellarImage}/>
                    <MovieCard MovieImage={MandalorianImage}/>
        </div>
    </div>
  )
}
