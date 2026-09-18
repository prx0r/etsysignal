import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {PetProps} from './types';

/** PhoneDemo — 9:16 vertical: podium frame, opening line, punchline, crowd. */
export const PhoneDemo: React.FC<PetProps> = (pet) => {
  const frame = useCurrentFrame();
  const punch = interpolate(frame, [90, 120], [0, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  return (
    <AbsoluteFill style={{backgroundColor: '#EBE6DA', alignItems: 'center'}}>
      <div style={{marginTop: 200, width: 800, height: 1300, backgroundColor: '#14141E', borderRadius: 60, padding: 60}}>
        <div style={{color: '#FFDC78', fontSize: 56, fontWeight: 800}}>
          THE ROAST — {pet.petName} AT THE PODIUM
        </div>
        <div style={{color: '#FFF', fontSize: 72, fontWeight: 900, marginTop: 60, opacity: punch}}>
          “{pet.punchline}”
        </div>
        <div style={{color: '#FFDC78', fontSize: 56, marginTop: 60, opacity: punch}}>
          WOOF WOOF WOOF WOOOOOF
        </div>
      </div>
    </AbsoluteFill>
  );
};
