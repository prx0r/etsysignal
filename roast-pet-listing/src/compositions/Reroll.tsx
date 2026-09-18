import React from 'react';
import {AbsoluteFill} from 'remotion';
import {PetProps} from './types';

/** Reroll — Take 1 ↔ Take 2, 1 FREE REROLL. */
export const Reroll: React.FC<PetProps> = (pet) => {
  return (
    <AbsoluteFill style={{backgroundColor: '#14141E', flexDirection: 'row', alignItems: 'center', justifyContent: 'center'}}>
      <div style={{margin: 40, padding: 60, backgroundColor: '#333', color: '#FFF', fontSize: 72, fontWeight: 900}}>
        TAKE 1<br />{pet.take1Label ?? 'Original'}
      </div>
      <div style={{margin: 40, padding: 60, backgroundColor: '#B41E1E', color: '#FFF', fontSize: 72, fontWeight: 900}}>
        TAKE 2<br />{pet.take2Label ?? 'Meaner'}
      </div>
      <div style={{position: 'absolute', bottom: 80, color: '#FFDC78', fontSize: 80, fontWeight: 900}}>
        1 FREE REROLL — YOU KEEP BOTH
      </div>
    </AbsoluteFill>
  );
};
