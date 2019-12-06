import React from "react";
//import React, { useState, useEffect, useContext } from "react";
//import cx from "classnames";
import Computer from "./Computer";
import programInput from "../problem_input";

const testProg = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8];
const testInput = [8];

export const PartA = () => {
  return (
    <div>
      <div>PartA</div>
      <Computer
        initialMemory={testProg}
        initialInputs={testInput}
        key={"AZZ"}
      />
      <Computer initialMemory={programInput} initialInputs={[1]} key={"A"} />
    </div>
  );
};
export default PartA;
