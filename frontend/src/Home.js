import './Home.css';
import { Form, Button, Spinner } from 'react-bootstrap';
import { useState } from 'react';
import axios from "axios";
import { useHistory } from "react-router-dom";
import jwt from 'jwt-decode'

function Home() {
    const [shortUrl, setShortUrl] = useState('');

    const history = useHistory();

    const onChangeShortUrl = (event) => {
        event.preventDefault();
        setShortUrl(event.target.value);
    };

    const onClickFind = (event) => {
        event.preventDefault()
        history.push(`/quiz/${shortUrl}`)
    }

    const onClickCreate = (event) => {
        event.preventDefault()
        history.push('/create')
    }

    const onClickLogout = (event) => {
        event.preventDefault()
        localStorage.removeItem('token')
        history.go(0)
    }

    return (
        <>
            <div className="greet">Hello, {jwt(localStorage.getItem("token")).nickname}!</div>
            <Form onSubmit={onClickFind} className="custom-card">
                <Form.Group controlId="formGridShortUrl">
                    <Form.Label>Find by URL</Form.Label>
                    <Form.Control placeholder="Enter short URL" onChange={onChangeShortUrl} value={shortUrl} />
                </Form.Group>

                <Button variant="primary" type="submit">
                    Find
                </Button>
            </Form>
            <div className="or-divider"> OR </div>
            <Form onSubmit={onClickCreate} className="custom-card">
                <Form.Group controlId="formGridCreate">
                    <Form.Label>Create new quiz</Form.Label>
                </Form.Group>

                <Button variant="primary" type="submit">
                    Create
                </Button>
            </Form>
            <div className="logout-divider"></div>

            <Button variant="dark" type="submit" onClick={onClickLogout}>
                Log out
            </Button>
            {/* </Form> */}
        </>
    );
}

export default Home;
