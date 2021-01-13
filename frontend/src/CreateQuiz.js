import './CreateQuiz.css';
import { Form, Button, Spinner } from 'react-bootstrap';
import { useState } from 'react';
import axios from "axios";
import { useHistory } from "react-router-dom";

function CreateQuiz() {
    const [shortUrl, setShortUrl] = useState('');
    const [question, setQuestion] = useState('');
    const [answersTarget, setAnswersTarget] = useState('');
    const [options, setOptions] = useState(['', '']);
    const [animation, setAnimation] = useState('');

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
        setAnswersTarget(event.target.value);
    };
    const onChangeOption = (event, id) => {
        event.preventDefault();
        let optionsClone = [...options]

        optionsClone[id] = event.target.value

        setOptions(optionsClone)
    };

    const onClickSubmit = (event) => {
        event.preventDefault()

        setAnimation("grow")
        axios
            .post('http://localhost:80/api/quizzes', {
                short_url: shortUrl, question, answers_target: answersTarget, texts: options
            }, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            })
            .then((res) => {
                alert('Successfully created.');
                history.push(`/quiz/${shortUrl}`)
            })
            .catch((e) => {
                setAnimation("")
                alert('Failed.');
            });
    }

    const onClickAddOptionButton = (event) => {
        let optionsClone = [...options]

        optionsClone.push('')

        setOptions(optionsClone)
    }

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
                return <Form.Group controlId="formGridOption">

                    <Form.Label>Option {id + 1}</Form.Label>
                    <Form.Control placeholder="Option" onChange={e => onChangeOption(e, id)} value={option} />
                </Form.Group>
            })}

            <Form.Group controlId="formGridAddOption">
                <Button onClick={onClickAddOptionButton}>
                    Add option
                </Button>
            </Form.Group>

            <Button variant="primary" type="submit">
                Create
                    <Spinner
                    animation={animation}
                    size="sm"
                    role="status"
                    aria-hidden="true"
                    visible="false"
                />
            </Button>
        </Form>
    );
}

export default CreateQuiz;
