import React, { useState, useCallback } from "react";
import ProgramGrid from "./ProgramGrid";

import programInput from "../problem_input";
programInput[1] = 12;
programInput[2] = 2;

const ADD = 1;
const MULT = 2;
// const STOP = 99;

export const PartA = () => {
  const [program, setProgram] = useState(programInput);
  const [i, setI] = useState(0);

  const [in1, setIn1] = useState(null);
  const [in2, setIn2] = useState(null);
  const [out1, setOut1] = useState(null);

  const step = useCallback(() => {
    const instruction = program[i];
    if (instruction === ADD) {
      const pos_in1 = program[i + 1];
      const pos_in2 = program[i + 2];
      const pos_out = program[i + 3];
      //             program[pos_out] = program[pos_in1] + program[pos_in2]
      setProgram(prevProgram => {
        let p = [...prevProgram];
        p[pos_out] = p[pos_in1] + p[pos_in2];
        return p;
      });
      setI(oldI => oldI + 4);
      setIn1(pos_in1);
      setIn2(pos_in2);
      setOut1(pos_out);
    } else if (instruction === MULT) {
      const pos_in1 = program[i + 1];
      const pos_in2 = program[i + 2];
      const pos_out = program[i + 3];
      //             program[pos_out] = program[pos_in1] + program[pos_in2]
      setProgram(prevProgram => {
        let p = [...prevProgram];
        p[pos_out] = p[pos_in1] * p[pos_in2];
        return p;
      });
      setI(oldI => oldI + 4);
      setIn1(pos_in1);
      setIn2(pos_in2);
      setOut1(pos_out);
    }
  }, [i, program]);
  return (
    <div>
      <div>Part A</div>
      <button onClick={() => step()}>Step</button>
      <ProgramGrid
        program={program}
        current={i}
        in1={in1}
        in2={in2}
        out1={out1}
      />
    </div>
  );
};
export default PartA;
