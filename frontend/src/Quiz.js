import './Quiz.css';
import { Form, Button } from 'react-bootstrap';
import { useEffect, useState } from 'react';
import axios from "axios";
import { useHistory } from "react-router-dom";

function AnswerQuiz({ quiz, setLoading }) {
    const history = useHistory();

    const onClickSubmit = (event, optionId) => {
        event.preventDefault()
        setLoading(true)

        axios
            .post(`http://localhost:80/api/quizzes/${quiz.id}/answer`, {
                option_id: optionId
            }, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            })
            .then((res) => {
                history.go(0);
            })
            .catch((e) => {
                setLoading(false)
                alert('Failed.');
            });
    }

    return <>
        <Form.Group controlId="formGridShortUrl">
            <Form.Label>{quiz.question}</Form.Label>
        </Form.Group>

        {quiz.options.map((option) => {
            return <Button className="option-button" onClick={e => onClickSubmit(e, option.id)}>
                {option.text}
            </Button>
        })}
    </>
}

function WaitResult() {
    return <Form.Group controlId="formGridShortUrl">
        <div className="spinner-border text-warning loading-spinner-results" role="status">
            <span className="sr-only">Loading...</span>
        </div>
        <Form.Label className="waiting-text">Waiting for more answers...</Form.Label>
    </Form.Group>
}


function Results({ quiz }) {
    return <>
        <Form.Label>Results</Form.Label>
        <Form.Group controlId="formGridShortUrl">
            <Form.Label>{quiz.question}</Form.Label>
        </Form.Group>

        <Button variant="success">
            {quiz.options.filter(e => e['id'] === quiz.result)[0]['text']}
        </Button>
    </>
}

function Quiz(props) {
    const shortUrl = props.match.params.short_url;
    const [loading, setLoading] = useState(true)
    const [invalid, setInvalid] = useState(false)
    const [quiz, setQuiz] = useState(undefined)
    const history = useHistory();

    const loadQuiz = () => {
        axios
            .get(`http://localhost:80/api/quizzes/short_url/${shortUrl}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            })
            .then((res) => {
                setQuiz(res.data)
                setLoading(false)
            })
            .catch((e) => {
                setInvalid(true)
                setLoading(false)
            });
    }

    const onClickBack = () => {
        history.push("/")
    }

    useEffect(() => {
        loadQuiz()
    }, [])

    var content = <></>

    if (loading) {
        content = <div className="spinner-border text-warning loading-spinner-quiz" role="status">
            <span className="sr-only">Loading...</span>
        </div>
    } else {
        if (invalid) {
            content = <div className="alert alert-danger invalid-register" role="alert">
                Invalid short URL
            </div>
        } else if (quiz.answered) {
            if (quiz.has_result) {
                content = <Results quiz={quiz} />
            } else {
                content = <WaitResult />
            }
        } else {
            content = <AnswerQuiz quiz={quiz} setLoading={setLoading} />
        }
    }

    return <Form className="custom-card">
        {content}

        <div className="home-divider"></div>

        <Button variant="dark" onClick={onClickBack}>
            Home
        </Button>
    </Form>
}

export default Quiz;
