// TelegramWidget.js
import React, { useEffect } from 'react';

const TelegramWidget = ({ post, width = '100%', userpic = 'true' }) => {
  useEffect(() => {
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://telegram.org/js/telegram-widget.js?22';
    script.setAttribute('data-telegram-post', post);
    script.setAttribute('data-width', width);
    script.setAttribute('data-userpic', userpic);
    document.getElementById(`telegram-widget-container-${post}`).appendChild(script);
  }, [post, width, userpic]);

  return <div id={`telegram-widget-container-${post}`}></div>;
};

export default TelegramWidget;
