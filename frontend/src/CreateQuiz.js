import './CreateQuiz.css';
import { Form, Button } from 'react-bootstrap';
import { useState } from 'react';
import axios from "axios";
import { useHistory } from "react-router-dom";
import Loading from "./Loading.js"

function CreateQuiz() {
    const [shortUrl, setShortUrl] = useState('');
    const [question, setQuestion] = useState('');
    const [answersTarget, setAnswersTarget] = useState('');
    const [options, setOptions] = useState(['', '']);
    const [isLoading, setIsLoading] = useState(false);
    const [invalid, setInvalid] = useState(false);

    const history = useHistory();

    const onChangeShortUrl = (event) => {
        event.preventDefault();
        setShortUrl(event.target.value);
    };

    const onChangeQuestion = (event) => {
        event.preventDefault();
        setQuestion(event.target.value);
    };

    const onChangeAnswersTarget = (event) => {
        event.preventDefault();
        if (event.target.value > 0) {
            setAnswersTarget(event.target.value);
        }
    };

    const onChangeOption = (event, id) => {
        event.preventDefault();
        let optionsClone = [...options]

        optionsClone[id] = event.target.value

        setOptions(optionsClone)
    };

    const onClickSubmit = (event) => {
        event.preventDefault()
        setIsLoading(true);

        axios
            .post('http://localhost:80/api/quizzes', {
                short_url: shortUrl, question, answers_target: answersTarget, texts: options
            }, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            })
            .then((res) => {
                setIsLoading(false);
                history.push(`/quiz/${shortUrl}`)
            })
            .catch((e) => {
                setInvalid(true);
                setIsLoading(false);
            });
    }

    const onClickAddOptionButton = (event) => {
        let optionsClone = [...options]

        optionsClone.push('')

        setOptions(optionsClone)
    }

    const onClickBack = (event) => {
        history.goBack(0);
    }

    if (isLoading) {
        return <Loading />
    } else {
        return (
            <Form onSubmit={onClickSubmit} className="custom-card">
                <Form.Group controlId="formGridShortUrl">
                    <Form.Label>Short URL</Form.Label>
                    <Form.Control placeholder="Enter short URL" onChange={onChangeShortUrl} value={shortUrl} />
                </Form.Group>

                <Form.Group controlId="formGridAnswersTarget">
                    <Form.Label>Answers Target</Form.Label>
                    <Form.Control type="number" placeholder="3" onChange={onChangeAnswersTarget} value={answersTarget} />
                </Form.Group>

                <Form.Group controlId="formGridQuestion">
                    <Form.Label>Question</Form.Label>
                    <Form.Control placeholder="Question" onChange={onChangeQuestion} value={question} />
                </Form.Group>

                {options.map((option, id) => {
                    return <Form.Group controlId="formGridOption" key={`group-option-${id}`}>

                        <Form.Label>Option {id + 1}</Form.Label>
                        <Form.Control placeholder="Option" onChange={e => onChangeOption(e, id)} value={option} />
                    </Form.Group>
                })}

                <Button onClick={onClickAddOptionButton}>
                    Add option
                </Button>

                <div className="create-divider"></div>

                {invalid &&
                    <div className="alert alert-danger invalid-register" role="alert">
                        Failed to create quiz
                    </div>
                }

                <Button variant="success" type="submit">
                    Create
                </Button>

                <div className="logout-divider"></div>

                <Button variant="dark" onClick={onClickBack}>
                    Back
                </Button>
            </Form>
        );
    }
}

export default CreateQuiz;
