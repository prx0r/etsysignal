import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {PetProps} from './types';

/**
 * Supercut — V2 listing video (northstar.md): sell the comedy, explain nothing.
 * Rapid cuts: PET ROASTS TARGET × 3, audience insane, YOUR PET. YOUR ROAST.
 * 450 frames @ 30fps. Silent. Props carry three roast cards + end title.
 */
export type SupercutProps = PetProps & {
  cuts?: {pet: string; target: string; line: string}[];
};

export const Supercut: React.FC<SupercutProps> = (pet) => {
  const cuts = pet.cuts ?? [
    {pet: pet.petName, target: pet.recipient, line: pet.punchline},
  ];
  const per = Math.floor(360 / Math.max(cuts.length, 1));
  return (
    <AbsoluteFill style={{backgroundColor: '#14141E'}}>
      {cuts.map((c, i) => (
        <Sequence key={`${c.pet}-${i}`} from={i * per} durationInFrames={per}>
          <AbsoluteFill style={{justifyContent: 'center', padding: 120}}>
            <div style={{color: '#FFDC78', fontSize: 72, fontWeight: 900}}>
              {c.pet.toUpperCase()} ROASTS {c.target.toUpperCase()}
            </div>
            <div style={{color: '#FFF', fontSize: 96, fontWeight: 900, marginTop: 40}}>
              “{c.line}”
            </div>
          </AbsoluteFill>
        </Sequence>
      ))}
      <Sequence from={360} durationInFrames={90}>
        <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', backgroundColor: '#B41E1E'}}>
          <div style={{color: '#FFF', fontSize: 120, fontWeight: 900}}>
            YOUR PET. YOUR ROAST.
          </div>
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};
