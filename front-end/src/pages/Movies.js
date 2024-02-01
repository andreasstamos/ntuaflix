import React, { useEffect, useState } from 'react'
import './Movies.css'
import MovieCard from '../components/MovieCard'
import MandalorianImage from '../assets/images/mandalorian.jpg'
import TopGunImage from '../assets/images/topgun.jpg'
import InterstellarImage from '../assets/images/interstellar.jpg'
import BatmanImage from '../assets/images/poster-2.jpg'
import OppenheimerImage from '../assets/images/oppenheimer.jpg'
import Preloader from '../components/Preloader'
import axiosInstance from '../api/api'
import Pagination from '@mui/material/Pagination'
import SearchBarTitles from '../components/SearchBarTitles'
import { Select, MenuItem } from '@mui/material'

export default function Movies() {

    const NO_GENRE_SELECTED_STRING = "none";

    const [genre, setGenre] = useState(NO_GENRE_SELECTED_STRING);
    const [titles, setTitles] = useState(null);
    const [loading, setLoading] = useState(true);
    const [page, setPage] = useState(1);
    const [searchValue, setSearchValue] = useState(null);
    const [genres, setGenres] = useState(null);
    const [totalPages, setTotalPages] = useState(null);

    async function fetchGenres() {
      const response = await axiosInstance.get('/get-genres');
      setGenres(response?.data);
    }

    async function fetchTitles(wait_in_func = true) {
      if (wait_in_func)
        setLoading(true)
      let genrePayload = genre === NO_GENRE_SELECTED_STRING ? "" : parseInt(genre);
      const response = await axiosInstance.get(`/get-movies?page=${page}${genrePayload ? `&qgenre=${genrePayload}` : ''}`);
      setTitles(response?.data?.titles);
      if (response?.data?.total_pages)
      setTotalPages(parseInt(response?.data?.total_pages))
      if (wait_in_func)
        setLoading(false)
    }

    useEffect(() => {
        if (genre === '' || genre === undefined) return;

        if (page === 1) fetchTitles(true);
        else setPage(1);
    }, [genre])

    useEffect( () => {
        const callBoth = async() => {
          setLoading(true);
          if (!genres)
              await fetchGenres();
          await fetchTitles(false);

          setLoading(false);
        }

        callBoth();

    }, [page])


  if (loading) return <Preloader />


  return (
    <div className='page-container'>


      <div className='filters'>
        <div className='filters-column'>
        <SearchBarTitles value={searchValue} handleChangeValue={(value) => {setSearchValue(value)}} />
        <Select
          labelId="demo-select-small-label"
          id="demo-select-small"
          value={genre}
          label="All Genres"
          onChange={(e) => setGenre(e.target.value)}
          size='small'
          sx={{width: 170}}
          
        >
          <MenuItem value={NO_GENRE_SELECTED_STRING} selected>
            All Genres
          </MenuItem>
          {genres && genres.map(genreItem => {
            return <MenuItem value={genreItem.id}>{genreItem.name}</MenuItem>
          })}
      </Select>
        </div>
        <div className='filters-column'>
          <Pagination count={totalPages} page={page} onChange={(event,value) => {setPage(value);}}/>
        </div>
      </div>
        <div className='movies-container'>
 
            {titles && titles.map((title) => {
              return <MovieCard 
                key={title.titleID} 
                movieID={title.titleID} 
                movieTitle={title.original_title} 
                averageRating={title.rating.avRating} 
                imageUrl={title?.titlePoster}/>
            })}

        </div>
          
          <div className='filters'>
            <div className='filters-column flex-end'>
              <Pagination count={totalPages} page={page} onChange={(event,value) => {setPage(value);}}/>
            </div>
        </div>
    </div>
  )
}
