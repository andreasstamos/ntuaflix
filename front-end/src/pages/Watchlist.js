import React from 'react'
import './Watchlist.css'
import AuthContext from '../context/AuthContext'
import { useContext, useEffect, useState } from 'react'
import NotRegistered from './NotRegistered';
import axiosInstance from '../api/api'
import { Link } from 'react-router-dom';
import { CgClapperBoard, CgPlayListAdd } from "react-icons/cg";


export default function Watchlist() {

    const {user} = useContext(AuthContext);
    const { authTokens } = useContext(AuthContext);

    const [watchlists, setWatchlists] = useState([]);
    const [newLibName, setNewLibName] = useState('');
    const [isCreating, setIsCreating] = useState(false);

    async function create(e) {
      e.preventDefault();

      try {
        const response = await axiosInstance.post(`/watchlists/${user.user_id}/create?lib_name=${newLibName}`, null, {
           headers: {
              Authorization: `Bearer ${authTokens}`,
              'Content-Type': 'application/json', 
           },
        });
  
        console.log(response);
            if (response.status === 200) {
                console.log(response.data.message);
            }
        } catch (error) {
            console.error('Error creating watchlist:');
        }
        setNewLibName('');
        setIsCreating(false);
  }

    useEffect(() => {
      
      const fetchWatchlists = async () => {
        try {
          const response = await axiosInstance.get(`/watchlists/${user.user_id}`, {
            headers: {
              Authorization: `Bearer ${authTokens}`,
            },
          });          

          if (response.status === 200)
            setWatchlists(response?.data);
        } 
        catch (error) {
          console.error('Error fetching watchlists:', error);
        }
      };
      fetchWatchlists();
    }, [user?.user_id, authTokens, isCreating]);


  
    if (!user) return <NotRegistered />

    return (
    <body>
    <div className='watchlist-background' >
        <h1 className='watchlist-title'>My Watchlists</h1>
        <nav className='watchlists-navbar'>

        {watchlists.map((watchlist) => (
        <Link to={`/libcontents/${watchlist.library_name}`} key={watchlist.library_name}>
          {watchlist.library_name}
          <span> <CgClapperBoard/>{watchlist.items} items</span>
        </Link>
      ))}
      </nav>
      

      {isCreating ? (
      <div className='create-container'>
        <form onSubmit={create}>
          <input type='text' className='create-input' placeholder='New Watchlist Title' required value={newLibName} onChange={(e) => setNewLibName(e.target.value)}/>
          <div className='create-buttons'>
            <button className = 'create-button' type ="submit">Create</button>
            <button className = 'create-button' type ="button" onClick={() => setIsCreating(false)} >Cancel</button>
          </div>
        </form>  
      </div>
      ) : (
      <button className = 'addButton' type ="submit" onClick={() => setIsCreating(true)} >+ Create New Watchlist</button>
      )}
    </div> 
  </body>
  )
}
