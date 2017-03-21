import React from 'react';
import { render } from 'react-dom';


const url = "/accounts_api/register/";


const attributes = [
    { type: "text", name: "username", required: true, label: "Login" },
    { type: "password", name: "password", required: true, label: "Hasło" },
    { type: "password", name: "password-again", required: true, label: "Hasło ponownie" },
    { type: "email", name: "email", required: true, label: "Email" },
];


class Register extends React.Component {
    render() {
        return (
            <form></form>
        );
    }
}

render(<Register />, document.getElementById('register'));
