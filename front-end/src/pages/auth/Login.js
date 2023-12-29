import React, { useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'

export default function Login() {


    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    async function submit(e) {
        e.preventDefault();
        setError(null);
        setLoading(true);


        const payload = {
            username: username,
            password: password,
        }
        setPassword('');

        console.log(payload);
    }


  return (
    <div className='form-wrapper'>
        <form onSubmit={submit}>
        <h1>Sign in</h1>

            <div className='form-input'>
                <input type='text' placeholder='Username' required value={username} onChange={(e) => setUsername(e.target.value)}/>
            </div>
            
            <div className='form-input'>
                <input type='password' placeholder='Password' required value={password} onChange={(e) => setPassword(e.target.value)}/>
            </div>

            <button type='submit' className='form-btn'>Sign in</button>
            
            <p className='form-error'></p>

            <div className='alternative-link'>
                <p>Don't have an account yet? Sign up <Link to='/auth/register'>here</Link>.</p>
            </div>
        </form>
    </div>
  )
}
