import React, { useState , useEffect } from 'react'
import axiosInstance from '../api/api';
import { useNavigate } from "react-router-dom";
import { useLocation } from 'react-router-dom';


export default function Profile() {
  const { pathname } = useLocation();

    const navigate = useNavigate();

    const [userProfile, setUserProfile] = useState({
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        dob: '',
      });

    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [dob, setDob] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    useEffect(() => {
        const fetchUserProfile = async (userId) => {
          try {
            const response = await axiosInstance.get(`/user-profile/${userId}`);
            setUserProfile(response.data);
          } catch (error) {
            console.error('Error fetching user profile:', error);
          }
        };
    
        // Replace userId with the actual user ID (you need to get it from somewhere)
        fetchUserProfile(1); // userId = 1
      }, []); // The empty dependency array ensures that this effect runs only once, similar to componentDidMount
    

    async function submit(e) {
        e.preventDefault();
        setError(null);
        setSuccess(null);

        const payload = {
            username: username,
            first_name: firstName,
            last_name: lastName,
            email: email,
            dob: dob,
        }


        try {
            const userId = 1; // Replace with the actual user ID
            const response = await axiosInstance.post(`/update-profile/${userId}`, payload);
            navigate('/', {replace:true})
        }
        catch (error) {
            setError(error?.response?.data?.detail)
        }
    }

    useEffect(() => {
      window.scrollTo(0, 0);
    }, [pathname]);


  return (
    <div className='auth-container'>
      <div className='form-wrapper'>
          <form onSubmit={submit}>
          <h1 className='title-with-line'>User Profile</h1>

              <div className='form-input'>
                  <input type='text' placeholder='Username' required value={username} onChange={(e) => setUsername(e.target.value)}/>
              </div>

              <div className='form-input'>
                  <input type='text' placeholder='First name' required value={firstName} onChange={(e) => setFirstName(e.target.value)}/>
              </div>

              <div className='form-input'>
                  <input type='text' placeholder='Last name' required value={lastName} onChange={(e) => setLastName(e.target.value)}/>
              </div>

              <div className='form-input'>
                  <input type='email' placeholder='Email' required value={email} onChange={(e) => setEmail(e.target.value)}/>
              </div>
              
              <div className='form-input'>
                  <input type="date" value={dob} onChange={(e) => setDob(e.target.value)} required />
              </div>


              <button type='submit' className='btn btn-primary btn-w100'>Update Profile</button>
              
              <p className='form-error'>{error}</p>
              <p className='form-success'>{success}</p>

          </form>
      </div>
    </div>
  )
}
