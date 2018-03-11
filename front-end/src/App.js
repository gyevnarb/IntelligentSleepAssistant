import React, { Component } from 'react';
import '../node_modules/react-vis/dist/style.css';
import AppBar from 'material-ui/AppBar';
import Cards from './Cards';
import {getAll} from './api'
import _ from 'lodash'

class App extends Component {
  state={
    cards:[]
  }

  componentDidMount = () => {
    getAll().then(json => {
      this.setState(({cards}) => ({
        cards:[
          {
            title:'Temperature',
            element:'LinePlot',
            data:_.zip(json.dateTime, json.tempData),
            xType:'time-utc',
            yDomain:[0,45]
          },
          {
            title:'Air Data',
            element:'LinePlot',
            data:_.zip(json.dateTime, json.airData),
            xType:'time-utc',
            yDomain:[0,1]
          },
          {
            title:'Light Data',
            element:'LinePlot',
            data:_.zip(json.dateTime, json.lightData),
            xType:'time-utc',
            yDomain:[0,1]
          },
          {
            title:'M O I S T',
            element:'LinePlot',
            data:_.zip(json.dateTime, json.moistureData),
            xType:'time-utc',
            yDomain:[0,1]
          },
          {
            title:'Some Setting',
            element:'TurnKnob',
            value:10,
            min:10,
            max:40,
            colorMin:'#FF0000',
            colorMax:'#00FF00',
            onChange:val => this.setState(prev => ({
              cards:[
                ...prev.cards.slice(0,4),
                {
                  ...prev.cards[4],
                  value:val
                }
              ]
            }))
          }
        ]
      }))
    })
  }

  render() {
    return (
      <div>
        <AppBar title="Intelligent Sleep Assistant"/>
        <Cards 
          cards={this.state.cards}
          style={{margin:10}}
        />
      </div>
    );
  }
}

export default App;
