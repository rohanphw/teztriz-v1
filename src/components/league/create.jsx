import React from "react";
import Navbar from "../Navbar";
// import ChangeName from "./components/ChangeName";

const Create = () => {
  return (
    <div className="bg-black min-h-screen">
      <Navbar />
      <div className="container pt-10 mx-auto">
        <div className="flex justify-center">
          <h1 className="text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-red-500 via-blue-300 to-red-400">
          Teztriz
          </h1>
        </div>
      </div>

      <div className="mt-20 flex justify-center">
        <form>
          <input type="text" id="Duration" name="Duration" placeholder="Duration"/><br />
          <input type="text" id="Min Players" name="Min Players" placeholder="Min Players" /><br />
          <input type="text" id="Max Players" name="Max Players" placeholder="Max Players" /><br />
          <input className="bg-red-500 px-6 py-2 rounded-sm text-xs font-semibold text-white cursor-pointer" type="submit" value="Create League" />
        </form> 
        </div>
    </div>
  );
};

export default Create;