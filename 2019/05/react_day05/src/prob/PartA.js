import React from "react";
//import React, { useState, useEffect, useContext } from "react";
//import cx from "classnames";
import Computer from "./Computer";
import programInput from "../problem_input";

export const PartA = () => {
  return (
    <div>
      <div>PartA</div>
      <Computer initialMemory={programInput} initialInputs={[1]} key={"A"} />
    </div>
  );
};
export default PartA;
