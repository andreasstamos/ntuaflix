import React, { useEffect, useState } from 'react'
import MovieCard from '../components/MovieCard'
import Hero from '../components/Hero'
import MandalorianImage from '../assets/images/mandalorian.jpg'
import TopGunImage from '../assets/images/topgun.jpg'
import InterstellarImage from '../assets/images/interstellar.jpg'
import BatmanImage from '../assets/images/poster-2.jpg'
import OppenheimerImage from '../assets/images/oppenheimer.jpg'
import './Index.css'
import axiosInstance from '../api/api'
import Preloader from '../components/Preloader'

export default function Index() {


    const [loading, setLoading] = useState(true);
    const [data, setData] = useState(null);

    async function fetchMovieData() {
      const response = await axiosInstance.get('/index-movies');
      

      setData(response?.data);
      console.log(response?.data)
      setLoading(false);

      for(let i =0; i < response?.data.length; ++i) {
        setTimeout(() => initiateHorizontalScroll(response?.data[i].genre), 2000);
      }
    }

    useEffect( () => {
      fetchMovieData();
    }, [])

    // useEffect( () => {

    // const cardContainer = document.getElementById('cardContainer');
    // const cards = cardContainer.querySelectorAll('.card');
    // const cardWidth = cards[0].offsetWidth; // Width of a card plus margin

    // let scrollPosition = 0;



    // function scrollCards() {

    //   scrollPosition += 0.5;
    //   cardContainer.scrollLeft = scrollPosition;

    //   if (scrollPosition >= cardWidth * cards.length - cardContainer.offsetWidth + 100) {
    //     scrollPosition = 0;
    //   }


    //   requestAnimationFrame(scrollCards);
    // }

    // // Start scrolling on page load
    //   scrollCards();

    // }, [])


    function initiateHorizontalScroll(genre) {
      try {
      const cardContainer = document.getElementById(`${genre}-container`);
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
    } catch(error)  {
      console.log(error);
    }
    
    }
    
  if(loading) return <Preloader />
  return (
    <>
        <Hero />
        {/* <div>
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
            </div>
        </div> */}
        {data && data.map((genre) => {
           return <div>
           <div className='section-title-container section-index'>
               <h2 className='h2 title-with-line'>{genre.genre}</h2>
               <a href="#" className='view-more-link'>View More</a>
           </div>
           <div className='cards-container' id={`${genre.genre}-container`}>
               {genre.movies.map((movie) => {
                return <MovieCard key={movie.tconst} movieID={movie.tconst} movieTitle={movie.primary_title} 
                averageRating={movie.average_rating} 
                imageUrl={movie.image_url || "https://img.freepik.com/premium-vector/default-image-icon-vector-missing-picture-page-website-design-mobile-app-no-photo-available_87543-11093.jpg?w=2000"} />
               })}
           </div>
       </div>
        })}
    </>
  )
}
