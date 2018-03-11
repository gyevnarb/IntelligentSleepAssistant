import React, { Component } from 'react';
import {Card, CardTitle} from 'material-ui/Card'
import LinePlot from './LinePlot'
import TurnKnob from './TurnKnob'
import Dialog from 'material-ui/Dialog'

export default class Cards extends Component {
  state = {
      cardSelected: null
  }

  getElement = (card, width, height) => {
    if (card.element === 'LinePlot')
        return (<LinePlot
            height={!height?(card.title||card.subtitle)?300-18:300:height}
            width={width||300}
            {...card}
        />)
    if (card.element === 'TurnKnob')
        return (
            <TurnKnob
                {...card}
            />
        )
    if (card.element === 'html')
        return card.html
  }

  render() {
    return (
      <div style={{
          display:'flex',
          flexDirection:'row',
          flexWrap:'wrap',
          justifyContent:'center',
          paddingLeft:'15%',
          paddingRight:'15%',
          ...this.props.style
      }}>
          {
              this.props.cards.map((card,i) => (
                <Card key={i} style={{
                    width:350,
                    height:350,
                    margin:10
                }}
                containerStyle={{height:'calc(100% - '+ (card.title||card.subtitle?68:0) +'px)'}}
                onClick={() => card.element === 'LinePlot'&&this.setState({cardSelected:card})}
                {...card.cardProps}>
                    {(card.title||card.subtitle)&&
                        <CardTitle title={card.title} subtitle={card.subtitle}/>
                    }
                    <div style={{
                        height:'100%',
                        display:'flex',
                        justifyContent:'center',
                        alignItems:'center',
                    }}>
                        {this.getElement(card)}
                    </div>
                </Card>
              ))
          }
          <Dialog open={!!this.state.cardSelected} onRequestClose={() => this.setState({cardSelected:null})} bodyStyle={{}}>{
            <Card style={{
                width:'700px',
                height:'500px'
            }}
            zDepth={0}
            containerStyle={{height:'calc(100% - '+ (this.state.cardSelected&&(this.state.cardSelected.title||this.state.cardSelected.subtitle)?68:0) +'px)'}}
            onClick={() => this.setState({cardSelected:null})}
            {...this.state.cardSelected&&this.state.cardSelected.cardProps}>
                {this.state.cardSelected&&<div>
                    {(this.state.cardSelected.title||this.state.cardSelected.subtitle)&&
                        <CardTitle title={this.state.cardSelected.title} subtitle={this.state.cardSelected.subtitle}/>
                    }
                    <div style={{
                        height:'100%',
                        display:'flex',
                        justifyContent:'center',
                        alignItems:'center',
                    }}>
                        {this.getElement(this.state.cardSelected, 670, 500-68)}
                    </div>
                </div>}
            </Card>
          }
          </Dialog>
      </div>
    );
  }
}
