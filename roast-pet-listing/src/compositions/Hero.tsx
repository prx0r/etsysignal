import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {PetProps} from './types';

/**
 * Hero — the Etsy thumbnail master (2000x2000).
 * Concept A "Magic card": physical card bottom-left, phone top-right,
 * eruption beam connecting them, headline band.
 * Zones must match listing/thumbs/A_spec.json.
 */
export const Hero: React.FC<PetProps> = (pet) => {
  return (
    <AbsoluteFill style={{backgroundColor: '#EBE6DA'}}>
      {/* phone: late-night set frame */}
      <div
        style={{
          position: 'absolute', left: 950, top: 250, width: 800, height: 1200,
          backgroundColor: '#14141E', borderRadius: 48,
        }}
      >
        {pet.showFrame ? (
          <Img src={staticFile(pet.showFrame)} style={{width: '100%', borderRadius: 48}} />
        ) : (
          <div style={{color: '#FFF', fontSize: 64, padding: 60}}>
            {pet.petName} AT THE DESK
          </div>
        )}
      </div>
      {/* eruption beam card -> phone */}
      <div
        style={{
          position: 'absolute', left: 700, top: 450, width: 600, height: 650,
          background: 'linear-gradient(180deg, #FFDC78 0%, rgba(255,220,120,0) 100%)',
        }}
      />
      {/* physical card */}
      <div
        style={{
          position: 'absolute', left: 250, top: 1050, width: 800, height: 800,
          backgroundColor: '#F5F0E6', border: '8px solid #282828',
        }}
      >
        {pet.cardFront ? (
          <Img src={staticFile(pet.cardFront)} style={{width: '100%'}} />
        ) : (
          <div style={{padding: 60, fontSize: 72, fontWeight: 900}}>
            {pet.headline}
            <br />
            {pet.subheadline}
          </div>
        )}
      </div>
      {/* headline band — card print carries the joke, no marketing overlay */}
      <div
        style={{
          position: 'absolute', left: 250, bottom: 150, width: 1500,
          backgroundColor: '#B41E1E', color: '#FFF',
          fontSize: 96, fontWeight: 900, padding: 40,
        }}
      >
        YOUR PET ROASTS YOU
      </div>
    </AbsoluteFill>
  );
};
