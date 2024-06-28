// TelegramWidgetCatalogue.js
import React from 'react';
import TelegramWidget from './TelegramWidget';

const widgetConfigs = [
  { post: 'yahooboohoo', width: '80%', userpic: 'true' },
  { post: 'yahooboohoo/5', width: '100%', userpic: 'true' },
  { post: 'yahooboohoo/6', width: '100%', userpic: 'true' },
  // Add more widget configurations here
];

const TelegramWidgetCatalogue = () => {
  return (
    <div>
      {widgetConfigs.map((config, index) => (
        <div key={index} style={{ marginBottom: '20px' }}>
          <TelegramWidget post={config.post} width={config.width} userpic={config.userpic} />
        </div>
      ))}
    </div>
  );
};

export default TelegramWidgetCatalogue;
