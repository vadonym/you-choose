import './Login.css';
import { Form, Button } from 'react-bootstrap';
import { useState } from 'react';
import { useHistory } from "react-router-dom";
import Loading from "./Loading.js"
import axios from "axios";

function Register({ setIsLoggedIn }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [invalid, setInvalid] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    const history = useHistory();

    const onChangeEmail = (event) => {
        event.preventDefault();
        setEmail(event.target.value);
    };

    const onChangePassword = (event) => {
        event.preventDefault();
        setPassword(event.target.value);
    };

    const onClickSubmit = (event) => {
        event.preventDefault()
        setIsLoading(true);

        axios
            .post('http://localhost:80/auth/login', {
                email, password
            })
            .then((res) => {
                localStorage.setItem("token", res.data.token);
                setIsLoggedIn(true);
                setIsLoading(false);
                history.push('/')
            })
            .catch((e) => {
                setInvalid(true);
                setIsLoading(false);
            });
    }

    const onClickRegister = (event) => {
        event.preventDefault()
        history.push('/register')
    }

    if (isLoading) {
        return <Loading />
    } else {
        return (
            <Form onSubmit={onClickSubmit} className="custom-card">
                <Form.Group controlId="formGridEmail">
                    <Form.Label>Email</Form.Label>
                    <Form.Control type="email" placeholder="Enter email" onChange={onChangeEmail} value={email} />
                </Form.Group>

                <Form.Group controlId="formGridPassword">
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder="Password" onChange={onChangePassword} value={password} />
                </Form.Group>

                <Form.Group controlId="formGridButtons" id="group-buttons">
                    {invalid &&
                        <div class="alert alert-danger invalid-login" role="alert">
                            Invalid email or password
                        </div>
                    }
                    <Button variant="primary" type="submit">
                        Login
                    </Button>
                    <div className="login-or-divider ">OR</div>
                    <Button variant="success" onClick={onClickRegister}>
                        Register
                    </Button>
                </Form.Group>
            </Form>
        );
    }
}

export default Register;
