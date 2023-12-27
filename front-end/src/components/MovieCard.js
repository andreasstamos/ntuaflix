import React from 'react'
import './MovieCard.css'


export default function MovieCard({MovieImage}) {
  return (
        <div class="card">
        <img src={MovieImage} />
        <div class="info">
            <h1>Interstellar</h1>
            <p>In the future, where Earth is becoming uninhabitable, farmer and ex-NASA pilot Cooper is asked to pilot a spacecraft
            along with a team of researchers to find a new planet for humans.</p>
            <h2><i class="fa fa-star" aria-hidden="true"></i> 8.9</h2>
            <button>View More</button>
        </div>
        </div>
 )
}
