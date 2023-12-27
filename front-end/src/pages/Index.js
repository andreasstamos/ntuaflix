import React from 'react'
import MovieCard from '../components/MovieCard'
import Hero from '../components/Hero'
import MandalorianImage from '../assets/images/mandalorian.jpg'
import TopGunImage from '../assets/images/topgun.jpg'
import InterstellarImage from '../assets/images/interstellar.jpg'
import BatmanImage from '../assets/images/poster-2.jpg'
import OppenheimerImage from '../assets/images/oppenheimer.jpg'
import './Index.css'

export default function Index() {
  return (
    <>
        <Hero />
        <div className='section-index'>
            <div className='section-title-container'>
                <h2 className='h2 title-with-line'>Upcoming Movies</h2>
                <a href="#" className='view-more-link'>View More</a>
            </div>
            <div className='cards-container'>
                <MovieCard MovieImage={MandalorianImage}/>
                <MovieCard MovieImage={TopGunImage}/>
                <MovieCard MovieImage={InterstellarImage}/>
                <MovieCard MovieImage={BatmanImage}/>
                <MovieCard MovieImage={OppenheimerImage}/>
            </div>
        </div>

        <div className='section-index'>
            <div className='section-title-container'>
                <h2 className='h2 title-with-line'>Upcoming Movies</h2>
                <a href="#" className='view-more-link'>View More</a>
            </div>
            <div className='cards-container'>
                <MovieCard MovieImage={MandalorianImage}/>
                <MovieCard MovieImage={TopGunImage}/>
                <MovieCard MovieImage={InterstellarImage}/>
                <MovieCard MovieImage={BatmanImage}/>
                <MovieCard MovieImage={OppenheimerImage}/>
            </div>
        </div>


        <div className='section-index'>
            <div className='section-title-container'>
                <h2 className='h2 title-with-line'>Upcoming Movies</h2>
                <a href="#" className='view-more-link'>View More</a>
            </div>
            <div className='cards-container'>
                <MovieCard MovieImage={MandalorianImage}/>
                <MovieCard MovieImage={TopGunImage}/>
                <MovieCard MovieImage={InterstellarImage}/>
                <MovieCard MovieImage={BatmanImage}/>
                <MovieCard MovieImage={OppenheimerImage}/>
            </div>
        </div>
    </>
  )
}
