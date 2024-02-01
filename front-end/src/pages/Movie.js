import React, { useEffect, useState } from 'react'
import InterstellarImage from '../assets/images/poster-2.jpg'
import StarBorderIcon from '@mui/icons-material/StarBorder';
import './Movie.css'
import axiosInstance from '../api/api';
import Preloader from '../components/Preloader';
import { Link, useParams } from 'react-router-dom';


export default function Movie() {

    const {movieID} = useParams();
    const [movieData, setMovieData] = useState(null);
    const [loading, setLoading] = useState(true);


    async function fetchMovieData() {
        const response = await axiosInstance.get(`/title/${movieID}`);
        
        setMovieData(response?.data);
        setLoading(false);
    }

    useEffect(() => {
        fetchMovieData();
    }, [])

  if (loading) return <Preloader/>
  return (
    <div className='movie-page-container' style={{background: `linear-gradient(to right, rgba(0, 0, 0, 0.52), rgba(0, 0, 0, 0.52)), url(${movieData.titlePoster})`}}>
        <div className='movie-container'>
            
            <div className='movie-column'>
                <div className='movie-row'>
                    
                    <p className='movie-genres'>{movieData.genres.map(obj => obj.genreName).join(', ')}</p>

                    <h1 className='title-with-line'>{movieData.original_title}</h1>

                    <div className='movie-metas'>
                        {movieData.rating.avRating && <div className='movie-stars'><StarBorderIcon/><h4>{movieData.rating.avRating}/10</h4></div>}
                        {movieData.startYear && <div className='movie-year'><h4>{movieData.startYear}</h4></div>}
                        {movieData.type && <div className='movie-type'><h4>{movieData.type}</h4></div>}
                        {/* <div className='movie-duration'><h4>2h 35m</h4></div> */}
                    </div>

                    {/* <div className='movie-description'>
                        <p>When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team of researchers, to find a new planet for humans.</p>
                    </div> */}
                    
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
            <img src={movieData.titlePoster} className='movie-poster' />

        </div>

        
        <div className='movie-container'>
            <div className='movie-column'>
                        <div className='movie-row'>
                            

                            <h1 className='title-with-line'>Principals</h1>
                            {movieData.principals && 
                            <ul style={{marginTop:35}} className='principals-list'>
                                    {movieData.principals.map(principal=>{
                                        return <li> 
                                            <div>
                                            <p><Link className='a-transition' to= {`/person/${principal.nameID}`}>{principal.primaryName}</Link></p>
                                            <p>{principal.category}</p>

                                            </div> 
                                            </li>  
                                    })}
            
                            </ul>
                            }
                            
                    </div>

            </div>
        
        </div>
    </div>
  )
}
