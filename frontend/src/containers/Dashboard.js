import React, { useState } from "react";

import axios from 'axios';
import NavBar from "./NavBar";
import Button from 'react-bootstrap/Button'
import Stack from 'react-bootstrap/Stack';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';
import '../App.css';
export default class Dashboard extends React.Component {
    state = { userList : [], brokerList:[], allUsers:[], game1stats : [], game2stats : [], };
    constructor(props)
    {
        super(props);
        window.MyVars = {accountDetails : {}}
    }
    async getGameBetStatus()
    {
        const game1stats = await axios.get("/game1-status/",{
            headers: {
              'Content-Type': 'application/json',
              'Authorization' : 'Token ' + localStorage.getItem("token"),
            }})
        
        this.setState({game1stats : JSON.parse(game1stats.data.status)})

        const game2stats = await axios.get("/game2-status/",{
            headers: {
              'Content-Type': 'application/json',
              'Authorization' : 'Token ' + localStorage.getItem("token"),
            }})
        
        this.setState({game2stats : JSON.parse(game2stats.data.status)})
    }
    async componentDidMount()
    {
        const userListResp = await axios.get("/list-created-users/",{
            headers: {
              'Content-Type': 'application/json',
              'Authorization' : 'Token ' + localStorage.getItem("token"),
            }})

        await this.setState({userList : userListResp.data.created_users})

        const allBrokers = await axios.get("/broker-list/",{
            headers: {
              'Content-Type': 'application/json',
              'Authorization' : 'Token ' + localStorage.getItem("token"),
            }})

        await this.setState({brokerList : allBrokers.data.broker_list})

        const allUsers = await axios.get("/list-all-users/",{
            headers: {
              'Content-Type': 'application/json',
              'Authorization' : 'Token ' + localStorage.getItem("token"),
            }})

        await this.setState({allUsers : allUsers.data.created_users})
        
        setInterval(() => this.getGameBetStatus(), 3000)

    }
    render()
    {
        return(
            <>
            <NavBar />
            <Container style={{justifyContent : "center", alignItems : "center"}}>

                <br />
                <br />
                {(window.MyVars.accountDetails.profile_type == "admin" || window.MyVars.accountDetails.profile_type == "manager") &&
                <>
                    <Row>
                    <Col>
                    <Card style={{ width: '18rem' }}>
                        <Card.Header>All brokers :</Card.Header>
                        <ListGroup variant="flush">
                            {
                                this.state.brokerList.map((item, key) =>
                                {
                                    return(
                                    <ListGroup.Item key={key}><a href={"user-details?id="+item.pk} >{item.user.username}</a></ListGroup.Item>
                                )
                            })
                        }

                        </ListGroup>
                    </Card>
                    </Col>
                    <Col>
                    <Card style={{ width: '18rem' }}>
                        <Card.Header>All Users :</Card.Header>
                        <ListGroup variant="flush">
                            {
                                this.state.allUsers.map((item, key) =>
                                {
                                    return(
                                        <ListGroup.Item key={key}><a href={"user-details?id="+item.pk} >{item.user.username}</a></ListGroup.Item>
                                        )
                                    })
                                }

                        </ListGroup>
                    </Card>
                    </Col>
                    </Row>
                </>

                }
                 {window.MyVars.accountDetails.profile_type == "broker" &&
                  <>
                              <Card style={{ width: '18rem' }}>
                    <Card.Header>Your created users :</Card.Header>
                    <ListGroup variant="flush">
                        {
                        this.state.userList.map((item, key) =>
                        {
                            return(
                                <ListGroup.Item key={key}><a href={"user-details?id="+item.pk} >{item.user.username}</a></ListGroup.Item>
                            )
                        })
                        }

                    </ListGroup>
                </Card>
                  </>
                    }

                <br />
                <br />
                <h2>Bet status, updated automatically every 3 seconds...</h2>
                <br />
<Row>
                    <Col>
                    <Card style={{ width: '18rem' }}>
                        <Card.Header>Game 1 bets</Card.Header>
                        <ListGroup variant="flush">
                            {
                                this.state.game1stats.map((item, key) =>
                                {
                                    return(
                                    <ListGroup.Item key={key}>number {key} has total points of {item}</ListGroup.Item>
                                )
                            })
                        }

                        </ListGroup>
                    </Card>
                    </Col>
                    <Col>
                    <Card style={{ width: '18rem' }}>
                        <Card.Header>Game 2 bets :</Card.Header>
                        <ListGroup variant="flush">
                        {
                                this.state.game2stats.map((item, key) =>
                                {
                                    return(
                                    <ListGroup.Item key={key}>number {key} has total points of {item}</ListGroup.Item>
                                )
                            })
                        }

                        </ListGroup>
                    </Card>
                    </Col>
                    </Row>
                    
                </Container>



                
            </>

        )
    }
}