import React from 'react';
import './App.css';
import TelegramWidget from './TelegramWidget';
//import './styles.css';
import TelegramEmbed from 'react-telegram-embed';
import HomePage from './HomePage';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    
    <div className="App">
      <div>
      <h1>I dont want to do this anymore</h1>
      {/* <TelegramWidget /> */}
    </div>
      <h1>Let's get clearing!</h1>
      <h2>Join our Telegram channels for real time updates!</h2>
      {/* {[3, 4, 5, 6, 7].map(n => {
        return <iframe key={n} src={`https://t.me/yahooboohoo/${1 + n}?embed=1`} frameBorder="0" />
      })} */}
      <div>
      <HomePage />
     </div>
      <div className="container bootstrap snippets">
        <h1 className="text-center text-muted">Product catalog</h1>
        <div className="row flow-offset-1">
          <div className="col-xs-6 col-md-4">
            <div className="product tumbnail thumbnail-3"><a href="#/"><img src="https://www.bootdey.com/image/350x280/FFB6C1/000000" alt=""/></a>
              <div className="caption">
                <h6><a href="#/">Short Sleeve T-Shirt</a></h6><span className="price">
                  <del>$24.99</del></span><span className="price sale">$12.49</span>
              </div>
            </div>
          </div>
          <div className="col-xs-6 col-md-4">
            <div className="product tumbnail thumbnail-3"><a href="#/"><img src="https://www.bootdey.com/image/350x280/87CEFA/000000" alt=""/></a>
              <div className="caption">
                <h6><a href="#/">Short Sleeve T-Shirt</a></h6><span className="price">
                  <del>$24.99</del></span><span className="price sale">$12.49</span>
              </div>
            </div>
          </div>
          <div className="col-xs-6 col-md-4">
            <div className="product tumbnail thumbnail-3"><a href="#/"><img src="https://www.bootdey.com/image/350x280/FF7F50/000000" alt=""/></a>
              <div className="caption">
                <h6><a href="#/">Short Sleeve T-Shirt</a></h6><span className="price">$12.49</span>
              </div>
            </div>
          </div>
          <div className="col-xs-6 col-md-4">
            <div className="product tumbnail thumbnail-3"><a href="#/"><img src="https://www.bootdey.com/image/350x280/20B2AA/000000" alt=""/></a>
              <div className="caption">
                <h6><a href="#/">Short Sleeve T-Shirt</a></h6><span className="price">
                  <del>$24.99</del></span><span className="price sale">$12.49</span>
              </div>
              </div>
            </div>
        </div>
      </div>
    </div>
  );
}

export default App;
