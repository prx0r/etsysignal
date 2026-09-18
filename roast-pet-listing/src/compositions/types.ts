/** One visual engine: change pet.json, re-render everything. */
export type PetProps = {
  petName: string;
  recipient: string;
  occasion: string;
  headline: string;
  subheadline: string;
  punchline: string;
  signoff: string;
  qrUrl: string;
  cardFront?: string;
  showFrame?: string;
  take1Label?: string;
  take2Label?: string;
};
