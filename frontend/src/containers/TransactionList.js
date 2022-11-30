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
export default class TransactionList extends React.Component {
    state = { incomingList : [], outgoingList:[] };
    constructor(props)
    {
        super(props);
        window.MyVars = {accountDetails : {}}
    }
    async componentDidMount()
    {
        const incomingListResp = await axios.get("/incoming-transactions/",{
            headers: {
              'Content-Type': 'application/json',
              'Authorization' : 'Token ' + localStorage.getItem("token"),
            }})

        await this.setState({incomingList : incomingListResp.data.incoming_transactions})

        const outgoingListResp = await axios.get("/outgoing-transactions/",{
            headers: {
              'Content-Type': 'application/json',
              'Authorization' : 'Token ' + localStorage.getItem("token"),
            }})

        await this.setState({outgoingList : outgoingListResp.data.outgoing_transactions})
    }
    render()
    {
        return(
            <>
            <NavBar />
            <Container style={{justifyContent : "center", alignItems : "center"}}>

                <br />
                <br />
                <>
                    <Row>
                    <Col>
                    <Card style={{ width: '18rem' }}>
                        <Card.Header>Incoming transactions :</Card.Header>
                        <ListGroup variant="flush">
                            {
                                this.state.incomingList.map((item, key) =>
                                {
                                    return(
                                    <ListGroup.Item key={key}>sender : {item.sender.user.username} {"->"} amount : {item.amount}</ListGroup.Item>
                                )
                            })
                        }

                        </ListGroup>
                    </Card>
                    </Col>
                    <Col>
                    <Card style={{ width: '18rem' }}>
                        <Card.Header>Outgoing transactions :</Card.Header>
                        <ListGroup variant="flush">
                            {
                                this.state.outgoingList.map((item, key) =>
                                {
                                    return(
                                        <ListGroup.Item key={key}>recevier : {item.receiver.user.username}  {"->"}  amount : {item.amount}</ListGroup.Item>
                                        )
                                    })
                                }

                        </ListGroup>
                    </Card>
                    </Col>
                    </Row>
                </>
                </Container>



                
            </>

        )
    }
}