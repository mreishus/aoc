import React, { useState, useCallback } from "react";
//import React, { useState, useEffect, useContext } from "react";
//import cx from "classnames";
import ProgramGrid from "./ProgramGrid";
import useInterval from "./useInterval";

const MODE_POSITION = 0;
const MODE_IMMEDIATE = 1;

const OP_ADD = 1;
const OP_MULT = 2;
const OP_SAVE = 3;
const OP_WRITE = 4;
const OP_JUMP_IF_TRUE = 5;
const OP_JUMP_IF_FALSE = 6;
const OP_LESS_THAN = 7;
const OP_EQUALS = 8;
const OP_HALT = 99;

// Light on comments.  You'll have to check my python and elixir
// solutions to see the same approach spelled out more clearly!
const digitFromRight = (x, n) => ~~(x / 10 ** n) % 10;
const direct = (memory, pc, n) => memory[pc + n];
const lookup = (memory, pc, n) => {
  const rawInstruction = memory[pc];
  // If instruction is 105, and n=1, mode is the "1", or the 2nd digit
  // from right 0 indexed (3rd when counting naturally)
  const mode = digitFromRight(rawInstruction, n + 1);
  if (mode === MODE_POSITION) {
    const position = direct(memory, pc, n);
    return memory[position];
  } else if (mode === MODE_IMMEDIATE) {
    return direct(memory, pc, n);
  } else {
    throw new Error("Unknown mode");
  }
};

export const Computer = ({ initialMemory, initialInputs }) => {
  const [memory, setMemory] = useState(initialMemory);
  const [inputs, setInputs] = useState(initialInputs);
  const [outputs, setOutputs] = useState([]);
  const [pc, setPC] = useState(0);
  const [halted, setHalted] = useState(false);
  const [autoRun, setAutoRun] = useState(false);

  const step = useCallback(() => {
    if (halted) {
      return;
    }
    const instruction = memory[pc] % 100;
    if (instruction === OP_ADD) {
      const result = lookup(memory, pc, 1) + lookup(memory, pc, 2);
      const outIndex = direct(memory, pc, 3);
      setMemory(oldMemory => {
        let m = [...oldMemory];
        m[outIndex] = result;
        return m;
      });
      setPC(oldPC => oldPC + 4);
    } else if (instruction === OP_MULT) {
      const result = lookup(memory, pc, 1) * lookup(memory, pc, 2);
      const outIndex = direct(memory, pc, 3);
      setMemory(oldMemory => {
        let m = [...oldMemory];
        m[outIndex] = result;
        return m;
      });
      setPC(oldPC => oldPC + 4);
    } else if (instruction === OP_SAVE) {
      // Save: 1 = INPUT
      const thisInput = inputs[0];
      setInputs(oldInputs => {
        let i = [...oldInputs];
        i.shift();
        return i;
      });
      const outIndex = direct(memory, pc, 1);
      setMemory(oldMemory => {
        let m = [...oldMemory];
        m[outIndex] = thisInput;
        return m;
      });
      setPC(oldPC => oldPC + 2);
    } else if (instruction === OP_WRITE) {
      // Write: Output = 1
      const thisOutput = lookup(memory, pc, 1);
      setOutputs(oldOutputs => {
        let m = [...oldOutputs];
        m.push(thisOutput);
        return m;
      });
      setPC(oldPC => oldPC + 2);
    } else if (instruction === OP_JUMP_IF_TRUE) {
      if (lookup(memory, pc, 1) !== 0) {
        setPC(lookup(memory, pc, 2));
      } else {
        setPC(oldPC => oldPC + 3);
      }
    } else if (instruction === OP_JUMP_IF_FALSE) {
      if (lookup(memory, pc, 1) === 0) {
        setPC(lookup(memory, pc, 2));
      } else {
        setPC(oldPC => oldPC + 3);
      }
    } else if (instruction === OP_LESS_THAN) {
      const result = lookup(memory, pc, 1) < lookup(memory, pc, 2) ? 1 : 0;
      const outIndex = direct(memory, pc, 3);
      setMemory(oldMemory => {
        let m = [...oldMemory];
        m[outIndex] = result;
        return m;
      });
      setPC(oldPC => oldPC + 4);
    } else if (instruction === OP_EQUALS) {
      const result = lookup(memory, pc, 1) === lookup(memory, pc, 2) ? 1 : 0;
      const outIndex = direct(memory, pc, 3);
      setMemory(oldMemory => {
        let m = [...oldMemory];
        m[outIndex] = result;
        return m;
      });
      setPC(oldPC => oldPC + 4);
    } else if (instruction === OP_HALT) {
      setHalted(true);
    }
  }, [halted, inputs, memory, pc]);

  const autoStep = useCallback(() => {
    if (autoRun) {
      step();
    }
  }, [autoRun, step]);

  useInterval(autoStep, 100);

  console.log(memory);
  return (
    <div>
      <div>Computer</div>
      <button className="bg-gray-300 rounded p-2" onClick={() => step()}>
        Step
      </button>
      <button
        className="bg-gray-300 rounded p-2 ml-2"
        onClick={() => setAutoRun(true)}
      >
        Auto Run
      </button>
      <ProgramGrid program={memory} current={pc} />
      <div className="bg-green-200 max-w-md mx-auto rounded p-2">
        Outputs:
        {outputs.map(o => (
          <span className="mx-2">{o}</span>
        ))}
      </div>
    </div>
  );
};
export default Computer;
