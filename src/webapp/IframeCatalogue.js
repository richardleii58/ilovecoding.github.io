import React from 'react';

const IframeCatalogue = () => {
  return (
    <div>
      {[3, 4, 5, 6, 7, 8, 9, 10, 11].map(n => (
        <iframe
          key={n}
          src={`https://t.me/yahooboohoo/${1 + n}?embed=1`}
          frameBorder="0"
          width="33%"
          height="400px" // Adjust the height as needed
          style={{ marginBottom: '2px' }}
        />
      ))}
    </div>
  );
};

export default IframeCatalogue;
