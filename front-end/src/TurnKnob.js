import React, { Component } from 'react';
import Knob from 'react-canvas-knob';

export default class TurnKnob extends Component {

    render() {
      let color = this.props.color||"#66CC66"
      if (this.props.colorMin && this.props.colorMax) {
          color = this.mixColors(this.props.colorMin, this.props.colorMax, (this.props.value - this.props.min)/(this.props.max-this.props.min))
      }
      return (
          <Knob
            angleArc={250}
            angleOffset={-125}
            fgColor={color}
            lineCap="round"
            {...this.props}
          />
      );
    }

    //https://stackoverflow.com/a/16360660/5236930
    mixColors(c1, c2, ratio) {
      let color1 = c1.charAt(0) === '#'?c1.slice(1):c1
      let color2 = c2.charAt(0) === '#'?c2.slice(1):c2

      let hex = function(x) {
        x = x.toString(16);
        return (x.length === 1) ? '0' + x : x;
      };

      let r = Math.ceil(parseInt(color1.substring(0,2), 16) * (1-ratio) + parseInt(color2.substring(0,2), 16) * ratio);
      let g = Math.ceil(parseInt(color1.substring(2,4), 16) * (1-ratio) + parseInt(color2.substring(2,4), 16) * ratio);
      let b = Math.ceil(parseInt(color1.substring(4,6), 16) * (1-ratio) + parseInt(color2.substring(4,6), 16) * ratio);

      let middle = hex(r) + hex(g) + hex(b);
      return '#' + middle
    }
  }
  