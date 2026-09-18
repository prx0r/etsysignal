import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {PetProps} from './types';

/**
 * CardReveal — the 15s silent listing video.
 * photo -> card -> phone scan -> show erupts -> YOUR PET. THEIR OWN COMEDY SHOW.
 * No audio dependency: Etsy strips it. Giant subtitles only.
 */
const SUBS = [
  {from: 0, to: 60, text: ''},
  {from: 60, to: 120, text: 'A CARD'},
  {from: 120, to: 180, text: 'SCAN IT'},
  {from: 180, to: 300, text: ''},
  {from: 300, to: 450, text: 'YOUR PET. THEIR OWN COMEDY SHOW.'},
];

export const CardReveal: React.FC<PetProps> = (pet) => {
  const frame = useCurrentFrame();
  const sub = SUBS.find((s) => frame >= s.from && frame < s.to);
  const erupt = interpolate(frame, [120, 200], [0, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{backgroundColor: '#14141E'}}>
      <div style={{position: 'absolute', inset: 0, opacity: 1 - erupt, backgroundColor: '#F5F0E6'}}>
        <div style={{fontSize: 120, fontWeight: 900, padding: 120}}>
          {pet.headline}<br />{pet.subheadline}
        </div>
      </div>
      <div style={{position: 'absolute', inset: 0, opacity: erupt, backgroundColor: '#14141E'}}>
        <div style={{fontSize: 150, fontWeight: 900, color: '#FFDC78', padding: 120}}>
          {pet.petName} TAKES THE PODIUM
        </div>
      </div>
      {sub?.text ? (
        <div
          style={{
            position: 'absolute', bottom: 80, left: 0, right: 0,
            textAlign: 'center', fontSize: 96, fontWeight: 900,
            color: '#FFF', textShadow: '0 6px 0 #000',
          }}
        >
          {sub.text}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
