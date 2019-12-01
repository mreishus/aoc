import React, { useRef } from "react";
import { useFrame } from "react-three-fiber";

export const Box = ({ area, posX, posY, posZ }) => {
  const side = Math.cbrt(area);
  const ref = useRef();
  useFrame(() => (ref.current.rotation.x = ref.current.rotation.y += 0.02));
  return (
    <>
      <mesh ref={ref} position={[posX, posY, posZ]}>
        <boxBufferGeometry attach="geometry" args={[side, side, side]} />
        <meshNormalMaterial attach="material" />
      </mesh>
    </>
  );
};
export default Box;
