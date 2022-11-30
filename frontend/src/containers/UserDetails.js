import React, { useState } from "react";

import axios from 'axios';
import NavBar from "./NavBar";
import Button from 'react-bootstrap/Button'
import Container from 'react-bootstrap/Container';
import Card from 'react-bootstrap/Card';
import Alert from 'react-bootstrap/Alert';
import ListGroup from 'react-bootstrap/ListGroup';
import '../App.css';
export default class UserDetails extends React.Component {
    state = { userData : {user:{}}, hasError:false, errorText:"", userTransactions: {transactions: []} };
    constructor(props)
    {
        super(props);
        window.MyVars = {accountDetails : {}}
    }
    async componentDidMount()
    {
        const queryParams = new URLSearchParams(window.location.search);
        const id = queryParams.get('id');
        const userDataResp = await axios.get("/user-details/"+id,{
            headers: {
              'Content-Type': 'application/json',
              'Authorization' : 'Token ' + localStorage.getItem("token"),
            }})

        const userTransactionsResp = await axios.get("/user-transactions/"+id, {
            headers:{'Content-Type': 'application/json',}
            
        })
        await this.setState({userData : userDataResp.data})
        await this.setState({userTransactions : userTransactionsResp.data})
    }
    onPointChange = (event) =>
    {
        this.setState({points : event.target.value})
    }

    onAddPoints = async() =>
    {
        const queryParams = new URLSearchParams(window.location.search);
        const id = queryParams.get('id');
        var requestData = {recevier : parseInt(id), amount : parseInt(this.state.points)}
        try {
            const addPointsResp = await axios.post("/send-points/", requestData, {
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization' : 'Token ' + localStorage.getItem("token"),
                }})
        } catch (error) {
            if(error.response.status == 403)
            {
                this.setState({hasError : true, errorText : error.response.data.error})
            }
        }

        
    }
    onWithdrawPoints = async() =>
    {
        const queryParams = new URLSearchParams(window.location.search);
        const id = queryParams.get('id');
        var requestData = {recevier : parseInt(id), amount : parseInt(this.state.points)}
        const addPointsResp = await axios.post("/withdraw-points/", requestData, {
            headers: {
              'Content-Type': 'application/json',
              'Authorization' : 'Token ' + localStorage.getItem("token"),
            }})

        console.log(addPointsResp.data)

    }
    render()
    {
        return(
            <>
            <NavBar />
            <Container style={{justifyContent : "center", alignItems : "center"}}>
                <br />
                <br />
                {this.state.hasError &&  <Alert key="danger" variant="danger">{this.state.errorText}</Alert> }
               
                <Card>
      <Card.Header>{this.state.userData.user.username}</Card.Header>
      <Card.Body>
        <Card.Title>Points : {this.state.userData.points}</Card.Title>
        {(window.MyVars.accountDetails.profile_type == "admin" && this.state.userData.profile_type == "user") &&
        <input
        className="form-control mt-1"
          placeholder="You can't give or withdraw points directly to users because you are not a broker !"
        onChange={this.onPointChange}
      />
    }

{(window.MyVars.accountDetails.profile_type == "broker" || (window.MyVars.accountDetails.profile_type == "admin" && this.state.userData.profile_type == "broker")) &&
        <>
        <input
                className="form-control mt-1"
                placeholder="amount of points to add :"
                onChange={this.onPointChange}
            />
            <br />
            <Button onClick={this.onAddPoints} variant="primary" >Add points</Button>
            <Button onClick={this.onWithdrawPoints} variant="primary" >Withdraw points</Button>
        </>

    }


      </Card.Body>
    </Card>
    <br></br>
    <h1> Transactions </h1>
    <ListGroup as="ol" numbered>

      {this.state.userTransactions.transactions.map((item, index) => (
                <ListGroup.Item as="li">transaction type : {item.transaction_type}  |  transaction amount : {item.amount} |  date : {item.date}</ListGroup.Item>
          ))}
    </ListGroup>
            </Container>


                
            </>

        )
    }
}