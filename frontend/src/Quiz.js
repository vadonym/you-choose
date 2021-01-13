import './Quiz.css';
import { Form, Button, Spinner } from 'react-bootstrap';
import { useEffect, useState } from 'react';
import axios from "axios";
import { useHistory } from "react-router-dom";

function AnswerQuiz({ quiz }) {
    const history = useHistory();

    const onClickSubmit = (event, optionId) => {
        event.preventDefault()

        axios
            .post(`http://localhost:80/api/quizzes/${quiz.id}/answer`, {
                option_id: optionId
            }, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            })
            .then((res) => {
                alert('Successfully created.');
                history.go(0);
            })
            .catch((e) => {
                alert('Failed.');
            });
    }

    return (
        <Form className="custom-card">
            <Form.Group controlId="formGridShortUrl">
                <Form.Label>{quiz.question}</Form.Label>
            </Form.Group>


            {quiz.options.map((option) => {
                return <Form.Group controlId="formGridOption">
                    <Button onClick={e => onClickSubmit(e, option.id)}>
                        {option.text}
                        <Spinner
                            size="sm"
                            role="status"
                            aria-hidden="true"
                            visible="false"
                        />
                    </Button>
                </Form.Group>
            })}

        </Form>
    );
}

function WaitResult() {
    return (
        <Form className="custom-card">
            <Form.Group controlId="formGridShortUrl">
                <Form.Label>Waiting for result...</Form.Label>
            </Form.Group>
        </Form>
    );
}

function Results({ quiz }) {
    return (
        <Form className="custom-card">
            <Form.Group controlId="formGridShortUrl">
                <Form.Label>{quiz.question} Result:</Form.Label>
            </Form.Group>

            <Form.Group controlId="formGridOption">
                <Button >
                    {quiz.options.filter(e => e['id'] == quiz.result)[0]['text']}
                    <Spinner
                        size="sm"
                        role="status"
                        aria-hidden="true"
                        visible="false"
                    />
                </Button>
            </Form.Group>
        </Form>
    );
}

function Quiz(props) {
    const [shortUrl, setShortUrl] = useState(props.match.params.short_url);
    const [loaded, setLoaded] = useState(false)
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
                setLoaded(true)
            })
            .catch((e) => {
                history.push('/')
            });
    }

    useEffect(() => {
        loadQuiz()
    }, [])

    if (loaded) {
        if (quiz.answered) {
            if (quiz.has_result) {
                return <Results quiz={quiz} />
            } else {
                return <WaitResult />
            }
        } else {
            return <AnswerQuiz quiz={quiz} />
        }
    } else {
        return <div>Loading...</div>
    }
}

export default Quiz;
