'use strict';

const e = React.createElement;

const mockSurvey = {
    title: "This is my mock survey"
};


function Survey(props) {
    const survey = props.survey;
    return (
        <h2>{ survey.title }</h2>
    )

}


function App() {
    console.log("Start app");
    const [survey, setSurvey] = React.useState(null);
    let timer1;


    // fetch('/survey')
    // .then(res => {
    //     console.log(res);
    // });
    
    React.useEffect(() => {
        console.log("use effect");
        timer1 = setTimeout(function () {
            console.log("after 1 sec");
            console.log(timer1);
            clearTimeout(timer1);
            setSurvey(mockSurvey);
        }, 1000);
    }, [])

    if (survey == null) {
        return (
            <div>Loading data</div>
        )
    } else {
        return (
            <Survey survey={survey}/>
        )
    }
    ;
}

class LikeButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {
    if (this.state.liked) {
      return 'You liked this.';
    }

    return (
        <button onClick={() => this.setState({ liked: true })}>
            Like
        </button>
    );
  }
}

const elApp = document.getElementById("app");
ReactDOM.render(React.createElement(App), elApp);
