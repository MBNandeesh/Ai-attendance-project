"use client";

import { Canvas, useFrame } from "@react-three/fiber";
import { useMemo, useRef } from "react";
import * as THREE from "three";

/* Particle field with subtle connection lines — calm, professional motion */
function ParticleField() {
  const group = useRef<THREE.Group>(null);

  const { points, lineGeometry } = useMemo(() => {
    const COUNT = 90;
    const positions = new Float32Array(COUNT * 3);
    const velocities: { x: number; y: number; z: number }[] = [];

    for (let i = 0; i < COUNT; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 24;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 14;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 10 - 2;
      velocities.push({
        x: (Math.random() - 0.5) * 0.006,
        y: (Math.random() - 0.5) * 0.006,
        z: (Math.random() - 0.5) * 0.004,
      });
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));

    // static connective lattice (cosmetic, faint)
    const linePositions: number[] = [];
    for (let i = 0; i < COUNT; i++) {
      for (let j = i + 1; j < COUNT; j++) {
        const dx = positions[i * 3] - positions[j * 3];
        const dy = positions[i * 3 + 1] - positions[j * 3 + 1];
        const dz = positions[i * 3 + 2] - positions[j * 3 + 2];
        if (dx * dx + dy * dy + dz * dz < 6.5) {
          linePositions.push(
            positions[i * 3], positions[i * 3 + 1], positions[i * 3 + 2],
            positions[j * 3], positions[j * 3 + 1], positions[j * 3 + 2],
          );
        }
      }
    }
    const lineGeometry = new THREE.BufferGeometry();
    lineGeometry.setAttribute("position", new THREE.Float32BufferAttribute(linePositions, 3));

    return { points: { geometry, velocities }, lineGeometry };
  }, []);

  useFrame((state, delta) => {
    const attr = points.geometry.getAttribute("position") as THREE.BufferAttribute;
    const arr = attr.array as Float32Array;

    for (let i = 0; i < arr.length / 3; i++) {
      const v = points.velocities[i];
      arr[i * 3] += v.x * delta * 60;
      arr[i * 3 + 1] += v.y * delta * 60;
      arr[i * 3 + 2] += v.z * delta * 60;

      // wrap around bounds
      if (Math.abs(arr[i * 3]) > 12) v.x *= -1;
      if (Math.abs(arr[i * 3 + 1]) > 7) v.y *= -1;
      if (Math.abs(arr[i * 3 + 2] + 2) > 5) v.z *= -1;
    }
    attr.needsUpdate = true;

    if (group.current) {
      const { x, y } = state.pointer;
      group.current.rotation.y += (x * 0.08 - group.current.rotation.y) * 0.02;
      group.current.rotation.x += (-y * 0.05 - group.current.rotation.x) * 0.02;
    }
  });

  return (
    <group ref={group}>
      <points>
        <primitive object={points.geometry} attach="geometry" />
        <pointsMaterial size={0.055} color="#5b7cfa" transparent opacity={0.75} sizeAttenuation />
      </points>
      <lineSegments>
        <primitive object={lineGeometry} attach="geometry" />
        <lineBasicMaterial color="#3a4a7a" transparent opacity={0.14} />
      </lineSegments>
    </group>
  );
}

/* Large slow-rotating wireframe icosahedron — depth anchor */
function WireframeSolid() {
  const ref = useRef<THREE.Mesh>(null);
  useFrame((_, delta) => {
    if (ref.current) {
      ref.current.rotation.y += delta * 0.05;
      ref.current.rotation.x += delta * 0.018;
    }
  });
  return (
    <mesh ref={ref} position={[0, 0, -6]}>
      <icosahedronGeometry args={[4.2, 1]} />
      <meshBasicMaterial color="#2a3560" wireframe transparent opacity={0.16} />
    </mesh>
  );
}

export default function BackgroundCanvas() {
  return (
    <div className="fixed inset-0 -z-10" aria-hidden>
      <Canvas
        camera={{ position: [0, 0, 8], fov: 55 }}
        dpr={[1, 1.6]}
        gl={{ antialias: true, alpha: true, powerPreference: "low-power" }}
        style={{ background: "transparent" }}
      >
        <ParticleField />
        <WireframeSolid />
      </Canvas>
    </div>
  );
}
