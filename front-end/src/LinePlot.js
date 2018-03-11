import React, { Component } from 'react';
import {XYPlot, XAxis, YAxis, HorizontalGridLines, LineSeries} from 'react-vis';

export default class LinePlot extends Component {

    render() {
      return (
        <XYPlot
            width={300}
            height={300}
            {...this.props}>
            <HorizontalGridLines />
            <LineSeries
              color="red"
              data={this.props.data.map(d => ({x:d[0], y:d[1]}) )}
            />
            <XAxis title="X" />
            <YAxis />
        </XYPlot>
      );
    }
  }
  