import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {PetProps} from './types';

/** HowItWorks — UPLOAD → WE ROAST → DELIVERED in three beats. */
const STEPS = ['UPLOAD 4 PHOTOS + GOSSIP', 'WE ROAST. CARD PRINTS.', 'SCAN. SHOW PLAYS.'];

export const HowItWorks: React.FC<PetProps> = () => {
  return (
    <AbsoluteFill style={{backgroundColor: '#F5F0E6', flexDirection: 'row', alignItems: 'center', justifyContent: 'center'}}>
      {STEPS.map((s, i) => (
        <Sequence key={s} from={i * 100} durationInFrames={300 - i * 100}>
          <div style={{margin: 40, padding: 60, backgroundColor: '#14141E', color: '#FFF', fontSize: 64, fontWeight: 900, maxWidth: 500}}>
            {i + 1}. {s}
          </div>
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
