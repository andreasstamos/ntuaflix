import React from 'react'
import './Reviews.css'
import AuthContext from '../context/AuthContext'
import { useContext, useEffect, useState } from 'react'
import NotRegistered from './NotRegistered';
import axiosInstance from '../api/api'
import { Link } from 'react-router-dom';

export default function Reviews() {

    const { user } = useContext(AuthContext);
    const { authTokens } = useContext(AuthContext);

    const [userOnly, setUserOnly] = useState(false);
    const [reviews, setReviews] = useState([]);


    return (
        <div className='theme'>
            <nav className='reviews-navbar'>
                <Link to={'/reviews/'} onClick={ () => setUserOnly(false) }> All Reviews </Link>
                <Link to={'/reviews/'} onClick={ () => setUserOnly(true) }> My Reviews </Link>
                <Link to={'/makereview/'}> Make Review </Link>
            </nav>
        </div>
    )
}