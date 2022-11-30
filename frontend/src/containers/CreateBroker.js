import React, { useState } from "react";
import Alert from 'react-bootstrap/Alert';
import axios from 'axios';
export default class CreateBroker extends React.Component {
    state = { hasError:false};
    handleSubmit = async (e) => {
        e.preventDefault(); 
        const loginData = JSON.stringify({ username: this.state.email, password : this.state.password });
        try {
          const response = await axios.post("/create-broker/", loginData, {
            headers: {
              'Content-Type': 'application/json',
              'Authorization' : 'Token ' + localStorage.getItem("token"),
            }})
        if (response.status == 201) {
          window.location.href = "../dashboard";
        }
        } catch (error) {
          this.setState({hasError : true});
        }

      }

    handleEmailChange = (event) => {    this.setState({email: event.target.value});  };
    handlePasswordChange = (event) => {    this.setState({password: event.target.value});  }

    render()
    {
        return (
          <>
          {this.state.hasError &&  <Alert key="danger" variant="danger">An error has occured when creating user, maybe the username is taken or is too short...</Alert> }
            <div className="Auth-form-container">
              <form className="Auth-form" onSubmit={this.handleSubmit}>
                <div className="Auth-form-content">
                  <h3 className="Auth-form-title">Create a new broker :</h3>
                  <div className="form-group mt-3">
                    <label>Username</label>
                    <input
                      className="form-control mt-1"
                      placeholder="Enter username"
                      onChange={this.handleEmailChange}
                    />
                  </div>
                  <div className="form-group mt-3">
                    <label>Password</label>
                    <input
                      type="password"
                      className="form-control mt-1"
                      placeholder="Enter password"
                      onChange={this.handlePasswordChange}
                    />
                  </div>
                  <div className="d-grid gap-2 mt-3">
                    <button type="submit" className="btn btn-primary">
                      Create
                    </button>
                  </div>
                </div>
              </form>
            </div>
            </>
          );
    }


}