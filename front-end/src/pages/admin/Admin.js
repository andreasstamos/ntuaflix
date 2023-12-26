import React, {useState, useEffect} from 'react'
import axiosInstance from '../../api/api'


export default function Admin() {

    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(true)
    
    async function admin() {
        const response = await axiosInstance.get('/admin/');
        console.log(response);
        setMessage(response?.data?.message)
        setLoading(false);
    }

    useEffect( () => {
        admin();
    }, [])

  if (loading) return (
    <div>loading...</div>
  )
  
  return (
    <div>{message}</div>
  )
}