import React, {useEffect} from 'react'
import './Navbar.css'
import { NavLink } from 'react-router-dom'
import NtuaflixLogo from '../assets/images/pyrforos.svg'
import { matchPath, } from 'react-router-dom'
import {useLocation} from 'react-router-dom'
// import GreekFlag from '../assets/images/greek_flag.svg'
// import AmericanFlag from '../assets/images/american_flag.svg'
// import LanguageMetas from '../metas/LanguageMetas'
import MenuIcon from '@mui/icons-material/Menu';
// import SvgIcon from '@mui/material/SvgIcon';
import CloseIcon from '@mui/icons-material/Close';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
export default function Navbar() {
  const location = useLocation();
  const match = matchPath({path:`/`, exact:true}, location.pathname)



  useEffect( () => {
    var duplicateScript = document.getElementById("navbarScript");
    if (duplicateScript) return;
    const inlineScript = document.createElement('script');
    inlineScript.setAttribute("id", "navbarScript");
    inlineScript.innerHTML = `
    const toggle = document.querySelector(".toggle");
    const menu = document.querySelector(".menu");
    const items = document.querySelectorAll(".item");
    const logo = document.querySelector("nav ul.menu .logo")
    const nav = document.getElementById("#top-nav");


    /* Toggle mobile menu */
    function toggleMenu() {
      if (window.innerWidth < 1078) { /* This item is new. Only if the user is using a mobile phone toggle the active class */
      if (menu.classList.contains("active")) {
        menu.classList.remove("active");
        //toggle.querySelector("a").innerHTML = "<i class='fas fa-bars'></i>";
        toggle.querySelector("a").innerHTML = "<svg class='MuiSvgIcon-root MuiSvgIcon-fontSizeMedium css-i4bv87-MuiSvgIcon-root css-vubbuv' focusable='false' aria-hidden='true' viewBox='0 0 24 24' data-testid='MenuIcon'><path d='M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z'></path></svg>"
      } else {
        menu.classList.add("active");
        //toggle.querySelector("a").innerHTML = "<i class='fas fa-times'></i>";
        toggle.querySelector("a").innerHTML = "<svg class='MuiSvgIcon-root MuiSvgIcon-fontSizeMedium css-i4bv87-MuiSvgIcon-root css-vubbuv' focusable='false' aria-hidden='true' viewBox='0 0 24 24' data-testid='CloseIcon'><path d='M19 6.41 17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z'></path></svg>"
      }
    } 

    }
    
  
    
    /* Activate Submenu */
    function toggleItem() {
      if (this.classList.contains("submenu-active")) {
        this.classList.remove("submenu-active");
      } else if (menu.querySelector(".submenu-active")) {
        menu.querySelector(".submenu-active").classList.remove("submenu-active");
        this.classList.add("submenu-active");
      } else {
        this.classList.add("submenu-active");
      }
    }
    
    /* Close Submenu From Anywhere */
    function closeSubmenu(e) {
      if (menu.querySelector(".submenu-active")) {
        let isClickInside = menu
          .querySelector(".submenu-active")
          .contains(e.target);
    
        if (!isClickInside && menu.querySelector(".submenu-active")) {
          menu.querySelector(".submenu-active").classList.remove("submenu-active");
        }
      }
    }
   


    /* when clicking on the logo, the menu must be closed no matter what! NOT TOGGLED (if the menu is not active by pressing on the logo it will open)*/
    function closeMenu() {
    if (window.innerWidth < 1078) { /* This item is new. Only if the user is using a mobile phone toggle the active class */
    if (menu.classList.contains("active")) {
      menu.classList.remove("active");
      //toggle.querySelector("a").innerHTML = "<i class='fas fa-bars'></i>";
      toggle.querySelector("a").innerHTML = "<svg class='MuiSvgIcon-root MuiSvgIcon-fontSizeMedium css-i4bv87-MuiSvgIcon-root css-vubbuv' focusable='false' aria-hidden='true' viewBox='0 0 24 24' data-testid='MenuIcon'><path d='M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z'></path></svg>"

    }
  } 
    }

    /* Event Listeners */
    toggle.addEventListener("click", toggleMenu, false);
    logo.addEventListener("click", closeMenu, false); /* this is new. If logo is clicked, toggle navbar */

    for (let item of items) {
        if (!item.querySelector(".submenu")) { /* this if statement is new. If item is not a dropdown then if it is clicked, automatically toggle navbar */
          item.addEventListener("click", toggleMenu, false);
        }

        if (item.querySelector(".submenu")) {
        item.addEventListener("click", toggleItem, false);
        }
        item.addEventListener("keypress", toggleItem, false);
    }
    document.querySelectorAll(".subitem").forEach((item) => item.addEventListener("click", toggleMenu, false)) /* this if statement is new. If item is in a dropdown then if it is clicked, automatically toggle navbar */
    document.addEventListener("click", closeSubmenu, false);
    `
    document.body.append(inlineScript);
  }, [])


  return (
    <>

    {/* <nav className={`navigation ${!match && 'colored'}`} id='#top-nav' role='navigation' aria-label='Main navigation'> */}
    <nav className={`navigation ${!match}`} id='#top-nav' role='navigation' aria-label='Main navigation'>
        <ul className="menu">
          <li className="logo"><NavLink className='not-color' to={`/`}><img src={NtuaflixLogo} width="85" alt='IEEE NTUA Student Branch.' /></NavLink></li>
          <li className="item"><NavLink to={`/`}>Αρχικη</NavLink></li>
          <li className="item"><NavLink to={`/watchlist/`}>WatchList</NavLink></li>
          <li className="item"><NavLink to={`/preloader/`}>Preloader</NavLink></li>
          <li className="item has-submenu">
            <a tabIndex="0">Genres<ExpandMoreIcon/></a>
            <ul className="submenu">
              <li className="subitem"><NavLink to={`/chapter/computer-society`} className='subitem-link'>Computer Society</NavLink></li>
              <li className="subitem"><NavLink to={`/chapter/robotics-automation-society`} className='subitem-link'>Robotics & Automation Society</NavLink></li>
              <li className="subitem"><NavLink to={`/chapter/power-energy-society`} className='subitem-link'>Power & Energy Society</NavLink></li>
              <li className="subitem"><NavLink to={`/chapter/engineering-in-medicine-biology-society`} className='subitem-link'>Engineering in Medicine & Biology Society</NavLink></li>
              <li className="subitem"><NavLink to={`/chapter/communications-society`} className='subitem-link'>Communications Society</NavLink></li>
            </ul>
          </li>
          {/* <li class="item has-submenu">
            <a tabIndex="0">Projects</a>
            <ul class="submenu">
              <li class="subitem"><a href="#">Freelancer</a></li>
              <li class="subitem"><a href="#">Startup</a></li>
              <li class="subitem"><a href="#">Enterprise</a></li>
            </ul>
          </li> */}
          <li className="item"><NavLink to={`/events`}>Movies</NavLink></li>

            <li className="item">
              <NavLink to={`/auth/register`} className='not-color cta' >
                <span> Sign up/in </span>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -13.54 122.88 122.88"><path d="M12.14 0h98.6c3.34 0 6.38 1.37 8.58 3.56 2.2 2.2 3.56 5.24 3.56 8.58v71.47c0 3.34-1.37 6.38-3.56 8.58a12.11 12.11 0 0 1-8.58 3.56h-19.2c-.16.03-.33.04-.51.04-.17 0-.34-.01-.51-.04H62.74c-.16.03-.33.04-.51.04-.17 0-.34-.01-.51-.04H33.31c-.16.03-.33.04-.51.04-.17 0-.34-.01-.51-.04H12.14c-3.34 0-6.38-1.37-8.58-3.56S0 86.95 0 83.61V12.14C0 8.8 1.37 5.76 3.56 3.56 5.76 1.37 8.8 0 12.14 0zm43.05 31.24 20.53 14.32a2.92 2.92 0 0 1 .1 4.87L55.37 64.57a2.928 2.928 0 0 1-4.78-2.27V33.63h.01c0-.58.17-1.16.52-1.67a2.93 2.93 0 0 1 4.07-.72zm38.76 48.21V89.9h16.78c1.73 0 3.3-.71 4.44-1.85a6.267 6.267 0 0 0 1.85-4.44v-4.16H93.95zM88.1 89.9V79.45H65.16V89.9H88.1zm-28.79 0V79.45H35.73V89.9h23.58zm-29.44 0V79.45H5.85v4.16c0 1.73.71 3.3 1.85 4.44a6.267 6.267 0 0 0 4.44 1.85h17.73zM5.85 73.6h111.18V22.2H5.85v51.4zM88.1 16.35V5.85H65.16v10.49H88.1v.01zm5.85-10.5v10.49h23.07v-4.2c0-1.73-.71-3.3-1.85-4.44a6.267 6.267 0 0 0-4.44-1.85H93.95zm-34.64 10.5V5.85H35.73v10.49h23.58v.01zm-29.44 0V5.85H12.14c-1.73 0-3.3.71-4.44 1.85a6.267 6.267 0 0 0-1.85 4.44v4.2h24.02v.01z"/></svg>               

              </NavLink>
            </li>
        <li className="toggle"><a href="#"><MenuIcon/></a></li>

        </ul>
      </nav>
      </>
  )
}
