import 'bootstrap/dist/css/bootstrap.css';
import './App.css';

import { BrowserRouter, Switch, Route, Redirect } from "react-router-dom";
import Register from "./Register.js"
import Login from "./Login.js"
import Quiz from "./Quiz.js"
import { useState } from 'react';
import CreateQuiz from './CreateQuiz';
import Header from './Header';
import Home from './Home';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(localStorage.getItem("token") != null);

  return (
    <div className="app">
      <BrowserRouter>
        <Header />
        <div className="content">
          <Switch>
            <Route
              exact
              path="/register"
              render={() => {
                return <Register />;
              }}
            />
            <Route
              exact
              path="/login"
              render={() => {
                if (!isLoggedIn) {
                  return <Login setIsLoggedIn={setIsLoggedIn} />;
                } else {
                  return <Redirect to="/"></Redirect>;
                }
              }}
            />
            <Route
              exact
              path="/create"
              render={() => {
                if (isLoggedIn) {
                  return <CreateQuiz />;
                } else {
                  return <Redirect to="/login"></Redirect>;
                }
              }}
            />
            <Route
              exact
              path="/quiz/:short_url"
              render={(props) => {
                if (isLoggedIn) {
                  return <Quiz {...props} />;
                } else {
                  return <Redirect to="/login"></Redirect>;
                }
              }}
            />
            <Route
              exact
              path="/"
              render={() => {
                if (isLoggedIn) {
                  return <Home />;
                } else {
                  return <Redirect to="/login"></Redirect>;
                }
              }}
            />
            <Route
              render={() => {
                return <Redirect to="/"></Redirect>;
              }}
            />
          </Switch>
        </div>
      </BrowserRouter>
    </div >
  );
}

export default App;
