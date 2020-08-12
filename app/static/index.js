'use strict';

const e = React.createElement;

const mockSurvey = {
    id: 1,
    title: "This is my mock survey",
    questions: [
        {
            id: 1,
            title: "Single choice",
            type: "single",
            answers: [
                {id: 1, title: "Answer1"},
                {id: 2, title: "Answer2"},
                {id: 3, title: "Answer3"},
            ],
            selected: null,
        },
        {
            id: 2,
            title: "Multi choices",
            type: "multi",
            answers: [
                {id: 1, title: "Answer1"},
                {id: 2, title: "Answer2"},
                {id: 3, title: "Answer3"},
            ],
            selected: []
        }
    ]
};


function AnswerMulti(props) {
    const onChange = function (e) {
        const val = e.target.value;
        // props.question.selected = e.target.value;
        if (e.target.checked) {
            if (!props.question.selected.includes(val)) props.question.selected.push(val);
        }
        else {
            props.question.selected = props.question.selected.filter(answerId => answerId != val);
        }
        console.log(e.target.value, e.target.checked);
    }
    return (
        <div>
            <input type="checkbox" name={props.question.id} value={props.answer.id} onChange={ onChange }/> { props.answer.title }
        </div>
    )

}

function AnswerSingle(props) {
    const onChange = function (e) {
        props.question.selected = e.target.value;
    }
    return (
        <div>
            <input type="radio" name={props.question.id} value={props.answer.id} onChange={ onChange }/> { props.answer.title }
        </div>
    )

}

function renderAnswer(answer, question) {
        if (question.type == "single") {
            return (<AnswerSingle key= {answer.id} answer={ answer} question={question}/>)
        }
        if (question.type == "multi") {
            return (<AnswerMulti key= {answer.id} answer={ answer} question={question}/>)
        }
}

function Question(props) {
    const answerItems = props.question.answers.map(answer => renderAnswer(answer, props.question))
    return (
        <div>
        <h3>{ props.question.title}</h3>
        { answerItems }
        </div>
    )
}

function Survey(props) {
    const survey = props.survey;
    const questionItems = survey.questions.map((q) => <Question key={ q.id } question={q} />);
    const saveResult = function () {
        alert("Save");
        console.log(survey);
    }
    return (
        <div>
        <h2>{ survey.title }</h2>
        { questionItems }
        <button onClick={ saveResult }>Save</button>
        </div>
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
