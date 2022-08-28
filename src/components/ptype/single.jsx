import React from "react";
import Navbar from "../Navbar";
// import ChangeName from "./components/ChangeName";

const Single = () => {
  return (
    <div className="bg-black min-h-screen">
      <Navbar />
      <div className="container pt-10 mx-auto">
        <div className="flex justify-center">
          <iframe src="https://tetris-bare-bone.vercel.app/" height="800" width="100%"> </iframe>
        </div>
      </div>
    </div>
  );
};

export default Single;