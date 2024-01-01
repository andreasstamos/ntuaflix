import React from 'react'
import './Watchlist.css'
import AuthContext from '../context/AuthContext'
import { useContext } from 'react'
import NotRegistered from './NotRegistered';


export default function Watchlist() {

    const {user} = useContext(AuthContext);

    if (!user) return <NotRegistered />
    
    return (
    <div>Watchlist</div>
  )
}
