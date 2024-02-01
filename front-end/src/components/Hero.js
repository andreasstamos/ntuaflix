import React from 'react'
import './Hero.css'

export default function Hero() {


    function handleScroll() {
        window.scrollTo({
            top:  window.innerHeight + 65,
            behavior: 'smooth', // Optional: Adds smooth scrolling animation
          });
    }

  return (
    <section class="hero hero-gradient">
        <div class="container">

            <div class="hero-content">

                <p class="hero-subtitle">Ntua<mark>Flix</mark></p>

                <h1 class="h1 hero-title">
                    Unlimited <strong>Movies</strong>, <br/> TVs Shows, & More.
                </h1>

                {/* <div class="meta-wrapper">

                <div class="badge-wrapper">
                    <div class="badge badge-fill">PG 18</div>

                    <div class="badge badge-outline">HD</div>
                </div>

                <div class="ganre-wrapper">
                    <a href="#">Romance,</a>

                    <a href="#">Drama</a>
                </div>

                <div class="date-time">

                    <div>
                    <ion-icon name="calendar-outline"></ion-icon>

                    <time datetime="2022">2022</time>
                    </div>

                    <div>
                    <ion-icon name="time-outline"></ion-icon>

                    <time datetime="PT128M">128 min</time>
                    </div>
                </div>
                </div> */}

                <button class="btn btn-primary" onClick={handleScroll}>
                    <span>EXPLORE</span>
                </button>

            </div>

        </div>
    </section>
  )
}
