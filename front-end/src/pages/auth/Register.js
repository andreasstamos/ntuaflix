import React, { useState } from 'react'
import { Link } from 'react-router-dom';

export default function Register() {


    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
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

        if (password !== passwordConfirm) {
            setError("Passwords do not match.");
            return;
        }

        setLoading(true);


        const payload = {
            username: username,
            email: email,
            dob: dob,
            password: password,
            passwordConfirm: passwordConfirm,
        }
        setPassword('');
        setPasswordConfirm('');


        console.log(payload);
    }


  return (
    <div className='form-wrapper'>
        <form onSubmit={submit}>
        <h1>Sign Up</h1>

            <div className='form-input'>
                <input type='text' placeholder='Username' required value={username} onChange={(e) => setUsername(e.target.value)}/>
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


            <button type='submit' className='form-btn'>Sign Up</button>
            
            <p className='form-error'>{error}</p>
            <p className='form-success'>{success}</p>
            <div className='alternative-link'>
                <p>Already have an account yet? Sign in <Link to='/auth/login/'>here</Link>.</p>
            </div>
        </form>
    </div>
  )
}
