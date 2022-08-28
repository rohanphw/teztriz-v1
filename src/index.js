import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import "./index.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Single from "./components/ptype/single";
import Multi from "./components/ptype/multi";
import Join from "./components/league/join"
import Create from "./components/league/create";


ReactDOM.render(
  <React.StrictMode>
    <Router>
          <Routes>
            <Route exact path="/" element={<App />} />
            <Route exact path="/single" element={<Single />} />
            <Route exact path="/multi" element={<Multi />} />
            <Route exact path="/join" element={<Join />} />
            <Route exact path="/create" element={<Create />} />
          </Routes>
        </Router>
  </React.StrictMode>,
  document.getElementById("root")
);
