import React, { useContext, useEffect, useState } from "react";
import AuthContext from "../context/AuthContext";
import NotRegistered from "./NotRegistered";
import "./Statistics.css";
import axiosInstance from "../api/api";
import { Link } from "react-router-dom";
import Preloader from "../components/Preloader";
import { useLocation } from "react-router-dom";
import PercentageChart from "../components/PercentageChart";

export default function Statistics() {
  const { pathname } = useLocation();

  const { authTokens } = useContext(AuthContext);

  const [TopGenres, setTopGenres] = useState(null);
  const [WatchlistsStatistics, setWatchlistsStatistics] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  async function fetchTopGenres() {
    try {
      setIsLoading(true);

      const response = await axiosInstance.get(`/top_genres_overall`, {
        headers: {
          "X-OBSERVATORY-AUTH": `${authTokens ? authTokens : "None"}`,
        },
      });

      if (response.status === 200) {
        setTopGenres(response?.data);
        setIsLoading(false);
        console.log(response?.data);
      }
    } catch (err) {
      setIsLoading(false);
      setError(err.message);
      console.log(error);
    }
  }

  async function fetchWatchlistsStatistics() {
    try {
      setIsLoading(true);

      const response = await axiosInstance.get(`/user_stats_watchlists`, {
        headers: {
          "X-OBSERVATORY-AUTH": `${authTokens ? authTokens : "None"}`,
        },
      });

      if (response.status === 200) {
        setWatchlistsStatistics(response?.data);
        setIsLoading(false);
        console.log(response?.data);
      }
    } catch (err) {
      setIsLoading(false);
      setError(err.message);
      console.log(error);
    }
  }

  function divide(x, y) {
    return Math.floor((100 * x) / y);
  }

  useEffect(() => {
    fetchTopGenres();
    fetchWatchlistsStatistics();
  }, []);

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  if (!authTokens) return <NotRegistered />;
  if (isLoading) return <Preloader />;

  return (
    <div className="page-container" style={{paddingTop: '0'}}>
      {TopGenres && WatchlistsStatistics && Boolean(TopGenres.total_number) ? (
        <div>
          <div className="statistics-container">
            <div className="statistics-column">
              <div className="statistics-row">
                <h1 className="title-with-line">Your Top Genres</h1>
                  <div style={{ marginBlock: 30 }}>
                    <small>
                      (based on the <b>{TopGenres.total_number}</b> titles
                      across all your watchlists)
                    </small>
                  </div>

                  <ul className="statistics-list">
                    {TopGenres.items_per_genre.map((genre) => {
                      return (
                        <li>
                          <p className="statistics-line">
                            {genre.genre_name}:
                            <PercentageChart
                              percentage={divide(
                                genre.title_count,
                                TopGenres.total_number
                              )}
                            />
                          </p>
                        </li>
                      );
                    })}
                  </ul>
              </div>
            </div>
          </div>
          <div>
            <h1 className="statistic-genres-title" >
              Take a closer look at all the genres appearing in each one of your
              watchlists:
            </h1>

            {WatchlistsStatistics.map((Watchlist, index) => {
              return (
                <div className="statistics-container">
                  <div className="statistics-column">
                    <div className="statistics-row">
                      <h1
                        style={{ marginBottom: 20 }}
                        className="title-with-line statistic-watchlist-title"
                      >
                        <Link
                          to={`/libcontents/${Watchlist.library_name}`}
                          className="watchlist-link a-transition"
                          key={Watchlist.library_name}
                        >
                          {Watchlist.library_name}
                        </Link>
                        <span>#{index+1}</span>
                      </h1>
                      <p style={{ marginBottom: 25 }}>
                        There are {Watchlist.item_count} titles in this
                        watchlist
                      </p>
                      <ul className="statistics-list">
                        {Watchlist.items_per_genre.map((genre) => {
                          return (
                            <li>
                              <p className="statistics-line">
                                {genre.genre_name}:
                                <PercentageChart
                                  percentage={divide(
                                    genre.title_count,
                                    Watchlist.item_count
                                  )}
                                />
                              </p>
                            </li>
                          );
                        })}
                      </ul>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ) : (
        <div>
          <p style={{ textAlign: "center", marginTop: 250 }}>
            It looks like you haven't added any titles to any of your watchlists
            yet!
            <br></br>
            Create watchlists and add titles <Link to="/watchlist/">
              here
            </Link>{" "}
            to get more personalised statistics!
          </p>
        </div>
      )}
    </div>
  );
}
