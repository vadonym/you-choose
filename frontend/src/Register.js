import './Register.css';
import { Form, Button } from 'react-bootstrap';
import { useState } from 'react';
import axios from "axios";
import { useHistory } from "react-router-dom";
import Loading from "./Loading.js"

function Register() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [nickname, setNickname] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [invalid, setInvalid] = useState(false);

    const history = useHistory();

    const onChangeEmail = (event) => {
        event.preventDefault();
        setEmail(event.target.value);
    };

    const onChangePassword = (event) => {
        event.preventDefault();
        setPassword(event.target.value);
    };

    const onChangeNickname = (event) => {
        event.preventDefault();
        setNickname(event.target.value);
    };

    const onClickSubmit = (event) => {
        event.preventDefault()
        setIsLoading(true);

        axios
            .post('http://localhost:80/api/users', {
                email, password, nickname
            })
            .then((res) => {
                alert('Successfully registered.');
                setIsLoading(false);
                history.push('/login')
            })
            .catch((e) => {
                setInvalid(true);
                setIsLoading(false);
            });
    }

    const onClickBack = (event) => {
        history.goBack(0);
    }

    if (isLoading) {
        return <Loading />
    } else {
        return (
            <div className="register-panel">
                <Form onSubmit={onClickSubmit} className="custom-card">
                    <Form.Group controlId="formGridEmail">
                        <Form.Label>Email</Form.Label>
                        <Form.Control type="email" placeholder="Enter email" onChange={onChangeEmail} value={email} />
                    </Form.Group>

                    <Form.Group controlId="formGridPassword">
                        <Form.Label>Password</Form.Label>
                        <Form.Control type="password" placeholder="Password" onChange={onChangePassword} value={password} />
                    </Form.Group>

                    <Form.Group controlId="formGridNickname">
                        <Form.Label>Nickname</Form.Label>
                        <Form.Control placeholder="Vasile Nebunu" onChange={onChangeNickname} value={nickname} />
                    </Form.Group>

                    {invalid &&
                        <div class="alert alert-danger invalid-register" role="alert">
                            Failed to register
                        </div>
                    }

                    <Button variant="primary" type="submit">
                        Register
                    </Button>

                    <div className="logout-divider"></div>

                    <Button variant="dark" onClick={onClickBack}>
                        Back
                    </Button>
                </Form>
            </div>
        );
    }
}

export default Register;
