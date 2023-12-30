import React, { useEffect } from 'react'
import MovieCard from '../components/MovieCard'
import Hero from '../components/Hero'
import MandalorianImage from '../assets/images/mandalorian.jpg'
import TopGunImage from '../assets/images/topgun.jpg'
import InterstellarImage from '../assets/images/interstellar.jpg'
import BatmanImage from '../assets/images/poster-2.jpg'
import OppenheimerImage from '../assets/images/oppenheimer.jpg'
import './Index.css'

export default function Index() {

    useEffect( () => {

    const cardContainer = document.getElementById('cardContainer');
    const cards = cardContainer.querySelectorAll('.card');
    const cardWidth = cards[0].offsetWidth; // Width of a card plus margin

    let scrollPosition = 0;



    function scrollCards() {

      scrollPosition += 0.5;
      cardContainer.scrollLeft = scrollPosition;

      if (scrollPosition >= cardWidth * cards.length - cardContainer.offsetWidth + 100) {
        scrollPosition = 0;
      }


      requestAnimationFrame(scrollCards);
    }

    // Start scrolling on page load
      scrollCards();

    }, [])

    

  return (
    <>
        <Hero />
        <div className=''>
            <div className='section-title-container section-index'>
                <h2 className='h2 title-with-line'>Upcoming Movies</h2>
                <a href="#" className='view-more-link'>View More</a>
            </div>
            <div className='cards-container' id='cardContainer'>
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
                {/* <MovieCard MovieImage={TopGunImage}/>
                <MovieCard MovieImage={InterstellarImage}/>
                <MovieCard MovieImage={BatmanImage}/>
                <MovieCard MovieImage={OppenheimerImage}/>
                <MovieCard MovieImage={BatmanImage}/>
                <MovieCard MovieImage={OppenheimerImage}/>
                <MovieCard MovieImage={InterstellarImage}/> */}

            </div>
        </div>

        <div className=''>
            <div className='section-title-container section-index'>
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
