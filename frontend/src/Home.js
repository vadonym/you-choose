import './Home.css';
import { Form, Button } from 'react-bootstrap';
import { useState } from 'react';
import { useHistory } from "react-router-dom";
import jwt from 'jwt-decode'
import Loading from "./Loading.js"

function Home() {
    const [shortUrl, setShortUrl] = useState('');
    const [isLoading, setIsLoading] = useState(false);

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
        setIsLoading(true);
        localStorage.removeItem('token')
        history.go(0)
    }

    if (isLoading) {
        return <Loading />
    } else {
        return (
            <div className="home">
                <Form onSubmit={onClickFind} className="custom-card">
                    <Form.Label>Hello, {jwt(localStorage.getItem("token")).nickname}!</Form.Label>

                    <Form.Group controlId="formGridShortUrl">
                        <Form.Control placeholder="Short URL" onChange={onChangeShortUrl} value={shortUrl} />
                    </Form.Group>

                    <Button variant="primary" type="submit" disabled={shortUrl === ""}>
                        Find
                    </Button>

                    <div className="or-divider">OR</div>

                    <Button variant="success" onClick={onClickCreate}>
                        Create new quiz
                    </Button>

                    <div className="logout-divider"></div>

                    <Button variant="dark" type="submit" onClick={onClickLogout}>
                        Log out
                    </Button>
                </Form>
            </div>
        );
    }
}

export default Home;
