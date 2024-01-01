import { createContext , useState, useEffect} from 'react'
import { jwtDecode } from "jwt-decode";
import {useNavigate } from 'react-router-dom';


const AuthContext = createContext();


export const AuthProvider = ({children}) => {    
    const [authTokens, setAuthTokens] = useState( () => localStorage.getItem('authTokens') ? localStorage.getItem('authTokens') : null);
    const [user, setUser] = useState( () => localStorage.getItem('authTokens') ? jwtDecode(localStorage.getItem('authTokens')) : null);

    const saveTokens = (tokens) => {
        localStorage.setItem('authTokens', tokens);
        setAuthTokens(tokens)
        setUser(jwtDecode(tokens));
    }

    const logoutUser = () => {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem('authTokens');
    }


    const contextData = {
        authTokens: authTokens,
        user: user,
        logoutUser: logoutUser,
        saveTokens: saveTokens,
    }

    return (
        <AuthContext.Provider  value={contextData}>
            {children}
        </AuthContext.Provider>
    )
}

export default AuthContext;

