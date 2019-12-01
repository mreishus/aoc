import React, { useRef } from "react";

export const StillBox = ({ area, posX, posY, posZ }) => {
  const side = Math.cbrt(area);
  const ref = useRef();
  return (
    <>
      <mesh ref={ref} position={[posX, posY, posZ]}>
        <boxBufferGeometry attach="geometry" args={[side, side, side]} />
        <meshNormalMaterial attach="material" />
      </mesh>
    </>
  );
};
export default StillBox;
