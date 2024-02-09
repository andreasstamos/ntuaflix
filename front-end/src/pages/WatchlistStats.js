import React, { useContext, useEffect, useState } from 'react'
import AuthContext from '../context/AuthContext'
import NotRegistered from './NotRegistered';
import './WatchlistStats.css';
import axiosInstance from '../api/api';
import { Link } from 'react-router-dom';
import Preloader from '../components/Preloader';
import { useLocation } from 'react-router-dom';


export default function WatchlistStats() {
    const { pathname } = useLocation();

    const {authTokens} = useContext(AuthContext);

    const [TopGenres, setTopGenres] = useState(null);
    const [WatchlistsStatistics, setWatchlistsStatistics] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    function divide(x, y) {
        return Math.floor(100 * x/y);
    }

    useEffect(() => {
        async function fetchTopGenres() {
            try {
                setIsLoading(true);
    
                const response = await axiosInstance.get(
                    `/top_genres_overall`,
                    {headers: {
                        'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`
                    }})
    
                if (response.status === 200) {
                    setTopGenres(response?.data);
                    setIsLoading(false);
                    console.log(response?.data);
                }
            }
    
            catch (err) {
                setIsLoading(false);
                console.log(err.message);
            }
        }
    
        async function fetchWatchlistsStatistics() {
            try {
                setIsLoading(true);
    
                const response = await axiosInstance.get(
                    `/user_stats_watchlists`,
                    {headers: {
                        'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`
                    }})
    
                if (response.status === 200) {
                    setWatchlistsStatistics(response?.data);
                    setIsLoading(false);
                    console.log(response?.data);
                }
            }
    
            catch (err) {
                setIsLoading(false);
                console.log(err.message);
            }
        }

        fetchTopGenres();
        fetchWatchlistsStatistics();
    }, [authTokens]);

    useEffect(() => {
        window.scrollTo(0, 0);
      }, [pathname]);

    if (!authTokens) return <NotRegistered />
    if (isLoading) return <Preloader /> 

    return (
        <div className='page-container'>                    

            {TopGenres && WatchlistsStatistics && Boolean(TopGenres.total_number) ?
                <div>
                <div className='watch_statistics-container'>
                <div className='watch_statistics-column'>
                <div className='watch_statistics-row'>
                    <div>
                        <h1 className='title-in-line' style={{marginBottom: 10}}>Your Top Genres</h1> 
                        <div>
                            <p style={{marginBottom: 30}}>
                                (based on the <b>{TopGenres.total_number}</b> titles across all your watchlists)
                            </p>

                            {TopGenres.items_per_genre.map(genre => {
                                return <li>
                                    <div>
                                        <p style={{marginTop: 20}}>
                                            {genre.genre_name}:&nbsp;&nbsp;&nbsp;{genre.title_count}/{TopGenres.total_number}
                                            &nbsp;&nbsp;&nbsp;(~{divide(genre.title_count, TopGenres.total_number)}%)
                                        </p>
                                    </div>
                                </li>
                            })}
                        </div>
                    </div></div></div>
                </div>
                <div>
                    <h1 style={{marginLeft: 150, marginTop: 500, marginBottom: 100}}>
                        Take a closer look at all the genres appearing in each one of your watchlists:
                    </h1>

                    {WatchlistsStatistics.map(Watchlist => {
                                return <div className='watch_statistics-container'>
                                    <div className='watch_statistics-column'>
                                        <div className='watch_statistics-row'>
                                            <h1 style={{marginBottom: 20}}>
                                            <Link className='a-transition' to={`/libcontents/${Watchlist.library_name}`}>
                                                {Watchlist.library_name}
                                            </Link>
                                            </h1>
                                            <p style={{marginBottom: 25}}>
                                                There are {Watchlist.item_count} titles in this watchlist
                                            </p>

                                            {Watchlist.items_per_genre.map(genre => {
                                                return <li>
                                                    <div>
                                                        <p style={{marginBottom: 20}}>
                                                            {genre.genre_name}:&nbsp;&nbsp;&nbsp;{genre.title_count}/{Watchlist.item_count}
                                                            &nbsp;&nbsp;&nbsp;(~{divide(genre.title_count, Watchlist.item_count)}%)
                                                        </p>
                                                    </div>
                                                </li>
                                            })}
                                    </div></div>
                                </div>
                            })}
                </div>
                </div>

                : <div>
                    <p style={{textAlign:'center', marginTop: 250}}>
                        It looks like you haven't added any titles to any of your watchlists yet!
                        <br></br>
                        Create watchlists <Link to='/watchlist/'>here</Link> and add new titles through browsing.
                        &nbsp;Explore all the titles <Link to='/movies/'>here</Link>!
                    </p>
                    </div>}
        </div>
    )

}