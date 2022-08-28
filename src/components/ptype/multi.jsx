import React from "react";
import Navbar from "../Navbar";
// import ChangeName from "./components/ChangeName";
import { Link } from "react-router-dom";


const Multi = () => {
  return (
    <div className="bg-black min-h-screen">
      <Navbar />
      <div className="container pt-10 mx-auto">
        <div className="flex justify-center">
          <h1 className="text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-red-500 via-blue-300 to-red-400">
            Teztriz
          </h1>
        </div>
        

        <div className="mt-20 flex justify-center">
        <Link className="bg-red-500 px-6 py-2 rounded-sm text-xs font-semibold text-white cursor-pointer" to="/join"> Join League </Link>
        <br />
        <Link className="bg-red-500 px-6 py-2 rounded-sm text-xs font-semibold text-white cursor-pointer" to="/create"> Create League </Link>
        </div>
      </div>
    </div>
  );
};

export default Multi;