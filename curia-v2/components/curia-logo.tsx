import React from "react";

export function CuriaLogo({ className = "" }: { className?: string }) {
  return (
    <svg 
      width="120" 
      height="50" 
      viewBox="0 0 120 50" 
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
    <g transform="translate(0,3.5), scale(1.2,1.2)">
      {/* Rotated and repositioned yellow wave with more flow */}
      <g transform="translate(29, 34) rotate(-12) scale(0.9, 0.9)">
        <path 
          d="M-5 0 Q10 -10 22 0 Q35 12 48 -5 Q55 5 58 -2" 
          stroke="oklch(92.627% 0.1247 98.494)" 
          strokeWidth="9" 
          fill="none" 
          strokeLinecap="round" 
          strokeLinejoin="round"
        />
      </g>
      
      {/* Reordered text elements with better flow */}
      <g transform="translate(4, 30) scale(1.2,1.2)">
        {/* "C" */}
        <text 
          x="-5.5" 
          y="0" 
          fontFamily="'Bodoni Moda', 'Baskerville', serif" 
          fontSize="30"
          fontWeight="600"
          fill="currentColor"
          style={{ filter: "drop-shadow(0px 1px 0.5px rgba(0,0,0,0.05))" }}
          transform="scale(0.85, 1) skewX(-1)"
        >
          C
        </text>
    </g>
    <g transform="translate(4, 30)">

        {/* "u" */}
        <text 
          x="18" 
          y="0" 
          fontFamily="'Bodoni Moda', 'Baskerville', serif" 
          fontSize="32"
          fontWeight="600"
          letterSpacing="-0.6"
          fill="currentColor"
          style={{ filter: "drop-shadow(0px 1px 0.5px rgba(0,0,0,0.05))" }}
          transform="scale(0.85, 1) skewX(-1)"
        >
          u
        </text>
        
        {/* "r" */}
        <text 
          x="38" 
          y="0" 
          fontFamily="'Bodoni Moda', 'Baskerville', serif" 
          fontSize="32"
          fontWeight="600"
          letterSpacing="-0.6"
          fill="currentColor"
          style={{ filter: "drop-shadow(0px 1px 0.5px rgba(0,0,0,0.05))" }}
          transform="scale(0.85, 1) skewX(-1)"
        >
          r
        </text>
        
        {/* "i" positioned after the curve */}
        <text 
          x="52.5" 
          y="0" 
          fontFamily="'Bodoni Moda', 'Baskerville', serif" 
          fontSize="32"
          fontWeight="600"
          fill="currentColor"
          style={{ filter: "drop-shadow(0px 1px 0.5px rgba(0,0,0,0.05))" }}
          transform="scale(0.85, 1) skewX(-1)"
        >
          i
        </text>
        
        {/* "a" */}
        <text 
          x="62" 
          y="0" 
          fontFamily="'Bodoni Moda', 'Baskerville', serif" 
          fontSize="32"
          fontWeight="600"
          fill="currentColor"
          style={{ filter: "drop-shadow(0px 1px 0.5px rgba(0,0,0,0.05))" }}
          transform="scale(0.85, 1) skewX(-1)"
        >
          a
        </text>
      </g>
      </g>
    </svg>
  );
}