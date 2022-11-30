import React, { useState } from "react";

import axios from 'axios';
export default class Login extends React.Component {

    handleSubmit = async (e) => {
        e.preventDefault(); 
        const loginData = JSON.stringify({ username: this.state.email, password : this.state.password });
        const response = await axios.post("/login/", loginData, {
            headers: {
              'Content-Type': 'application/json'
            }})
        if (response.status == 200) {
            localStorage.setItem("token", response.data.token)
            window.location.href = "../dashboard";
        }
      }

    handleEmailChange = (event) => {    this.setState({email: event.target.value});  };
    handlePasswordChange = (event) => {    this.setState({password: event.target.value});  }

    render()
    {
        return (

            <div className="Auth-form-container">
              <form className="Auth-form" onSubmit={this.handleSubmit}>
                <div className="Auth-form-content">
                  <h3 className="Auth-form-title">Sign In</h3>
                  <div className="form-group mt-3">
                    <label>username</label>
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
                      Submit
                    </button>
                  </div>
                </div>
              </form>
            </div>
          );
    }


}