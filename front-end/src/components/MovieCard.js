import React from 'react'
import './MovieCard.css'
import { Link } from 'react-router-dom'
import StarBorderIcon from '@mui/icons-material/StarBorder';

export default function MovieCard({imageUrl, movieTitle, averageRating, movieID}) {
  
  return (
        <div className="card">
        <img src={imageUrl} />
        <div className="info">
            <h3 className='h3'>{movieTitle}</h3>
            {/* <p>In the future, where Earth is becoming uninhabitable, farmer and ex-NASA pilot Cooper is asked to pilot a spacecraft
            along with a team of researchers to find a new planet for humans.</p> */}
            {averageRating && <h3 className='h3'><StarBorderIcon/> {averageRating}</h3>}
            <Link to={`/movie/${movieID}`}>View More</Link>
        </div>
        </div>
 )
}
