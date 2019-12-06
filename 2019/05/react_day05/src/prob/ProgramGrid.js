import React from "react";
import cx from "classnames";

export const ProgramGrid = ({ program, current, in1, in2, out1 }) => {
  console.log(program);
  return (
    <div className="container mx-auto">
      <div>ProgramGrid</div>
      {program.map((x, i) => {
        // const col = i % 10;
        // const row = Math.floor(i / 10);
        return (
          <div
            className={cx("inline-block h-8 w-12 rounded m-1 text-lg", {
              "bg-red-400 font-semibold": i === current,
              "bg-green-400": i === in1 || i === in2,
              "bg-purple-400": i === out1,
              "bg-blue-200":
                i !== current && i !== in1 && i !== in2 && i !== out1
            })}
            key={i}
          >
            {x}
          </div>
        );
      })}
    </div>
  );
};
export default ProgramGrid;
