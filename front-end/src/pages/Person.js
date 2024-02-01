import React, { useEffect, useState } from 'react'
import './Person.css'
import { useParams } from 'react-router-dom'
import axiosInstance from '../api/api';
import Preloader from '../components/Preloader';

export default function Person() {

  const {personID} = useParams();
  const [personData, setPersonData] = useState(null);
  const [loading, setLoading] = useState(true);

  async function fetchPerson() {
    const response = await axiosInstance.get(`/name/${personID}`);
    setPersonData(response?.data);
    setLoading(false);
  }

  useEffect( () => {
    fetchPerson();
  }, []) 

  if (loading) return <Preloader />
  
  return (
    <div className='page-container'>
        <div className='movie-container'>
            <div className='person-container'>
              <h1 className='title-with-line'>Person</h1>
              <img src={personData?.namePoster} />
            </div>
        </div>
    </div>
  )
}
