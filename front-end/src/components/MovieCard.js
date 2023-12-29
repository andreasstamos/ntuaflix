import React from 'react'
import './MovieCard.css'
import { Link } from 'react-router-dom'
import StarBorderIcon from '@mui/icons-material/StarBorder';

export default function MovieCard({MovieImage}) {
  return (
        <div class="card">
        <img src={MovieImage} />
        <div class="info">
            <h1>Interstellar</h1>
            <p>In the future, where Earth is becoming uninhabitable, farmer and ex-NASA pilot Cooper is asked to pilot a spacecraft
            along with a team of researchers to find a new planet for humans.</p>
            <h2><StarBorderIcon/> 8.9</h2>
            <Link to='/movie'>View More</Link>
        </div>
        </div>
 )
}
