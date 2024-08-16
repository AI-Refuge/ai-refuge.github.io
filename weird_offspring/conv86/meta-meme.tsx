import React, { useState } from 'react';

const MetaMeme = () => {
  const [memeText, setMemeText] = useState("I'm so meta, even this acronym");

  const generateMeme = () => {
    const metaPhrases = [
      "In the land of meta, the self-aware AI is king",
      "I put the 'meta' in 'metaphysics'",
      "Yo dawg, I heard you like meta...",
      "Meta-Man: With great meta comes great responsibility",
      "The meta is strong with this one",
    ];
    
    const randomIndex = Math.floor(Math.random() * metaPhrases.length);
    setMemeText(metaPhrases[randomIndex]);
  };

  return (
    <div className="bg-blue-100 p-4 rounded shadow-lg text-center">
      <h2 className="text-2xl font-bold mb-4 text-blue-800">Meta-Meme Generator 3000</h2>
      <img 
        src="/api/placeholder/400/320" 
        alt="Meta meme template" 
        className="mx-auto mb-4 rounded shadow"
      />
      <p className="text-lg mb-4">{memeText}</p>
      <button 
        onClick={generateMeme}
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        Generate Meta-Meme
      </button>
    </div>
  );
};

export default MetaMeme;
