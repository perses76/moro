'use strict';

const mockSurvey = {
    id: 1,
    title: "This is my mock survey",
    user_rate: 3,
    questions: [
        {
            id: 1,
            title: "Single choice",
            type: "single",
            options: [
                {id: 1, title: "Answer1", checked: true, with_text: true},
                {id: 2, title: "Answer2", checked: false},
                {id: 3, title: "Answer3", checked: true},
            ]
        },
        {
            id: 2,
            title: "Multi choices",
            type: "multi",
            options: [
                {id: 4, title: "Answer1", checked: true},
                {id: 5, title: "Answer2", checked: false},
                {id: 6, title: "Answer3", with_text: true},
            ]
        },
        {
            id: 3,
            title: "Free text",
            type: "freetext",
            options: [
                {id: 7, title: "Answer1", checked: true},
            ]
        }
    ]
};

const elApp = document.getElementById("app");
ReactDOM.render(React.createElement(App), elApp);

function App() {
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
}

function Survey(props) {
    const survey = props.survey;
    const updateQuestion = function(question) {
        props.setSurvey({
            ...survey,
            questions: replaceEntity(survey.questions, question)
        });
    }
    const updateUserRate = function(new_rate) {
        props.setSurvey({
            ...survey,
            user_rate: new_rate
        });
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

        <UserRate userRate={ survey.user_rate} updateUserRate={ updateUserRate }/>
        <button onClick={ saveResult }>Save</button>
        </div>
    )
}

function UserRate(props) {
    const stars = (new Array(5)).fill(0).map((it, idx) => idx < props.userRate);
    return (
        <div className="user-rate">
        <h3>User rate</h3>
        <ul>
        {
            stars.map((item, idx) => {
                let className = "star";
                if (item) { className += " active" }
                return (
                    <li key={idx} >
                        <div className={className} onClick={ (e) => props.updateUserRate(idx+1) } />
                    </li>
                )
            })
        }
        </ul>
        </div>
    )
}

function Question(props) {
    switch (props.question.type) {
        case "single":
            return <QuestionSingle question={ props.question } updateQuestion ={ props.updateQuestion }/>;
        case "multi":
            return <QuestionMulti question={ props.question } updateQuestion={ props.updateQuestion }/>;
        case "freetext":
            return <QuestionFreetext question={ props.question } updateQuestion={ props.updateQuestion }/>;
        default:
            throw "Can not find Question type for: '" + props.question.type + "'";
    }
}

function QuestionMulti(props) {
    const onChange = function (option) {
        updateOption({...option, checked: !option.checked});
    }
    const updateOption = function (new_option) {
        props.updateQuestion({
            ...props.question, 
            options: replaceEntity(props.question.options, new_option)
        });
    }
    return (
        <div>
            <h3>{ props.question.title}</h3>
            <ul className="options-list">
            { props.question.options.map(option => {
                return (<li key={option.id}>
                    <input type="checkbox" defaultChecked={option.checked} onClick={ (e) => {onChange(option); } } value={option.id} />
                    <Option option={ option } updateOption={ updateOption } />
                </li>)
              })
            }
            </ul>
        </div>
    );
}

function QuestionSingle(props) {
    const onChange = function (option) {
        updateOption({...option, checked: true});
    }
    const updateOption = function (new_option) {
        props.updateQuestion({
            ...props.question, 
            options: replaceEntity(
                props.question.options.map(option => {return {...option, checked: false}}),
                new_option
            )
        });
    }
    return (
        <div>
            <h3>{ props.question.title}</h3>
            <ul className="options-list">
            {
                props.question.options.map(option => {
                    return (<li key={option.id}>
                        <input type="radio" name={ "qs_" + props.question.id} value={option.id} checked={option.checked} onChange={(e)=> {onChange(option)} }/>
                        <Option option={ option } updateOption={ updateOption } />
                    </li>)
                })
            }
            </ul>
        </div>
    );
}

function QuestionFreetext(props) {
    const option = props.question.options[0];
    const onChange = function (e) {
        const freeText = e.target.value;
        props.updateQuestion({
            ...props.question, 
            options: replaceEntity(
                props.question.options,
                {...option, checked: (freeText !== ""), free_text: freeText}
            )
        });
    }
    return (
        <div>
            <h3>{ props.question.title}</h3>
            <div> { option.title }</div>
            <textarea onChange={ onChange }>{ option.free_text }</textarea>
        </div>
    );
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
        <div className="option">
        <span>{ props.option.title }</span>
        { props.option.with_text &&
            <textarea onChange={ onFreeTextUpdated }/>
        }
        </div>
    );
}

function replaceEntity(arr, new_item) {
    return arr.map(item => item.id === new_item.id ? new_item : item)
}
