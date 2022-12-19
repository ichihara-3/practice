import React, { FC } from "react";
import logo from "./logo.svg";
import "./App.css";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <Clock />
      </header>
    </div>
  );
}

interface ClockState {
  date: Date;
}

class Clock extends React.Component<{}, ClockState> {

  timerID: NodeJS.Timer | null

  constructor(props: {}) {
    super(props);
    this.state = { date: new Date() };
    this.timerID = null;
  }

  tick(): void {
    this.setState({
      date: new Date(),
    });
  }

  componentDidMount(): void {
    this.timerID = setInterval(() => this.tick(), 1000);
  }

  componentWillUnmount(): void {
    if (this.timerID) {
      clearInterval(this.timerID);
    }
  }

  render(): JSX.Element {
    return (
      <div>
        <p>The Time is...</p>
        <FormattedDate {...{ date: this.state.date }} />
        <FormattedDate {...{ date: this.state.date }} />
        <FormattedDate {...{ date: this.state.date }} />
      </div>
    );
  }
}

const FormattedDate: FC<{ date: Date }> = (props) => {
  return (
    <p className="clock">
      {props.date.toLocaleTimeString()}
    </p>
  )
}

export default App;
