import React from 'react'
import InterstellarImage from '../assets/images/poster-2.jpg'
import StarBorderIcon from '@mui/icons-material/StarBorder';
import './Movie.css'


export default function Movie() {
  return (
    <div className='movie-page-container'>
        <div className='movie-container'>
            <div className='movie-column'>
                <div className='movie-row'>
                    <h1 className='title-with-line'>The Dark Knight</h1>

                    <div className='movie-metas'>
                        <div className='movie-stars'><StarBorderIcon/><h4>8.6/10</h4></div>
                        <div className='movie-year'><h4>2003</h4></div>
                        <div className='movie-duration'><h4>2h 35m</h4></div>
                    </div>

                    <div className='movie-description'>
                        <p>When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team of researchers, to find a new planet for humans.</p>
                    </div>

                    <div className='movie-actions'>
                        <button className='btn btn-primary'>Add to WatchList</button>
                    </div>
                </div>

                {/* <div className='movie-metas'>
                    <div className='movie-stars'><StarBorderIcon/><h3>8.6/10</h3>  2.8m</div>
                    <div className='movie-year'><h3>2003</h3></div>
                    <div className='movie-duration'><h3>2h 35m</h3></div>

                </div> */}
            </div>
            <img src={InterstellarImage} />

        </div>

        


       

    </div>
  )
}
