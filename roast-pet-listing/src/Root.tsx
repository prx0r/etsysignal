import React from 'react';
import {Composition} from 'remotion';
import {Hero} from './compositions/Hero';
import {CardReveal} from './compositions/CardReveal';
import {PhoneDemo} from './compositions/PhoneDemo';
import {HowItWorks} from './compositions/HowItWorks';
import {Reroll} from './compositions/Reroll';
import pet from './pet.json';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* 2000x2000 Etsy hero still */}
      <Composition
        id="Hero"
        component={Hero}
        durationInFrames={1}
        fps={30}
        width={2000}
        height={2000}
        defaultProps={pet}
      />
      {/* 15s silent listing video, 1920x1080 (Etsy strips audio anyway) */}
      <Composition
        id="ListingVideo"
        component={CardReveal}
        durationInFrames={450}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={pet}
      />
      {/* 9:16 vertical ad for TikTok/Reels */}
      <Composition
        id="VerticalAd"
        component={PhoneDemo}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={pet}
      />
      <Composition
        id="HowItWorks"
        component={HowItWorks}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={pet}
      />
      <Composition
        id="Reroll"
        component={Reroll}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={pet}
      />
    </>
  );
};
