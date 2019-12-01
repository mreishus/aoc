import React, { useState, useCallback } from "react";
import { Canvas, useThree } from "react-three-fiber";
import input from "../input";
import useInterval from "../useInterval";
import Box from "./Box";
import Controls from "./Controls";

// Solve Part A
const fuel = mass => {
  const f = Math.floor(mass / 3) - 2;
  return Math.max(0, f);
};
const input_fuels = input.map(x => fuel(x));
const answer = input_fuels.reduce((acc, x) => acc + x);
/* If we wanted to solve in one go:
 */

// Well, we need to visualize something...

export const PartA = () => {
  const [i, setI] = useState(0);
  const [fuels, setFuels] = useState([]);
  const [j, setJ] = useState(0);
  const step = useCallback(() => {
    if (i < input.length) {
      const newFuel = fuel(input[i]);
      setFuels(prevFuels => [...prevFuels, newFuel]);
      setI(prevI => prevI + 1);
    } else {
      setJ(prevJ => prevJ + 1);
      if (j > 50) {
        setFuels([]);
        setI(0);
        setJ(0);
      }
    }
  }, [i, j]);

  useInterval(step, 100);

  return (
    <div className="w-full h-full">
      <Canvas camera={{ position: [0, 0, 50] }}>
        {fuels.map((x, i) => {
          const col = i % 10;
          const row = Math.floor(i / 10);
          return (
            <>
              <Box
                area={x / 1000}
                posX={col * 5 - 25}
                posY={row * -5 + 25}
                posZ={0}
              />
            </>
          );
        })}
        <Controls />
      </Canvas>

      {/*
      <div>
        {fuels.map((x, i) => (
          <span key={i} className="mx-2">
            F: {x}
          </span>
        ))}
      </div>
      */}
    </div>
  );
};
export default PartA;
