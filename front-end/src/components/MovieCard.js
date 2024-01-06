import React from 'react'
import './MovieCard.css'
import { Link } from 'react-router-dom'
import StarBorderIcon from '@mui/icons-material/StarBorder';

export default function MovieCard({image_url, movie_title}) {
  
  return (
        <div className="card">
        <img src={image_url} />
        <div className="info">
            <h3 className='h3'>{movie_title}</h3>
            <p>In the future, where Earth is becoming uninhabitable, farmer and ex-NASA pilot Cooper is asked to pilot a spacecraft
            along with a team of researchers to find a new planet for humans.</p>
            <h3 className='h3'><StarBorderIcon/> 8.9</h3>
            <Link to='/movie'>View More</Link>
        </div>
        </div>
 )
}
