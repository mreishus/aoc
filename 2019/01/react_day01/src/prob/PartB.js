import React, { useState, useCallback } from "react";
import { Canvas } from "react-three-fiber";
import input from "../input";
import useInterval from "../useInterval";
import StillBox from "./StillBox";
import Controls from "./Controls";

// Solve Part A
const fuel = mass => {
  const f = Math.floor(mass / 3) - 2;
  return Math.max(0, f);
};
const fuel_total = mass => {
  let total = 0;
  let parts = [];
  let this_fuel = mass;
  while (1) {
    this_fuel = fuel(this_fuel);
    if (this_fuel <= 0) {
      break;
    }
    parts.push(this_fuel);
    total += this_fuel;
  }
  return { total, parts };
};

// Well, we need to visualize something...

export const PartB = () => {
  const [i, setI] = useState(0);
  const [fuels, setFuels] = useState([]);
  const [j, setJ] = useState(0);
  const step = useCallback(() => {
    if (i < input.length) {
      const newFuel = fuel_total(input[i]);
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
        {fuels.map((fuel_item, i) => {
          const col = i % 10;
          const row = Math.floor(i / 10);
          return (
            <>
              {fuel_item.parts.map((x, j) => (
                <StillBox
                  area={x / 1000}
                  posX={col * 5 - 25 + j * 0.25}
                  posY={row * -5 + 25 + j * 0.25}
                  posZ={j * 1}
                />
              ))}
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
export default PartB;
