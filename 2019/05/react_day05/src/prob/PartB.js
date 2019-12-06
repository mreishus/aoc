import React from "react";
//import React, { useState, useEffect, useContext } from "react";
//import cx from "classnames";
import Computer from "./Computer";
import programInput from "../problem_input";

export const PartB = () => {
  return (
    <div>
      <div>PartB</div>
      <Computer initialMemory={programInput} initialInputs={[5]} key={"B"} />
    </div>
  );
};
export default PartB;
