'use strict';

const mockSurvey = {
    id: 1,
    title: "This is my mock survey",
    questions: [
        {
            id: 1,
            title: "Single choice",
            type: "single",
            options: [
                {id: 1, title: "Answer1", checked: true, with_text: true},
                {id: 2, title: "Answer2", checked: false},
                {id: 3, title: "Answer3", checked: true},
            ],
            selected: null,
        },
        {
            id: 2,
            title: "Multi choices",
            type: "multi",
            options: [
                {id: 4, title: "Answer1", checked: true},
                {id: 5, title: "Answer2", checked: false},
                {id: 6, title: "Answer3", with_text: true},
            ],
            selected: []
        }
    ]
};

const ResultFull = {
    survey_id: 1,
    questions: [
        {id: 1, options: [{id: 1, free_text: "Hello"}]},
        {id: 2, options: [{id: 1}, {id: 2}]}
    ]
}

const Result = {
    survey_id: 1,
    questions: [
        {id: 1, options: []},
        {id: 2, options: []}
    ]
}

function renderAnswer(answer, question) {
        if (question.type == "single") {
            return (<AnswerSingle key= {answer.id} answer={ answer} question={question}/>)
        }
        if (question.type == "multi") {
            return (<AnswerMulti key= {answer.id} answer={ answer} question={question}/>)
        }
}


function Option(props) {
    const onFreeTextUpdated = function (e) {
        const freeText = e.target.value;
        const new_option = {
            ...props.option,
            checked: true
        }
        if (props.option.with_text) {
            new_option.free_text = freeText
        }
        props.updateOption(new_option);
    }
    return (
        <span>
        <span>{ props.option.title }</span>
        { props.option.with_text &&
            <textarea onChange={ onFreeTextUpdated }/>
        }
        </span>
    );
}

function QuestionMulti(props) {
    const onChange = function (option) {
        const new_option = {...option, checked: !option.checked}
        console.log("new_option=", new_option);
        updateOption(new_option);
    }
    const updateOption = function (new_option) {
        console.log("question before=", props.question);
        const new_question = {
            ...props.question, 
            options: props.question.options.map((option) => option.id == new_option.id ? new_option : {...option})
        }
        console.log("question after=", new_question);
        props.updateQuestion(new_question);
    }
    const optionItems = props.question.options.map(option => {
        return (<div key={option.id}>
            <input type="checkbox" defaultChecked={option.checked} onClick={ (e) => {onChange(option); } } value={option.id} />
            <Option option={ option } updateOption={ updateOption } />
        </div>)
    });
    return (
        <div>
        { console.log("render QuesionMulti") }
        { console.log(optionItems) }
        { props.question.options.map(option => console.log("option=", option)) }
            <h3>{ props.question.title}</h3>
            { optionItems }
        </div>
    );
}

function QuestionSingle(props) {
    const onChange = function (selected_option) {
        const new_option = {...selected_option, checked: true}
        updateOption(new_option);
    }
    const updateOption = function (new_option) {
        console.log("question before=", props.question);
        const new_question = {
            ...props.question, 
            options: props.question.options.map((option) => option.id == new_option.id ? new_option : {...option, checked: false})
        }
        console.log("question after=", new_question);
        props.updateQuestion(new_question);
    }
    const optionItems = props.question.options.map(option => {
        return (<div key={option.id}>
            <input type="radio" name={ "qs_" + props.question.id} value={option.id} checked={option.checked} onChange={()=> onChange(option) }/>
            <Option option={ option } updateOption={ updateOption } />
        </div>)
    });
    return (
        <div>
            <h3>{ props.question.title}</h3>
            { optionItems }
        </div>
    );
}

function Question(props) {
    switch (props.question.type) {
        case "single":
            return <QuestionSingle question={ props.question } updateQuestion ={ props.updateQuestion }/>;
        case "multi":
            return <QuestionMulti question={ props.question } updateQuestion={ props.updateQuestion }/>;
        default:
            throw "Can not find Question type for: '" + props.question.type + "'";
    }
}

function Survey(props) {
    const survey = props.survey;
    const updateQuestion = function(question) {
        console.log("Update question: ", question);
        const new_survey = {
            ...survey,
            questions: survey.questions.map((q) => q.id ==question.id ? question : q)
        }
        props.setSurvey(new_survey);
    }
    const saveResult = function () {
        alert("Save");
        console.log(survey);
    }
    return (
        <div>
        <h2>{ survey.title }</h2>
        {
            survey.questions.map((q) => <Question key={ q.id } question={q} updateQuestion= { updateQuestion } />)
        }
        <button onClick={ saveResult }>Save</button>
        </div>
    )
}

function App() {
    console.log("Start app");
    const [survey, setSurvey] = React.useState(null);
    const [result, setResult] = React.useState(null);
    let timer1;


    // fetch('/survey')
    // .then(res => {
    //     console.log(res);
    // });
    
    React.useEffect(() => {
        console.log("use effect");
        timer1 = setTimeout(function () {
            console.log("after 1 sec");
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
            <Survey survey={survey} result = {result} setSurvey={ setSurvey }/>
        )
    }
    ;
}

const elApp = document.getElementById("app");
ReactDOM.render(React.createElement(App), elApp);
