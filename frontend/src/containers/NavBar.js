import React, { useState } from "react";

import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import axios from "axios";
export default class NavBar extends React.Component {
    state = {accountDetails : {user:{}}}
    async componentDidMount()
    {
        
        if (localStorage.getItem("token") == null) {
            window.location.href = "../login";
        }

        const userDetails = await axios.get("/account-details/",{
            headers: {
              'Content-Type': 'application/json',
              'Authorization' : 'Token ' + localStorage.getItem("token"),
            }})
        
        this.setState({accountDetails:userDetails.data})

        window.MyVars = {
            accountDetails: userDetails.data,
        };
    }
    render()
    {
        return (
            <>
              <Navbar bg="primary" variant="dark">
                <Container>
                  <Navbar.Brand href="#home">Lottery app</Navbar.Brand>
                  <Nav className="me-auto">
                    <Nav.Link href="#home">Logged in as : {this.state.accountDetails.user.username}</Nav.Link>
                    <Nav.Link href="/dashboard">Dashboard</Nav.Link>
                    <Nav.Link href="/logout">logout</Nav.Link>
                    {this.state.accountDetails.profile_type == "admin" &&
                    <>
                                                            <Nav.Link href="/create-broker">Create new broker</Nav.Link>
                                                            <Nav.Link href="/create-manager">Create new manager</Nav.Link>
                    </>

                    }

{this.state.accountDetails.profile_type == "broker" &&
                    <>
                                                            <Nav.Link href="/create-broker">Create new broker</Nav.Link>
                                        <Nav.Link href="/create-user">Create new user</Nav.Link> 
                                        <Nav.Link href="#">Available points : {this.state.accountDetails.points}</Nav.Link> 
                    </>

                    }

                  </Nav>
                </Container>
              </Navbar>
            </>
          );
    }
}