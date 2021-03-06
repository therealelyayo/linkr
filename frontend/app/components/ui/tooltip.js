/* global setTimeout, clearInterval */

import React from 'react';

export const GRACE_TIMEOUT_INTERVAL = 150;

/**
 * Component used to display tooltips over children elements when the user mouse-hovers over the
 * children elements. Contains logic to intelligently tolerate minor mouse-out events, so to not
 * collapse the tooltip the instance the mouse leaves the target area.
 */
export default class Tooltip extends React.Component {
  static propTypes = {
    contents: React.PropTypes.element,
    tooltipClassName: React.PropTypes.string,
    tooltipStyle: React.PropTypes.object,
    alwaysDisplay: React.PropTypes.bool
  };
  static defaultProps = {
    tooltipStyle: {},
    alwaysDisplay: false
  };

  constructor(props) {
    super(props);

    this.state = {
      displayTooltip: props.alwaysDisplay
    };
  }

  onMouseOver() {
    // If we mouse-over the element again before the timeout expires, simply clear the interval so
    // that the display is maintained.
    clearInterval(this.interval);

    this.setState({
      displayTooltip: true
    });
  }

  onMouseOut() {
    const {alwaysDisplay} = this.props;

    // The logic here is to set a delay before actually changing the state of the component to
    // no longer display the tooltip. This allows the mouse to temporarily exit the tooltip zone
    // while still preserving display of the tooltip.
    this.interval = setTimeout(() => {
      this.setState({
        displayTooltip: alwaysDisplay
      });
    }, GRACE_TIMEOUT_INTERVAL);
  }

  render() {
    const {contents, tooltipClassName, tooltipStyle, children} = this.props;
    const {displayTooltip} = this.state;

    // Conditionally display the tooltip based on current state
    const style = {
      ...tooltipStyle,
      opacity: displayTooltip ? 1 : 0,
      visibility: displayTooltip ? 'inherit' : 'hidden'
    };

    return (
      <div
        className="tooltip-container"
        onMouseOver={this.onMouseOver.bind(this)}
        onMouseOut={this.onMouseOut.bind(this)}
      >
        <div className="tooltip-children">
          {children}
        </div>

        {
          contents && (
            <span className={`tooltip transition ${tooltipClassName}`} style={style}>
              {contents}
            </span>
          )
        }
      </div>
    );
  }
}
