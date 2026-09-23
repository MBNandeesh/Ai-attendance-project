"use client";

import { Canvas, useFrame } from "@react-three/fiber";
import { Float, Environment, ContactShadows, Sparkles } from "@react-three/drei";
import { useMemo, useRef } from "react";
import * as THREE from "three";

/* ---------------------------------------------------------- */
/* A rotating glassy torus-knot "orb" — the hero centerpiece  */
/* ---------------------------------------------------------- */
function HeroOrb() {
  const mesh = useRef<THREE.Mesh>(null);
  const ring1 = useRef<THREE.Mesh>(null);
  const ring2 = useRef<THREE.Mesh>(null);

  useFrame((state, delta) => {
    const t = state.clock.elapsedTime;
    if (mesh.current) {
      mesh.current.rotation.x += delta * 0.25;
      mesh.current.rotation.y += delta * 0.35;
    }
    if (ring1.current) {
      ring1.current.rotation.z = t * 0.5;
      ring1.current.rotation.x = Math.sin(t * 0.4) * 0.35 + 1.2;
    }
    if (ring2.current) {
      ring2.current.rotation.z = -t * 0.35;
      ring2.current.rotation.y = Math.cos(t * 0.3) * 0.4 + 0.6;
    }
    // gentle mouse parallax on the whole group
    if (mesh.current?.parent) {
      const { x, y } = state.pointer;
      mesh.current.parent.rotation.y += (x * 0.25 - mesh.current.parent.rotation.y) * 0.04;
      mesh.current.parent.rotation.x += (-y * 0.15 - mesh.current.parent.rotation.x) * 0.04;
    }
  });

  return (
    <group>
      <Float speed={2} rotationIntensity={0.4} floatIntensity={1.1}>
        <mesh ref={mesh}>
          <torusKnotGeometry args={[1.05, 0.34, 220, 36]} />
          <meshPhysicalMaterial
            color="#6366f1"
            metalness={0.85}
            roughness={0.18}
            clearcoat={1}
            clearcoatRoughness={0.15}
            emissive="#312e81"
            emissiveIntensity={0.45}
          />
        </mesh>
      </Float>

      {/* orbiting scan rings */}
      <mesh ref={ring1}>
        <torusGeometry args={[1.9, 0.015, 16, 128]} />
        <meshBasicMaterial color="#22d3ee" transparent opacity={0.85} />
      </mesh>
      <mesh ref={ring2}>
        <torusGeometry args={[2.25, 0.01, 16, 128]} />
        <meshBasicMaterial color="#a78bfa" transparent opacity={0.55} />
      </mesh>

      {/* orbiting satellite spheres */}
      <Satellite radius={1.9} speed={0.9} offset={0} color="#22d3ee" size={0.09} />
      <Satellite radius={1.9} speed={0.9} offset={Math.PI} color="#a3e635" size={0.07} />
      <Satellite radius={2.25} speed={-0.6} offset={1.2} color="#fbbf24" size={0.06} />
    </group>
  );
}

function Satellite({
  radius,
  speed,
  offset,
  color,
  size,
}: {
  radius: number;
  speed: number;
  offset: number;
  color: string;
  size: number;
}) {
  const ref = useRef<THREE.Mesh>(null);
  useFrame(({ clock }) => {
    const t = clock.elapsedTime * speed + offset;
    if (ref.current) {
      ref.current.position.set(Math.cos(t) * radius, Math.sin(t) * radius * 0.35, Math.sin(t) * radius * 0.6);
    }
  });
  return (
    <mesh ref={ref}>
      <sphereGeometry args={[size, 24, 24]} />
      <meshBasicMaterial color={color} />
    </mesh>
  );
}

/* ------------------------------------------------------------ */
/* Floating face-recognition "tiles" — scanning frame wireframe */
/* ------------------------------------------------------------ */
function ScanFrame() {
  const ref = useRef<THREE.Group>(null);
  useFrame(({ clock }) => {
    if (ref.current) {
      ref.current.rotation.y = Math.sin(clock.elapsedTime * 0.4) * 0.3;
    }
  });
  return (
    <group ref={ref} position={[0, 0, 0]}>
      <Float speed={1.5} floatIntensity={0.8}>
        <mesh position={[-3.4, 0.9, -1.2]} rotation={[0.2, 0.5, 0.1]}>
          <boxGeometry args={[1.15, 1.45, 0.04]} />
          <meshBasicMaterial color="#6366f1" wireframe transparent opacity={0.35} />
        </mesh>
      </Float>
      <Float speed={1.8} floatIntensity={1}>
        <mesh position={[3.5, -0.7, -0.8]} rotation={[-0.15, -0.4, -0.08]}>
          <boxGeometry args={[0.95, 1.25, 0.04]} />
          <meshBasicMaterial color="#22d3ee" wireframe transparent opacity={0.3} />
        </mesh>
      </Float>
    </group>
  );
}

/* ---------------------------------------------------------- */
/* Full canvas                                                */
/* ---------------------------------------------------------- */
export default function HeroScene() {
  return (
    <div className="absolute inset-0 -z-10">
      <Canvas
        camera={{ position: [0, 0, 6.2], fov: 50 }}
        dpr={[1, 1.8]}
        gl={{ antialias: true, alpha: true }}
        style={{ background: "transparent" }}
      >
        <ambientLight intensity={0.35} />
        <pointLight position={[6, 5, 6]} intensity={60} color="#818cf8" />
        <pointLight position={[-6, -3, 4]} intensity={40} color="#22d3ee" />
        <spotLight position={[0, 7, 3]} angle={0.5} intensity={50} color="#a78bfa" />

        <HeroOrb />
        <ScanFrame />

        <Sparkles count={130} scale={[11, 7, 6]} size={2.2} speed={0.35} color="#9aa3ff" opacity={0.65} />

        <ContactShadows position={[0, -2.4, 0]} opacity={0.4} scale={12} blur={2.6} color="#1e1b4b" />
        <Environment preset="city" />
      </Canvas>
    </div>
  );
}
