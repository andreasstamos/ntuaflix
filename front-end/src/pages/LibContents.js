import React from 'react'
import AuthContext from '../context/AuthContext'
import { useContext, useEffect, useState, useMemo } from 'react'
import NotRegistered from './NotRegistered';
import axiosInstance from '../api/api'
import { useParams } from 'react-router-dom';
import { CgPlayListAdd, CgTrash} from "react-icons/cg";
import LibContent from '../components/LibContent';
import { useLocation } from 'react-router-dom';
import './LibContents.css'


export default function LibContents() {
  const { pathname } = useLocation();

    const {user} = useContext(AuthContext);
    const { authTokens } = useContext(AuthContext);
    const { library_name } = useParams();

    const response_dict = useMemo(() => ({
      204: `${library_name}: This watchlist is empty!`,
      403: `${library_name}: This watchlist doesn't belong to you!`,
      404: `${library_name}: This Watchlist doesn't exist!`,
      401: 'You must sign in first! ',
    }), [library_name]);

    const [movies, setMovies] = useState([]); 
    const [status, setStatus]= useState();

    
    useEffect(() => {
        const fetchLibContents = async () => {
          try {
            const response = await axiosInstance.get(`/watchlists/${user.user_id}/${library_name}`, {
              headers: {
                'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`
              },
            });
    
            if (response.status === 200) {
              setMovies(response.data);
            }
            else {
                setStatus(response.status);
            }
          } catch (error) {
            if (error.response && error.response.status in response_dict) {
                // Handle 404 error specifically
                setStatus(error.response.status);
            }
            console.error(`Error fetching contents for ${library_name}:`, error);
          }
        };
    
        fetchLibContents();
      }, [library_name, user?.user_id, authTokens, response_dict]);
      

      const removeWatchlist = async () => {
        try {
          const response = await axiosInstance.delete(`/watchlists/${user.user_id}/${library_name}`, {
            headers: {
              'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`,
            },
          });
          if (response.status === 200) {
            console.log("Lib deleted successfully");
            window.location.reload();
          }
        }
          catch (error){
            console.error(error,status);
          }
          
        };

        useEffect(() => {
          window.scrollTo(0, 0);
        }, [pathname]);
        

    if (!user) return <NotRegistered />

    return (
        <div>

          {status ? (
                <div>
                <h2 className="watchlist-title">{response_dict[status]}</h2>
                {status === 204 && 
                <div>
                <button className='btn btn-primary add-movie button-align-center'> <CgPlayListAdd />Add Movies</button>
                <button className='btn btn-primary remove-lib button-align-center' onClick={removeWatchlist}><CgTrash/>Remove Watchlist</button>
                </div>
                }
            </div>
          ) :

          (
            <div>
            <h1 className="watchlist-title">All movies in '{library_name}'</h1>
            <button className='btn btn-primary add-movie button-align-center'> <CgPlayListAdd />Add Movies </button>
            <button className='btn btn-primary remove-lib button-align-center' onClick={removeWatchlist}><CgTrash/></button>
            <LibContent movies={movies} />
            </div>
          )}

          </div>
      );
      
}