import React, { useState } from 'react'
import { Link } from 'react-router-dom';
import axiosInstance from '../../api/api';

export default function Register() {


    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [password, setPassword] = useState('');
    const [passwordConfirm, setPasswordConfirm] = useState('');
    const [dob, setDob] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [loading, setLoading] = useState(false);


    async function submit(e) {
        e.preventDefault();
        setError(null);
        setSuccess(null);

        // if (password !== passwordConfirm) {
            // setError("Passwords do not match.");
            // return;
        // }

        setLoading(true);


        const payload = {
            username: username,
            first_name: firstName,
            last_name: lastName,
            email: email,
            dob: dob,
            password: password,
            password_confirm: passwordConfirm,
        }
        setPassword('');
        setPasswordConfirm('');

        try {
            const response = await axiosInstance.post('/register', payload);
            console.log(response);
        }
        catch (error) {
            setError(error?.response?.data?.detail)
        }
    }


  return (
    <div className='form-wrapper'>
        <form onSubmit={submit}>
        <h1>Sign up</h1>

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

            <div className='form-input'>
                <input type='password' placeholder='Password' required value={password} onChange={(e) => setPassword(e.target.value)}/>
            </div>

            <div className='form-input'>
                <input type='password' placeholder='Confirm Password' required value={passwordConfirm} onChange={(e) => setPasswordConfirm(e.target.value)}/>
            </div>


            <button type='submit' className='btn btn-primary btn-w100'>Sign Up</button>
            
            <p className='form-error'>{error}</p>
            <p className='form-success'>{success}</p>
            <div className='alternative-link'>
                <p>Already have an account yet? Sign in <Link to='/auth/login/'>here</Link>.</p>
            </div>
        </form>
    </div>
  )
}
