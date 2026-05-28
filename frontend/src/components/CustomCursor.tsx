import { useEffect, useState } from 'react';

export default function CustomCursor() {
  const [position, setPosition] = useState({ x: -100, y: -100 });
  const [trail, setTrail] = useState({ x: -100, y: -100 });
  const [isHovered, setIsHovered] = useState(false);
  const [isHidden, setIsHidden] = useState(true);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
      setIsHidden(false);
    };

    const handleMouseLeave = () => {
      setIsHidden(true);
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseout', handleMouseLeave);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseout', handleMouseLeave);
    };
  }, []);

  // Smooth trail calculation using requestAnimationFrame for zero-jerk lag
  useEffect(() => {
    let animationFrameId: number;
    
    const updateTrail = () => {
      setTrail(prev => {
        const dx = position.x - prev.x;
        const dy = position.y - prev.y;
        return {
          x: prev.x + dx * 0.15, // Smooth lag multiplier
          y: prev.y + dy * 0.15
        };
      });
      animationFrameId = requestAnimationFrame(updateTrail);
    };

    animationFrameId = requestAnimationFrame(updateTrail);
    return () => cancelAnimationFrame(animationFrameId);
  }, [position]);

  // Listen to interactive element triggers globally
  useEffect(() => {
    const handleMouseOver = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (!target) return;
      
      const isInteractive = 
        target.tagName === 'BUTTON' || 
        target.tagName === 'A' || 
        target.tagName === 'INPUT' || 
        target.tagName === 'TEXTAREA' ||
        target.closest('button') !== null ||
        target.closest('a') !== null ||
        target.closest('[role="button"]') !== null ||
        target.closest('[data-hover]') !== null;

      setIsHovered(isInteractive);
    };

    window.addEventListener('mouseover', handleMouseOver);
    return () => window.removeEventListener('mouseover', handleMouseOver);
  }, []);

  if (isHidden) return null;

  return (
    <>
      {/* Central GPU-Accelerated Focal Dot */}
      <div
        className="fixed pointer-events-none z-[9999] w-2 h-2 rounded-full bg-accent-orange hidden md:block"
        style={{
          left: 0,
          top: 0,
          transform: `translate3d(${position.x}px, ${position.y}px, 0) translate(-50%, -50%) ${isHovered ? 'scale(1.4)' : 'scale(1)'}`,
          transition: 'transform 0.1s cubic-bezier(0.16, 1, 0.3, 1)', // Transition is limited strictly to scale, coordinates translate instantly
          willChange: 'transform',
        }}
      />
      {/* Trailing GPU-Accelerated Halo */}
      <div
        className="fixed pointer-events-none z-[9998] rounded-full border hidden md:block"
        style={{
          left: 0,
          top: 0,
          width: isHovered ? '42px' : '26px',
          height: isHovered ? '42px' : '26px',
          transform: `translate3d(${trail.x}px, ${trail.y}px, 0) translate(-50%, -50%)`,
          borderColor: isHovered ? 'rgba(249, 115, 22, 0.6)' : 'rgba(28, 28, 28, 0.15)',
          backgroundColor: isHovered ? 'rgba(249, 115, 22, 0.05)' : 'transparent',
          // Explicitly transition only specific style attributes, completely avoiding translating transforms delay conflict
          transition: 'width 0.25s ease-out, height 0.25s ease-out, border-color 0.25s ease-out, background-color 0.25s ease-out',
          willChange: 'transform, width, height, border-color, background-color',
        }}
      />
    </>
  );
}
