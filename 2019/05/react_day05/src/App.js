import React, { useState } from "react";
import "./App.css";
import PartA from "./prob/PartA";
import PartB from "./prob/PartB";

function App() {
  const [showB, setShowB] = useState(false);
  const [isHidden, setIsHidden] = useState(false);
  return (
    <>
      <div className="container text-center mx-auto">
        <button
          className="bg-blue-200 rounded p-1"
          onClick={() => setShowB(state => !state)}
        >
          Switch A/B
        </button>
        {/* <button */}
        {/*   className="bg-gray-200 rounded p-1 ml-2" */}
        {/*   onClick={() => setIsHidden(state => !state)} */}
        {/* > */}
        {/*   Hide/Show */}
        {/* </button> */}
      </div>
      {!isHidden && (
        <div className="App" style={{ height: "95%" }}>
          {!showB && <PartA />}
          {showB && <PartB />}
        </div>
      )}
    </>
  );
}

export default App;
