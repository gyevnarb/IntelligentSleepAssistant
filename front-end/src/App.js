import React, { Component } from 'react';
import '../node_modules/react-vis/dist/style.css';
import AppBar from 'material-ui/AppBar';
import Cards from './Cards';
import {getAll, getProcessedData} from './api'
import _ from 'lodash'
class App extends Component {
  state={
    cards:[],
    processedData:{}
  }

  refresh = () => {
    getProcessedData().then(json => {
      this.setState({processedData:json})
    });
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
            yDomain:[0,1500]
          },
          {
            title:'Light Data',
            element:'LinePlot',
            data:_.zip(json.dateTime, json.lightData),
            xType:'time-utc',
            yDomain:[0,4000]
          },
          {
            title:'Moisture Data',
            element:'LinePlot',
            data:_.zip(json.dateTime, json.moistureData),
            xType:'time-utc',
            yDomain:[0,100]
          },
          {
            title:'Thermostat',
            element:'TurnKnob',
            value:28,
            min:10,
            max:40,
            colorMin:'#e63b00',
            colorMax:'#00e63b',
            onChange:val => this.setState(prev => ({
              cards:[
                ...prev.cards.slice(0,4),
                {
                  ...prev.cards[4],
                  value:val
                },
                ...prev.cards.slice(5)
              ]
            }))
          },
          {
            title:'Recommended Temperature',
            element:'TurnKnob',
            value:Math.floor(this.state.processedData.tempData),
            min:10,
            max:40,
            readOnly:true,
            colorMin:'#e63b00',
            colorMax:'#00e63b'
          },
          {
            title:'Recommended Air Quality',
            element:'TurnKnob',
            value:Math.floor(this.state.processedData.airData),
            min:0,
            max:1500,
            readOnly:true,
            colorMax:'#e63b00',
            colorMin:'#00e63b'
          },
          {
            title:'Recommended Light Amount',
            element:'TurnKnob',
            value:Math.floor(this.state.processedData.lightData),
            min:0,
            max:4000,
            readOnly:true,
            colorMin:'#e63b00',
            colorMax:'#00e63b'
          },
          {
            title:'Recommended Moisture',
            element:'TurnKnob',
            value:Math.floor(this.state.processedData.moistureData),
            min:0,
            max:100,
            readOnly:true,
            colorMin:'#e63b00',
            colorMax:'#00e63b'
          }
        ]
      }))
    })
  }

  componentDidMount = () => {
    this.refresh();
    this.interval = setInterval(this.refresh,1000)
  }

  componentWillUnmount = () => {
    clearInterval(this.interval)
  }

  render() {
    return (
      <div>
        <AppBar title={<img src="logo.png" style={{height:56, marginTop:4}}></img>}/>
        <Cards 
          cards={this.state.cards}
          style={{margin:10}}
        />
      </div>
    );
  }
}

export default App;
